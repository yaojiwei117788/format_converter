import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
from PIL import Image
import os

class PNGtoPDFConverter:
    def __init__(self, master):
        self.master = master
        master.title("PNG to PDF Converter")

        # 初始化变量
        self.png_files = []
        self.output_dir = ""
        self.pdf_filename = tk.StringVar()

        # 创建GUI元素
        self.create_widgets()

    def create_widgets(self):
        # 文件选择按钮
        self.select_files_button = tk.Button(self.master, text="选择PNG文件", command=self.select_png_files)
        self.select_files_button.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        # 显示选择的文件列表
        self.files_listbox = tk.Listbox(self.master, width=50, height=5)
        self.files_listbox.grid(row=1, column=0, columnspan=2, padx=10, pady=5, sticky="we")

        # 输出目录选择按钮
        self.select_output_dir_button = tk.Button(self.master, text="选择输出目录", command=self.select_output_directory)
        self.select_output_dir_button.grid(row=2, column=0, padx=10, pady=10, sticky="w")

        # 显示输出目录
        self.output_dir_label = tk.Label(self.master, text="输出目录：")
        self.output_dir_label.grid(row=3, column=0, padx=10, pady=5, sticky="w")
        self.output_dir_text = tk.Entry(self.master, width=40)
        self.output_dir_text.grid(row=3, column=1, padx=10, pady=5, sticky="we")

        # 转换按钮
        self.convert_button = tk.Button(self.master, text="转换为PDF", command=self.convert_to_pdf)
        self.convert_button.grid(row=5, column=0, columnspan=2, padx=10, pady=20)

        # 状态栏
        self.status_label = tk.Label(self.master, text="请选择PNG文件和输出目录")
        self.status_label.grid(row=6, column=0, columnspan=2, padx=10, pady=5, sticky="w")

    def select_png_files(self):
        """打开文件对话框，选择PNG文件"""
        self.png_files = filedialog.askopenfilenames(
            title="选择PNG文件",
            filetypes=[("PNG files", "*.png"), ("All files", "*.*")]
        )

        # 更新文件列表显示
        self.files_listbox.delete(0, tk.END)
        for file in self.png_files:
            self.files_listbox.insert(tk.END, file)

    def select_output_directory(self):
        """打开目录对话框，选择输出目录"""
        self.output_dir = filedialog.askdirectory(title="选择输出目录")

        # 更新输出目录显示
        self.output_dir_text.delete(0, tk.END)
        self.output_dir_text.insert(0, self.output_dir)

    def convert_to_pdf(self):
        """将选择的PNG文件转换为PDF"""
        if not self.png_files:
            messagebox.showerror("错误", "请选择PNG文件")
            return

        if not self.output_dir:
            messagebox.showerror("错误", "请选择输出目录")
            return

        try:
            for png_file in self.png_files:
                # 获取PNG文件名，不包含扩展名
                base_name = os.path.splitext(os.path.basename(png_file))[0]

                # 询问用户自定义文件名
                pdf_filename = simpledialog.askstring("保存PDF", f"请输入 {base_name}.png 的PDF文件名 (留空则使用原文件名):",
                                                        parent=self.master)

                if pdf_filename:
                    # 使用用户自定义的文件名
                    if not pdf_filename.endswith(".pdf"):
                        pdf_filename += ".pdf"
                    output_path = os.path.join(self.output_dir, pdf_filename)
                else:
                    # 使用原始PNG文件名作为PDF文件名
                    output_filename = base_name + ".pdf"
                    output_path = os.path.join(self.output_dir, output_filename)

                # 打开PNG文件
                try:
                    img = Image.open(png_file).convert('RGB')  # 确保图像为RGB模式
                except Exception as e:
                    messagebox.showerror("错误", f"无法打开图像 {png_file}: {str(e)}")
                    continue # 跳过此文件

                # 保存为PDF
                try:
                    img.save(
                        output_path,
                        "PDF",
                        resolution=100.0,
                    )
                    self.status_label.config(text=f"成功转换为PDF: {output_path}")
                    messagebox.showinfo("成功", f"PDF已保存到: {output_path}")

                except Exception as e:
                    messagebox.showerror("错误", f"转换 {png_file} 失败: {str(e)}")
                    self.status_label.config(text=f"转换 {png_file} 失败: {str(e)}")


        except Exception as e:
            messagebox.showerror("错误", f"转换失败: {str(e)}")
            self.status_label.config(text=f"转换失败: {str(e)}")

root = tk.Tk()
converter = PNGtoPDFConverter(root)
root.mainloop()
