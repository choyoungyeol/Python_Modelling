import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np

# 엑셀 파일에서 데이터를 읽어옵니다.
data = pd.read_excel('D:/Data/GS3.xlsx', header=None)

# 필요한 열만 남기고 나머지 열들을 삭제합니다.
data = data.iloc[:, :5]

# 열 이름을 변경합니다.
data.columns = ['Date', 'Channel', 'VWC', 'Temp', 'EC']

# 날짜와 시간 정보를 합쳐서 datetime 형태로 변환합니다. (errors='coerce'를 사용하여 오류가 발생하는 행은 NaT로 처리합니다.)
data['Date'] = pd.to_datetime(data['Date'], errors='coerce')

# Remove rows with NaT values in the 'Date' column
data.dropna(subset=['Date'], inplace=True)

# 'VWC', 'Temp', 'EC' 열을 실수형으로 변환합니다.
data['VWC'] = pd.to_numeric(data['VWC'], errors='coerce')
data['Temp'] = pd.to_numeric(data['Temp'], errors='coerce')
data['EC'] = pd.to_numeric(data['EC'], errors='coerce')

# 빈 칸을 보간하여 데이터를 채웁니다. (보간은 VWC, Temp, EC 열에만 적용됩니다.)
data['VWC'].interpolate(method='linear', inplace=True)
data['Temp'].interpolate(method='linear', inplace=True)
data['EC'].interpolate(method='linear', inplace=True)

# # 전 데이터와 후 데이터의 평균값으로 보간하는 방법을 적용합니다.
# # 전전데이터, 전데이터와의 평균, 이후데이터와의 평균으로 보간하는 방법을 적용합니다.
# def interpolate_with_mean_or_previous(row):
#     for i in range(2, 5):
#         if pd.isnull(row[i]) or not np.isreal(row[i]):
#             # Check if previous, previous previous, subsequent, and subsequent subsequent data are available and numeric
#             if i - 2 >= 0 and not pd.isnull(row[i - 2]) and np.isreal(row[i - 2]) \
#                     and not pd.isnull(row[i - 1]) and np.isreal(row[i - 1]) \
#                     and i + 1 < len(row) and not pd.isnull(row[i + 1]) and np.isreal(row[i + 1]) \
#                     and i + 2 < len(row) and not pd.isnull(row[i + 2]) and np.isreal(row[i + 2]):
#                 prev_prev_data = row[i - 2]
#                 prev_data = row[i - 1]
#                 next_data = row[i + 1]
#                 next_next_data = row[i + 2]
#
#                 # Calculate differences
#                 prev_diff = abs(row[i] - prev_data)
#                 prev_prev_diff = abs(row[i] - prev_prev_data)
#                 next_diff = abs(row[i] - next_data)
#                 next_next_diff = abs(row[i] - next_next_data)
#
#                 # Use previous data if the difference is greater than 50% of the previous data and previous previous data
#                 if prev_diff > abs(0.5 * prev_data) and prev_diff > abs(0.5 * prev_prev_data):
#                     row[i] = prev_data
#                 # Use next data if the difference is greater than 50% of the next data and next next data
#                 elif next_diff > abs(0.5 * next_data) and next_diff > abs(0.5 * next_next_data):
#                     row[i] = next_data
#                 # Use mean of previous and next data
#                 else:
#                     row[i] = (prev_data + next_data) / 2
#             # If only previous and subsequent data are available and numeric, use mean of them
#             elif i - 1 >= 0 and i + 1 < len(row) and not pd.isnull(row[i - 1]) and np.isreal(row[i - 1]) \
#                     and not pd.isnull(row[i + 1]) and np.isreal(row[i + 1]):
#                 prev_data = row[i - 1]
#                 next_data = row[i + 1]
#                 row[i] = (prev_data + next_data) / 2
#             # If only previous data is available and numeric, use that
#             elif i - 1 >= 0 and not pd.isnull(row[i - 1]) and np.isreal(row[i - 1]):
#                 row[i] = row[i - 1]
#             # If only subsequent data is available and numeric, use that
#             elif i + 1 < len(row) and not pd.isnull(row[i + 1]) and np.isreal(row[i + 1]):
#                 row[i] = row[i + 1]
#             else:
#                 row[i] = np.nan
#     return row
#
# # Apply the interpolation function to the entire dataset
# data = data.apply(interpolate_with_mean_or_previous, axis=1)
#
# # Save the interpolated data to a new file
# interpolated_file_path = 'D:/Data/GS3_interpolated.xlsx'
# data.to_excel(interpolated_file_path, index=False)

def interpolate_with_mean_or_previous(row):
    for i in range(2, 5):
        if pd.isnull(row[i]) or not np.isreal(row[i]):
            # Check if previous, previous previous, subsequent, and subsequent subsequent data are available and numeric
            if i - 2 >= 0 and not pd.isnull(row[i - 2]) and np.isreal(row[i - 2]) \
                    and not pd.isnull(row[i - 1]) and np.isreal(row[i - 1]) \
                    and i + 1 < len(row) and not pd.isnull(row[i + 1]) and np.isreal(row[i + 1]) \
                    and i + 2 < len(row) and not pd.isnull(row[i + 2]) and np.isreal(row[i + 2]):
                prev_prev_data = row[i - 2]
                prev_data = row[i - 1]
                next_data = row[i + 1]
                next_next_data = row[i + 2]

                # Calculate differences
                prev_diff = abs(row[i] - prev_data)
                prev_prev_diff = abs(row[i] - prev_prev_data)
                next_diff = abs(row[i] - next_data)
                next_next_diff = abs(row[i] - next_next_data)

                # Use previous data if the difference is greater than 50% of the previous data and previous previous data
                if prev_diff > abs(0.5 * prev_data) and prev_diff > abs(0.5 * prev_prev_data):
                    row[i] = prev_data
                # Use next data if the difference is greater than 50% of the next data and next next data
                elif next_diff > abs(0.5 * next_data) and next_diff > abs(0.5 * next_next_data):
                    row[i] = next_data
                # Use mean of previous and next data
                else:
                    row[i] = (prev_data + next_data) / 2
            # If only previous and subsequent data are available and numeric, use mean of them
            elif i - 1 >= 0 and i + 1 < len(row) and not pd.isnull(row[i - 1]) and np.isreal(row[i - 1]) \
                    and not pd.isnull(row[i + 1]) and np.isreal(row[i + 1]):
                prev_data = row[i - 1]
                next_data = row[i + 1]
                row[i] = (prev_data + next_data) / 2
            # If only previous data is available and numeric, use that
            elif i - 1 >= 0 and not pd.isnull(row[i - 1]) and np.isreal(row[i - 1]):
                row[i] = row[i - 1]
            # If only subsequent data is available and numeric, use that
            elif i + 1 < len(row) and not pd.isnull(row[i + 1]) and np.isreal(row[i + 1]):
                row[i] = row[i + 1]
            else:
                row[i] = np.nan
    return row

# Apply the interpolation function to the entire dataset
data = data.apply(interpolate_with_mean_or_previous, axis=1)

# Save the interpolated data to a new file
interpolated_file_path = 'D:/Data/GS3_interpolated.xlsx'
data.to_excel(interpolated_file_path, index=False)

# 시각화 함수 (서서히 변화하는 그래프)
def animate(i):
    plt.clf()  # 현재 그래프를 지웁니다.

    plt.title('Sensor Data Visualization')
    plt.xlabel('Time')
    plt.ylabel('Value')

    # 현재 시간에서 1시간 이전까지의 데이터만 보여줍니다.
    end_time = data['Date'].iloc[-1]
    start_time = end_time - pd.Timedelta(hours=1)
    mask = (data['Date'] >= start_time) & (data['Date'] <= end_time)
    x = data['Date'][mask]

    # Plot VWC and Temp
    line_vwc, = plt.plot(x, data['VWC'][mask], 'g.-', label='VWC')
    line_temp, = plt.plot(x, data['Temp'][mask], 'b.-', label='Temp')

    # EC를 제2Y축으로 표시합니다.
    ax2 = plt.twinx()
    ax2.set_ylabel('EC Value', color='m')
    line_ec, = ax2.plot(x, data['EC'][mask], 'm.-', label='EC')

    # 범례를 표시합니다.
    lines = [line_vwc, line_temp, line_ec]
    labels = [line.get_label() for line in lines]
    plt.legend(lines, labels)

    plt.xticks(rotation=45, ha='right')


# 초기 그래프를 생성합니다.
fig, ax = plt.subplots()

# 최근 1시간 동안의 데이터 갯수를 구합니다.
end_time = data['Date'].iloc[-1]
start_time = end_time - pd.Timedelta(hours=1)
num_data_points = len(data[(data['Date'] >= start_time) & (data['Date'] <= end_time)])

# FuncAnimation을 호출할 때 frames 인자를 최근 1시간 동안의 데이터 갯수로 설정합니다.
ani = FuncAnimation(fig, animate, frames=num_data_points, interval=50, repeat=False)

# 보간된 파일명을 출력합니다.
interpolated_file_path = 'D:/Data/GS3_interpolated.xlsx'
print("Interpolated File: ", interpolated_file_path)

plt.show()
