import speech_recognition as sr

r = sr.Recognizer()

with sr.AudioFile('path/to/audiofile.wav') as source:
    audio = r.record(source)

r.recognize_google(audio, language='fr-FR')










"""Recognizing Speech in Languages Other Than English

Throughout this tutorial, we’ve been recognizing speech in English, which is the default language for each recognize_*() method of the SpeechRecognition package. However, it is absolutely possible to recognize speech in other languages, and is quite simple to accomplish.

To recognize speech in a different language, set the language keyword argument of the recognize_*() method to a string corresponding to the desired language. Most of the methods accept a BCP-47 language tag, such as 'en-US' for American English, or 'fr-FR' for French. For example, the following recognizes French speech in an audio file:

"""
