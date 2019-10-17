# the speech is recognized and search on either youtube or google as specified


import speech_recognition as sr
import selenium as wb

#NOTE: here "selenium" is used to access web browers , there are other packages also availabe like "webbrowser"

r1=sr.Recognizer()
r2=sr.Recognizer()
r3=sr.Recognizer()

with sr.Microphone as source:
    print("search:")
    print("speak now:")
    audio=r3.listen(source)
if 'youtube' in r2.recognize_google(audio):
    r2=sr.Recognizer()
    url='https://www.youtube.com/results?search_query='
    with sr.Mircophone as source:
        print('search query')
        audio=r2.listen(source)
        
        try:
            get=r2.recognize_google(audio)
            print(get)
            wb.get().open_new(url+get)
        except sr.UnknownValueError:
            print('error')
        except sr.RequestError as e:
            print('faled to recognize')
if 'Google' in r2.recognize_google(audio):
    r2=sr.Recognizer()
    url='https://www.google.com/search?q='
    with sr.Mircophone as source:
        print('search query')
        audio=r2.listen(source)
        
        try:
            get=r2.recognize_google(audio)
            print(get)
            wb.get().open_new(url+get)
        except sr.UnknownValueError:
            print('error')
        except sr.RequestError as e:
            print('faled to recognize')    
