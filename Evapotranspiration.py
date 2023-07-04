import pandas as pd
from sklearn.linear_model import LinearRegression
import math
import matplotlib.pyplot as plt
from tkinter import *
from tkinter import messagebox
import matplotlib.font_manager as fm

def calculate_evapotranspiration(x, selected_features):
    # 주어진 x값과 선택된 항목을 기반으로 증발산량 계산
    evapotranspiration = []

    for _, row in x.iterrows():
        feature_values = [row[feature] for feature in selected_features]

        # 선택된 항목에 따른 증발산량 계산식 예시
        if 'PAR' in selected_features:
            par = feature_values[selected_features.index('PAR')]
            # 계산식 적용
            evapotranspiration.append(85.67 * par + 11.08)
        elif 'Temp' in selected_features:
            temp = feature_values[selected_features.index('Temp')]
            # 계산식 적용
            evapotranspiration.append(12.71 * temp - 236.71)
        elif 'VPD' in selected_features:
            vpd = feature_values[selected_features.index('VPD')]
            # 계산식 적용
            evapotranspiration.append(-54.10 * vpd + 86.64)
        elif 'PAR' in selected_features and 'VPD' in selected_features:
            par = feature_values[selected_features.index('PAR')]
            vpd = feature_values[selected_features.index('VPD')]
            # 계산식 적용
            evapotranspiration.append(82.31 * par - 20.51 * vpd + 32.64)
        elif 'PAR' in selected_features and 'Temp' in selected_features:
            par = feature_values[selected_features.index('PAR')]
            temp = feature_values[selected_features.index('Temp')]
            # 계산식 적용
            evapotranspiration.append(73.57 * par + 3.11 * temp - 51.72)
        elif 'PAR' in selected_features and 'Temp' in selected_features and 'VPD' in selected_features:
            par = feature_values[selected_features.index('PAR')]
            temp = feature_values[selected_features.index('Temp')]
            vpd = feature_values[selected_features.index('VPD')]
            # 계산식 적용
            evapotranspiration.append(58.8 * par - 34.81 * vpd + 5.44 * temp - 62.22)
        else:
            # 선택된 항목에 따른 다른 계산식 적용
            evapotranspiration.append(0)  # 예시로 0으로 설정

    return evapotranspiration

def get_selected_features():
    # 항목 선택을 위한 윈도우 창 생성
    window = Tk()
    window.title("Feature Selection")
    window.geometry("400x300")

    def submit():
        # 선택된 항목을 반환하고 창 종료
        selected_features = [feature for idx, feature in enumerate(features) if var[idx].get() == 1]
        window.destroy()
        run_model(selected_features)

    # 엑셀 파일로부터 데이터 불러오기
    data = pd.read_excel('D:/Data/Environment_Melon.xlsx')
    features = data.columns.tolist()
    features.remove('Date')

    var = []
    for _ in range(len(features)):
        var.append(IntVar())

    for idx, feature in enumerate(features):
        checkbox = Checkbutton(window, text=feature, variable=var[idx], font=("Arial", 12))
        checkbox.pack(pady=5)

    button_frame = Frame(window)
    button_frame.pack(pady=10)

    button = Button(button_frame, text="Submit", command=submit, font=("Arial", 12))
    button.pack(side=LEFT, padx=10)

    close_button = Button(button_frame, text="Close", command=window.destroy, font=("Arial", 12))
    close_button.pack(side=LEFT)

    window.mainloop()

def run_model(selected_features):
    # 엑셀 파일로부터 데이터 불러오기
    data = pd.read_excel('D:/Data/Environment_Melon.xlsx')

    # 선택된 항목 데이터 추출
    X = data[selected_features]

    # 학습 데이터와 테스트 데이터로 분할 (예시로 80:20 비율로 분할)
    train_X = X[:int(len(X)*0.8)]
    train_y = calculate_evapotranspiration(train_X, selected_features)  # 증발산량 계산 함수를 사용하여 y값 계산
    test_X = X[int(len(X)*0.8):]
    test_y = calculate_evapotranspiration(test_X, selected_features)  # 증발산량 계산 함수를 사용하여 y값 계산

    # 선형 회귀 모델 학습
    model = LinearRegression()
    model.fit(train_X, train_y)

    # 테스트 데이터로 예측 수행
    predictions = model.predict(test_X)

    # 예측 결과 출력 및 그래프 그리기
    plt.rcParams.update({'font.size': 14})
    plt.plot(range(len(test_y)), test_y, label='Measured Value', color='blue')
    plt.plot(range(len(predictions)), predictions, label='Estimated Value', color='red')
    plt.xlabel('Data')
    plt.ylabel('Evapotranspiration')
    plt.title('Comparison of Measured and Estimated Value')
    plt.legend()
    plt.show()

    # 측정값 출력
    print("Measured Values:")
    for idx, value in enumerate(test_y):
        print(f"Data {idx + 1}: {value}")

    # 예측값 출력
    print("Predicted Values:")
    for idx, pred in enumerate(predictions):
        print(f"Data {idx + 1}: {pred}")

# 항목 선택 윈도우 창 실행
get_selected_features()
