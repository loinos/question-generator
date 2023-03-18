from vosk import Model, KaldiRecognizer, SetLogLevel
from pydub import AudioSegment
import subprocess
import json
import os

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
mp3 = AudioSegment.from_mp3(r'C:\Users\loinos\Desktop\Hack\ai\song.mp3')
mp3 = mp3.set_channels(CHANNELS)
mp3 = mp3.set_frame_rate(FRAME_RATE)

# Преобразуем вывод в json
rec.AcceptWaveform(mp3.raw_data)
result = rec.Result()
print(result)
text = json.loads(result)["text"]

# Добавляем пунктуацию
cased = subprocess.check_output('python C:\\Users\\loinos\\Desktop\\Hack\\ai\\vosk-recasepunc-ru-0.22\\recasepunc.py predict C:\\Users\\loinos\\Desktop\\Hack\\ai\\checkpoint', shell=True, text=True, input=text)

# Записываем результат в файл "data.txt"
with open('data.txt', 'w') as f: 
    json.dump(cased, f, ensure_ascii=False, indent=4)