#! /usr/bin/env python3

##  pip3 install gTTS pyttsx3 playsound pydub

import os
from datetime import datetime
import gtts
import random
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.pdfbase.ttfonts import TTFont
from pydub import AudioSegment

# 清空文件夹
def empty_folder(folder_path):
    # 遍历文件夹中的所有文件
    for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_name)
        # 如果是文件，则删除
        if os.path.isfile(file_path):
            os.remove(file_path)
        # 如果是文件夹，则递归调用 empty_folder 函数清空该文件夹
        elif os.path.isdir(file_path):
            empty_folder(file_path)

# 创建文件夹
def create_folder_if_not_exists(today_date):
    
    # 构建文件夹路径
    folder_path = os.path.join(os.getcwd(), today_date)
    
    # 检查目录是否存在
    if not os.path.exists(folder_path):
        # 如果不存在，创建目录
        os.makedirs(folder_path)
        print(f"文件夹 '{today_date}' 已创建！")
    else:
        print(f"文件夹 '{today_date}' 已存在！")
        empty_folder(folder_path)
        print(f"文件夹 '{today_date}' 已清空！")
    return folder_path
        
# 读取文本文件
def read_text_file(filePath):
    with open(filePath, "r", encoding='utf-8') as f:
        lines = f.readlines()
    return lines

# 打乱文本行的顺序
def shuffle_lines(lines):
    random.shuffle(lines)
    return lines
    
# 将文本行写入PDF文件
def write_to_pdf(lines, pdf_path):
    c = canvas.Canvas(pdf_path, pagesize=letter)  # 创建一个PDF画布
    # c.setFont("Noto Sans CJK JP", 12)  # 设置使用的字体
    y = 750  # 设置起始的纵坐标
    for line in lines:
        c.drawString(100, y, line.strip())  # 在PDF上写入文本行
        y -= 15  # 更新纵坐标，以便下一行文本
        if y < 50:  # 如果纵坐标超出页面范围，则创建新页面
            c.showPage()  # 显示当前页面
            c.save()  # 保存PDF文件
            return  # 结束函数
    c.showPage()  # 显示最后一页
    c.save()  # 保存PDF文件
    
# 按行生成语音
def text_to_speech_by_lines(lines,output_folder_path):
    # print(gtts.lang.tts_langs()) 输出支持的语言
    for line in lines:
        try:
            tts = gtts.gTTS(line.strip(), lang='ja')  ##  request google to get synthesis
            tts.save(output_folder_path +'/'+ line.strip()+'.mp3')  ##  save audio
        except Exception as e:
            print(f"转换 '{line}' 出现错误：{e}")

# 按整个文件生成语音
def text_to_speech_by_file(lines,output_folder_path):
    try:
    	tts = gtts.gTTS(' '.join(lines), lang='ja')  ##  request google to get synthesis
    	tts.save(output_folder_path +'/'+ 'output.mp3')  ##  save audio
    	# playsound('output.mp3')  ##  play audio
    except Exception as e:
        print(f"转换出现错误：{e}")
        
# 合成声音文件
def merge_audio_with_silence(input_folder, output_file):

    # 筛选出所有的 mp3 文件
    audio_files = [file for file in os.listdir(input_folder) if file.endswith(".mp3")]
    
    non_empty_mp3_files = []
    # 筛选出所有不是空的 mp3 文件
    for file in audio_files:
        file_path = os.path.join(input_folder, file)
        if os.path.getsize(file_path) > 0:
            non_empty_mp3_files.append(file_path)
            
    # 根据文件的创建时间排序
    non_empty_mp3_files.sort(key=lambda x: os.path.getctime(os.path.join(input_folder, x)))

    audio_segments = []
    for file in non_empty_mp3_files:
        # print(file)
        # 将每个音频文件加载为音频段
        audio_segments.append(AudioSegment.from_mp3(os.path.join(input_folder, file)))
        # 插入 3 秒的静音
        audio_segments.append(AudioSegment.silent(duration=3000))

    # 删除最后一个静音段，因为最后一个音频文件后面不需要插入静音
    audio_segments.pop()

    # 合并所有音频段
    final_audio = AudioSegment.empty()
    for segment in audio_segments:
        final_audio += segment

    # 将合并后的音频保存为 mp3 文件
    final_audio.export(output_file, format="mp3")

    print("合并完成！")    
    
# 主函数
def main():
    
    today_date = datetime.now().strftime('%Y-%m-%d') # 获取当天日期
    output_folder_path = create_folder_if_not_exists(today_date) # 以当天的日期作为文件夹名创建文件夹
    input_file = 'your_text_file.txt'  # 输入文本文件路径
    output_pdf = output_folder_path +'/'+ today_date + '.pdf'  # 输出PDF文件路径
    merged_mp3 = output_folder_path +'/'+ today_date + '.mp3'  # 输出合并后的mp3文件路径
    
    lines = read_text_file(input_file)  # 读取文本文件
    # new_lines = shuffle_lines(lines)  # 打乱文本行的顺序
    # text_to_speech_by_file(new_lines,output_folder_path) # 生成语音文件
    text_to_speech_by_lines(lines,output_folder_path)
    merge_audio_with_silence(output_folder_path,merged_mp3) # 合并声音并插入3秒静音
    # write_to_pdf(new_lines, output_pdf)  # 将打乱后的文本行写入PDF文件
    print("程序结束")
    
if __name__ == "__main__":
    main()

