import time

import speech_recognition as sr
import webbrowser as wb

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


def search_query(engine, term):
    if engine.lower() == 'youtube':
        url = "https://www.youtube.com/results?search_query=" + term
        wb.get().open_new(url)
    elif engine.lower() == 'google':
        url = "https://www.google.com/search?q=" + term
        wb.get().open_new(url)
    elif engine.lower() == 'bing':
        pass
    else:
        print("We do not support anything other than Google, Youtube, and Bing. Thank You.")

def extract_query(query_term):
    try:
        # search on google for bla bla bla
        engine = query_term[query_term.index('on') + 3:query_term.index('for') - 1]
        term = query_term[query_term.index('for') + 4:]
        print("engine: " + engine)
        print("term: " + term)
        search_query(engine, term)
    except ValueError:
        print("I didn't catch that. What did you say?\n") 


if __name__ == "__main__":
    # create recognizer and mic instances
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    run = True
    while run:
        print("Speak!")
        response = recognize_speech_from_mic(recognizer, microphone)
        # if there was an error, stop the process
        if response["error"]:
            print("ERROR: {}".format(response["error"]))
            run = False
        if not response["success"]:
            print("I didn't catch that. What did you say?\n")
        
        if response["transcription"]:
            if "Terminate" in response["transcription"]:
                run = False
                print("Program Terminated.")
            else:
                extract_query(response["transcription"])
        else:
            print("I didn't catch that. What did you say?\n")