Working With Microphones

To access your microphone with SpeechRecognizer, you’ll have to install the PyAudio package. Go ahead and close your current interpreter session, and let’s do that.
Installing PyAudio

The process for installing PyAudio will vary depending on your operating system.
Debian Linux

If you’re on Debian-based Linux (like Ubuntu) you can install PyAudio with apt:

$ sudo apt-get install python-pyaudio python3-pyaudio

Once installed, you may still need to run pip install pyaudio, especially if you are working in a virtual environment.
macOS

For macOS, first you will need to install PortAudio with Homebrew, and then install PyAudio with pip:

$ brew install portaudio
$ pip install pyaudio

Windows

On Windows, you can install PyAudio with pip:

$ pip install pyaudio

Testing the Installation

Once you’ve got PyAudio installed, you can test the installation from the console.

$ python -m speech_recognition

Make sure your default microphone is on and unmuted. If the installation worked, you should see something like this:

A moment of silence, please...
Set minimum energy threshold to 600.4452854381937
Say something!

Go ahead and play around with it a little bit by speaking into your microphone and seeing how well SpeechRecognition transcribes your speech.

Note: If you are on Ubuntu and get some funky output like ‘ALSA lib … Unknown PCM’, refer to this page for tips on suppressing these messages. This output comes from the ALSA package installed with Ubuntu—not SpeechRecognition or PyAudio. In all reality, these messages may indicate a problem with your ALSA configuration, but in my experience, they do not impact the functionality of your code. They are mostly a nuisance.
The Microphone Class

Open up another interpreter session and create an instance of the recognizer class.

>>> import speech_recognition as sr
>>> r = sr.Recognizer()

Now, instead of using an audio file as the source, you will use the default system microphone. You can access this by creating an instance of the Microphone class.

>>> mic = sr.Microphone()

If your system has no default microphone (such as on a RaspberryPi), or you want to use a microphone other than the default, you will need to specify which one to use by supplying a device index. You can get a list of microphone names by calling the list_microphone_names() static method of the Microphone class.

>>> sr.Microphone.list_microphone_names()
['HDA Intel PCH: ALC272 Analog (hw:0,0)',
 'HDA Intel PCH: HDMI 0 (hw:0,3)',
 'sysdefault',
 'front',
 'surround40',
 'surround51',
 'surround71',
 'hdmi',
 'pulse',
 'dmix', 
 'default']

Note that your output may differ from the above example.

The device index of the microphone is the index of its name in the list returned by list_microphone_names(). For example, given the above output, if you want to use the microphone called “front,” which has index 3 in the list, you would create a microphone instance like this:

>>> # This is just an example; do not run
>>> mic = sr.Microphone(device_index=3)

For most projects, though, you’ll probably want to use the default system microphone.
Using listen() to Capture Microphone Input

Now that you’ve got a Microphone instance ready to go, it’s time to capture some input.

Just like the AudioFile class, Microphone is a context manager. You can capture input from the microphone using the listen() method of the Recognizer class inside of the with block. This method takes an audio source as its first argument and records input from the source until silence is detected.

>>> with mic as source:
...     audio = r.listen(source)
...

Once you execute the with block, try speaking “hello” into your microphone. Wait a moment for the interpreter prompt to display again. Once the “>>>” prompt returns, you’re ready to recognize the speech.

>>> r.recognize_google(audio)
'hello'

If the prompt never returns, your microphone is most likely picking up too much ambient noise. You can interrupt the process with +ctrl+c++ to get your prompt back.

To handle ambient noise, you’ll need to use the adjust_for_ambient_noise() method of the Recognizer class, just like you did when trying to make sense of the noisy audio file. Since input from a microphone is far less predictable than input from an audio file, it is a good idea to do this anytime you listen for microphone input.

>>> with mic as source:
...     r.adjust_for_ambient_noise(source)
...     audio = r.listen(source)
...

After running the above code, wait a second for adjust_for_ambient_noise() to do its thing, then try speaking “hello” into the microphone. Again, you will have to wait a moment for the interpreter prompt to return before trying to recognize the speech.

Recall that adjust_for_ambient_noise() analyzes the audio source for one second. If this seems too long to you, feel free to adjust this with the duration keyword argument.

The SpeechRecognition documentation recommends using a duration no less than 0.5 seconds. In some cases, you may find that durations longer than the default of one second generate better results. The minimum value you need depends on the microphone’s ambient environment. Unfortunately, this information is typically unknown during development. In my experience, the default duration of one second is adequate for most applications.
Handling Unrecognizable Speech

Try typing the previous code example in to the interpeter and making some unintelligible noises into the microphone. You should get something like this in response:

Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "/home/david/real_python/speech_recognition_primer/venv/lib/python3.5/site-packages/speech_recognition/__init__.py", line 858, in recognize_google
    if not isinstance(actual_result, dict) or len(actual_result.get("alternative", [])) == 0: raise UnknownValueError()
speech_recognition.UnknownValueError

Audio that cannot be matched to text by the API raises an UnknownValueError exception. You should always wrap calls to the API with try and except blocks to handle this exception.

Note: You may have to try harder than you expect to get the exception thrown. The API works very hard to transcribe any vocal sounds. Even short grunts were transcribed as words like “how” for me. Coughing, hand claps, and tongue clicks would consistently raise the exception.
Putting It All Together: A “Guess the Word” Game

Now that you’ve seen the basics of recognizing speech with the SpeechRecognition package let’s put your newfound knowledge to use and write a small game that picks a random word from a list and gives the user three attempts to guess the word.

Here is the full script:

import random
import time

import speech_recognition as sr


def recognize_speech_from_mic(recognizer, microphone):
    """Transcribe speech from recorded from `microphone`.

    Returns a dictionary with three keys:
    "success": a boolean indicating whether or not the API request was
               successful
    "error":   `None` if no error occured, otherwise a string containing
               an error message if the API could not be reached or
               speech was unrecognizable
    "transcription": `None` if speech could not be transcribed,
               otherwise a string containing the transcribed text
    """
    # check that recognizer and microphone arguments are appropriate type
    if not isinstance(recognizer, sr.Recognizer):
        raise TypeError("`recognizer` must be `Recognizer` instance")

    if not isinstance(microphone, sr.Microphone):
        raise TypeError("`microphone` must be `Microphone` instance")

    # adjust the recognizer sensitivity to ambient noise and record audio
    # from the microphone
    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    # set up the response object
    response = {
        "success": True,
        "error": None,
        "transcription": None
    }

    # try recognizing the speech in the recording
    # if a RequestError or UnknownValueError exception is caught,
    #     update the response object accordingly
    try:
        response["transcription"] = recognizer.recognize_google(audio)
    except sr.RequestError:
        # API was unreachable or unresponsive
        response["success"] = False
        response["error"] = "API unavailable"
    except sr.UnknownValueError:
        # speech was unintelligible
        response["error"] = "Unable to recognize speech"

    return response


if __name__ == "__main__":
    # set the list of words, maxnumber of guesses, and prompt limit
    WORDS = ["apple", "banana", "grape", "orange", "mango", "lemon"]
    NUM_GUESSES = 3
    PROMPT_LIMIT = 5

    # create recognizer and mic instances
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    # get a random word from the list
    word = random.choice(WORDS)

    # format the instructions string
    instructions = (
        "I'm thinking of one of these words:\n"
        "{words}\n"
        "You have {n} tries to guess which one.\n"
    ).format(words=', '.join(WORDS), n=NUM_GUESSES)

    # show instructions and wait 3 seconds before starting the game
    print(instructions)
    time.sleep(3)

    for i in range(NUM_GUESSES):
        # get the guess from the user
        # if a transcription is returned, break out of the loop and
        #     continue
        # if no transcription returned and API request failed, break
        #     loop and continue
        # if API request succeeded but no transcription was returned,
        #     re-prompt the user to say their guess again. Do this up
        #     to PROMPT_LIMIT times
        for j in range(PROMPT_LIMIT):
            print('Guess {}. Speak!'.format(i+1))
            guess = recognize_speech_from_mic(recognizer, microphone)
            if guess["transcription"]:
                break
            if not guess["success"]:
                break
            print("I didn't catch that. What did you say?\n")

        # if there was an error, stop the game
        if guess["error"]:
            print("ERROR: {}".format(guess["error"]))
            break

        # show the user the transcription
        print("You said: {}".format(guess["transcription"]))

        # determine if guess is correct and if any attempts remain
        guess_is_correct = guess["transcription"].lower() == word.lower()
        user_has_more_attempts = i < NUM_GUESSES - 1

        # determine if the user has won the game
        # if not, repeat the loop if user has more attempts
        # if no attempts left, the user loses the game
        if guess_is_correct:
            print("Correct! You win!".format(word))
            break
        elif user_has_more_attempts:
            print("Incorrect. Try again.\n")
        else:
            print("Sorry, you lose!\nI was thinking of '{}'.".format(word))
            break

Let’s break that down a little bit.

The recognize_speech_from_mic() function takes a Recognizer and Microphone instance as arguments and returns a dictionary with three keys. The first key, "success", is a boolean that indicates whether or not the API request was successful. The second key, "error", is either None or an error message indicating that the API is unavailable or the speech was unintelligible. Finally, the "transcription" key contains the transcription of the audio recorded by the microphone.

The function first checks that the recognizer and microphone arguments are of the correct type, and raises a TypeError if either is invalid:

if not isinstance(recognizer, sr.Recognizer):
    raise TypeError('`recognizer` must be `Recognizer` instance')

if not isinstance(microphone, sr.Microphone):
    raise TypeError('`microphone` must be a `Microphone` instance')

The listen() method is then used to record microphone input:

with microphone as source:
    recognizer.adjust_for_ambient_noise(source)
    audio = recognizer.listen(source)

The adjust_for_ambient_noise() method is used to calibrate the recognizer for changing noise conditions each time the recognize_speech_from_mic() function is called.

Next, recognize_google() is called to transcribe any speech in the recording. A try...except block is used to catch the RequestError and UnknownValueError exceptions and handle them accordingly. The success of the API request, any error messages, and the transcribed speech are stored in the success, error and transcription keys of the response dictionary, which is returned by the recognize_speech_from_mic() function.

response = {
    "success": True,
    "error": None,
    "transcription": None
}

try:
    response["transcription"] = recognizer.recognize_google(audio)
except sr.RequestError:
    # API was unreachable or unresponsive
    response["success"] = False
    response["error"] = "API unavailable"
except sr.UnknownValueError:
    # speech was unintelligible
    response["error"] = "Unable to recognize speech"

return response

You can test the recognize_speech_from_mic() function by saving the above script to a file called “guessing_game.py” and running the following in an interpreter session:

>>> import speech_recognition as sr
>>> from guessing_game import recognize_speech_from_mic
>>> r = sr.Recognizer()
>>> m = sr.Microphone()
>>> recognize_speech_from_mic(r, m)
{'success': True, 'error': None, 'transcription': 'hello'}
>>> # Your output will vary depending on what you say

The game itself is pretty simple. First, a list of words, a maximum number of allowed guesses and a prompt limit are declared:

WORDS = ['apple', 'banana', 'grape', 'orange', 'mango', 'lemon']
NUM_GUESSES = 3
PROMPT_LIMIT = 5

Next, a Recognizer and Microphone instance is created and a random word is chosen from WORDS:

recognizer = sr.Recognizer()
microphone = sr.Microphone()
word = random.choice(WORDS)

After printing some instructions and waiting for 3 three seconds, a for loop is used to manage each user attempt at guessing the chosen word. The first thing inside the for loop is another for loop that prompts the user at most PROMPT_LIMIT times for a guess, attempting to recognize the input each time with the recognize_speech_from_mic() function and storing the dictionary returned to the local variable guess.

If the "transcription" key of guess is not None, then the user’s speech was transcribed and the inner loop is terminated with break. If the speech was not transcribed and the "success" key is set to False, then an API error occurred and the loop is again terminated with break. Otherwise, the API request was successful but the speech was unrecognizable. The user is warned and the for loop repeats, giving the user another chance at the current attempt.

for j in range(PROMPT_LIMIT):
    print('Guess {}. Speak!'.format(i+1))
    guess = recognize_speech_from_mic(recognizer, microphone)
    if guess["transcription"]:
        break
    if not guess["success"]:
        break
    print("I didn't catch that. What did you say?\n")

Once the inner for loop terminates, the guess dictionary is checked for errors. If any occurred, the error message is displayed and the outer for loop is terminated with break, which will end the program execution.

if guess['error']:
    print("ERROR: {}".format(guess["error"]))
    break

If there weren’t any errors, the transcription is compared to the randomly selected word. The lower() method for string objects is used to ensure better matching of the guess to the chosen word. The API may return speech matched to the word “apple” as “Apple” or “apple,” and either response should count as a correct answer.

If the guess was correct, the user wins and the game is terminated. If the user was incorrect and has any remaining attempts, the outer for loop repeats and a new guess is retrieved. Otherwise, the user loses the game.

guess_is_correct = guess["transcription"].lower() == word.lower()
user_has_more_attempts = i < NUM_GUESSES - 1

if guess_is_correct:
    print('Correct! You win!'.format(word))
    break
elif user_has_more_attempts:
    print('Incorrect. Try again.\n')
else:
    print("Sorry, you lose!\nI was thinking of '{}'.".format(word))
    break

When run, the output will look something like this:

I'm thinking of one of these words:
apple, banana, grape, orange, mango, lemon
You have 3 tries to guess which one.

Guess 1. Speak!
You said: banana
Incorrect. Try again.

Guess 2. Speak!
You said: lemon
Incorrect. Try again.

Guess 3. Speak!
You said: Orange
Correct! You win!

Recap and Additional Resources

In this tutorial, you’ve seen how to install the SpeechRecognition package and use its Recognizer class to easily recognize speech from both a file—using record()—and microphone input—using listen(). You also saw how to process segments of an audio file using the offset and duration keyword arguments of the record() method.

You’ve seen the effect noise can have on the accuracy of transcriptions, and have learned how to adjust a Recognizer instance’s sensitivity to ambient noise with adjust_for_ambient_noise(). You have also learned which exceptions a Recognizer instance may throw—RequestError for bad API requests and UnkownValueError for unintelligible speech—and how to handle these with try...except blocks.
