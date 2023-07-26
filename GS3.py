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
    plt.cla()  # Clear the current plot

    plt.title('Sensor Data Visualization')
    plt.xlabel('Time')
    plt.ylabel('Value')

    x = data['Date'][:i]  # Slice the data to show up to the current index
    vwc_value = data['VWC'][:i]
    temp_value = data['Temp'][:i]
    ec_value = data['EC'][:i]

    plt.plot(x, vwc_value, 'g.-', label='VWC')
    plt.plot(x, temp_value, 'b.-', label='Temp')
    plt.plot(x, ec_value, 'm.-', label='EC')

    plt.legend()
    plt.xticks(rotation=45, ha='right')

# Create the animation
ani = FuncAnimation(plt.gcf(), animate, frames=len(data), interval=100, repeat=False)

plt.tight_layout()
plt.show()
