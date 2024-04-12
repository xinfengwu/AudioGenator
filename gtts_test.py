#! /usr/bin/env python3

##  pip3 install gTTS pyttsx3 playsound

import gtts
from playsound import playsound
import random

# 读取文本文件
with open("your_text_file.txt", "r") as f:
    lines = f.readlines()

# 随机组合文本行
random.shuffle(lines)

tts = gtts.gTTS(' '.join(lines), lang='ja')  ##  request google to get synthesis

tts.save('hello.mp3')  ##  save audio
playsound('hello.mp3')  ##  play audio

## print(gtts.lang.tts_langs()) 输出支持的语言
