import tkinter as tk
from tkinter import ttk

def calculate_irrigation_amount():
    fc = int(fc_scale.get())
    w = int(w_scale.get())
    D = int(D_scale.get())
    Ie = int(Ie_scale.get())

    irrigation_amount = (fc - w) / 100 * D * 100 / Ie
    irrigation_amount_2 = irrigation_amount 

    result_label_1.config(text="관수해야 할 관수량: {:.2f} mm".format(irrigation_amount))
    result_label_2.config(text="관수해야 할 관수량: {:.2f} L/m²".format(irrigation_amount_2))

# 윈도우 창 생성
window = tk.Tk()
window.title("토양 관수량 계산기")

# 스타일 설정
style = ttk.Style()
style.configure("TLabel", font=("Helvetica", 12, "bold"))

# 스트롤바 레이블 및 스케일
fc_label = ttk.Label(window, text="포장용수량(용적비, %)")
fc_label.pack()
fc_value = tk.StringVar()
fc_scale = ttk.Scale(window, from_=0, to=100, orient="horizontal", variable=fc_value, command=lambda x: fc_value.set(int(float(x))))
fc_scale.pack()
fc_entry = ttk.Entry(window, textvariable=fc_value, state="readonly")
fc_entry.pack()

w_label = ttk.Label(window, text="관수 전 토양의 함수량(용적비, %)")
w_label.pack()
w_value = tk.StringVar()
w_scale = ttk.Scale(window, from_=0, to=100, orient="horizontal", variable=w_value, command=lambda x: w_value.set(int(float(x))))
w_scale.pack()
w_entry = ttk.Entry(window, textvariable=w_value, state="readonly")
w_entry.pack()

D_label = ttk.Label(window, text="근군의 깊이(mm)")
D_label.pack()
D_value = tk.StringVar()
D_scale = ttk.Scale(window, from_=0, to=500, orient="horizontal", variable=D_value, command=lambda x: D_value.set(int(float(x))))
D_scale.pack()
D_entry = ttk.Entry(window, textvariable=D_value, state="readonly")
D_entry.pack()

Ie_label = ttk.Label(window, text="관수효율(%)")
Ie_label.pack()
Ie_value = tk.StringVar()
Ie_scale = ttk.Scale(window, from_=0, to=100, orient="horizontal", variable=Ie_value, command=lambda x: Ie_value.set(int(float(x))))
Ie_scale.pack()
Ie_entry = ttk.Entry(window, textvariable=Ie_value, state="readonly")
Ie_entry.pack()

# 계산 버튼
calculate_button = ttk.Button(window, text="계산하기", command=calculate_irrigation_amount)
calculate_button.pack()

# 결과 표시 레이블
result_label_1 = ttk.Label(window, text="관수해야 할 관수량 (mm): ")
result_label_1.pack()

result_label_2 = ttk.Label(window, text="관수해야 할 관수량 (L/m²): ")
result_label_2.pack()

# 스트롤바 값 표시 업데이트 함수
def update_scale_entry(scale, entry, value):
    scale.set(value)
    entry.configure(state="normal")
    entry.delete(0, tk.END)
    entry.insert(tk.END, value)
    entry.configure(state="readonly")

# 스트롤바 값과 표시 업데이트
update_scale_entry(fc_scale, fc_entry, fc_scale.get())
update_scale_entry(w_scale, w_entry, w_scale.get())
update_scale_entry(D_scale, D_entry, D_scale.get())
update_scale_entry(Ie_scale, Ie_entry, Ie_scale.get())

# 윈도우 창 실행
window.mainloop()
