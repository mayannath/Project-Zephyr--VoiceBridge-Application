# Project Zephyr -- Voice Bridge Application

An innovative voice translation pipeline that leverages Google Cloud's powerful APIs along with LLM voice synthesis to break down language barriers in real-time. This project combines the capabilities of Google Cloud Speech-to-Text, Translation, Text-to-Speech APIs, plus OpenAI API to create a seamless voice-to-voice translation experience.

## Description of Files

- **vbridge-withGoogleAPIs-and-OpenAIAPIs-and-SentimentAnalysis-colorCoded-with-SSML.py**: This file adds emotional context to generated speech through sentiment analysis by modifying the pitch and tone of the final speech. Only works for Supported languages.
- **requirements.txt**: includes all packages needed to run this app.

## Key Features

- **Speech Recognition**: Utilizes Google Cloud Speech-to-Text API to accurately transcribe spoken words from local audio sources.
- **Language Translation**: Employs Google Cloud Translation API to convert text from one language to another with high accuracy.
- **Voice Conversion**: Implements Google Cloud Text-to-Speech API to generate speech in the target language.
- **Low-Latency Processing**: Designed for low-latency performance, enabling rapid voice translation.
- **Multi-language Support**: Capable of handling a wide range of languages and dialects.
- **LLM Speech Synthesis Support (based on the file)**: To make speech more human-like and natural sounding.
- **Sentiment Analysis (based on the file)**: To add emotional context 

## Technical Overview

Voice Bridge is built as a modular pipeline:

1. **Audio Input**: Captures audio from microphone.
2. **Speech-to-Text**: Converts audio to text in the source language.
3. **Translation**: Translates the text to the target language.
4. **LLM Speech Synthesis (based on the file)**: Makes speech more human-like with punctuations, grammer, and tonality (to some degree.)
5. **Text-to-Speech**: Generates audio output in the target language.

The project is structured to allow easy integration with various front-end applications, making it suitable for use in mobile apps, web services, or standalone desktop applications.

## Potential Applications

- Public Testimony Translations
- Accessibility features for multilingual content
- Cross-language customer support systems

## Limitations

- Up to 1 minute Audio. Can be extended through code modification and utilizing a Google Cloud storage account to host the Audio File.
- Translation is not expected to be word-for-word. The emphasis with LLM support is to provide full context of the input language to get a concise response. Its focused more on the content and message than word-for-word translation. This is by design.

## Future Improvements

- build end-to-end encryption.
- Expand sentiment analysis to support more languages.
- Add detailed error messages and better input validation.
- Optimize for faster performance and lower API costs.
- Support multi-language translations and configurable voice options.
- Improve user interface with better feedback and accessibility.
- Re-factor code with classes/modules for better maintainability.

