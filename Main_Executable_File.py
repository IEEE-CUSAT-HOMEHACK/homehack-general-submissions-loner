import ctypes
import time
import pyautogui as pg
import speech_recognition as sr
import random
import subprocess as sp
import finger as fd

SendInput = ctypes.windll.user32.SendInput


Esc=0x01
One=0x02
Backspace=0x0E
Enter=0x1C
Caps=0x3A
Tab=0x0F
Q=0x10
W=0x11
E=0x12
R=0x13
T=0x14
Y=0x15
U=0x16
I=0x17
O=0x18
P=0x19
A=0x1E
S=0x1F
D=0x20
F=0x21
G=0x22
H=0x23
J=0x24
K=0x25
L=0x26
Z=0x2C
X=0x2D
C=0x2E
V=0x2F
B=0x30
N=0x31
M=0x32
Space=0x39
LShift=0x2A
RShift=0x36
Ctrl=0x1D
Alt=0x38
Left=0x4B
Right=0x4D
Up=0x48
Down=0x50

PUL = ctypes.POINTER(ctypes.c_ulong)
class KeyBdInput(ctypes.Structure):
    _fields_ = [("wVk", ctypes.c_ushort),
                ("wScan", ctypes.c_ushort),
                ("dwFlags", ctypes.c_ulong),
                ("time", ctypes.c_ulong),
                ("dwExtraInfo", PUL)]

class HardwareInput(ctypes.Structure):
    _fields_ = [("uMsg", ctypes.c_ulong),
                ("wParamL", ctypes.c_short),
                ("wParamH", ctypes.c_ushort)]

class MouseInput(ctypes.Structure):
    _fields_ = [("dx", ctypes.c_long),
                ("dy", ctypes.c_long),
                ("mouseData", ctypes.c_ulong),
                ("dwFlags", ctypes.c_ulong),
                ("time",ctypes.c_ulong),
                ("dwExtraInfo", PUL)]

class Input_I(ctypes.Union):
    _fields_ = [("ki", KeyBdInput),
                 ("mi", MouseInput),
                 ("hi", HardwareInput)]

class Input(ctypes.Structure):
    _fields_ = [("type", ctypes.c_ulong),
                ("ii", Input_I)]


def PressKey(hexKeyCode):
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput( 0, hexKeyCode, 0x0008, 0, ctypes.pointer(extra) )
    x = Input( ctypes.c_ulong(1), ii_ )
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))

def ReleaseKey(hexKeyCode):
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput( 0, hexKeyCode, 0x0008 | 0x0002, 0, ctypes.pointer(extra) )
    x = Input( ctypes.c_ulong(1), ii_ )
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))

def PressThese(Order):
    Order=[x.capitalize() for x in Order]
    for iterator in range(len(Order)):
        try:
            PressKey(eval(Order[iterator]))
            time.sleep(1)
            ReleaseKey(eval(Order[iterator]))
            time.sleep(1)
        except:
            print("I can't press {}".format(Order[iterator:]))

def recognize_speech_from_mic(recognizer, microphone):
    if not isinstance(recognizer, sr.Recognizer):
        raise TypeError("`recognizer` must be `Recognizer` instance")

    if not isinstance(microphone, sr.Microphone):
        raise TypeError("`microphone` must be `Microphone` instance")

    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    response = {
        "success": True,
        "error": None,
        "transcription": None
    }
    try:
        response["transcription"] = recognizer.recognize_google(audio)
    except sr.RequestError:
        response["success"] = False
        response["error"] = "API unavailable"
    except sr.UnknownValueError:
        response["error"] = "Unable to recognize speech"
    return response

if __name__ == '__main__':
    try:
        print("Say Something..(try saying 'open mario')")
        recognizer = sr.Recognizer()
        microphone = sr.Microphone()
        time.sleep(5)

        while True:
            guess = recognize_speech_from_mic(recognizer, microphone)
            if guess["error"]:
                print("I didn't catch that. What did you say?")
            else:
                print("You said: {}".format(guess["transcription"]))
                time.sleep(1)
                if 'press' in guess['transcription']:
                    tempolist=guess['transcription'].split()
                    if tempolist.index('press') is len(tempolist)-1:
                        print("What to press?")
                    else:
                        temporlist=[]
                        temporlist.append(tempolist[tempolist.index('press')+1])
                        PressThese(temporlist)
                elif 'open' in guess['transcription']:
                    tempolist=guess['transcription'].split()
                    if tempolist.index('open') is len(tempolist)-1:
                        print("What to open?")
                    else:
                        GarbageVal=sp.Popen('C:\\Program Files\\DOSBox\\DOSBox.exe')
                        time.sleep(7)
                        pg.typewrite('mount c c:\\users\\das\\downloads\\mario \n',interval=0.15)
                        time.sleep(1)
                        pg.typewrite('c:\n',interval=0.15)
                        time.sleep(1)
                        pg.typewrite('mario\n',interval=0.15)
                        time.sleep(5)
                        Order=['enter','enter','enter','enter']
                        PressThese(Order)
                        break
        fd.main()
        
        
    except KeyboardInterrupt:
        print("Exiting...")
