import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PyPDF2 import PdfReader
import os
from threading import Thread

class PDFConverterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("PDF转TXT工具 v1.0")
        self.root.geometry("500x250")
        
        # 创建界面组件
        self.create_widgets()
        
        # 设置样式
        style = ttk.Style()
        style.theme_use('clam')

    def create_widgets(self):
        # PDF文件选择区域
        frame_select = ttk.LabelFrame(self.root, text="选择文件")
        frame_select.pack(pady=10, padx=20, fill='x')
        
        self.pdf_path = tk.StringVar()
        ttk.Entry(frame_select, textvariable=self.pdf_path, width=40).grid(row=0, column=0, padx=5)
        ttk.Button(frame_select, text="选择PDF", command=self.select_pdf).grid(row=0, column=1, padx=5)

        # 转换按钮区域
        ttk.Button(self.root, text="开始转换", command=self.start_conversion).pack(pady=15)

        # 进度条
        self.progress = ttk.Progressbar(self.root, orient='horizontal', length=300, mode='determinate')
        self.progress.pack(pady=5)

        # 状态标签
        self.status = ttk.Label(self.root, text="准备就绪")
        self.status.pack(pady=5)

    def select_pdf(self):
        file_path = filedialog.askopenfilename(
            title="选择PDF文件",
            filetypes=[("PDF文件", "*.pdf")]
        )
        if file_path:
            self.pdf_path.set(file_path)

    def conversion_task(self, pdf_path):
        try:
            txt_path = os.path.splitext(pdf_path)[0] + ".txt"
            
            with open(pdf_path, 'rb') as pdf_file:
                reader = PdfReader(pdf_file)
                total_pages = len(reader.pages)
                self.progress["maximum"] = total_pages
                
                text = ""
                for page_num in range(total_pages):
                    page = reader.pages[page_num]
                    text += page.extract_text() + "\n\n"
                    self.progress["value"] = page_num + 1
                    self.root.update_idletasks()

            with open(txt_path, 'w', encoding='utf-8') as txt_file:
                txt_file.write(text)
                
            self.status.config(text="转换完成！")
            messagebox.showinfo("成功", f"文件已保存至：\n{txt_path}")
            
        except Exception as e:
            messagebox.showerror("错误", f"转换失败：\n{str(e)}")
        finally:
            self.progress["value"] = 0

    def start_conversion(self):
        pdf_path = self.pdf_path.get()
        if not pdf_path:
            messagebox.showwarning("警告", "请先选择PDF文件！")
            return
            
        if not pdf_path.lower().endswith('.pdf'):
            messagebox.showwarning("警告", "请选择有效的PDF文件！")
            return

        self.status.config(text="转换中...")
        # 使用线程防止界面冻结
        Thread(target=self.conversion_task, args=(pdf_path,)).start()

if __name__ == "__main__":
    root = tk.Tk()
    app = PDFConverterApp(root)
    root.mainloop()
