import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PyPDF2 import PdfReader
import os
from threading import Thread

class PDFConverterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("PDF批量转TXT工具 v2.0")
        self.root.geometry("600x300")
        
        # 初始化变量
        self.selected_files = []
        self.output_dir = tk.StringVar()
        
        # 创建界面
        self.create_widgets()
        
    def create_widgets(self):
        # 文件选择区域
        frame_files = ttk.LabelFrame(self.root, text="选择PDF文件（可多选）")
        frame_files.pack(pady=10, padx=20, fill='x')
        
        ttk.Button(frame_files, text="添加PDF文件", command=self.select_pdfs).pack(side=tk.LEFT, padx=5)
        ttk.Button(frame_files, text="清空列表", command=self.clear_list).pack(side=tk.LEFT, padx=5)
        
        # 文件列表框
        self.listbox = tk.Listbox(frame_files, width=70, height=4)
        self.listbox.pack(pady=5, padx=5)
        
        # 输出路径区域
        frame_output = ttk.LabelFrame(self.root, text="输出设置")
        frame_output.pack(pady=10, padx=20, fill='x')
        
        ttk.Entry(frame_output, textvariable=self.output_dir, width=50).pack(side=tk.LEFT, padx=5)
        ttk.Button(frame_output, text="选择目录", command=self.select_output_dir).pack(side=tk.LEFT)
        ttk.Checkbutton(frame_output, text="同源目录", command=self.toggle_output_dir).pack(side=tk.RIGHT, padx=5)
        
        # 控制按钮
        ttk.Button(self.root, text="开始批量转换", command=self.start_conversion).pack(pady=10)
        
        # 进度条
        self.progress = ttk.Progressbar(self.root, orient='horizontal', length=400, mode='determinate')
        self.progress.pack(pady=5)
        
        # 状态标签
        self.status = ttk.Label(self.root, text="就绪状态：等待操作")
        self.status.pack(pady=5)

    def select_pdfs(self):
        files = filedialog.askopenfilenames(
            title="选择多个PDF文件",
            filetypes=[("PDF文件", "*.pdf")]
        )
        if files:
            self.selected_files.extend(files)
            self.update_listbox()
            
    def clear_list(self):
        self.selected_files.clear()
        self.listbox.delete(0, tk.END)
    
    def select_output_dir(self):
        directory = filedialog.askdirectory()
        if directory:
            self.output_dir.set(directory)
    
    def toggle_output_dir(self):
        self.output_dir.set("")  # 清空路径即表示使用源目录
    
    def update_listbox(self):
        self.listbox.delete(0, tk.END)
        for f in self.selected_files:
            self.listbox.insert(tk.END, os.path.basename(f))
    
    def conversion_task(self):
        try:
            total = len(self.selected_files)
            self.progress["maximum"] = total
            success = 0
            
            for idx, pdf_path in enumerate(self.selected_files):
                # 更新进度
                self.progress["value"] = idx + 1
                self.status.config(text=f"正在转换：{os.path.basename(pdf_path)}")
                self.root.update_idletasks()
                
                # 处理输出路径
                if self.output_dir.get():
                    output_path = os.path.join(
                        self.output_dir.get(),
                        os.path.basename(pdf_path).replace(".pdf", ".txt")
                    )
                else:
                    output_path = pdf_path.replace(".pdf", ".txt")
                
                # 执行转换
                try:
                    with open(pdf_path, 'rb') as f:
                        reader = PdfReader(f)
                        text = "\n\n".join(
                            [page.extract_text() for page in reader.pages]
                        )
                    
                    with open(output_path, 'w', encoding='utf-8') as f:
                        f.write(text)
                    
                    success += 1
                except Exception as e:
                    continue
                    
            messagebox.showinfo(
                "转换完成",
                f"成功转换 {success}/{total} 个文件\n"
                f"失败{total - success}个"
            )
            self.status.config(text=f"批量转换完成")
            
        except Exception as e:
            messagebox.showerror("错误", f"批量转换失败：{str(e)}")
        finally:
            self.progress["value"] = 0
    
    def start_conversion(self):
        if not self.selected_files:
            messagebox.showwarning("警告", "请先添加PDF文件！")
            return
            
        if len(self.selected_files) > 20:
            if not messagebox.askyesno("确认", "批量转换超过20个文件可能耗时较长，继续吗？"):
                return
        
        # 检查输出目录有效性（如果指定了目录）
        if self.output_dir.get() and not os.path.exists(self.output_dir.get()):
            messagebox.showerror("错误", "指定的输出目录不存在！")
            return
        
        Thread(target=self.conversion_task).start()

if __name__ == "__main__":
    root = tk.Tk()
    app = PDFConverterApp(root)
    root.mainloop()
