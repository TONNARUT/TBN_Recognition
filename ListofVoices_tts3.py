# Print all available voices
import pyttsx3
engine = pyttsx3.init()

voices = engine.getProperty('voices')
for voice in voices:
    print("Voice:")
    print(" - ID: %s" % voice.id)
    print(" - Name: %s" % voice.name)
    print(" - Languages: %s" % voice.languages)
    print(" - Gender: %s" % voice.gender)
    print(" - Age: %s" % voice.age)

my_voice_id = "english-us"
amount = 500 

engine.setProperty('volume', 0.9)  # Volume 0-1
engine.setProperty('rate', 120)  #148
#engine.setProperty('voice', my_voice_id)
engine.setProperty('voice', voices[11].id)
engine.say(str(amount) + 'baht')
engine.say('Hello , my name is Narut')
engine.runAndWait()