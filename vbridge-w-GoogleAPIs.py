import os
import uuid
import gradio as gr
from google.cloud import translate_v2 as translate
from google.cloud import speech_v1p1beta1 as speech
from google.cloud import texttospeech
from pathlib import Path

# Initialize Google Translate client
def init_google_translate_client():
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/Users/mayan/VoiceBridgeApp/myenv/psychic-karma-434602-f2-fd6bcd4cd937.json"  # Set your credentials path
    return translate.Client()

translate_client = init_google_translate_client()

# Function to transcribe audio using Google Cloud Speech-to-Text
def transcribe_audio_google(audio_file, language_code):
    client = speech.SpeechClient()

    with open(audio_file, 'rb') as f:
        audio_content = f.read()

    audio = speech.RecognitionAudio(content=audio_content)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,  # Modify if needed based on your input
        #sample_rate_hertz=44100,  # COmmented out since the API itself auto-selects the sample rate of the WAV audio.
        language_code=language_code,  # Set input language from the Gradio dropdown
    )

    response = client.recognize(config=config, audio=audio)

    # Return the best transcript result
    for result in response.results:
        return result.alternatives[0].transcript

# Function to translate text using Google Cloud Translate API
def translate_text_google(text, target_language="en"):
    translation = translate_client.translate(text, target_language=target_language)
    return translation['translatedText']

# Function to generate speech from text using Google Cloud Text-to-Speech API
def text_to_speech_google(text):
    client = texttospeech.TextToSpeechClient()

    input_text = texttospeech.SynthesisInput(text=text)
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US",  # Output in US English
        ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
    )
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    response = client.synthesize_speech(input=input_text, voice=voice, audio_config=audio_config)

    # Save audio to a file
    output_file = f"{uuid.uuid4()}.mp3"
    with open(output_file, "wb") as out:
        out.write(response.audio_content)

    return output_file

# Main pipeline to handle voice-to-voice translation
def voice_to_voice(audio_file, language_code):
    # Step 1: Transcribe audio using Google Cloud Speech-to-Text
    transcript = transcribe_audio_google(audio_file, language_code)

    # Step 2: Translate the transcript to English using Google Cloud Translate
    translated_text = translate_text_google(transcript)

    # Step 3: Convert the translated text to speech using Google Cloud Text-to-Speech
    generated_audio_file = text_to_speech_google(translated_text)

    # Return the audio file and translated text
    return generated_audio_file, translated_text

# Gradio interface with improved layout
with gr.Blocks() as demo:
    gr.Markdown("""
    <h1 style='text-align: left;'>Project Zephyr</h1>
    <h3 style='text-align: left;'>BOS Public Comment Translator: Proof-of-Concept</h3>
    <p style='text-align: left;'>Translate the Public Comment Testimony LIVE</p>
    """)

    
    #gr.Markdown("### Step 1: Select Input Language and Record Audio")
    
    with gr.Row():
        with gr.Column(scale=1):
            # Dropdown to select input language
            language_input = gr.Dropdown(
                label="Input Language",
                choices=[
                    ("Arabic", "ar"),
                    ("Armenian", "hy"),
                    ("Chinese (Simplified)", "zh-CN"),
                    ("Filipino", "tl"),
                    ("Hindi", "hi"),
                    ("Italian", "it"),
                    ("Japanese", "ja"),
                    ("Korean", "ko"),
                    ("Spanish", "es"),
                    ("Vietnamese", "vi"),
                ],
                value="es",  # Default to Spanish
                interactive=True
            )

        with gr.Column(scale=2):
            # Input audio component
            audio_input = gr.Audio(
                label="Record Public Comment",
                sources=["microphone"], 
                type="filepath", 
                show_download_button=True,
                interactive=True,
                #max_duration=120 # Max duration not working in this version of Gradio :{
            )

    # Action buttons
    with gr.Row():
        submit = gr.Button("Translate", variant="primary", scale=1)
        btn = gr.Button("Clear", scale=1)

    # Output Section
    gr.Markdown("### Translation Result")

    with gr.Row():
        with gr.Column(scale=1):
            # English text output
            en_text = gr.Markdown(label="Translated English Text")
        
        with gr.Column(scale=1):
            # English audio output
            en_output = gr.Audio(label="Translated English Audio", interactive=False)

    # Define actions for buttons
    submit.click(
        fn=voice_to_voice, 
        inputs=[audio_input, language_input], 
        outputs=[en_output, en_text], 
        show_progress=True
    )

    btn.click(
        fn=lambda: (None, None, ""), 
        outputs=[audio_input, en_output, en_text]
    )

if __name__ == "__main__":
    demo.launch()
