import tkinter as tk
from tkinter import ttk
from tkcalendar import Calendar
import matplotlib.pyplot as plt
import pandas as pd


def show_calendar(text_entry):
    def on_date_select():
        selected_date = cal.selection_get().strftime("%Y-%m-%d")
        text_entry.delete(0, tk.END)
        text_entry.insert(0, selected_date)
        calendar_window.destroy()

    calendar_window = tk.Toplevel()
    calendar_window.title("달력")

    cal = Calendar(calendar_window, selectmode="day", date_pattern="yyyy-mm-dd")
    cal.pack(padx=20, pady=20)

    select_button = ttk.Button(calendar_window, text="선택", command=on_date_select)
    select_button.pack(pady=10)

    calendar_window.mainloop()


def update_temperature():
    start_date = start_date_entry.get()
    end_date = end_date_entry.get()

    # 주요 온도 설정
    min_temp_value = 5.4
    opt_temp_value = 26.0
    max_temp_value = 36.0

    # 발아일 예측온도
    germination_temp = -86.4

    # 만개기 적산온도
    flowering_temp = 231.3

    # 엑셀 파일로부터 데이터 읽어오기
    df = pd.read_excel("D:/Data/Pear_Weather.xlsx")

    # 기간에 해당하는 데이터 추출
    mask = (df['날짜'] >= start_date) & (df['날짜'] <= end_date)
    filtered_df = df.loc[mask]

    # 최저온도, 적정온도, 최고온도 추출
    min_temp = filtered_df['최저온도'].values
    avg_temp = filtered_df['평균온도'].values
    max_temp = filtered_df['최고온도'].values

    # 그래프 표시
    plt.plot(filtered_df['날짜'], min_temp, label="Min Temp")
    plt.plot(filtered_df['날짜'], avg_temp, label="Avg Temp")
    plt.plot(filtered_df['날짜'], max_temp, label="Max Temp")

    # 주요 온도 범위에 대한 계산식 적용
    chill_day = [0] * len(min_temp)
    anti_chill_day = [0] * len(min_temp)
    for i in range(len(min_temp)):
        if 0 <= min_temp_value <= min_temp[i] <= max_temp[i]:
            anti_chill_day[i] = avg_temp[i] - min_temp_value
        elif 0 <= min_temp[i] <= min_temp_value <= max_temp[i]:
            chill_day[i] = - ((avg_temp[i] - min_temp[i]) - ((max_temp[i] - min_temp_value) / 2))
            anti_chill_day[i] = (max_temp[i] - min_temp_value) / 2
        elif 0 <= min_temp[i] <= max_temp[i] <= min_temp_value:
            chill_day[i] = - (avg_temp[i] - min_temp[i])
        elif min_temp[i] <= 0 < max_temp[i] <= min_temp_value:
            chill_day[i] = - ((max_temp[i] / (max_temp[i] - min_temp[i])) * (max_temp[i] / 2))
        elif min_temp[i] <= 0 <= min_temp_value <= max_temp[i]:
            chill_day[i] = - ((max_temp[i] / (max_temp[i] - min_temp[i])) * (max_temp[i] / 2) - ((max_temp[i] - min_temp_value) / 2))
            anti_chill_day[i] = - ((max_temp[i] - min_temp_value) / 2)

    # 수평선 추가
    for day in chill_day:
        plt.axhline(y=day, color='red', linestyle='--')
    for day in anti_chill_day:
        plt.axhline(y=day, color='blue', linestyle='--')

    plt.xlabel("Date")
    plt.ylabel("Temperature (oC)")
    plt.title("Temperature during the Period")
    plt.legend()
    plt.show()


# 메인 창 생성
root = tk.Tk()
root.title("날짜와 온도 설정")

# 날짜 설정 프레임
date_frame = ttk.Frame(root)
date_frame.pack(pady=20)

# 시작 날짜 입력
start_date_label = ttk.Label(date_frame, text="시작 날짜:")
start_date_label.grid(row=0, column=0, padx=5)
start_date_entry = ttk.Entry(date_frame)
start_date_entry.grid(row=0, column=1, padx=5)

# 시작 날짜 선택 버튼
start_date_button = ttk.Button(date_frame, text="날짜 선택", command=lambda: show_calendar(start_date_entry))
start_date_button.grid(row=0, column=2, padx=5)

# 종료 날짜 입력
end_date_label = ttk.Label(date_frame, text="종료 날짜:")
end_date_label.grid(row=1, column=0, padx=5)
end_date_entry = ttk.Entry(date_frame)
end_date_entry.grid(row=1, column=1, padx=5)

# 종료 날짜 선택 버튼
end_date_button = ttk.Button(date_frame, text="날짜 선택", command=lambda: show_calendar(end_date_entry))
end_date_button.grid(row=1, column=2, padx=5)

# 설정 버튼
set_button = ttk.Button(root, text="날짜 및 온도 설정", command=update_temperature)
set_button.pack(pady=10)

root.mainloop()
