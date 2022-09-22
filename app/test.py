import requests

# resp = requests.post("http://127.0.0.1:8080/predict", files={"file":open("test.wav", "rb")})


resp = requests.post("http://cradle-server.herokuapp.com/predict",
                      files={"file":open("yeni2.wav", "rb")})

# resp = requests.post("http://localhost:5000/predict",
#                       files={"file":open("test.wav", "rb")})

print(resp.text)





import pyaudio

def record_and_send():
    pa = pyaudio.PyAudio()

    stream_in = pa.open(
                        rate=22050,
                        channels=1,
                        format=pyaudio.paInt16,
                        input=True,                   # input stream flag
                        input_device_index=7,         # input device index
                        frames_per_buffer=1024
                        )

    audio_bytes=  stream_in.read(5*22050)



    resp = requests.post("http://cradle-server.herokuapp.com/predict",
                      files={"file":None},
                      data=audio_bytes)


    print(resp.text)