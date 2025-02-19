import tkinter as tk
from tkinter import filedialog, messagebox
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph, Spacer, SimpleDocTemplate
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import os

class TXTtoPDFConverter:
    def __init__(self, master):
        self.master = master
        master.title("TXT to PDF Converter")

        # 初始化变量
        self.txt_file = ""
        self.output_dir = ""
        self.pdf_filename = tk.StringVar()

        # 创建GUI元素
        self.create_widgets()

        # 注册字体
        self.register_font()

    def register_font(self):
        """注册字体 (SimSun)"""
        try:
            pdfmetrics.registerFont(TTFont('SimSun', 'simsun.ttc'))
            self.has_chinese_font = True
        except Exception as e:
            print(f"无法注册 SimSun 字体: {e}")
            self.has_chinese_font = False

    def create_widgets(self):
        # 文件选择按钮
        self.select_file_button = tk.Button(self.master, text="选择TXT文件", command=self.select_txt_file)
        self.select_file_button.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        # 显示选择的文件路径
        self.file_path_label = tk.Label(self.master, text="TXT文件路径:")
        self.file_path_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.file_path_text = tk.Entry(self.master, width=40)
        self.file_path_text.grid(row=1, column=1, padx=10, pady=5, sticky="we")

        # 输出目录选择按钮
        self.select_output_dir_button = tk.Button(self.master, text="选择输出目录", command=self.select_output_directory)
        self.select_output_dir_button.grid(row=2, column=0, padx=10, pady=10, sticky="w")

        # 显示输出目录
        self.output_dir_label = tk.Label(self.master, text="输出目录：")
        self.output_dir_label.grid(row=3, column=0, padx=10, pady=5, sticky="w")
        self.output_dir_text = tk.Entry(self.master, width=40)
        self.output_dir_text.grid(row=3, column=1, padx=10, pady=5, sticky="we")

        # 文件名输入框
        self.filename_label = tk.Label(self.master, text="PDF文件名：")
        self.filename_label.grid(row=4, column=0, padx=10, pady=5, sticky="w")
        self.filename_entry = tk.Entry(self.master, textvariable=self.pdf_filename, width=30)
        self.filename_entry.grid(row=4, column=1, padx=10, pady=5, sticky="we")

        # 转换按钮
        self.convert_button = tk.Button(self.master, text="转换为PDF", command=self.convert_to_pdf)
        self.convert_button.grid(row=5, column=0, columnspan=2, padx=10, pady=20)

        # 状态栏
        self.status_label = tk.Label(self.master, text="请选择TXT文件和输出目录")
        self.status_label.grid(row=6, column=0, columnspan=2, padx=10, pady=5, sticky="w")

    def select_txt_file(self):
        """打开文件对话框，选择TXT文件"""
        self.txt_file = filedialog.askopenfilename(
            title="选择TXT文件",
            filetypes=[("TXT files", "*.txt"), ("All files", "*.*")]
        )

        # 更新文件路径显示
        self.file_path_text.delete(0, tk.END)
        self.file_path_text.insert(0, self.txt_file)

    def select_output_directory(self):
        """打开目录对话框，选择输出目录"""
        self.output_dir = filedialog.askdirectory(title="选择输出目录")

        # 更新输出目录显示
        self.output_dir_text.delete(0, tk.END)
        self.output_dir_text.insert(0, self.output_dir)

    def convert_to_pdf(self):
        """将选择的TXT文件转换为PDF"""
        if not self.txt_file:
            messagebox.showerror(title="错误", message="请选择TXT文件", parent=self.master)
            return

        if not self.output_dir:
            messagebox.showerror(title="错误", message="请选择输出目录", parent=self.master)
            return

        pdf_filename = self.pdf_filename.get()
        if not pdf_filename:
            messagebox.showerror(title="错误", message="请输入PDF文件名", parent=self.master)
            return

        # 确保文件名以.pdf结尾
        if not pdf_filename.endswith(".pdf"):
            pdf_filename += ".pdf"

        output_path = os.path.join(self.output_dir, pdf_filename)

        try:
            # 读取TXT文件内容
            with open(self.txt_file, "r", encoding="utf-8") as f:
                text = f.read()

            # 创建PDF
            doc = SimpleDocTemplate(output_path, pagesize=letter)
            styles = getSampleStyleSheet()
            style = styles["Normal"]
            style.wordWrap = 'CJK'  # 支持中文换行
            style.leading = 14  # 设置行距

            if self.has_chinese_font:
                style.fontName = 'SimSun'
            else:
                style.fontName = 'Helvetica'

            story = []
            for paragraph_text in text.split("\n"):
                paragraph = Paragraph(paragraph_text, style)
                story.append(paragraph)
                story.append(Spacer(1, 0.2*inch))  # 添加段落间距

            doc.build(story)

            self.status_label.config(text=f"成功转换为PDF: {output_path}")
            messagebox.showinfo(title="成功", message=f"PDF已保存到: {output_path}", parent=self.master)

        except Exception as e:
            messagebox.showerror(title="错误", message=f"转换失败: {str(e)}", parent=self.master)
            self.status_label.config(text=f"转换失败: {str(e)}")
