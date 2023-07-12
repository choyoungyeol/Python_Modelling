import os
import numpy as np
import cv2
from datetime import datetime
from keras.models import Sequential
from keras.layers import LSTM, Dense, TimeDistributed, Flatten
from keras.layers.convolutional import Conv2D, MaxPooling2D
from sklearn.model_selection import train_test_split

# Tipburn 데이터 폴더 경로
data_folder = "D:/AI/Lettuce_Piumi/Lettuce"
tipburn_folder = os.path.join(data_folder, "Tipburn")
normal_folder = os.path.join(data_folder, "Healthy")

# Tipburn 데이터 로드 및 전처리
tipburn_images = []
tipburn_timestamps = []
for filename in os.listdir(tipburn_folder):
    if filename.endswith(".jpg"):
        img = cv2.imread(os.path.join(tipburn_folder, filename))
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # 그레이스케일로 변환
        img = cv2.resize(img, (32, 32))  # 이미지 크기 조정
        tipburn_images.append(img)

        # 파일명에서 날짜 정보 추출
        filename = filename.split(".")[0]  # 파일명에서 확장자 부분을 제외한 부분 추출
        date_str, time_str = filename.split("-")

        if "_" not in date_str or "_" not in time_str:
            raise ValueError("날짜 또는 시간 정보가 올바르게 구성되지 않았습니다.")

        date_parts = date_str.split("_")
        time_parts = time_str.split("_")

        if len(date_parts) != 3 or len(time_parts) != 3:
            raise ValueError("날짜 또는 시간 정보가 올바르게 구성되지 않았습니다.")

        year_str, month_str, day_str = date_parts
        hour_str, minute_str, second_str = time_parts

        date_time_str = f"{year_str}-{month_str}-{day_str}_{hour_str}-{minute_str}-{second_str}"
        timestamp = datetime.strptime(date_time_str, "%Y-%m-%d_%H-%M-%S").date()
        tipburn_timestamps.append(timestamp)

# Normal 데이터 로드 및 전처리
normal_images = []
normal_timestamps = []
for filename in os.listdir(normal_folder):
    if filename.endswith(".jpg"):
        img = cv2.imread(os.path.join(normal_folder, filename))
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # 그레이스케일로 변환
        img = cv2.resize(img, (32, 32))  # 이미지 크기 조정
        normal_images.append(img)

        # 파일명에서 날짜 정보 추출
        filename = filename.split(".")[0]  # 파일명에서 확장자 부분을 제외한 부분 추출
        date_str, time_str = filename.split("-")

        if "_" not in date_str or "_" not in time_str:
            raise ValueError("날짜 또는 시간 정보가 올바르게 구성되지 않았습니다.")

        date_parts = date_str.split("_")
        time_parts = time_str.split("_")

        if len(date_parts) != 3 or len(time_parts) != 3:
            raise ValueError("날짜 또는 시간 정보가 올바르게 구성되지 않았습니다.")

        year_str, month_str, day_str = date_parts
        hour_str, minute_str, second_str = time_parts

        date_time_str = f"{year_str}-{month_str}-{day_str}_{hour_str}-{minute_str}-{second_str}"
        timestamp = datetime.strptime(date_time_str, "%Y-%m-%d_%H-%M-%S").date()
        normal_timestamps.append(timestamp)

# Tipburn과 Normal 데이터를 합쳐서 X, y로 구성
X = np.array(tipburn_images + normal_images)
y = np.array([1] * len(tipburn_images) + [0] * len(normal_images))

# 시간 순으로 데이터 정렬
timestamps = np.array(tipburn_timestamps + normal_timestamps)
sorted_indices = np.argsort(timestamps)
X = X[sorted_indices]
y = y[sorted_indices]

# 데이터 분할: 훈련 데이터와 테스트 데이터로 나눔
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# # 데이터 reshape
# X_train = X_train.reshape(X_train.shape[0], X_train.shape[1], X_train.shape[2], 1)
# X_test = X_test.reshape(X_test.shape[0], X_test.shape[1], X_test.shape[2], 1)
#
# # y_train과 y_test를 2차원으로 변환
# # 주석으로 표시한 위치에 아래 코드 추가
# # -------------------------------------
# y_train = np.reshape(y_train, (-1, 1))
# y_test = np.reshape(y_test, (-1, 1))
# # -------------------------------------

print("X_train의 차원:", X_train.ndim)
print("X_test의 차원:", X_test.ndim)
print("X_train의 모양:", X_train.shape)
print("X_test의 모양:", X_test.shape)

# 데이터 reshape
X_train = X_train.reshape(X_train.shape[0], X_train.shape[1], X_train.shape[2], 1)
X_test = X_test.reshape(X_test.shape[0], X_test.shape[1], X_test.shape[2], 1)

# LSTM 모델 구축
model = Sequential()
model.add(Conv2D(32, (3, 3), activation='relu', input_shape=(X_train.shape[1], X_train.shape[2], 1)))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Flatten())
model.add(RepeatVector(1))
model.add(LSTM(64))
model.add(Dense(1, activation='sigmoid'))

# 모델 컴파일
model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

# 모델 훈련
model.fit(X_train, y_train, epochs=10, batch_size=32, validation_data=(X_test, y_test))

# 모델 저장
model.save("D:/AI/tipburn_lstm_model.h5")

from keras.models import load_model

# 모델 불러오기
loaded_model = load_model("D:/AI/tipburn_lstm_model.h5")

# 모델 평가
loss, accuracy = loaded_model.evaluate(X_test, y_test)
print("평가 결과 - 손실: {:.4f}, 정확도: {:.4f}".format(loss, accuracy))

import cv2
import numpy as np

# 입력 이미지 경로
image_path = "D:/AI/Lettuce_Piumi/Lettuce/Healthy/2023_04_24-13_43_37.jpg"

# 이미지 로드
img = cv2.imread(image_path)

if img is not None:
    # 이미지 전처리
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # 그레이스케일로 변환
    img = cv2.resize(img, (32, 32))  # 이미지 크기 조정
    input_image = np.expand_dims(img, axis=0)  # 모델 입력 형태로 변환
    input_image = np.expand_dims(input_image, axis=-1)  # 차원을 추가하여 (1, 32, 32, 1)로 변환

    # Tipburn 예측
    prediction = loaded_model.predict(input_image)
    prediction_label = "Tipburn 발생" if prediction[0][0] > 0.5 else "Tipburn 미발생"
    prediction_confidence = prediction[0][0] if prediction[0][0] > 0.5 else 1 - prediction[0][0]

    print("Tipburn 예측 결과: {} (확률: {:.2f}%)".format(prediction_label, prediction_confidence * 100))
else:
    print("이미지를 로드할 수 없습니다.")

# Tipburn 발생 시점 예측
predictions = loaded_model.predict(X_test)
predicted_timestamps = timestamps[sorted_indices][-len(X_test):]
predicted_tipburn_timestamps = predicted_timestamps[predictions.flatten() > 0.5]

# 시퀀스 예측
input_sequence = np.expand_dims(X_test, axis=-1)  # 시퀀스 입력 형태로 변환
sequence_predictions = loaded_model.predict(input_sequence)
predicted_timestamp = timestamps[np.argmax(sequence_predictions)]  # 최댓값을 갖는 타임스탬프 선택

print("Tipburn 예측 결과: {} (확률: {:.2f}%)".format(prediction_label, prediction_confidence * 100))
print("Tipburn 발생 시점 예측: {} 시점".format(predicted_timestamp))
