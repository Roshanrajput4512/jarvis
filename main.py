import pyttsx3
import speech_recognition as sr
import random
import webbrowser
import datetime
import wikipedia

try:
    import google.generativeai as genai
    genai_available = True
except ModuleNotFoundError:
    genai_available = False

# Configure Gemini API (If available)
if genai_available:
    genai.configure(api_key="YOUR_API_KEY")  # Replace with your actual API key

# Initialize TTS engine
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id if len(voices) > 1 else voices[0].id)
engine.setProperty("rate", 170)

def speak(audio):
    """Speaks the given text"""
    print("Assistant:", audio)
    engine.say(audio)
    engine.runAndWait()

def command():
    """Listens to user input and returns the recognized text"""
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("\nListening...")
        r.adjust_for_ambient_noise(source)
        try:
            audio = r.listen(source, timeout=5)
            content = r.recognize_google(audio, language='en-in')
            print("You said:", content)
            return content.lower()
        except sr.UnknownValueError:
            print("Could not understand, please try again...")
            return None
        except sr.RequestError:
            print("Could not connect to Google API.")
            return None
        except sr.WaitTimeoutError:
            print("Listening timed out, please speak again.")
            return None

def query_wikipedia(topic):
    """Searches Wikipedia for the given topic"""
    speak(f"Searching Wikipedia for {topic}...")
    try:
        result = wikipedia.summary(topic, sentences=2)
        print("Wikipedia Result:", result)
        speak(result)
    except wikipedia.exceptions.DisambiguationError as e:
        speak("There are multiple results for this topic. Please be more specific.")
    except wikipedia.exceptions.PageError:
        speak("Sorry, I couldn't find any information on Wikipedia.")
    except Exception as e:
        speak("An error occurred while searching Wikipedia.")
        print("Wikipedia Error:", e)

def query_gemini(prompt):
    """Sends a prompt to the Gemini API and returns the response"""
    if not genai_available:
        speak("Gemini AI is not installed. Please install google-generativeai package.")
        return None

    try:
        response = genai.generate_content(
            model='gemini-1.5-pro-002', contents=[prompt]
        )
        return response.text
    except Exception as e:
        print("Gemini API error:", e)
        return "Sorry, I couldn't process your request."

def main_process():
    speak("Hello! I am your assistant. How can I help you?")
    
    while True:
        request = command()
        if not request:
            continue

        if "hello" in request:
            speak("Welcome, How can I help you.")

        elif "exit" in request or "bye" in request:
            speak("Goodbye! Have a nice day!")
            break

        elif "play music" in request:
            speak("Playing music")
            song = random.choice([
                "https://www.youtube.com/watch?v=afxHk0247bg&list=PLRBp0Fe2GpgnIh0AiYKh7o7HnYAej-5ph",
                "https://www.youtube.com/watch?v=K4DyBUG242c&list=RDQMTgh66LaGkb4&start_radio=1",
                "https://www.youtube.com/watch?v=yJg-Y5byMMw&pp=ygUUY29weXJpZ2h0IGZyZWUgbXVzaWM%3D"
            ])
            webbrowser.open(song)

        elif "time" in request:
            now_time = datetime.datetime.now().strftime("%I:%M %p")
            speak(f"Current time is {now_time}")

        elif "date" in request:
            now_date = datetime.datetime.now().strftime("%d-%m-%Y")
            speak(f"Today's date is {now_date}")

        elif "wikipedia" in request:
            topic = request.replace("wikipedia", "").strip()
            if topic:
                query_wikipedia(topic)
            else:
                speak("Please specify what you want to search on Wikipedia.")

        else:
            speak(f"Searching Wikipedia for {request}...")
            query_wikipedia(request)

main_process()
