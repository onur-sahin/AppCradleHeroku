

import wave
from flask import Flask, request, jsonify
from app.utils import transform_audio
from app.cry_detection.createModel      import is_it_crying
from app.cry_classification.createModel import classification
import io
import soundfile
import numpy as np
import torch

from typing import BinaryIO


app = Flask(__name__)

ALLOWED_EXTENSIONS = {'wav', 'ogg'}

def allowed_file(filename:str):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# @app.before_first_request
# class detectionmodel:
#     def __init__():
#         pass


@app.route('/', methods=["POST"])
def index():
    return "<h1> APPLICATION ON HEROKU IS RUNNING</h1>"

@app.route('/predict', methods=["POST"])
def predict():

    file:BinaryIO = request.files.get('file')
    
    data = request.data

    if (data==None and file==None):
        return jsonify({"erorr": "NO FILE OR DATA"})

    elif file != None:

        if file.filename == "":
            return jsonify({"erorr": "NO FILE"})

        if not allowed_file(file.filename):
            return jsonify({"error": "FORMAT NOT SUPPORTED"})

        
        audio_bytes:BinaryIO = file.read()

        sig:tuple[np.ndarray, int] = soundfile.read( io.BytesIO(audio_bytes), dtype='float32' )

        waveform:torch.Tensor = torch.from_numpy(sig[0].transpose())
        sr:int = sig[1]

        sig = (waveform, sr)

    elif data != None:

        temp = io.BytesIO()
        
        wave_write = wave.open(temp, "wb")

        wave_write.setnchannels(1)        # number of channels  - mono channel
        wave_write.setsampwidth(2)        # sample width in bytes
        wave_write.setframerate(22050)    # sampling rate in Hz

        wave_write.writeframes(data)

        wave_write.close()
        temp.seek(0)

        sig =  soundfile.read(temp, dtype="float32")

        waveform:torch.Tensor = torch.from_numpy(sig[0].transpose())
        sr:int = sig[1]

        sig = (waveform, sr)


    try:
        

        spectrom = transform_audio(sig)

        outputs_detection = is_it_crying(spectrom)

        # labels = ["belly pain", "burping", "discomfort", "hungry", "tired"]
        # labels = ['Crying baby', 'Silence', 'Noise', 'Baby laugh']

        if(max(outputs_detection, key=outputs_detection.get) == "Crying baby"):

            outputs_classification = classification(spectrom)

        else:
            outputs_classification = None
        

        return jsonify({"output_detection"       : outputs_detection,
                        "outputs_classification" : outputs_classification})

    except BaseException as err:
        return jsonify({"error": str(err)+"\nERROR IN READ/TRASFORM/PREDICTION"})




if __name__ == '__main__':
    app.run(debug=True)
        
