import os
import pyttsx3
import datetime
import webbrowser
import smtplib
import wikipedia
import pyjokes
import requests
from twilio.rest import Client
import ctypes
import time
import wolframalpha
import pyautogui
import MyAlarm
import urllib.request
import cv2
import speech_recognition as sr
import numpy as np 
import pyautogui as p
import PyPDF2
import operator
import random 


def initialize_speech_engine():
    engine = pyttsx3.init('sapi5')
    voices = engine.getProperty('voices');
    engine.setProperty('voices', voices[0].id)
    engine.setProperty('rate',200)
    return engine

#text to speech
def speak(engine, audio):
    engine.say(audio)
    print(audio)
    engine.runAndWait()

def pdf_reader():
    book = open('RichDadPoorDad.pdf', 'rb')
    pdfReader = PyPDF2.PdfReader(book)
    pages = len(pdfReader.pages)
    
    speak(engine, f"Total number of pages in this book: {pages}")
    speak(engine, "Sir, please enter the page number I have to read")
    
    pg = int(input("Please enter the page number: "))
    page = pdfReader.pages[pg - 1]  # Adjust for 0-based index
    text = page.extract_text()
    
    speak(engine, text)
    

#To convert voice into text
def  take_command(recognizer):
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("listening...")
        recognizer.pause_threshold = 1
        audio = recognizer.listen(source,timeout=5,phrase_time_limit=8)

    try:
        print("Recognizing...")
        query = recognizer.recognize_google(audio, language='en-in')
        print(f"user said: {query}\n")

    except Exception as e:
        speak(engine, "Unable to Recognize your voice.")
        return "None"
    
    return query




#to wish
def wishme(engine):
    hour = int(datetime.datetime.now().hour)
    tt = time.strftime("%I:%M %p")

    if hour >= 0 and hour <= 12:
        speak(engine, f"good morning, its {tt}")
    elif hour >= 12 and hour <= 18:
        speak(engine, f"good afternoon, its {tt}")
    else:
        speak(engine, f"good evening, its {tt}")
    speak(engine, "i am rex sir. please tell me how may i help you")

"""    
#to send email
def sendEmail(to,content):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login('YOUR EMAIL ADDRESS', 'YOUR PASSWORD')
    server.sendmail('YOUR EMAIL ADDRESS', to, content)
    server.close()
 """
 
 

#for news updates
def news():
    main_url = 'http://newsapi.org/v2/top-headlines?sources=techcrunch&apiKey="YOUR_API_HERE"'

    main_page = requests.get(main_url).json()
    # print(main_page)
    articles = main_page["articles"]
    # print(articles)
    head = []
    day=["first","second","third","fourth","fifth","sixth","seventh","eighth","ninth","tenth"]
    for ar in articles:
        head.append(ar["title"])
    for i in range (len(day)):
        # print(f"today's {day[i]} news is: ", head[i])
        speak(engine, f"today's {day[i]} news is: {head[i]}")



if __name__ == "__main__": #main program
    engine = initialize_speech_engine()
    recognizer = sr.Recognizer()
    wishme(engine)
    while True:
    # if 1:

        query = take_command(engine).lower()

        #logic building for tasks

        if "open notepad" in query:
            npath = "C:\\Windows\\system32\\notepad.exe"
            os.startfile(npath)
            
        elif 'hey' in query:
            speak(engine, 'Hello sir, how may I help you?')
        
        elif "open adobe reader" in query:
            apath = "C:\\Program Files (x86)\\Adobe\\Reader 11.0\\Reader\\AcroRd32.exe"
            os.startfile(apath)

        elif "open command prompt" in query:
            os.system("start cmd")
            
        elif "open youtube" in query:
            webbrowser.open("https://www.youtube.com")
            
        elif "open google" in query:
            webbrowser.open("https://www.google.com")
            
        elif "open wikipedia" in query:
            webbrowser.open("https://www.wikipedia.com")
            
        elif "open instagram" in query:
            webbrowser.open("https://www.instagram.com")
            
        elif 'joke' in query:
            speak(engine, pyjokes.get_joke())
        
        elif 'MAke me laugh' in query:
            speak(engine, pyjokes.get_joke())


        elif "open camera" in query:
            cap = cv2.VideoCapture(0)
            while True:
                ret, img = cap.read()
                cv2.imshow('webcam', img)
                k = cv2.waitKey(50)
                if k==27:
                    break;
            cap.release()
            cv2.destroyAllWindows()

        elif "play music" in query:
            music_dir = "E:\\music"
            songs = os.listdir(music_dir)
            # rd = random.choice(songs)
            for song in songs:
                if song.endswith('.mp3'):
                    os.startfile(os.path.join(music_dir, song))
     
     
        elif "hide all files" in query or "hide this folder" in query or "visible for everyone" in query:
            speak(engine, "sir please tell me you want to hide this folder or make it visible for everyone")
            condition = take_command(recognizer).lower()
            if "hide" in condition:
                os.system("attrib +h /s /d") #os module
                speak(engine, "sir, all the files in ths folder are now hidden.")
                
            elif "visible" in condition:
                os.system("attrib -h /s /d")
                speak(engine, "sir, all the files in this folder are now visible to everyone. i wish you are taking this decision on your own peace")
                
            elif "leave it" in condition or "leave for now" in condition:
                speak(engine, "Ok sir")
     
        elif "do some calculations" in query or "can you calculate" in query:
            r = sr.Recognizer()
            with sr.Microphone() as source:
                speak(engine, "Say what you want to calculate, example: 3 plus 3")
                print("listening.....")
                r.adjust_for_ambient_noise(source)
                audio = r.listen(source)
            my_string= r.recognize_google(audio)
            print(my_string)
            def get_operator_fn(op):
                return {
                    '+' : operator.add, #plus
                    '-' : operator.sub, #minus
                    'x' : operator.mul, #multiplied by
                    'dividend' :operator.__truediv__, #divided
                }[op]
            # Assuming you have a function eval_binary_expr defined like this:
            def get_operator_fn(op):
                return {
                    '+' : operator.add, #plus
                    '-' : operator.sub, #minus
                    '*' : operator.mul, #multiplied by
                    'divided' : operator.__truediv__, #dividend
                    }[op]
            def eval_binary_expr(op1, oper, op2):
                op1,op2 = int(op1), int(op2)
                return get_operator_fn(oper)(op1, op2)
            speak(engine, "your result is")
            speak(engine, eval_binary_expr(*(my_string.split())))
        
     
     #Reading Pdf 
        elif "audiobook" in query:
            pdf_reader()
            
    #Telling my exact locatin through IP address
       
        elif "where i am" in query or "where we are" in query:
            speak("wait sir. let me check")
            try:
                ipAdd = requests.get('https://api.ipify.org').text
                print(ipAdd)
                url = 'https://get.geojs.io/v1/ip/geo/'+ipAdd+'.json'
                geo_requests = requests.get(url)
                geo_data = geo_requests.json()
                # print(geo_data)
                city = geo_data['city']
                # state = geo_data['state']
                country = geo_data['country']
                speak(engine, f"sir i am not sure, but i think we are in {city} city of {country} country")
                
            except Exception as e:
                speak(engine, "sorry sir, Due to network issue i am not able to find where we are.")
                pass
        
        
        #Open instagram profile of any user by entering username    
        elif "instagram profile" in query or "profile on instagram" in query:
            speak(engine, "sir please enter the username correctly.")
            name = input("Enter username here:")
            webbrowser.open(f"www.instagram.com/{name}")
            speak(engine, f"Sir here is the profile of the user {name}")

        #Take a screenshot   
        elif "take screenshot" in query or "take a screenshot" in query:
            speak(engine, "sir, please tell me the name for this screenshot file")
            name = take_command(recognizer).lower()
            speak(engine, "please sir hold the screen for few seconds, i am taking screenshot")
            time.sleep(3)
            img = pyautogui.screenshot()
            img.save(f"{name}.png")
            speak(engine, "i am done sir, the screenshot is saved in our main folder. now i am ready for the next instruction")
        
        #Ask anything..
        elif "activate how to do mode" in query:
            from pywikihow import search_wikihow
            speak(engine, "How to do mode is activated")
            while True:
                speak(engine,"please tell me what you want to know")
                how = take_command(recognizer)
                try:
                    if "exit" in how or "close" in how:
                        speak("okay sir, how to do mode is closed")
                    else:
                        max_results = 1
                        how_to = search_wikihow(how, max_results)
                        assert len(how_to) == 1
                        speak(engine, how_to[0].summary)
                except Exception as e:
                    speak(engine, "Sorry sir, i am not able to find this")
        
        #Tells the percentage of battery left in my system 
        elif "how much power left" in query or "how much power we have" in query or "battery" in query:
            import psutil
            battery = psutil.sensors_battery()
            percentage = battery.percent
            speak(engine, f"sir our system have {percentage} percent battery")
            print(f"sir our system have {percentage} percent battery")
        
        #Tell the download and upload speed of internet
        elif "internet speed" in query:
            speak(engine, "Ok sir please wait, let me check")
            
            from speedtest import Speedtest

            st = speedtest.Speedtest()
            download_speed = st.download()
            upload_speed = st.upload()
            print(f"Download speed: {download_speed:.2f}Mbps")
            print(f"Upload speed: {upload_speed:.2f}Mbps")
            speak(f"Download speed: {download_speed:.2f} Mbps")
            speak(f"Upload speed: {upload_speed:.2f} Mbps")
            
       #Send message on my phone
        elif "send message" in query:
            speak(engine, "Sir, what should I say")
            msz = take_command(recognizer)
            
            from twilio.rest import Client
            
            account_sid = 'ACdf58f0804c41ab71b0af1cb968a8354f'
            auth_token = '59c70aac498241d9b8be6b7df52b0ace'
            
            client = Client(account_sid, auth_token)
            
            message = client.messages \
                .create(
                    body= msz,
                    from_= '+17697172361',
                    to='+918452900936'
                )
            
            print(message.sid)
            speak(engine, "Sir, message has been sent")
        
        #Call on my phone  
        elif "call" in query:

            from twilio.rest import Client
            
            account_sid = 'ACdf58f0804c41ab71b0af1cb968a8354f'
            auth_token = '59c70aac498241d9b8be6b7df52b0ace'
            
            client = Client(account_sid, auth_token)
            
            message = client.calls \
                .create(
                    twiml='<Response><Say>This is just a testing call from rex...</Say></Response>',
                    from_= '+17697172361',
                    to='+918452900936'
                )
            
            print(message.sid)
        
        #Making volume up, down and mute of my system   
        elif "volume up" in query:
            pyautogui.press("volumeup")
            
        elif "volume down" in query:
            pyautogui.press("volumedown")
            
        elif "volume mute" in query:
            pyautogui.press("volumemute")
         
        #Set alarm   
        elif "alarm" in query:
            speak(engine, "sir please tell me the time to set alarm. for example, set alarm to 5:40pm")
            tt = take_command(recognizer)
            tt = tt.replace("set alarm to ", "")
            tt = tt.replace(".","")
            tt = tt.upper()
            MyAlarm.alarm(tt)
        
        #Open my mobile camera through IP webcam
        elif "open mobile camera" in query:
            URL = "http://192.168.86.28:8080/shot.jpg"
            while True:
                img_arr = np.array(bytearray(urllib.request.urlopen(URL).read()),dtype=np.uint8)
                img = cv2.imdecode(img_arr,-1)
                cv2.imshow('IPWebcam',img)
                q = cv2.waitKey(1)
                if q == ord("q"):
                    break;
                
            cv2.destroyAllWindows()
        
        #Exit function   
        elif "exit" in query:
            speak(engine, "Thanks for giving me your time")
            exit()


