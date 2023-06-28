import tkinter as tk
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

def simulate_graph(x, cm, rm, tb):
    # 그래프 시뮬레이션
    y1 = [cm / rm * np.log(1 + np.exp(rm * (xi - tb))) for xi in x]
    y2 = [0.034 * yi for yi in y1]
    return y1, y2

def calculate_cm(temperature):
    # cm 계산 함수
    cm = 391.161 * ((36 - temperature[-1]) / 12) * ((temperature[-1] - 2.5) / 21.5) ** (21.6 / 12)
    return cm

def calculate_rm(temperature):
    # rm 계산 함수
    rm = 0.374 * ((36 - temperature[-1]) / 12) * ((temperature[-1] - 2.5) / 21.5) ** (21.6 / 12)
    return rm

def calculate_tb(temperature):
    # tb 계산 함수
    tb = 30 - 23.2 * ((42 - temperature[-1]) / 16.6) * ((temperature[-1] - 4) / 21.4) ** (21.4 / 16.6)
    return tb

def update_graph():
    # 그래프 업데이트
    try:
        df = pd.read_excel('D:/Data/temperature_data.xlsx')

        # 엑셀 값에서 x와 일평균 온도 추출
        x = df['정식후날짜'].tolist()
        temperature = df['일평균온도'].tolist()

        cm = calculate_cm(temperature)
        rm = calculate_rm(temperature)
        tb = calculate_tb(temperature)

        # cm, rm, tb 값을 표시할 레이블 업데이트
        cm_label.config(text="Crop growth rate: {:.3f}".format(cm))
        rm_label.config(text="Relative growth rate: {:.3f}".format(rm))
        tb_label.config(text="tb: {:.3f}".format(tb))

    except (pd.errors.EmptyDataError, FileNotFoundError, KeyError, IndexError):
        x = np.linspace(0, 50, 100)
        temperature = [0.0] * 100  # 값이 비어있거나 파일을 찾을 수 없을 때 기본값 0.0 설정
        cm, rm, tb = 0.0, 0.0, 0.0

    y1, y2 = simulate_graph(x, cm, rm, tb)

    # y1과 y2의 최종 결과값 출력
    y1_label.config(text="Fresh weight (g/m2): {:.1f}".format(y1[-1]))
    y2_label.config(text="Dry weight (g/m2): {:.1f}".format(y2[-1]))

    plt.cla()
    plt.plot(x, y1, label='y1')
    plt.xlabel('Days after transplant (DAT)')
    plt.ylabel('Fresh weight (g/m2)')
    plt.title('Graph')

    # y2 값을 제2 Y축으로 표시
    ax2 = plt.gca().twinx()
    ax2.plot(x, y2, label='y2', color='red')
    ax2.set_ylabel('Dry weight (g/m2)', color='red')

    plt.grid(True)
    plt.show()


def reset_values():
    # 초기화
    cm_label.config(text="Crop growth rate: {:.1f}".format(0.0))
    rm_label.config(text="Relative growth rate: {:.2f}".format(0.0))
    tb_label.config(text="tb: {:.1f}".format(0.0))


# 윈도우 창 생성
window = tk.Tk()
window.title("Graph Simulation")
window.geometry("400x600")
window.configure(bg="#F0F0F0")

# y1과 y2 값을 표시할 레이블 생성
y1_label = tk.Label(window, text="Fresh weight (g/m2): ", bg="#F0F0F0", font=("Arial", 12))
y1_label.pack()

y2_label = tk.Label(window, text="Dry weight (g/m2): ", bg="#F0F0F0", font=("Arial", 12))
y2_label.pack()

# cm, rm, tb 값을 표시할 레이블 생성
cm_label = tk.Label(window, text="Crop growth rate: {:.1f}".format(0.0), bg="#F0F0F0", font=("Arial", 12))
cm_label.pack()

rm_label = tk.Label(window, text="Relative growth rate: {:.2f}".format(0.0), bg="#F0F0F0", font=("Arial", 12))
rm_label.pack()

tb_label = tk.Label(window, text="tb: {:.1f}".format(0.0), bg="#F0F0F0", font=("Arial", 12))
tb_label.pack()

# 버튼 프레임
button_frame = tk.Frame(window, bg="#F0F0F0")
button_frame.pack()

# 버튼 생성
graph_button = tk.Button(button_frame, text="시뮬레이션", command=update_graph, font=("Arial", 12))
graph_button.pack(side=tk.LEFT, padx=5, pady=10)

reset_button = tk.Button(button_frame, text="초기화", command=reset_values, font=("Arial", 12))
reset_button.pack(side=tk.LEFT, padx=5, pady=10)

# 종료 버튼
close_button = tk.Button(window, text="닫기", command=window.destroy, font=("Arial", 12))
close_button.pack(pady=10)

# 윈도우 창 실행
window.mainloop()
