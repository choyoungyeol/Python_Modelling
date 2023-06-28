import tkinter as tk
import matplotlib.pyplot as plt
import numpy as np
import math

# 그래프 데이터 생성
x = np.linspace(0, 50, 100)

def simulate_graph(cm, rm, tb):
    # 그래프 시뮬레이션
    y = cm / rm * np.log(1 + np.exp(rm*(x - tb)))
    #y = cm / rm * math.log(1 + math.exp(rm * (x - tb)))
    return y

def update_graph():
    # 그래프 업데이트
    cm = float(cm_entry.get())
    rm = float(rm_entry.get())
    tb = float(tb_entry.get())

    y = simulate_graph(cm, rm, tb)

    plt.cla()
    plt.draw()
    plt.plot(x, y)
    plt.xlabel('Days after transplant (DAT)')
    plt.ylabel('Dry weight (g/m2)')
    plt.title('Graph')
    plt.grid(True)
    plt.show()
    for i in range(len(y)):
        if y[i] >= y_var.get():
            result_var.set("Result: (DAT = {:.1f}, Weight (g) = {:.1f})".format(x[i], y[i]))
            break

def reset_values():
    # 초기화
    cm_var.set(0.2)
    rm_var.set(0.03)
    tb_var.set(10)
    y_var.set(100)
    result_var.set("")

# 윈도우 창 생성
window = tk.Tk()
window.title("Graph Simulation")
window.geometry("400x600")
window.configure(bg="#F0F0F0")

# 그래프 초기화
fig, ax = plt.subplots()
y = simulate_graph(0.2, 0.03, 10)  # 초기 값으로 시뮬레이션
line, = ax.plot(x, y)

# cm 입력 필드
def update_cm(*args):
    # cm 입력 필드 업데이트
    cm_scale.set(float(cm_var.get()))

cm_label = tk.Label(window, text="Crop growth rate", bg="#F0F0F0", font=("Arial", 12))
cm_label.pack()
cm_var = tk.DoubleVar(value=0.2)
cm_scale = tk.Scale(window, variable=cm_var, from_=0.1, to=1, resolution=0.1, command=update_cm, orient=tk.HORIZONTAL, length=200)
cm_scale.pack()
cm_entry = tk.Entry(window, textvariable=cm_var, font=("Arial", 12))
cm_entry.pack()

# rm 입력 필드
def update_rm(*args):
    # cm 입력 필드 업데이트
    rm_scale.set(float(rm_var.get()))

# cm 입력 필드
rm_label = tk.Label(window, text="Relative growth rate", bg="#F0F0F0", font=("Arial", 12))
rm_label.pack()
rm_var = tk.DoubleVar(value=0.03)
rm_scale = tk.Scale(window, variable=rm_var, from_=0.01, to=0.1, resolution=0.01, command=update_rm, orient=tk.HORIZONTAL, length=200)
rm_scale.pack()
rm_entry = tk.Entry(window, textvariable=rm_var, font=("Arial", 12))
rm_entry.pack()

# tb 입력 필드
def update_tb(*args):
    # cm 입력 필드 업데이트
    tb_scale.set(tb_var.get())

# cm 입력 필드
tb_label = tk.Label(window, text="tb", bg="#F0F0F0", font=("Arial", 12))
tb_label.pack()
tb_var = tk.DoubleVar(value=10)
tb_scale = tk.Scale(window, variable=tb_var, from_=1, to=20, command=update_tb, orient=tk.HORIZONTAL, length=200)
tb_scale.pack()
tb_entry = tk.Entry(window, textvariable=tb_var, font=("Arial", 12))
tb_entry.pack()

# 수확물량 입력 필드
def update_y(*args):
    # cm 입력 필드 업데이트
    y_scale.set(y_var.get())

# cm 입력 필드
y_label = tk.Label(window, text="Weight", bg="#F0F0F0", font=("Arial", 12))
y_label.pack()
y_var = tk.DoubleVar(value=100)
y_scale = tk.Scale(window, variable=y_var, from_=10, to=200, command=update_y, orient=tk.HORIZONTAL, length=200)
y_scale.pack()
y_entry = tk.Entry(window, textvariable=y_var, font=("Arial", 12))
y_entry.pack()

# 결과 텍스트 표시
result_var = tk.StringVar()
result_label = tk.Label(window, textvariable=result_var)
result_label.pack()

# 버튼 프레임
button_frame = tk.Frame(window, bg="#F0F0F0")
button_frame.pack()

# 버튼 생성
graph_button = tk.Button(button_frame, text="시뮬레이션", command=update_graph, font=("Arial", 12))
graph_button.pack(side=tk.LEFT, padx=5, pady=10)

reset_button = tk.Button(button_frame, text="초기화", command=reset_values, font=("Arial", 12))
reset_button.pack(side=tk.LEFT, padx=5, pady=10)

# 윈도우 창 실행
window.mainloop()
