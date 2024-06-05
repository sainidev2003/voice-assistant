import pyttsx3
import speech_recognition as sr
import datetime
import wikipedia
import webbrowser
import os
import smtplib
import random

engine = pyttsx3.init('sapi5')  # instance of text to speech module using 'sapi5(Speech API by Microsoft)'
voices = engine.getProperty('voices')  # getting the voices property from pyttsx3 module
engine.setProperty('voice', voices[0].id)  # assigning the value as the ID of a specific voice from the available voices
print("\033[4m\033[1m" + "\t\t\t\t\t\t\tBARRY VOICE ASSISTANCE" + "\033[0m")


def speak(text):  # function to speak the text passed using pyttsx3 module
    engine.say(text)
    engine.runAndWait()


def wishMe():  # function to fetch current hour(time) and wish me accordingly
    hour = int(datetime.datetime.now().hour)
    if 0 <= hour < 12:
        speak("Good Morning!")
    elif 12 <= hour < 18:
        speak("Good Afternoon!")
    else:
        speak("Good Evening!")
    speak("I am BARRY. How may I help you?")


def takeCommand():  # function to take microphone input from the user and returns string output
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        try:
            audio = r.listen(source, timeout=5)  # Listen for a maximum of 5 seconds
        except sr.WaitTimeoutError:
            print("No speech detected in the last 5 seconds. Stopping listening.")
            return "None"

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}\n")
    except sr.UnknownValueError:
        print("Say that again please...")
        return "None"
    except sr.RequestError as e:
        print(f"Could not request results; {e}")
        return "None"
    return query


def manage_notes_and_tasks():
    notes = []

    while True:
        speak("What would you like to do with your notes and tasks?")
        action = takeCommand().lower()

        if "add" in action:
            speak("What would you like to add?")
            note = takeCommand()
            if note != "None":
                notes.append(note)
                speak("Note added.")
            else:
                speak("No note was added.")

        elif "read" in action:
            if not notes:
                speak("You have no notes or tasks.")
            else:
                speak("Here are your notes and tasks:")
                for i, note in enumerate(notes, 1):
                    speak(f"Note {i}: {note}")

        elif "update" in action:
            if not notes:
                speak("You have no notes or tasks to update.")
            else:
                try:
                    speak("Which note or task would you like to update? Please specify the number.")
                    index = int(takeCommand())
                    if 1 <= index <= len(notes):
                        original_note = notes[index - 1]
                        speak(f"You selected note {index}: {original_note}. What would you like to update it to?")
                        new_note = takeCommand()
                        if new_note != "None":
                            notes[index - 1] = new_note
                            speak("Note updated successfully.")
                        else:
                            speak("No new content provided. Note remains unchanged.")
                    else:
                        speak("Invalid note number.")
                except ValueError:
                    speak("Invalid input. Please specify a valid note number.")

        elif "delete" in action:
            if not notes:
                speak("You have no notes or tasks to delete.")
            else:
                try:
                    speak("Which note or task would you like to delete? Please specify the number.")
                    index = int(takeCommand())
                    if 1 <= index <= len(notes):
                        deleted_note = notes.pop(index - 1)
                        speak(f"Note deleted: {deleted_note}")
                    else:
                        speak("Invalid note number.")
                except ValueError:
                    speak("Invalid input. Please specify a valid note number.")

        elif "exit" in action:
            speak("Exiting the notes and tasks feature.")
            break

        else:
            speak("Sorry, I didn't understand your request. Please try again.")


def sendEmail(to, content):  # function to send email using simple mail transfer protocol (SMTP)
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login('your-email@gmail.com', 'your-password')
    server.sendmail('your-email@gmail.com', to, content)
    server.close()


def tell_joke():  # function to tell a joke among the list of manually added jokes
    jokes = [
        "Why did the golgappa go to school? Because it wanted to become a 'paani puri'-st!",
        "Why was the computer cold? It left its Windows open!",
        "Why did the tomato turn red? Because it saw the salad dressing!",
        "Why don't we tell secrets on a farm? Because the potatoes have eyes, the corn has ears, and the beans stalk!",
        "Why was the math book sad? Because it had too many problems!",
        "Why did the mobile phone go to school? To improve its 'cell-f' esteem!",
        "Why did the bicycle fall over? Because it was two-tired!"
    ]
    joke = random.choice(jokes)
    return joke


def length_conversion(value, from_unit, to_unit):
    conversions = {
        "meters": {"meters": 1, "feet": 3.28084, "inches": 39.3701},
        "feet": {"meters": 0.3048, "feet": 1, "inches": 12},
        "inches": {"meters": 0.0254, "feet": 0.0833333, "inches": 1}
    }
    try:
        result = value * conversions[from_unit][to_unit]
        return result
    except KeyError:
        return None


def weight_conversion(value, from_unit, to_unit):
    conversions = {
        "kilograms": {"kilograms": 1, "pounds": 2.20462},
        "pounds": {"kilograms": 0.453592, "pounds": 1}
    }
    try:
        result = value * conversions[from_unit][to_unit]
        return result
    except KeyError:
        return None


wishMe()

# main logic where we will execute task according to the queries
while True:
    query = takeCommand().lower()

    if 'in wikipedia' in query:  # wikipedia
        speak('Searching Wikipedia...')
        query = query.replace("wikipedia", "")
        results = wikipedia.summary(query, sentences=2)
        speak("According to Wikipedia")
        print(results)
        speak(results)
        speak("thank you")

    elif 'open youtube' in query:  # youtube
        webbrowser.open("youtube.com")

    elif 'open google' in query:  # google
        webbrowser.open("google.com")

    elif 'play music' in query:  # play music
        music_dir = 'D:\\Song'
        songs = os.listdir(music_dir)
        if songs:
            os.startfile(os.path.join(music_dir, songs[0]))
        else:
            speak("No songs found in the directory.")

    elif 'the time' in query:  # spelling the time
        strTime = datetime.datetime.now().strftime("%H:%M:%S")
        speak(f"Sir, the time is {strTime}")

    elif 'send an email' in query:  # sending an email
        try:
            speak("What should I say?")
            content = takeCommand()
            if content == "None":
                speak("No content provided.")
                continue
            speak("Please enter the email to whom you want to send your message.")
            to = input("E-mail: ")
            sendEmail(to, content)
            speak("Email has been sent!")
        except Exception as e:
            print(e)
            speak("Sorry Vishal Singh. I am not able to send this email")

    elif 'calculation' in query:  # performing a calculation
        speak("Sure, please provide the mathematical expression.")
        expression = input("Expression: ")
        try:
            result = eval(expression)
            print(f"Result: {result}")
            speak(f"The result of {expression} is {result}")
        except Exception as e:
            speak("Sorry, I couldn't calculate that.")

    elif 'joke' in query:  # spelling a joke
        speak("Sure, here I present you a funny one.")
        speak(tell_joke())
        speak("Hope, you enjoyed it")

    elif 'note' in query:
        manage_notes_and_tasks()

    elif 'conversion' in query:  # do a conversion based
        speak("Sure, I can help you with unit conversion. Please specify the value.")
        try:
            value = float(takeCommand())
        except ValueError:
            speak("Invalid value provided. Please try again.")
            continue

        speak("Great! Now, please tell me the source unit (e.g., meters, feet, kilograms, pounds).")
        from_unit = takeCommand().lower()

        speak("Excellent! Now, tell me the target unit (e.g., meters, feet, kilograms, pounds).")
        to_unit = takeCommand().lower()

        result = None

        if from_unit in ["meters", "feet", "inches"] and to_unit in ["meters", "feet", "inches"]:
            result = length_conversion(value, from_unit, to_unit)
        elif from_unit in ["kilograms", "pounds"] and to_unit in ["kilograms", "pounds"]:
            result = weight_conversion(value, from_unit, to_unit)

        if result is not None:
            speak(f"{value} {from_unit} is equal to {result:.2f} {to_unit}.")
        else:
            speak("I'm sorry, I can't perform this unit conversion.")

    elif 'exit' in query:  # exit from the loop
        speak("Bye. See you, Vishal Singh.")
        break

    else:
        speak("Sorry, no query matched from my database. Please speak again or try with different commands.")
        print("No query matched")
  