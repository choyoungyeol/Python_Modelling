import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import re

# 엑셀 파일에서 센서 데이터 불러오기 (가정: 데이터가 'data.xlsx' 파일에 저장되어 있음)
data = pd.read_excel('D:/Data/GS3.xlsx', header=None)

# 열에 대한 제목 지정 (가정: 각 열에 대한 순서는 날짜와 시간을 같이 포함한 열, Channel, VWC, Temp, EC 순서)
data.columns = ['Date', 'Channel', 'VWC', 'Temp', 'EC']

# 정규식을 사용하여 날짜와 시간 정보 추출
pattern = re.compile(r'(\d{4}-\d{2}-\d{2})\s+(\d{2}:\d{2}:\d{2})')
extracted_data = data['Date'].astype(str).str.extract(pattern)

# '날짜'와 '시간' 열로 분리하여 추가
data['Day'] = extracted_data[0]
data['Time'] = extracted_data[1]

# 날짜와 시간 정보를 합쳐서 datetime 형태로 변환
data['Date'] = pd.to_datetime(data['Day'] + ' ' + data['Time'])

# 시간에 따라 데이터를 정렬
data = data.sort_values(by='Date')

# 'Channel' 항목 삭제
data = data.drop(columns='Channel')

# 시각화 함수 (서서히 변화하는 그래프)
def animate(i):
    plt.clf()  # 현재 그래프를 지웁니다.

    plt.title('Sensor Data Visualization')
    plt.xlabel('Time')
    plt.ylabel('Value')

    x = data['Date'][:i]  # 현재 인덱스까지의 데이터를 슬라이싱합니다.

    # Plot VWC and Temp
    line_vwc, = plt.plot(x, data['VWC'][:i], 'g.-', label='VWC')
    line_temp, = plt.plot(x, data['Temp'][:i], 'b.-', label='Temp')

    # EC를 제2Y축으로 표시합니다.
    ax2 = plt.twinx()
    ax2.set_ylabel('EC Value', color='m')
    line_ec, = ax2.plot(x, data['EC'][:i], 'm.-', label='EC')

    # 범례를 표시합니다.
    lines = [line_vwc, line_temp, line_ec]
    labels = [line.get_label() for line in lines]
    plt.legend(lines, labels)

    plt.xticks(rotation=45, ha='right')

# 초기 그래프를 생성합니다.
fig, ax = plt.subplots()
plt.tight_layout()

# 애니메이션을 생성합니다. (참고: 성능을 향상시키기 위해 blit=False로 설정합니다.)
ani = FuncAnimation(fig, animate, frames=len(data), interval=100, repeat=False, blit=False)

plt.show()
