import ctypes
import tkinter as tk
from tkinter import ttk, messagebox
import os
from datetime import datetime

# 加载库
if os.name == "nt":
    lib = ctypes.CDLL("./matrix_core.dll")
else:
    lib = ctypes.CDLL("./libmatrix_core.so")

lib.add.restype = ctypes.c_double
lib.add.argtypes = [ctypes.c_double, ctypes.c_double]

Matrix2x2 = (ctypes.c_double * 2) * 2
lib.matrix_mult.argtypes = [Matrix2x2, Matrix2x2, Matrix2x2]
lib.matrix_mult.restype = None


def py_matrix_mult(A_list, B_list):
    A = Matrix2x2()
    B = Matrix2x2()
    C_out = Matrix2x2()

    for i in range(2):
        for j in range(2):
            A[i][j] = A_list[i][j]
            B[i][j] = B_list[i][j]
    lib.matrix_mult(A, B, C_out)
    res = [[C_out[i][j] for j in range(2)] for i in range(2)]
    return res


# 20260904新增打印日志功能    HW
def append_log(log_widget, A, B, C):
    """
    1 组装日志字符串 A=[[...]], B=[[...]],结果C=[[...]]
    2 更新GUI文本框
    3 追加写入 log.txt
    """
    time_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_line = f"[{time_str}] A={A}, B={B}, result: C={C}\n"
    
    # 写入本地文件，a=追加模式
    with open("log.txt", "a", encoding="utf-8") as f:
        f.write(log_line)
        
    # GUI Text组件插入日志，跳到滚动到底部
    log_widget.config(state=tk.NORMAL)
    log_widget.insert(tk.END, log_line)
    log_widget.see(tk.END)
    log_widget.config(state=tk.DISABLED)   # 设置只读，用户不能编辑日志区
    

# def format_matrix(mat):
#     """美化格式化矩阵字符串，不要原始python list"""
#     lines = []
#     for row in mat:
#         items = f"{row[0]:>6.1f}  {row[1]:>6.1f}"
#         lines.append(items)
#     return "\n".join(lines)


def on_calc(log_text_widget):
    try:
        A = [
            [float(eA00.get()), float(eA01.get())],
            [float(eA10.get()), float(eA11.get())]
        ]
        B = [
            [float(eB00.get()), float(eB01.get())],
            [float(eB10.get()), float(eB11.get())]
        ]
        result_C = py_matrix_mult(A, B)
        # 写入日志
        append_log(log_text_widget, A, B, result_C)        
        # pretty_text = "矩阵计算结果：\n" + format_matrix(result)
        # out_text.set(pretty_text)
    except Exception as e:
        messagebox.showerror("输入错误", str(e))


root = tk.Tk()
root.title("C‑ctypes GUI Demo")
root.geometry("580x420")  # 固定窗口大小
root.resizable(True, True)

# 设置全局字体
style = ttk.Style(root)
style.configure("TLabel", font=("Microsoft YaHei", 12))
style.configure("TButton", font=("Microsoft YaHei", 12))

# 标题
ttk.Label(root, text="矩阵A", font=("Microsoft YaHei",14)).grid(row=0, column=0, columnspan=2, pady=8)
ttk.Label(root, text="矩阵B", font=("Microsoft YaHei",14)).grid(row=0, column=3, columnspan=2, pady=8)

# 输入框
eA00 = ttk.Entry(root, width=8); eA00.grid(row=1, column=0, padx=4, pady=2)
eA01 = ttk.Entry(root, width=8); eA01.grid(row=1, column=1, padx=4, pady=2)
eA10 = ttk.Entry(root, width=8); eA10.grid(row=2, column=0, padx=4, pady=2)
eA11 = ttk.Entry(root, width=8); eA11.grid(row=2, column=1, padx=4, pady=2)

eB00 = ttk.Entry(root, width=8); eB00.grid(row=1, column=3, padx=4, pady=2)
eB01 = ttk.Entry(root, width=8); eB01.grid(row=1, column=4, padx=4, pady=2)
eB10 = ttk.Entry(root, width=8); eB10.grid(row=2, column=3, padx=4, pady=2)
eB11 = ttk.Entry(root, width=8); eB11.grid(row=2, column=4, padx=4, pady=2)

# 按钮，把日志控件传进回调
log_text = tk.Text(root, font=("Consolas", 10), height=12)
btn = ttk.Button(root, text="调用C计算矩阵乘法", command=lambda: on_calc(log_text))
btn.grid(row=3, column=0, columnspan=5, pady=12)

# 日志显示框+滚动条
log_text.grid(row=4, column=0, columnspan=5, padx=8, sticky="NSEW")
scroll = ttk.Scrollbar(root, orient=tk.VERTICAL, command=log_text.yview)
scroll.grid(row=4, column=5, sticky="NS")
log_text.configure(yscrollcommand=scroll.set)
log_text.config(state=tk.DISABLED) # 日志框只读

# 窗口网格权重，拉伸窗口日志框跟着放大
root.grid_rowconfigure(4, weight=1)
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)
root.grid_columnconfigure(2, weight=1)
root.grid_columnconfigure(3, weight=1)
root.grid_columnconfigure(4, weight=1)

# # 输出文本区域，改用多行Label
# out_text = tk.StringVar()
# lab_out = ttk.Label(
#     root,
#     textvariable=out_text,
#     font=("Consolas",13),
#     justify="center"
# )
# lab_out.grid(row=4, column=0, columnspan=5, padx=12)

# 默认测试数据
eA00.insert(0, "1"); eA01.insert(0, "2")
eA10.insert(0, "3"); eA11.insert(0, "4")
eB00.insert(0, "5"); eB01.insert(0, "6")
eB10.insert(0, "7"); eB11.insert(0, "8")

root.mainloop()
