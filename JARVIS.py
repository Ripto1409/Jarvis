import pyttsx3
import speech_recognition as sr
import datetime
import wikipedia
import webbrowser
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import QTimer, QTime, QDate, Qt
from PyQt5.QtGui import QMovie
from PyQt5.QtWidgets import QMainWindow, QApplication
import sys
from jarvisUI import Ui_MainWindow  # Adjust the filename as needed

# Initialize text-to-speech engine
engine = pyttsx3.init('sapi5')
voice = engine.getProperty('voices')  # Getting details of current voice
engine.setProperty('voices', voice[0].id)

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def wishMe():
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour < 12:
        print("Good Morning Ripto")
        speak("Good Morning Ripto")
    elif hour >= 12 and hour < 18:
        print("Good Afternoon Ripto")
        speak("Good Afternoon Ripto")
    else:
        print("Good Evening Ripto!")
        speak("Good Evening Ripto!")
    speak("I AM JARVIS! HOW CAN I HELP YOU")

class MainThread(QtCore.QThread):
    def __init__(self):
        super(MainThread, self).__init__()

    def run(self):
        self.TaskExecution()

    def takeCommand(self):
        # Takes microphone input from the user and returns string output
        r = sr.Recognizer()
        with sr.Microphone() as source:
            print("Listening...")
            r.pause_threshold = 1
            audio = r.listen(source)
        try:
            print("Recognizing...")
            query = r.recognize_google(audio, language='en-in')
            print(f"User said: {query}\n")
        except Exception as e:
            print("Say that again please...")
            return "None"
        return query

    def TaskExecution(self):
        while True:
            self.query = self.takeCommand().lower()  # Convert user query into lowercase

            # Logic for executing tasks based on query
            if 'wikipedia' in self.query:
                speak('Searching Wikipedia...')
                self.query = self.query.replace("wikipedia", "")
                results = wikipedia.summary(self.query, sentences=2)
                speak("According to Wikipedia")
                print(results)
                speak(results)

            elif 'open youtube' in self.query:
                webbrowser.open("youtube.com")

            elif 'open google' in self.query:
                webbrowser.open("google.com")

            elif 'the time' in self.query:
                strTime = datetime.datetime.now().strftime("%H:%M:%S")
                speak(f"Sir, the time is {strTime}")

class Main(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(self.startTask)
        self.ui.pushButton_2.clicked.connect(self.close)
        self.thread = MainThread()  # Create the MainThread instance

    def startTask(self):
        wishMe()  # Call wishMe when the RUN button is clicked
        self.ui.movie = QMovie("../../../Downloads/7LP8.gif")
        self.ui.label.setMovie(self.ui.movie)
        self.ui.movie.start()
        self.ui.movie = QMovie("../../../Downloads/jarvis gif 2.gif")
        self.ui.label_2.setMovie(self.ui.movie)
        self.ui.movie.start()
        timer = QTimer(self)
        timer.timeout.connect(self.showTime)
        timer.start(1000)
        self.thread.start()  # Start the MainThread when the RUN button is clicked

    def showTime(self):
        current_time = QTime.currentTime()
        current_date = QDate.currentDate()
        label_time = current_time.toString('hh:mm:ss')
        label_date = current_date.toString(Qt.ISODate)
        self.ui.textBrowser.setText(label_date + '\n' + label_time)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    JarvisUI = Main()
    JarvisUI.show()
    sys.exit(app.exec_())
