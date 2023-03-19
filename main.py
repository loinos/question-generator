from fastapi import FastAPI, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from pathlib import *
import uuid
import sys
import os
import openai
import json
from types import SimpleNamespace
from vosk import Model, KaldiRecognizer, SetLogLevel
from pydub import AudioSegment
import subprocess
openai.api_key = "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"

app = FastAPI()

def get_questions(n,text):
    messages = []
    message = r"user: составь json файл формата {'questions':[{'question':'*',options[*,*,*,*],'answer':'*номер правильного ответа*'},...]}  на" + str(n) + "вопросов по вот этому тексту :"+str(text)  # вводим сообщение 
    messages.append({"role": "user", "content": message})
    chat = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages = messages)
    reply = chat.choices[0].message.content
    return reply

def mp3_to_text(fdir):
    SetLogLevel(0)

    # Проверяем наличие модели
    if not os.path.exists("model"):
        print ("Please download the model from https://alphacephei.com/vosk/models and unpack as 'model' in the current folder.")
        exit (1)

    # Устанавливаем Frame Rate
    FRAME_RATE = 16000
    CHANNELS=1
    model = Model("model")
    rec = KaldiRecognizer(model, FRAME_RATE)
    rec.SetWords(True)
    # Используя библиотеку pydub делаем предобработку аудио
    mp3 = AudioSegment.from_mp3(fdir)
    mp3 = mp3.set_channels(CHANNELS)
    mp3 = mp3.set_frame_rate(FRAME_RATE)
    # Преобразуем вывод в json
    rec.AcceptWaveform(mp3.raw_data)
    result = rec.Result()
    text = json.loads(result)["text"]
    return text



sys.path.append('..')




@app.post('neuro/questions')
def generate_questions(n:int,text:str):
    try:
        data = get_questions(n,text)
        x = json.loads(data, object_hook=lambda d: SimpleNamespace(**d))
        return x
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
 
@app.post("neuro/mp3")
def read_root(file: UploadFile):
    try:
        if file.filename.split('.')[1] !='mp3':
            print(123)
            raise Exception('wrong type of file')

        fileName = f'{uuid.uuid4()}_{file.filename}'

        new_file = open((fileName),'wb')
        new_file.write(file.file.read())
        new_file.close()
        fileDir = fileName
        # data = main_script(fileDir,500000)
        data = mp3_to_text(fileDir)
        os.remove(fileDir)

        return data#data
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))