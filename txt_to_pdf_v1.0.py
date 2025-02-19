import tkinter as tk
from tkinter import filedialog
import os
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import letter
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# 尝试注册中文字体（如果存在）
try:
    pdfmetrics.registerFont(TTFont('SimSun', 'simsun.ttc'))
    HAS_CHINESE_FONT = True
except:
    HAS_CHINESE_FONT = False
    print("警告：SimSun字体未找到，中文可能无法正确显示。")


class TXTtoPDFConverter:
    def __init__(self, master):
        self.master = master
        master.title("TXT to PDF Converter")

        # GUI elements
        self.input_file_label = tk.Label(master, text="选择TXT文件:")
        self.input_file_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")

        self.input_file = tk.StringVar()
        self.input_file_entry = tk.Entry(master, textvariable=self.input_file, width=50)
        self.input_file_entry.grid(row=0, column=1, padx=5, pady=5, sticky="we")

        self.browse_button = tk.Button(master, text="浏览", command=self.browse_file)
        self.browse_button.grid(row=0, column=2, padx=5, pady=5)

        self.convert_button = tk.Button(master, text="转换为PDF", command=self.convert_to_pdf)
        self.convert_button.grid(row=1, column=1, padx=5, pady=10)

        self.status_label = tk.Label(master, text="准备就绪", fg="black")
        self.status_label.grid(row=2, column=0, columnspan=3, padx=5, pady=5)

        # Configure grid layout
        master.grid_columnconfigure(1, weight=1)  # 让输入框可以扩展

    def browse_file(self):
        filename = filedialog.askopenfilename(filetypes=[("TXT files", "*.txt")])
        if filename:
            self.input_file.set(filename)

    def convert_to_pdf(self):
        input_path = self.input_file.get()
        if not input_path.endswith('.txt'):
            self.status_label.config(text="错误：请选择有效的TXT文件。", fg="red")
            return

        # 获取输出路径
        output_path = filedialog.asksaveasfilename(defaultextension=".pdf",
                                                    filetypes=[("PDF files", "*.pdf")])
        if not output_path:  # 用户取消选择
            self.status_label.config(text="已取消保存。", fg="orange")
            return

        try:
            with open(input_path, 'r', encoding='utf-8') as f:
                text = f.read()

            # 分割段落
            paragraphs = text.split('\n')

            # 创建PDF文档
            doc = SimpleDocTemplate(output_path, pagesize=letter,
                                    rightMargin=72, leftMargin=72,
                                    topMargin=72, bottomMargin=72)
            styles = getSampleStyleSheet()
            style = styles['Normal']

            # 设置字体 (根据是否成功注册中文字体)
            if HAS_CHINESE_FONT:
                style.fontName = 'SimSun'
            else:
                style.fontName = 'Courier'  # 默认使用 Courier 等宽字体

            story = []
            for para in paragraphs:
                if para.strip() == '':  # 忽略空行
                    continue
                p = Paragraph(para, style)
                story.append(p)
                story.append(Spacer(1, 12))  # 段落后添加空行
            doc.build(story)
            self.status_label.config(text="转换成功！", fg="green")

        except Exception as e:
            self.status_label.config(text=f"错误：{str(e)}", fg="red")


root = tk.Tk()
converter = TXTtoPDFConverter(root)
root.mainloop()
