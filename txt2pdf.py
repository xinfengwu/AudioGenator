# pip install reportlab
# sudo apt-get install fonts-noto 安装字体


import random
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.pdfbase.ttfonts import TTFont

# 读取文本文件并返回文本行列表
def read_text_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    return lines

# 打乱文本行的顺序
def shuffle_lines(lines):
    random.shuffle(lines)

# 将文本行写入PDF文件
def write_to_pdf(lines, pdf_path):
    c = canvas.Canvas(pdf_path, pagesize=letter)  # 创建一个PDF画布
    c.setFont("Noto Sans CJK JP", 12)  # 设置使用的字体
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

# 主函数
def main():
    input_file = 'your_text_file.txt'  # 输入文本文件路径
    output_pdf = 'your_text_file.pdf'  # 输出PDF文件路径

    lines = read_text_file(input_file)  # 读取文本文件
    shuffle_lines(lines)  # 打乱文本行的顺序
    write_to_pdf(lines, output_pdf)  # 将打乱后的文本行写入PDF文件

if __name__ == "__main__":
    main()

