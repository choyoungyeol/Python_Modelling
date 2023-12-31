import tkinter as tk
import pandas as pd
from tkinter import ttk
from tkcalendar import Calendar
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import datetime

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
    germination_temp = -84.4

    # 만개기 적산온도
    flowering_temp = 231.3

    # 엑셀 파일로부터 데이터 읽어오기
    df = pd.read_excel("D:/Data/Pear_Weather.xlsx")

    # 기간에 해당하는 데이터 추출
    mask = (df['날짜'] >= start_date) & (df['날짜'] <= end_date)
    filtered_df = df.loc[mask].copy()

    # 데이터 프레임의 날짜 열을 datetime 형식으로 변환
    filtered_df['날짜'] = pd.to_datetime(filtered_df['날짜'])

    # 최저온도, 평균온도, 최고온도 추출
    min_temp = filtered_df['최저온도']
    avg_temp = filtered_df['평균온도']
    max_temp = filtered_df['최고온도']

    # 그래프 표시
    fig, ax = plt.subplots()
    ax.plot(filtered_df['날짜'], min_temp, label="Min Temp")
    ax.plot(filtered_df['날짜'], avg_temp, label="Avg Temp")
    ax.plot(filtered_df['날짜'], max_temp, label="Max Temp")
    ax.set_xlabel("Date")
    ax.set_ylabel("Temperature (oC)")
    ax.set_title("Temperature during the Period")
    ax.legend()

    # 그래프를 tkinter 창에 표시
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.draw()
    canvas.get_tk_widget().pack()

    # 주요 온도 범위에 대한 계산식 적용
    chill_day = []
    anti_chill_day = []
    anti_chill_day_dates = []
    chill_day_dates = []
    flowering_dates = []
    for i in filtered_df.index:
        if 0 <= min_temp_value <= filtered_df.loc[i, '최저온도'] <= filtered_df.loc[i, '최고온도']:
            chill_day.append(0)
            anti_chill_day.append(filtered_df.loc[i, '평균온도'] - min_temp_value)
        elif 0 <= filtered_df.loc[i, '최저온도'] <= min_temp_value <= filtered_df.loc[i, '최고온도']:
            chill_day.append(-((filtered_df.loc[i, '평균온도'] - filtered_df.loc[i, '최저온도']) - (
                    (filtered_df.loc[i, '최고온도'] - min_temp_value) / 2)))
            anti_chill_day.append((filtered_df.loc[i, '최고온도'] - min_temp_value) / 2)
        elif 0 <= filtered_df.loc[i, '최저온도'] <= filtered_df.loc[i, '최고온도'] <= min_temp_value:
            chill_day.append(-(filtered_df.loc[i, '평균온도'] - filtered_df.loc[i, '최저온도']))
            anti_chill_day.append(0)
        elif filtered_df.loc[i, '최저온도'] <= 0 < filtered_df.loc[i, '최고온도'] <= min_temp_value:
            chill_day.append(-(
                    (filtered_df.loc[i, '최고온도'] / (filtered_df.loc[i, '최고온도'] - filtered_df.loc[i, '최저온도'])) * (
                            filtered_df.loc[i, '최고온도'] / 2)))
            anti_chill_day.append(0)
        elif filtered_df.loc[i, '최저온도'] <= 0 <= min_temp_value <= filtered_df.loc[i, '최고온도']:
            chill_day.append(-(
                    (filtered_df.loc[i, '최고온도'] / (filtered_df.loc[i, '최고온도'] - filtered_df.loc[i, '최저온도'])) * (
                            filtered_df.loc[i, '최고온도'] / 2) - ((filtered_df.loc[i, '최고온도'] - min_temp_value) / 2)))
            anti_chill_day.append(-((filtered_df.loc[i, '최고온도'] - min_temp_value) / 2))

    flowering_dates = []
    chill_day_sum = 0  # chill_day_sum 초기화
    anti_chill_day_sum = 0  # anti_chill_day_sum 초기화
    for i in range(len(chill_day)):  # chill_day 리스트의 길이만큼 반복
        chill_day_sum += chill_day[i]  # chill_day_sum 값을 누적
        if chill_day_sum <= germination_temp:
            anti_chill_day_sum += anti_chill_day[i]  # anti_chill_day_sum 값을 누적
            if anti_chill_day_sum >= flowering_temp:
                flowering_dates.append(filtered_df['날짜'].iloc[i])

    # Anti Chill Days 출력 윈도우
    anti_chill_day_label.config(text=f"Anti Chill Days: {sum(anti_chill_day)}")

    # Chill Days 출력 윈도우
    chill_day_label.config(text=f"Chill Days: {sum(chill_day)}")

    # 첫개화시기 출력
    if len(flowering_dates) > 0:
        first_flowering_date = flowering_dates[0]  # 첫번째 개화 시기를 가져옴
        formatted_first_flowering_date = first_flowering_date.strftime("%Y-%m-%d")  # 원하는 포맷으로 날짜를 변환
        first_flowering_label.config(text=f"첫개화시기: {formatted_first_flowering_date}")
    else:
        first_flowering_label.config(text="첫개화시기: 없음")

    # 만개시기 출력
    if len(flowering_dates) > 0:
        last_flowering_date = flowering_dates[-1]  # 마지막 개화 시기를 가져옴
        formatted_last_flowering_date = last_flowering_date.strftime("%Y-%m-%d")  # 원하는 포맷으로 날짜를 변환
        last_flowering_label.config(text=f"만개시기: {formatted_last_flowering_date}")
    else:
        last_flowering_label.config(text="만개시기: 없음")

    # Anti Chill Days 출력 윈도우
    anti_chill_day_label.config(text=f"Anti Chill Days: {sum(anti_chill_day)}")
    print(f"Anti Chill Days: {sum(anti_chill_day)}")

    # Chill Days 출력 윈도우
    chill_day_label.config(text=f"Chill Days: {sum(chill_day)}")
    print(f"Chill Days: {sum(chill_day)}")


# 메인 창 생성
root = tk.Tk()
root.title("날짜와 온도 설정")

# 날짜 설정 프레임
date_frame = ttk.Frame(root)
date_frame.pack(pady=20)

# 시작 날짜 입력
start_date_label = ttk.Label(date_frame, text="시작 날짜:")
start_date_label.grid(row=0, column=0, padx=10)

start_date_entry = ttk.Entry(date_frame)
start_date_entry.grid(row=0, column=1, padx=10)

start_date_button = ttk.Button(date_frame, text="달력", command=lambda: show_calendar(start_date_entry))
start_date_button.grid(row=0, column=2, padx=10)

# 종료 날짜 입력
end_date_label = ttk.Label(date_frame, text="종료 날짜:")
end_date_label.grid(row=1, column=0, padx=10)

end_date_entry = ttk.Entry(date_frame)
end_date_entry.grid(row=1, column=1, padx=10)

end_date_button = ttk.Button(date_frame, text="달력", command=lambda: show_calendar(end_date_entry))
end_date_button.grid(row=1, column=2, padx=10)

# 주요 온도 설정 프레임
temp_frame = ttk.Frame(root)
temp_frame.pack(pady=10)

min_temp_label = ttk.Label(temp_frame, text="최저 온도 (Min Temp):")
min_temp_label.grid(row=0, column=0, padx=10)

min_temp_value_label = ttk.Label(temp_frame, text="5.4")
min_temp_value_label.grid(row=0, column=1, padx=10)

opt_temp_label = ttk.Label(temp_frame, text="최적 온도 (Opt Temp):")
opt_temp_label.grid(row=1, column=0, padx=10)

opt_temp_value_label = ttk.Label(temp_frame, text="26.0")
opt_temp_value_label.grid(row=1, column=1, padx=10)

max_temp_label = ttk.Label(temp_frame, text="최고 온도 (Max Temp):")
max_temp_label.grid(row=2, column=0, padx=10)

max_temp_value_label = ttk.Label(temp_frame, text="36.0")
max_temp_value_label.grid(row=2, column=1, padx=10)

# 발아일 예측온도, 만개기 적산온도 프레임
calc_frame = ttk.Frame(root)
calc_frame.pack(pady=10)

germination_temp_label = ttk.Label(calc_frame, text="발아일 예측온도:")
germination_temp_label.grid(row=0, column=0, padx=10)

germination_temp_value_label = ttk.Label(calc_frame, text="-84.4")
germination_temp_value_label.grid(row=0, column=1, padx=10)

flowering_temp_label = ttk.Label(calc_frame, text="만개기 적산온도:")
flowering_temp_label.grid(row=1, column=0, padx=10)

flowering_temp_value_label = ttk.Label(calc_frame, text="231.3")
flowering_temp_value_label.grid(row=1, column=1, padx=10)

# 결과 출력 프레임
result_frame = ttk.Frame(root)
result_frame.pack(pady=10)

anti_chill_day_label = ttk.Label(result_frame, text="Anti Chill Days: ")
anti_chill_day_label.grid(row=0, column=0, padx=10)

chill_day_label = ttk.Label(result_frame, text="Chill Days: ")
chill_day_label.grid(row=1, column=0, padx=10)

# first_flowering_label = ttk.Label(result_frame, text="첫개화시기: ")
# first_flowering_label.grid(row=2, column=0, padx=10)

# 개화시기 출력 라벨
first_flowering_label = tk.Label(root, text="첫개화시기: 없음")
first_flowering_label.pack()
last_flowering_label = tk.Label(root, text="만개시기: 없음")
last_flowering_label.pack()


# 업데이트 버튼
update_button = ttk.Button(root, text="업데이트", command=update_temperature)
update_button.pack(pady=10)

# 닫기 버튼 함수
def close_window():
    root.destroy()

# 닫기 버튼
close_button = ttk.Button(root, text="닫기", command=close_window)
close_button.pack(pady=10)

root.mainloop()
