import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
import matplotlib.pyplot as plt
from matplotlib.dates import date2num, DateFormatter

# 엑셀 파일 읽기
data = pd.read_excel('D:/Data/Weather.xlsx')

# 특성과 타겟 데이터 분리
X = data['Date'].values
y = data[['Temp', 'RH', 'CO2', 'DLI', 'PAR']].values

# 데이터 정규화
scaler_X = MinMaxScaler()
scaler_y = MinMaxScaler()
X_scaled = scaler_X.fit_transform(X.reshape(-1, 1))
y_scaled = scaler_y.fit_transform(y)

# 시계열 데이터 준비
lookback = 7  # 과거 7일 데이터를 사용하여 예측
X_lstm = []
y_lstm = []
for i in range(len(X_scaled) - lookback):
    X_lstm.append(X_scaled[i:i + lookback])
    y_lstm.append(y_scaled[i + lookback])
X_lstm = np.array(X_lstm)
y_lstm = np.array(y_lstm)

# 학습 데이터와 테스트 데이터 분리
train_size = int(len(X_lstm) * 0.8)
X_train, X_test = X_lstm[:train_size], X_lstm[train_size:]
y_train, y_test = y_lstm[:train_size], y_lstm[train_size:]
dates_test = X[train_size + lookback:]

# LSTM 모델 생성
model = Sequential()
model.add(LSTM(64, input_shape=(lookback, 1)))
model.add(Dense(y.shape[1]))
model.compile(loss='mean_squared_error', optimizer='adam')

# LSTM 모델 학습
model.fit(X_train, y_train, epochs=10, batch_size=16, verbose=1)

# 예측
y_pred = model.predict(X_test)

# 예측 결과 역정규화
y_pred = scaler_y.inverse_transform(y_pred)
y_test = scaler_y.inverse_transform(y_test)

# 그래프 초기화
figs = []
axes = []
lines = []

for i in range(y.shape[1]):
    fig = plt.figure(figsize=(12, 6))
    ax = fig.add_subplot(111)
    line1, = ax.plot(dates_test, y_test[:, i], color='gray', label='Measured value')
    line2, = ax.plot([], [], color='blue', label='Estimated value')
    ax.set_xlabel('Date')
    ax.set_ylabel(data.columns[i+1])
    ax.set_title(data.columns[i+1])
    ax.legend()
    figs.append(fig)
    axes.append(ax)
    lines.append((line1, line2))

# 날짜 형식 지정
date_format = DateFormatter('%Y-%m-%d')

# 그래프 업데이트 함수
def update_graph(i, frame):
    line2 = lines[i][1]
    line2.set_data(dates_test[frame:], y_pred[:len(dates_test)-frame, i])
    line2.set_xdata(dates_test[frame:])

    #plt.pause(0.2)  # 그래프 업데이트 후 일시 중지

# 그래프 업데이트
for i in range(len(y_pred[0])):
    for j in range(len(dates_test)):
        update_graph(i, j)

    # x축 날짜 형식 설정
    axes[i].xaxis.set_major_formatter(date_format)

# 그래프 표시
plt.show()
