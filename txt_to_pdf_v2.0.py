import queue
import threading
from tkinter import *
from tkinter import ttk, filedialog, messagebox
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

# 引入中文字体支持 [^1]
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# 注册中文字体，这里使用宋体，需要确保系统安装了宋体 [^2]
pdfmetrics.registerFont(TTFont('SimSun', 'simsun.ttc'))

from pathlib import Path

class PDFConverterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("TXT to PDF Converter")
        self.root.geometry("700x400")
        self.file_list = []
        self.running = False
        self.queue = queue.Queue()
        self.create_widgets()

    def create_widgets(self):
        main_frame = Frame(self.root)
        main_frame.pack(padx=10, pady=10, fill=BOTH, expand=True)

        # 文件列表框
        self.listbox_frame = Frame(main_frame)
        self.listbox_frame.pack(pady=5, fill=BOTH, expand=True)
        Label(self.listbox_frame, text="选择TXT文件:").pack(anchor=W)
        self.listbox = Listbox(self.listbox_frame, selectmode=EXTENDED)
        self.listbox.pack(fill=BOTH, expand=True)
        listbox_scrollbar = Scrollbar(self.listbox_frame, orient=VERTICAL, command=self.listbox.yview)
        listbox_scrollbar.pack(side=RIGHT, fill=Y)
        self.listbox.config(yscrollcommand=listbox_scrollbar.set)

        # 按钮
        self.button_frame = Frame(main_frame)
        self.button_frame.pack(pady=5)
        Button(self.button_frame, text="添加文件", command=self.add_files).pack(side=LEFT, padx=5)
        Button(self.button_frame, text="开始转换", command=self.start_conversion, bg="#4CAF50", fg="white", padx=20).pack(side=LEFT, padx=5)

        # 进度条
        self.progress_frame = Frame(main_frame)
        self.progress_frame.pack(pady=5, fill=X)
        Label(self.progress_frame, text="转换进度:").pack(side=LEFT)
        self.progress_bar = ttk.Progressbar(self.progress_frame, orient=HORIZONTAL, length=300, mode='determinate')
        self.progress_bar.pack(side=LEFT, fill=X, expand=True, padx=5)

        # 状态标签
        self.status_label = Label(main_frame, text="", fg="black")
        self.status_label.pack(pady=5)

    def add_files(self):
        files = filedialog.askopenfilenames(filetypes=[("Text files", "*.txt")])
        for f in files:
            if f not in self.file_list:
                self.file_list.append(f)
                self.listbox.insert(END, Path(f).name)

    def wrap_text(self, text, max_line_length=80):
        lines = []
        for paragraph in text.split('\n'):
            words = []
            for word in paragraph.split():
                words.append(word)
                current_line = ' '.join(words)
                if len(current_line) > max_line_length:
                    lines.append(' '.join(words[:-1]))
                    words = [word]
            if words:
                lines.append(' '.join(words))
            lines.append('') # paragraph break
        return '\n'.join(lines)

    def convert_file(self, input_path, output_dir):
        try:
            with open(input_path, 'r', encoding='utf-8') as f:
                raw_text = f.read()
            wrapped_text = self.wrap_text(raw_text)
            output_path = Path(output_dir) / f"{Path(input_path).stem}.pdf"
            doc = SimpleDocTemplate(
                str(output_path),
                pagesize=letter,
                leftMargin=72,
                rightMargin=72,
                topMargin=72,
                bottomMargin=72
            )
            styles = getSampleStyleSheet()
            style = styles['Normal']
            # 修改字体为支持中文的宋体 [^3]
            style.fontName = 'SimSun'
            style.fontSize = 12
            style.leading = 16
            # 增加中文自动换行 [^4]
            style.wordWrap = 'CJK'
            content = []
            paragraphs = wrapped_text.split('\n')
            for p in paragraphs:
                if p.strip() == '':
                    content.append(Spacer(1, 12))
                else:
                    content.append(Paragraph(p, style))
            doc.build(content)
            return True, output_path
        except Exception as e:
            return False, str(e)

    def start_conversion(self):
        if not self.file_list:
            messagebox.showerror("错误", "请先选择要转换的TXT文件")
            return

        if self.running:
            messagebox.showinfo("提示", "转换正在进行中，请稍后")
            return

        output_dir = filedialog.askdirectory(title="选择PDF文件输出目录")
        if not output_dir:
            return

        self.running = True
        self.progress_bar['value'] = 0
        self.status_label.config(text="转换中，请稍候...", fg="black")
        self.total_files = len(self.file_list)
        self.converted_files = 0
        self.error_files = 0
        self.queue = queue.Queue() # 清空队列

        thread = threading.Thread(target=self.batch_convert, args=(output_dir,))
        thread.start()
        self.root.after(100, self.update_ui) # 定时更新UI

    def batch_convert(self, output_dir):
        for input_file in self.file_list:
            success, result = self.convert_file(input_file, output_dir)
            self.queue.put((success, input_file, result)) # 将结果放入队列
        self.queue.put(None) # 放入结束信号

    def update_ui(self):
        while not self.queue.empty():
            result = self.queue.get_nowait()
            if result is None: # 接收到结束信号
                self.running = False
                if self.error_files > 0:
                    self.status_label.config(text=f"转换完成，成功: {self.converted_files}, 失败: {self.error_files}", fg="red")
                else:
                    self.status_label.config(text=f"全部转换成功，共 {self.converted_files} 个文件", fg="green")
                self.progress_bar['value'] = 100
                return

            success, input_file, convert_result = result
            self.converted_files += 1
            if not success:
                self.error_files += 1
                error_message = f"文件 {Path(input_file).name} 转换失败: {convert_result}"
                print(error_message) # 可以在控制台输出详细错误信息
                # messagebox.showerror("错误", error_message) #  可以选择弹出错误框，但批量处理时会弹出很多

            self.progress_bar['value'] = (self.converted_files / self.total_files) * 100
            self.progress_bar.update()

        if self.running:
            self.root.after(100, self.update_ui) # 继续定时检查队列

if __name__ == "__main__":
    root = Tk()
    app = PDFConverterApp(root)
    root.mainloop()
