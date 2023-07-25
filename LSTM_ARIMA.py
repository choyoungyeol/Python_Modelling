import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import statsmodels.api as sm

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

# LSTM 모델 생성
model = Sequential()
model.add(LSTM(64, input_shape=(lookback, 1)))
model.add(Dense(5))  # y 데이터의 특성 개수는 5로 고정
model.compile(loss='mean_squared_error', optimizer='adam')

# LSTM 모델 학습
model.fit(X_train, y_train, epochs=10, batch_size=16, verbose=1)

# 예측
y_pred = model.predict(X_test)

# 예측 결과 역정규화
y_pred = scaler_y.inverse_transform(y_pred)
y_test = scaler_y.inverse_transform(y_test)

# 추가 예측
X_additional = X_test[-1:]  # 마지막 테스트 데이터
y_additional = []

for _ in range(7):  # 1주일 동안의 예측
    X_additional_scaled = scaler_X.transform(X_additional.reshape(-1, 1))
    X_additional_lstm = X_additional_scaled[-lookback:].reshape(1, lookback, 1)
    y_additional_scaled = model.predict(X_additional_lstm)
    y_additional.append(scaler_y.inverse_transform(y_additional_scaled).flatten())
    X_additional = np.append(X_additional, y_additional_scaled[:, -1])

y_additional = np.array(y_additional)

# 시간 간격에 맞춰서 Date 생성
last_date = X[-1].astype('datetime64[h]').astype(datetime)  # 마지막 실제 데이터의 날짜와 시간을 datetime.datetime 형식으로 변환
date_list = [last_date + timedelta(hours=i) for i in range(1, len(y_additional)+1)]

# 각 항목별로 개별 윈도우 창에 그래프 생성
for i in range(y.shape[1]):
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(range(len(y_test)), y_test[:, i], label='M')
    ax.plot(range(len(y_test)), y_pred[:, i], label='E')
    ax.plot(range(len(y_test), len(y_test) + len(y_additional)), y_additional[:, i], label='EE')
    ax.set_xticks(range(len(y_test), len(y_test) + len(y_additional)))
    ax.set_xticklabels(date_list, rotation=45)
    ax.set_xlabel('Time')
    ax.set_ylabel(data.columns[i+1])
    ax.set_title(data.columns[i+1])
    ax.legend()
    ax.set_ylim(0)  # y축을 항상 0으로 표기

    # ARIMA 모델 생성과 예측
    series = data[data.columns[i+1]]
    model = sm.tsa.ARIMA(series, order=(1, 0, 0))  # ARIMA(p, d, q) 모델로 설정
    model_fit = model.fit()  # 'disp' argument 제거
    y_arima = model_fit.forecast(steps=7)  # 7일 동안의 예측

    # 예측 결과를 그래프에 추가
    ax.plot(range(len(y_test) + len(y_additional), len(y_test) + len(y_additional) + 7), y_arima, label='ARIMA', linestyle='dashed', color='red')

# 그래프 표시
plt.tight_layout()
plt.show()
