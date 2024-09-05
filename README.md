# VocalBridge

An innovative voice translation pipeline that leverages Google Cloud's powerful APIs to break down language barriers in real-time. This project combines the capabilities of Google Cloud Speech-to-Text, Translation, and Text-to-Speech APIs to create a seamless voice-to-voice translation experience.

## Key Features

- **Speech Recognition**: Utilizes Google Cloud Speech-to-Text API to accurately transcribe spoken words from local audio sources.
- **Language Translation**: Employs Google Cloud Translation API to convert text from one language to another with high accuracy.
- **Voice Synthesis**: Implements Google Cloud Text-to-Speech API to generate natural-sounding speech in the target language.
- **Low-Latency Processing**: Designed for low-latency performance, enabling rapid voice translation.
- **Multi-language Support**: Capable of handling a wide range of languages and dialects.

## Technical Overview

VocalBridge is built as a modular pipeline:

1. **Audio Input**: Captures audio from microphone.
2. **Speech-to-Text**: Converts audio to text in the source language.
3. **Translation**: Translates the text to the target language.
4. **Text-to-Speech**: Generates audio output in the target language.

The project is structured to allow easy integration with various front-end applications, making it suitable for use in mobile apps, web services, or standalone desktop applications.

## Potential Applications

- Public Testimony Translations
- Accessibility features for multilingual content
- Cross-language customer support systems

## Limitations

- 1 minute Audio. Can be extended through code modification.

