# Project Zephyr -- Voice Bridge Application

An innovative voice translation pipeline that leverages Google Cloud's powerful APIs along with LLM voice synthesis to break down language barriers in real-time. This project combines the capabilities of Google Cloud Speech-to-Text, Translation, Text-to-Speech APIs, plus OpenAI API to create a seamless voice-to-voice translation experience.

## Description of Files

- **vbridge-w-GoogleAPIs.py**: This file utilizes the Google APIs only, namely Google Cloud Speech-to-Text, Translate, and Text-to-Speech
- **vbridge-w-GoogleAPIs-and-OpenAIAPIs.py**: This file utilizes the Google APIs + OpenAI API to synthesize and clean up the speech rendition for a cleaner, punctuated speech experience.

## Key Features

- **Speech Recognition**: Utilizes Google Cloud Speech-to-Text API to accurately transcribe spoken words from local audio sources.
- **Language Translation**: Employs Google Cloud Translation API to convert text from one language to another with high accuracy.
- **Voice Conversion**: Implements Google Cloud Text-to-Speech API to generate speech in the target language.
- **Low-Latency Processing**: Designed for low-latency performance, enabling rapid voice translation.
- **Multi-language Support**: Capable of handling a wide range of languages and dialects.
- **LLM Speech Synthesis Support (based on the file)**: To make speech more human-like and natural sounding.

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

- Up to 1 minute Audio. Can be extended through code modification.
- Translation is not expected to be word-for-word. The emphasis with LLM support is to provide full context of the input language to get a concise response. Its focused more on the content and message than word-for-word translation. This is by design.

