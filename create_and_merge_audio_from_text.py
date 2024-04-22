#! /usr/bin/env python3

import os
from datetime import datetime
import gtts
import random
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen.canvas import Canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
from reportlab.lib.pagesizes import A4  # Import A4 page size definition
from pydub import AudioSegment
import io
from PyPDF2 import PdfReader,PdfWriter
from reportlab.pdfgen import canvas

# 删除空文件 
def empty_folder(folder_path):
    # 遍历文件夹中的所有文件
    for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_name)
            
        # 如果是空文件，则删除
        if os.path.isfile(file_path) and os.path.getsize(file_path) == 0: # 空文件
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

# 在页脚添加页码
def add_page_number(canvas,pdf):
    # Retrieve page number and total page count
    page_number = canvas.getPageNumber()
    total_pages = len(pdf.pages)
    
    # Draw page number centered at the bottom of the page
    canvas.setFont('HeiseiMin-W3',9)
    canvas.drawCentredString(
        A4[0] / 2,
        25,
        f'Page {page_number} of {total_pages}'
    )
# 在页眉加标题
def add_title(canvas,title):
    # Draw the title centered at the top of the page
    canvas.setFont('HeiseiMin-W3',16)
    canvas.drawCentredString(
        A4[0] / 2,
        A4[1] - 35,
        title
    )

# 加标题和页码
def add_titles_and_page_numbers(input_pdf_path, output_pdf_path, titles):
    input_pdf = PdfReader(input_pdf_path)
    output_pdf = PdfWriter()

    # 添加日语字体支持 https://www.reportlab.com/docs/reportlab-userguide.pdf
    pdfmetrics.registerFont(UnicodeCIDFont('HeiseiMin-W3'))
    # 添加中文字体支持
    pdfmetrics.registerFont(UnicodeCIDFont('STSong-Light'))

    for i, page in enumerate(input_pdf.pages):
        packet = io.BytesIO()
        can = canvas.Canvas(packet, pagesize=A4)
        add_page_number(can, input_pdf)
        add_title(can, titles[0])
        can.save()

        # Move to the beginning of the StringIO buffer
        packet.seek(0)
        new_pdf = PdfReader(packet)

        # Merge the page with the existing one
        page.merge_page(new_pdf.pages[0])
        output_pdf.add_page(page)

    # Write the combined PDF to a file
    with open(output_pdf_path, "wb") as output_stream:
        output_pdf.write(output_stream)


# 将文本行写入PDF文件
def write_to_pdf(lines, pdf_path):
        
    # Set Page Size and Margins
    page_width, page_height = A4

    c = Canvas(pdf_path, pagesize=(page_width, page_height)) # Create the Canvas object and set page size 


    # 添加日语字体支持 https://www.reportlab.com/docs/reportlab-userguide.pdf
    pdfmetrics.registerFont(UnicodeCIDFont('HeiseiMin-W3'))
    # 添加中文字体支持
    pdfmetrics.registerFont(UnicodeCIDFont('STSong-Light'))

    margin ={ # Adjust margin as needed
        "left": 30,
        "right": 30,
        "top": 70,
        "bottom": 50
    }
    column_width = (page_width - (margin["left"]+margin["right"])) / 3  # Calculate column width

    # Define x-coordinates for each column
    column_spacing = 10  # Adjust spacing between columns as desired
    column_x = [margin["left"], margin["left"] + column_width, margin["left"] + 2 * column_width]

    # Draw Text in Columns
    x = column_x[0] # 设置起始的横坐标
    y = page_height - margin["top"]  # 设置起始的纵坐标
    c.setFont('HeiseiMin-W3', 16)
    c.setFont('STSong-Light', 16)
    c.setFillColor((0,0,0)) # 设置字体颜色为黑色

    for line in lines:
        # Draw text in each column, update y-coordinate
        c.drawString(x, y, "□ "+line.strip()) # 写字
        y -= 28  # 更新纵坐标，以便下一行文本
        # 调整坐标在第2列书写
        if x==column_x[0] and y <  margin["bottom"]:
            x = column_x[1]
            y = page_height - margin["top"]
        # 调整坐标在第3列书写
        if x==column_x[1] and y < margin["bottom"]:
            x = column_x[2]
            y = page_height - margin["top"]
        # 如果纵坐标超出页面范围，则创建新页面
        if x==column_x[2] and y < margin["bottom"]:
            c.showPage()
            x = column_x[0]
            y = page_height - margin["top"]
            c.setFont('HeiseiMin-W3', 16)
            c.setFont('STSong-Light', 16)
            c.setFillColor("#000000") # 设置字体颜色为黑色

    c.save() # 保存PDF文件
    
# 按行生成语音
def text_to_speech_by_lines(lines,output_folder_path):
    # print(gtts.lang.tts_langs()) 输出支持的语言
    for line in lines:
        try:
            tts = gtts.gTTS(line.strip(), lang='ja')  ##  request google to get synthesis
            output_file_path = output_folder_path +'/'+ line.strip()+'.mp3'
            if not os.path.exists(output_file_path): 
                tts.save(output_file_path)  ##  save audio
        except Exception as e:
            print(f"转换 '{line.strip()}' 出现错误：{e}")

# 按整个文件生成语音
def text_to_speech_by_file(lines,output_folder_path):
    try:
        tts = gtts.gTTS(' '.join(lines), lang='ja')  ##  request google to get synthesis
        output_file_path = output_folder_path +'/'+ 'output.mp3'
        if not os.path.exists(output_file_path): 
            tts.save(output_file_path)  ##  save audio
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
    # today_date = "2024-04-17"
    output_folder_path = create_folder_if_not_exists(today_date) # 以当天的日期作为文件夹名创建文件夹
    input_file = today_date+'.txt'  # 输入文本文件路径
    output_pdf = output_folder_path +'/'+ today_date + '.pdf'  # 输出PDF文件路径
    output_merged_mp3 = output_folder_path +'/'+ today_date + '.mp3'  # 输出合并后的mp3文件路径
    
    lines = read_text_file(input_file)  # 读取文本文件
    #  new_lines = shuffle_lines(lines)  # 打乱文本行的顺序
    #  text_to_speech_by_file(new_lines,output_folder_path) # 生成语音文件
    text_to_speech_by_lines(lines,output_folder_path)
    merge_audio_with_silence(output_folder_path,output_merged_mp3) # 合并声音并插入3秒静音
    write_to_pdf(lines, output_pdf)  # 将文本写入PDF文件
    # add_titles_and_page_numbers(today_date + '.pdf',today_date + '.pdf',today_date + '单词表')

    
    print("程序结束")
    
if __name__ == "__main__":
    main()

