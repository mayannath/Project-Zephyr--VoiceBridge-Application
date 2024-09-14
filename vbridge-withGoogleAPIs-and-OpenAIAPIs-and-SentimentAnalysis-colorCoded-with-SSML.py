import os
import uuid
import gradio as gr
from google.cloud import translate_v2 as translate
from google.cloud import speech_v1p1beta1 as speech
from google.cloud import texttospeech
from google.cloud.language_v1 import LanguageServiceClient  # For Natural Language API
from pathlib import Path
import openai

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
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        language_code=language_code,
        enable_automatic_punctuation=True
    )

    response = client.recognize(config=config, audio=audio)

    for result in response.results:
        return result.alternatives[0].transcript

# Function to analyze sentiment using Google Cloud Natural Language API
def analyze_sentiment(text, language_code="en"):
    client = LanguageServiceClient()

    # List of supported languages for sentiment analysis
    supported_languages = ["en", "es", "ja", "zh", "ar", "it", "ko", "vi"]

    # Check if the language is supported for sentiment analysis
    if language_code not in supported_languages:
        return f"Sentiment analysis is not supported for {language_code}. Defaulting to English sentiment analysis."

    document = {"content": text, "type_": "PLAIN_TEXT", "language": language_code}
    response = client.analyze_sentiment(request={"document": document})

    sentiment = response.document_sentiment
    sentiment_score = round(sentiment.score, 1)  # Round sentiment score to nearest 0.1
    sentiment_magnitude = round(sentiment.magnitude, 1)

    if sentiment_score > 0.25:
        sentiment_result = f"<span style='color:green; font-weight: bold;'>Positive</span>"
    elif sentiment_score < -0.25:
        sentiment_result = f"<span style='color:red; font-weight: bold;'>Negative</span>"
    else:
        sentiment_result = f"<span style='color:yellow; font-weight: bold;'>Neutral</span>"

    return f"<b>Sentiment:</b> {sentiment_result} (Score: {sentiment_score}, Magnitude: {sentiment_magnitude})"


# Function to translate text using Google Cloud Translate API
def translate_text_google(text, target_language="en"):
    translation = translate_client.translate(text, target_language=target_language)
    return translation['translatedText']

# Function to generate speech from text using Google Cloud Text-to-Speech API, with emotions based on sentiment using the Speech Synthesis Markup Language that is part of the Google Cloud Text-to-Speech API
def text_to_speech_google(text, sentiment_score):
    client = texttospeech.TextToSpeechClient()

    # Define the SSML based on sentiment score
    if sentiment_score > 0.25:  # Positive
        ssml_text = f'<speak><prosody pitch="+10%" rate="105%"> {text} </prosody></speak>'
    elif sentiment_score < -0.25:  # Negative
        ssml_text = f'<speak><prosody pitch="-10%" rate="90%"> {text} </prosody></speak>'
    else:  # Neutral
        ssml_text = f'<speak><prosody pitch="0%" rate="100%"> {text} </prosody></speak>'

    input_text = texttospeech.SynthesisInput(ssml=ssml_text)
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US",
        ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
    )
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    response = client.synthesize_speech(input=input_text, voice=voice, audio_config=audio_config)

    output_file = f"{uuid.uuid4()}.mp3"
    with open(output_file, "wb") as out:
        out.write(response.audio_content)

    return output_file

# Function to enhance the translation using OpenAI GPT (with the latest API)
def enhance_translation_with_llm(translated_text, source_language):
    openai.api_key = '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'

    # Define the conversation as a series of messages (system and user)
    messages = [
        {"role": "system", "content": "You are a professional translator who understands the emotional and tonal queues in speech."},
        {
            "role": "user",
            "content": f"Please refine this translation from {source_language} to English. The translation needs to take into account emotions, grammar, punctuation, and natural language flow.\n\n"
                       f"Original Translation: {translated_text}\n\n"
                       f"Refined Translation:"
        }
    ]

    # Use the ChatCompletion API to access models like gpt-3.5-turbo or gpt-4
    response = openai.ChatCompletion.create(
        model="gpt-4o",  # You can also use gpt-3.5-turbo if available
        messages=messages,
        temperature=0.1,
        max_tokens=4096
    )

    # Access the content from the response properly
    return response.choices[0].message['content'].strip()

# Main pipeline to handle voice-to-voice translation
def voice_to_voice(audio_file, language_code):
    # Step 1: Transcribe audio using Google Cloud Speech-to-Text
    transcript = transcribe_audio_google(audio_file, language_code)

    # Step 2: Analyze sentiment
    sentiment_result = analyze_sentiment(transcript, language_code)
    sentiment_score = 0  # Default neutral sentiment if unsupported
    if "Score" in sentiment_result:
        sentiment_score = float(sentiment_result.split("Score: ")[1].split(",")[0])

    # Step 3: Translate the transcript to English using Google Cloud Translate
    translated_text = translate_text_google(transcript)

    # Step 4: Enhance the translation using OpenAI GPT
    enhanced_translation = enhance_translation_with_llm(translated_text, language_code)

    # Step 5: Convert the enhanced translation to speech using Google Cloud Text-to-Speech with emotions
    generated_audio_file = text_to_speech_google(enhanced_translation, sentiment_score)

    # Return the audio file, enhanced translated text, and sentiment analysis result
    return generated_audio_file, enhanced_translation, sentiment_result

# Gradio interface with sentiment analysis
with gr.Blocks() as demo:
    gr.Markdown("""
    # Project Zephyr - VoiceBridge App
    Public Comment Translator - Proof-of-Concept
    """)
    gr. Markdown("This version of the App offers accurate translations and expressive speech output using SSML. Positive sentiment results in a higher pitch and faster speech, negative sentiment lowers the pitch and slows the speech, while neutral sentiment maintains a default tone. The goal is to create an emotion-aware output that reflects the emotional context of the input. For all unsupported languages on the list, the sentiment analysis is skipped, and the speech is delivered in a neutral tone with default pitch and rate. Whether the language sentiment is supported or not, the app still provides an effective transcription and translation, ensuring reliable output across different languages.")
    gr.Markdown("### Select Input Language and Record Audio")
    gr.Markdown("NOTE: Languages marked with * DO NOT support Sentiment Analysis")

    with gr.Row():
        with gr.Column(scale=1):
            language_input = gr.Dropdown(
                label="Select Language",
                choices=[
                    ("Arabic", "ar"),
                    ("Armenian *", "hy"),
                    ("Chinese", "zh"),
                    ("Filipino *", "tl"),
                    ("Hindi *", "hi"),
                    ("Italian", "it"),
                    ("Japanese", "ja"),
                    ("Korean", "ko"),
                    ("Spanish", "es"),
                    ("Vietnamese", "vi"),
                ],
                value="es",
                interactive=True
            )

        with gr.Column(scale=2):
            audio_input = gr.Audio(
                label="Record Public Comment",
                sources=["microphone"], 
                type="filepath", 
                show_download_button=True,
                interactive=True,
            )

    with gr.Row():
        submit = gr.Button("Translate", variant="primary", scale=1)
        btn = gr.Button("Clear", scale=1)

    #gr.Markdown("### Translation Result")

    with gr.Row():
        with gr.Column(scale=1):
            en_text = gr.Markdown(label="Translated English Text")
            gr.Markdown("<br>")
        # New Sentiment Heading with color coding in HTML
            sentiment_output = gr.HTML()
        
        with gr.Column(scale=1):
            en_output = gr.Audio(label="Translated English Audio", interactive=False)

    submit.click(
        fn=voice_to_voice, 
        inputs=[audio_input, language_input], 
        outputs=[en_output, en_text, sentiment_output], 
        show_progress=True
    )

    btn.click(
        fn=lambda: (None, None, "", ""), 
        outputs=[audio_input, en_output, en_text, sentiment_output]
    )

if __name__ == "__main__":
    demo.launch()
