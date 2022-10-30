import requests

import pyaudio

import wave

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
    
    wave_write = wave.open("./app/testAudio/test.wav", "wb")
    
    wave_write.setnchannels(1)        # number of channels  - mono channel
    wave_write.setsampwidth(2)        # sample width in bytes
    wave_write.setframerate(22050)    # sampling rate in Hz

    wave_write.writeframes(audio_bytes)

    wave_write.close()

    # print(type(audio_bytes))

    # resp = requests.post(   "http://cradle-server.herokuapp.com/predict",
                            # files={"file":open("./app/testAudio/test.wav", "rb")},
                            # data=audio_bytes
                        # )

    resp = requests.post(   "http://cradle-server.herokuapp.com/predict",
                            files=None,
                            data=audio_bytes
                    )

    print(resp.text)



record_and_send() 


# resp = requests.post("http://127.0.0.1:8080/predict", files={"file":open("./app/testAudio/yeni.wav", "rb")})


# resp = requests.post("http://cradle-server.herokuapp.com/predict",
                      # files={"file":open("./app/testAudio/test.wav", "rb")})

# resp = requests.post("http://localhost:5000/predict",
#                       files={"file":open("./app/testAudio/test.wav", "rb")})




# print(resp.text)



