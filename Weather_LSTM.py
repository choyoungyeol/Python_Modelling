import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
from tensorflow.keras.callbacks import EarlyStopping
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QTabWidget
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

# 데이터 로드
data = pd.read_excel("D:/Data/Weather.xlsx")  # 엑셀 파일 경로를 입력하세요.

# 필요한 데이터 컬럼 선택
selected_columns = ["Date", "Temp", "RH", "CO2", "PAR"]
data = data[selected_columns]

# 날짜 컬럼을 인덱스로 설정
data.set_index("Date", inplace=True)

# 결측치 처리 (필요에 따라 진행)
data.fillna(method="ffill", inplace=True)  # 앞의 값으로 결측치 채우기

# 데이터 정규화
scaler = MinMaxScaler()
data_normalized = scaler.fit_transform(data)

# 시퀀스 데이터 생성
seq_length = 24  # 시퀀스 길이 (24시간)
X, y = [], []
for i in range(len(data_normalized) - seq_length):
    X.append(data_normalized[i : i + seq_length])
    y.append(data_normalized[i + seq_length])

X = np.array(X)
y = np.array(y)

# 훈련 및 테스트 데이터 분할
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# LSTM 모델 구성
model = Sequential()
model.add(LSTM(64, activation="relu", input_shape=(X.shape[1], X.shape[2])))
model.add(Dense(4))  # 예측할 다섯 가지 특성(온도, 상대습도, 이산화탄소, 일사량)
model.compile(optimizer="adam", loss="mse")

# 조기 종료 콜백 설정
early_stopping = EarlyStopping(patience=5, restore_best_weights=True)

# 모델 훈련
model.fit(X_train, y_train, epochs=200, batch_size=32, validation_split=0.2, callbacks=[early_stopping])

# 테스트 데이터로 예측
y_pred = model.predict(X_test)

# 예측된 값을 원래 스케일로 변환
y_pred_rescaled = scaler.inverse_transform(y_pred)
y_test_rescaled = scaler.inverse_transform(y_test)

# 예측 결과 출력
predictions = pd.DataFrame(y_pred_rescaled, columns=data.columns)
ground_truth = pd.DataFrame(y_test_rescaled, columns=data.columns)

# PyQt5 기반 윈도우 클래스
class WeatherPredictionWindow(QMainWindow):
    def __init__(self, predictions, ground_truth, week_predictions):
        super().__init__()

        # 윈도우 설정
        self.setWindowTitle("Weather Prediction")
        self.setGeometry(100, 100, 800, 600)

        # 탭 위젯 설정
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)
        self.tabs = QTabWidget(self.central_widget)

        # 각 항목별 탭 생성
        items = predictions.columns
        for item in items:
            tab = QWidget()
            layout = QVBoxLayout(tab)
            self.tabs.addTab(tab, item)
            fig, ax = plt.subplots(figsize=(8, 6))
            layout.addWidget(FigureCanvas(fig))
            self.plot_results(predictions, ground_truth, item, ax)
            fig.tight_layout()

        # 1주일 예측값 탭 생성
        if week_predictions is not None:
            week_tab = QWidget()
            week_layout = QVBoxLayout(week_tab)
            self.tabs.addTab(week_tab, "2 days Prediction")
            week_fig, week_ax = plt.subplots(figsize=(8, 6))
            week_layout.addWidget(FigureCanvas(week_fig))
            self.plot_week_results(week_predictions, week_ax)
            week_fig.tight_layout()

        layout = QVBoxLayout(self.central_widget)
        layout.addWidget(self.tabs)

    def plot_results(self, predictions, ground_truth, item, ax):
        ax.plot(predictions.index, predictions[item], label="Estimated {}".format(item), color='red')
        ax.plot(ground_truth.index, ground_truth[item], label="Measured {}".format(item), color='blue')
        ax.set_title("{} Prediction".format(item))
        ax.legend()

    def plot_week_results(self, week_predictions, ax):
        for item in week_predictions.columns:
            ax.plot(week_predictions.index, week_predictions[item], label="Estimated {}".format(item))
        ax.set_title("2 days Prediction")
        ax.legend()

# 실행 함수
def run_gui(predictions, ground_truth, week_predictions=None):
    app = QApplication(sys.argv)
    window = WeatherPredictionWindow(predictions, ground_truth, week_predictions)
    window.show()
    sys.exit(app.exec_())

# 테스트 데이터로 예측
y_pred_extended = model.predict(X_test)

# 예측된 값을 원래 스케일로 변환
y_pred_extended_rescaled = scaler.inverse_transform(y_pred_extended)

# 1시간 이후의 예측 데이터 생성
next_hour_date = data.index[-1] + pd.DateOffset(hours=1)
date_list = pd.date_range(start=next_hour_date, periods=24, freq="H")
week_data_df = pd.DataFrame(y_pred_extended_rescaled[-24:], columns=data.columns, index=date_list)

# 예측된 값을 1시간 이후의 데이터에 추가
for i in range(24):
    next_hour_date += pd.DateOffset(hours=1)
    next_hour_predictions = pd.DataFrame([y_pred_extended_rescaled[i]], columns=data.columns, index=[next_hour_date])
    week_data_df.update(next_hour_predictions)

# 2일 예측 데이터를 "week_data_df.xlsx"로 저장
week_data_df.to_excel("D:/Data/week_data.xlsx", index=True)

# 결과 출력
run_gui(predictions, ground_truth, week_data_df)
