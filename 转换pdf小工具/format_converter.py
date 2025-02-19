import tkinter as tk
from tkinter import ttk
import png_to_pdf_gui
import txt_to_pdf

class MainApp:
    def __init__(self, master):
        self.master = master
        master.title("格式转换工具箱")

        # 设置窗口大小
        master.geometry("300x200")

        # 使用ttk.Style来设置主题
        style = ttk.Style()
        style.theme_use('clam')  # 'clam', 'alt', 'default', 'classic'

        # 创建PNG to PDF按钮
        self.png_to_pdf_button = ttk.Button(master, text="PNG to PDF", command=self.open_png_to_pdf)
        self.png_to_pdf_button.pack(pady=20)

        # 创建TXT to PDF按钮
        self.txt_to_pdf_button = ttk.Button(master, text="TXT to PDF", command=self.open_txt_to_pdf)
        self.txt_to_pdf_button.pack(pady=20)

        # 添加退出按钮
        self.exit_button = ttk.Button(master, text="退出", command=master.destroy)
        self.exit_button.pack(pady=20)

    def open_png_to_pdf(self):
        """打开PNG to PDF转换器窗口"""
        top = tk.Toplevel(self.master)  # 创建一个顶级窗口
        png_to_pdf_gui.PNGtoPDFConverter(top)  # 启动PNG to PDF GUI

    def open_txt_to_pdf(self):
        """打开TXT to PDF转换器窗口"""
        top = tk.Toplevel(self.master)  # 创建一个顶级窗口
        txt_to_pdf.TXTtoPDFConverter(top)  # 启动TXT to PDF GUI

if __name__ == "__main__":
    root = tk.Tk()
    app = MainApp(root)
    root.mainloop()
