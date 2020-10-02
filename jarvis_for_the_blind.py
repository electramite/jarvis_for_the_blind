import cv2
import numpy as np
import pyttsx3
import RPi.GPIO as GPIO # this module is available only for raspberry pi to perform any operation on its GPIO pins
import speech_recognition as sr
import datetime
import smtplib
import wikipedia

engine = pyttsx3.init()
def wishMe(): # this function wish the user depending upon the real time
    hour =int(datetime.datetime.now().hour)
    if hour>= 0 and hour< 12:
        speak('good morning')
    elif hour >= 12 and hour < 18:
        speak('good afternoon')
    else:
        speak('good evening')
    speak('how can i help you  ?')

def takeCommand():#this function stores the voice command and return the command in string format
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("listning...")
        audio = r.listen(source)
    try:
        print('recognizing..')
        query = r.recognize_google(audio, language='en-in')
        print(f"user said: {query}\n")
    except Exception as e:
        print(e)
        print('say that again please')
        return "none"
    return query

def speak(audio): # this function converts the string into audio(voice) format
    engine.say(audio)
    engine.runAndWait()

def sendEmail(to, msg):# this function used to send email to the reciever
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login('sender@gmail.com', 'password') # sender's email
    server.sendmail('electramite@gmail.com', to, msg)
    server.close()

GPIO.setmode(GPIO.BOARD) # we are using board configuration (physical configuration)
button = 12 # attaching a button to the pin number 12
GPIO.setup(button, GPIO.IN, pull_up_down=GPIO.PUD_UP)
cap = cv2.VideoCapture(0)

while cap.isOpened():
    _, frame = cap.read()
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV) # changing color space from RGB to HSV

    red_lower = np.array([136, 87, 111]) # thresholding the HSV image for RED color
    red_upper = np.array([180, 255, 255])

    blue_lower = np.array([99, 115, 150])  # thresholding the HSV image for BLUE color
    blue_upper = np.array([110, 255, 255])

    yellow_lower = np.array([22, 60, 200])  # thresholding the HSV image for YELLOW color
    yellow_upper = np.array([60, 255, 255])

    green_lower = np.array([65,60,60])  # thresholding the HSV image for GREEN color
    green_upper = np.array([80,255,255])

    white_lower = np.array([180,255,200])  # thresholding the HSV image for WHITE color
    white_upper = np.array([180,255,255])

    black_lower = np.array([180,255,0]) # thresholding the HSV image for BLACK color
    black_upper = np.array([180,255,30])

    red = cv2.inRange(hsv, red_lower, red_upper) # extracting RED object from the image
    blue = cv2.inRange(hsv, blue_lower, blue_upper) # extracting BLUE object from the image
    yellow = cv2.inRange(hsv, yellow_lower, yellow_upper) # extracting YELLOW object from the image
    green = cv2.inRange(hsv, green_lower, green_upper) # extracting GREEN object from the image
    white = cv2.inRange(hsv, white_lower, white_upper) # extracting WHITE object from the image
    black = cv2.inRange(hsv, black_lower, black_upper) # extracting BLACK object from the image

    kernal = np.ones((5, 5), "uint8")

    red = cv2.dilate(red, kernal) # applying morphological transformation
    res = cv2.bitwise_and(frame, frame, mask=red) # masking of RED objects

    blue = cv2.dilate(blue, kernal)
    res1 = cv2.bitwise_and(frame, frame, mask=blue) # masking of BLUE objects

    yellow = cv2.dilate(yellow, kernal)
    res2 = cv2.bitwise_and(frame, frame, mask=yellow) # masking of YELLOW objects

    green = cv2.dilate(green, kernal)
    res3 = cv2.bitwise_and(frame, frame, mask=green) # masking of GREEN objects

    white = cv2.dilate(white, kernal)
    res4 = cv2.bitwise_and(frame, frame, mask=white) # masking of WHITE objects

    black = cv2.dilate(black, kernal)
    res5 = cv2.bitwise_and(frame, frame, mask=black) # masking of BLACK objects

    if GPIO.input(button) == 0:

     #traking of red object
        (_, contours, hierarchy) = cv2.findContours(red, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        for pic, contour in enumerate(contours):
            engine = pyttsx3.init()
            area = cv2.contourArea(contour)
            if (area > 500):
                x, y, w, h = cv2.boundingRect(contour)
                img = cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
                cv2.putText(frame, "RED", (x, y), cv2.FONT_HERSHEY_SCRIPT_SIMPLEX, 0.7, (0, 0, 255))
                if GPIO.input(button) == 0 and area >= 500: #if button is pressed and detected area is more than 500
                    engine.say('red')#pronounce the name of color
                    engine.runAndWait()

    # traking of blue object
        (_, contours, hierarchy) = cv2.findContours(blue, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        for pic, contour in enumerate(contours):
            area = cv2.contourArea(contour)
            if (area > 500):
                x, y, w, h = cv2.boundingRect(contour)
                img = cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
                cv2.putText(frame, "BLUE", (x, y), cv2.FONT_HERSHEY_SCRIPT_SIMPLEX, 0.7, (255, 0, 0))
                if GPIO.input(button) == 0 and area >= 500: #if button is pressed and detected area is more than 500
                    engine.say('blue')#pronounce the name of color
                    engine.runAndWait()

    # traking of yellow object
        (_, contours, hierarchy) = cv2.findContours(yellow, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        for pic, contour in enumerate(contours):
            area = cv2.contourArea(contour)
            if (area > 500):
                x, y, w, h = cv2.boundingRect(contour)
                img = cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                cv2.putText(img, "yellow  color", (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 255, 0))
                if GPIO.input(button) == 0 and area >= 500:#if button is pressed and detected area is more than 500
                    engine.say('yellow') #pronounce the name of color
                    engine.runAndWait()

    # traking of green object
        (_, contours, hierarchy) = cv2.findContours(green, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        for pic, contour in enumerate(contours):
            area = cv2.contourArea(contour)
            if (area > 500):
                x, y, w, h = cv2.boundingRect(contour)
                img = cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
                cv2.putText(frame, "GREEN", (x, y), cv2.FONT_HERSHEY_SCRIPT_SIMPLEX, 0.7, (255, 0, 0))
                if GPIO.input(button) == 0 and area >= 500: #if button is pressed and detected area is more than 500
                    engine.say('green')#pronounce the name of color
                    engine.runAndWait()
    # traking of white object
        (_, contours, hierarchy) = cv2.findContours(white, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        for pic, contour in enumerate(contours):
            area = cv2.contourArea(contour)
            if (area > 500):
                x, y, w, h = cv2.boundingRect(contour)
                img = cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
                cv2.putText(frame, "WHITE", (x, y), cv2.FONT_HERSHEY_SCRIPT_SIMPLEX, 0.7, (255, 0, 0))
                if GPIO.input(button) == 0 and area >= 500: #if button is pressed and detected area is more than 500
                    engine.say('white')#pronounce the name of color
                    engine.runAndWait()

    # traking of black object
        (_, contours, hierarchy) = cv2.findContours(black, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        for pic, contour in enumerate(contours):
            area = cv2.contourArea(contour)
            if (area > 500):
                x, y, w, h = cv2.boundingRect(contour)
                img = cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
                cv2.putText(frame, "BLACK", (x, y), cv2.FONT_HERSHEY_SCRIPT_SIMPLEX, 0.7, (255, 0, 0))
                if GPIO.input(button) == 0 and area >= 500: #if button is pressed and detected area is more than 500
                    engine.say('black')#pronounce the name of color
                    engine.runAndWait()
        cv2.imshow("object", frame)
    else:
    #jarvis
        query = takeCommand().lower() # converting the command string in lowercase string
        if 'send email' in query: # if send email is present in the query
            try:
                speak("what should i say?")
                msg = takeCommand() # stores the message
                to = "receiver@gmail.com" # receivers email
                sendEmail(to, msg)
                speak("sent")
            except Exception as e:
                print(e)
                speak("i am sorry") # if unable to send email say sorry
        elif 'wikipedia' in query: # if user want to search anything on wikipedia
            speak('searching wikipedia')
            query = query.replace('wikipedia', '')
            results = wikipedia.summary(query, sentences=2)
            speak("According to wikipedia")
            speak(results) # pronounce the search results
        elif 'the time' in query:# if user wants to know the time
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"the time is {strTime}")

    if cv2.waitKey(1) & 0xFF == ord('q'):
        cap.release()
        cv2.destroyAllWindows()
        break