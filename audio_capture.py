import speech_recognition as sr
import pyaudio
from vosk import Model, KaldiRecognizer, SetLogLevel

SetLogLevel(-1)

chunk = 1024
py = pyaudio.PyAudio()
stream = py.open(format=pyaudio.paInt16,
                         channels=1,
                         rate=44100,
                         input=True,
                         frames_per_buffer=chunk)

def listen(stream, chunk=1024)->None:
    '''Uses the stream and chunk arguments to enter audio data into the Kaldi Recognizer sequentially and return data
    in the from of a string.'''
    a = 0
    text=""
    model = Model("vosk_models/model")
    rec = KaldiRecognizer(model, 41000)
    print("Start speaking.")
    while True:
        try:
            if rec.AcceptWaveform(stream.read(chunk//2)):
                text+= " "+rec.Result()[14:-3]
                print(text)
                print(a)
                a+=1

        except:
            
            stream.close()
            break


listen(stream, chunk)
