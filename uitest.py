from tkinter import *

root = Tk()
# root.option_readfile("info.txt")
root.title("顶级窗口")

label1 = Label(root, text="这是主窗口（默认）")
label1.pack()

t1 = Toplevel(root)
label2 = Label(t1, text="这是一个子窗口")
label2.pack()

t2 = Toplevel(root)
label3 = Label(t2, text="这是一个临时窗口 ")
label3.pack()
t2.transient(root)  # 建立一个临时窗口，会随主窗口最小化而最小化，关闭而关闭，在最前面

t3 = Toplevel(root, borderwidth=5, bg="blue")
label4 = Label(t3, text="no wm decorations", bg="blue", fg="white")
label4.pack(padx=10, pady=10)
# t3.overrideredirect(1)  # 建立一个没有任何按钮，无法关闭，最大化，最小化的窗口
t3.geometry("200x200+140+130")

root.mainloop()
