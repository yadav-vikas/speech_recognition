# speech_recognition
Speech recognition is the process of converting spoken words to text.
Python supports many speech recognition engines and APIs, including Google Speech Engine, Google Cloud Speech API,
Microsoft Bing Voice Recognition and IBM Speech to Text.


Picking a Python Speech Recognition Package

A handful of packages for speech recognition exist on PyPI. A few of them include:

    apiai
    assemblyai
    google-cloud-speech
    pocketsphinx
    SpeechRecognition
    watson-developer-cloud
    wit

Some of these packages—such as wit and apiai—offer built-in features, like natural language processing for identifying a speaker’s intent, which go beyond basic speech recognition. Others, like google-cloud-speech, focus solely on speech-to-text conversion.

There is one package that stands out in terms of ease-of-use: SpeechRecognition.

Recognizing speech requires audio input, and SpeechRecognition makes retrieving this input really easy. Instead of having to build scripts for accessing microphones and processing audio files from scratch, SpeechRecognition will have you up and running in just a few minutes.

The SpeechRecognition library acts as a wrapper for several popular speech APIs and is thus extremely flexible. One of these—the Google Web Speech API—supports a default API key that is hard-coded into the SpeechRecognition library. That means you can get off your feet without having to sign up for a service.

The flexibility and ease-of-use of the SpeechRecognition package make it an excellent choice for any Python project. However, support for every feature of each API it wraps is not guaranteed. You will need to spend some time researching the available options to find out if SpeechRecognition will work in your particular case.

So, now that you’re convinced you should try out SpeechRecognition, the next step is getting it installed in your environment.
Installing SpeechRecognition

SpeechRecognition is compatible with Python 2.6, 2.7 and 3.3+, but requires some additional installation steps for Python 2. For this tutorial, I’ll assume you are using Python 3.3+.

You can install SpeechRecognition from a terminal with pip:

$ pip install SpeechRecognition

Once installed, you should verify the installation by opening an interpreter session and typing:

>>> import speech_recognition as sr
>>> sr.__version__
'3.8.1'

Note: The version number you get might vary. Version 3.8.1 was the latest at the time of writing.

Go ahead and keep this session open. You’ll start to work with it in just a bit.

SpeechRecognition will work out of the box if all you need to do is work with existing audio files. Specific use cases, however, require a few dependencies. Notably, the PyAudio package is needed for capturing microphone input.

The Recognizer Class

All of the magic in SpeechRecognition happens with the Recognizer class.

The primary purpose of a Recognizer instance is, of course, to recognize speech. Each instance comes with a variety of settings and functionality for recognizing speech from an audio source.

Creating a Recognizer instance is easy. In your current interpreter session, just type:

>>> r = sr.Recognizer()

Each Recognizer instance has seven methods for recognizing speech from an audio source using various APIs. These are:

    recognize_bing(): Microsoft Bing Speech
    recognize_google(): Google Web Speech API
    recognize_google_cloud(): Google Cloud Speech - requires installation of the google-cloud-speech package
    recognize_houndify(): Houndify by SoundHound
    recognize_ibm(): IBM Speech to Text
    recognize_sphinx(): CMU Sphinx - requires installing PocketSphinx
    recognize_wit(): Wit.ai

Of the seven, only recognize_sphinx() works offline with the CMU Sphinx engine. The other six all require an internet connection.

A full discussion of the features and benefits of each API is beyond the scope of this tutorial. Since SpeechRecognition ships with a default API key for the Google Web Speech API, you can get started with it right away. For this reason, we’ll use the Web Speech API in this guide. The other six APIs all require authentication with either an API key or a username/password combination. For more information, consult the SpeechRecognition docs.

Caution: The default key provided by SpeechRecognition is for testing purposes only, and Google may revoke it at any time. It is not a good idea to use the Google Web Speech API in production. Even with a valid API key, you’ll be limited to only 50 requests per day, and there is no way to raise this quota. Fortunately, SpeechRecognition’s interface is nearly identical for each API, so what you learn today will be easy to translate to a real-world project.

Each recognize_*() method will throw a speech_recognition.RequestError exception if the API is unreachable. For recognize_sphinx(), this could happen as the result of a missing, corrupt or incompatible Sphinx installation. For the other six methods, RequestError may be thrown if quota limits are met, the server is unavailable, or there is no internet connection.


>>> r.recognize_google()

What happened?

You probably got something that looks like this:

Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: recognize_google() missing 1 required positional argument: 'audio_data'

You might have guessed this would happen. How could something be recognized from nothing?

All seven recognize_*() methods of the Recognizer class require an audio_data argument. In each case, audio_data must be an instance of SpeechRecognition’s AudioData class.

There are two ways to create an AudioData instance: from an audio file or audio recorded by a microphone. Audio files are a little easier to get started with




A library that helps is named “SpeechRecognition”. You should install it with pyenv, pipenv or virtualenv. 
You can also install it system wide

----->pip install SpeechRecognition

The SpeechRecognition module depends on pyaudio, you can install them from your package manager.
On Manjaro Linux these packages are called “python-pyaudio” and “python2-pyaudio”, they may have another name in your system

------>pip install pyaudio

 Google Speech Recognition engine, which I’ve tested for the English language.

For testing purposes, it uses the default API key.
To use another API key, use

---->r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
