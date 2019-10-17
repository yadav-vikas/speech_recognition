Working With Audio Files

Before you continue, you’ll need to download an audio file. The one I used to get started, “harvard.wav,” can be found here.
Make sure you save it to the same directory in which your Python interpreter session is running.

SpeechRecognition makes working with audio files easy thanks to its handy AudioFile class. 
This class can be initialized with the path to an audio file and provides a context manager interface for reading and working with the file’s contents.

Supported File Types

Currently, SpeechRecognition supports the following file formats:

    WAV: must be in PCM/LPCM format
    AIFF
    AIFF-C
    FLAC: must be native FLAC format; OGG-FLAC is not supported

If you are working on x-86 based Linux, macOS or Windows, you should be able to work with FLAC files without a problem. On other platforms, you will need to install a FLAC encoder and ensure you have access to the flac command line tool. You can find more information here if this applies to you.
Using record() to Capture Data From a File

Type the following into your interpreter session to process the contents of the “harvard.wav” file:

>>> harvard = sr.AudioFile('harvard.wav')
>>> with harvard as source:
...    audio = r.record(source)
...

The context manager opens the file and reads its contents, storing the data in an AudioFile instance called source. Then the record() method records the data from the entire file into an AudioData instance. You can confirm this by checking the type of audio:

>>> type(audio)
<class 'speech_recognition.AudioData'>

You can now invoke recognize_google() to attempt to recognize any speech in the audio. Depending on your internet connection speed, you may have to wait several seconds before seeing the result.

>>> r.recognize_google(audio)
'the stale smell of old beer lingers it takes heat
to bring out the odor a cold dip restores health and
zest a salt pickle taste fine with ham tacos al
Pastore are my favorite a zestful food is the hot
cross bun'

Congratulations! You’ve just transcribed your first audio file!

If you’re wondering where the phrases in the “harvard.wav” file come from, they are examples of Harvard Sentences. These phrases were published by the IEEE in 1965 for use in speech intelligibility testing of telephone lines. They are still used in VoIP and cellular testing today.

The Harvard Sentences are comprised of 72 lists of ten phrases. You can find freely available recordings of these phrases on the Open Speech Repository website. Recordings are available in English, Mandarin Chinese, French, and Hindi. They provide an excellent source of free material for testing your code.
Capturing Segments With offset and duration

What if you only want to capture a portion of the speech in a file? The record() method accepts a duration keyword argument that stops the recording after a specified number of seconds.

For example, the following captures any speech in the first four seconds of the file:

>>> with harvard as source:
...     audio = r.record(source, duration=4)
...
>>> r.recognize_google(audio)
'the stale smell of old beer lingers'

The record() method, when used inside a with block, always moves ahead in the file stream. This means that if you record once for four seconds and then record again for four seconds, the second time returns the four seconds of audio after the first four seconds.

>>> with harvard as source:
...     audio1 = r.record(source, duration=4)
...     audio2 = r.record(source, duration=4)
...
>>> r.recognize_google(audio1)
'the stale smell of old beer lingers'
>>> r.recognize_google(audio2)
'it takes heat to bring out the odor a cold dip'

Notice that audio2 contains a portion of the third phrase in the file. When specifying a duration, the recording might stop mid-phrase—or even mid-word—which can hurt the accuracy of the transcription. More on this in a bit.

In addition to specifying a recording duration, the record() method can be given a specific starting point using the offset keyword argument. This value represents the number of seconds from the beginning of the file to ignore before starting to record.

To capture only the second phrase in the file, you could start with an offset of four seconds and record for, say, three seconds.

>>> with harvard as source:
...     audio = r.record(source, offset=4, duration=3)
...
>>> recognizer.recognize_google(audio)
'it takes heat to bring out the odor'

The offset and duration keyword arguments are useful for segmenting an audio file if you have prior knowledge of the structure of the speech in the file. However, using them hastily can result in poor transcriptions. To see this effect, try the following in your interpreter:

>>> with harvard as source:
...     audio = r.record(source, offset=4.7, duration=2.8)
...
>>> recognizer.recognize_google(audio)
'Mesquite to bring out the odor Aiko'

By starting the recording at 4.7 seconds, you miss the “it t” portion a the beginning of the phrase “it takes heat to bring out the odor,” so the API only got “akes heat,” which it matched to “Mesquite.”

Similarly, at the end of the recording, you captured “a co,” which is the beginning of the third phrase “a cold dip restores health and zest.” This was matched to “Aiko” by the API.

There is another reason you may get inaccurate transcriptions. Noise! The above examples worked well because the audio file is reasonably clean. In the real world, unless you have the opportunity to process audio files beforehand, you can not expect the audio to be noise-free.

Supported File Types

Currently, SpeechRecognition supports the following file formats:

    WAV: must be in PCM/LPCM format
    AIFF
    AIFF-C
    FLAC: must be native FLAC format; OGG-FLAC is not supported

If you are working on x-86 based Linux, macOS or Windows, you should be able to work with FLAC files without a problem. On other platforms, you will need to install a FLAC encoder and ensure you have access to the flac command line tool. You can find more information here if this applies to you.
Using record() to Capture Data From a File

Type the following into your interpreter session to process the contents of the “harvard.wav” file:

>>> harvard = sr.AudioFile('harvard.wav')
>>> with harvard as source:
...    audio = r.record(source)
...

The context manager opens the file and reads its contents, storing the data in an AudioFile instance called source. Then the record() method records the data from the entire file into an AudioData instance. You can confirm this by checking the type of audio:

>>> type(audio)
<class 'speech_recognition.AudioData'>

You can now invoke recognize_google() to attempt to recognize any speech in the audio. Depending on your internet connection speed, you may have to wait several seconds before seeing the result.

>>> r.recognize_google(audio)
'the stale smell of old beer lingers it takes heat
to bring out the odor a cold dip restores health and
zest a salt pickle taste fine with ham tacos al
Pastore are my favorite a zestful food is the hot
cross bun'

Congratulations! You’ve just transcribed your first audio file!

If you’re wondering where the phrases in the “harvard.wav” file come from, they are examples of Harvard Sentences. These phrases were published by the IEEE in 1965 for use in speech intelligibility testing of telephone lines. They are still used in VoIP and cellular testing today.

The Harvard Sentences are comprised of 72 lists of ten phrases. You can find freely available recordings of these phrases on the Open Speech Repository website. Recordings are available in English, Mandarin Chinese, French, and Hindi. They provide an excellent source of free material for testing your code.
Capturing Segments With offset and duration

What if you only want to capture a portion of the speech in a file? The record() method accepts a duration keyword argument that stops the recording after a specified number of seconds.

For example, the following captures any speech in the first four seconds of the file:

>>> with harvard as source:
...     audio = r.record(source, duration=4)
...
>>> r.recognize_google(audio)
'the stale smell of old beer lingers'

The record() method, when used inside a with block, always moves ahead in the file stream. This means that if you record once for four seconds and then record again for four seconds, the second time returns the four seconds of audio after the first four seconds.

>>> with harvard as source:
...     audio1 = r.record(source, duration=4)
...     audio2 = r.record(source, duration=4)
...
>>> r.recognize_google(audio1)
'the stale smell of old beer lingers'


The Effect of Noise on Speech Recognition

Noise is a fact of life. All audio recordings have some degree of noise in them, and un-handled noise can wreck the accuracy of speech recognition apps.

To get a feel for how noise can affect speech recognition, download the “jackhammer.wav” file here. As always, make sure you save this to your interpreter session’s working directory.

This file has the phrase “the stale smell of old beer lingers” spoken with a loud jackhammer in the background.

What happens when you try to transcribe this file?

>>> jackhammer = sr.AudioFile('jackhammer.wav')
>>> with jackhammer as source:
...     audio = r.record(source)
...
>>> r.recognize_google(audio)
'the snail smell of old gear vendors'

Way off!

So how do you deal with this? One thing you can try is using the adjust_for_ambient_noise() method of the Recognizer class.

>>> with jackhammer as source:
...     r.adjust_for_ambient_noise(source)
...     audio = r.record(source)
...
>>> r.recognize_google(audio)
'still smell of old beer vendors'

That got you a little closer to the actual phrase, but it still isn’t perfect. Also, “the” is missing from the beginning of the phrase. Why is that?

The adjust_for_ambient_noise() method reads the first second of the file stream and calibrates the recognizer to the noise level of the audio. Hence, that portion of the stream is consumed before you call record() to capture the data.

You can adjust the time-frame that adjust_for_ambient_noise() uses for analysis with the duration keyword argument. This argument takes a numerical value in seconds and is set to 1 by default. Try lowering this value to 0.5.

>>> with jackhammer as source:
...     r.adjust_for_ambient_noise(source, duration=0.5)
...     audio = r.record(source)
...
>>> r.recognize_google(audio)
'the snail smell like old Beer Mongers'

Well, that got you “the” at the beginning of the phrase, but now you have some new issues! Sometimes it isn’t possible to remove the effect of the noise—the signal is just too noisy to be dealt with successfully. That’s the case with this file.

If you find yourself running up against these issues frequently, you may have to resort to some pre-processing of the audio. This can be done with audio editing software or a Python package (such as SciPy) that can apply filters to the files. A detailed discussion of this is beyond the scope of this tutorial—check out Allen Downey’s Think DSP book if you are interested. For now, just be aware that ambient noise in an audio file can cause problems and must be addressed in order to maximize the accuracy of speech recognition.

When working with noisy files, it can be helpful to see the actual API response. Most APIs return a JSON string containing many possible transcriptions. The recognize_google() method will always return the most likely transcription unless you force it to give you the full response.

You can do this by setting the show_all keyword argument of the recognize_google() method to True.

>>> r.recognize_google(audio, show_all=True)
{'alternative': [
  {'transcript': 'the snail smell like old Beer Mongers'}, 
  {'transcript': 'the still smell of old beer vendors'}, 
  {'transcript': 'the snail smell like old beer vendors'},
  {'transcript': 'the stale smell of old beer vendors'}, 
  {'transcript': 'the snail smell like old beermongers'}, 
  {'transcript': 'destihl smell of old beer vendors'}, 
  {'transcript': 'the still smell like old beer vendors'}, 
  {'transcript': 'bastille smell of old beer vendors'}, 
  {'transcript': 'the still smell like old beermongers'}, 
  {'transcript': 'the still smell of old beer venders'}, 
  {'transcript': 'the still smelling old beer vendors'}, 
  {'transcript': 'musty smell of old beer vendors'}, 
  {'transcript': 'the still smell of old beer vendor'}
], 'final': True}

As you can see, recognize_google() returns a dictionary with the key 'alternative' that points to a list of possible transcripts. The structure of this response may vary from API to API and is mainly useful for debugging.

By now, you have a pretty good idea of the basics of the SpeechRecognition package. You’ve seen how to create an AudioFile instance from an audio file and use the record() method to capture data from the file. You learned how record segments of a file using the offset and duration keyword arguments of record(), and you experienced the detrimental effect noise can have on transcription accuracy.

Now for the fun part. Let’s transition from transcribing static audio files to making your project interactive by accepting input from a microphone.

>>> r.recognize_google(audio2)
'it takes heat to bring out the odor a cold dip'

Notice that audio2 contains a portion of the third phrase in the file. When specifying a duration, the recording might stop mid-phrase—or even mid-word—which can hurt the accuracy of the transcription. More on this in a bit.

In addition to specifying a recording duration, the record() method can be given a specific starting point using the offset keyword argument. This value represents the number of seconds from the beginning of the file to ignore before starting to record.

To capture only the second phrase in the file, you could start with an offset of four seconds and record for, say, three seconds.

>>> with harvard as source:
...     audio = r.record(source, offset=4, duration=3)
...
>>> recognizer.recognize_google(audio)
'it takes heat to bring out the odor'

The offset and duration keyword arguments are useful for segmenting an audio file if you have prior knowledge of the structure of the speech in the file. However, using them hastily can result in poor transcriptions. To see this effect, try the following in your interpreter:

>>> with harvard as source:
...     audio = r.record(source, offset=4.7, duration=2.8)
...
>>> recognizer.recognize_google(audio)
'Mesquite to bring out the odor Aiko'

By starting the recording at 4.7 seconds, you miss the “it t” portion a the beginning of the phrase “it takes heat to bring out the odor,” so the API only got “akes heat,” which it matched to “Mesquite.”

Similarly, at the end of the recording, you captured “a co,” which is the beginning of the third phrase “a cold dip restores health and zest.” This was matched to “Aiko” by the API.

There is another reason you may get inaccurate transcriptions. Noise! The above examples worked well because the audio file is reasonably clean. In the real world, unless you have the opportunity to process audio files beforehand, you can not expect the audio to be noise-free.
