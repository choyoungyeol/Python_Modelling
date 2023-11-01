import pandas as pd
import numpy as np
import joblib

# 저장된 XGBoost 모델과 스케일러 불러오기
model = joblib.load('D:/Data/xgboost_model.pkl')
scaler_X_env = joblib.load('D:/Data/scaler_X_env.pkl')
scaler_y_growth = joblib.load('D:/Data/scaler_y_growth.pkl')

# 새로운 환경 변수 데이터 불러오기 (날짜 정보 포함)
new_env_data = pd.read_excel('D:/Data/Growth_XGboost.xlsx', parse_dates=['Date'])

# 날짜 열을 제외한 환경 변수 데이터 추출
env_data = new_env_data[['Temp', 'RH', 'VPD', 'CO2']].values

# 환경 변수 스케일링
scaled_env_data = scaler_X_env.transform(env_data)

# 성장량 예측
predicted_growth_scaled = model.predict(scaled_env_data)

# 예측 결과 역정규화
predicted_growth = scaler_y_growth.inverse_transform(predicted_growth_scaled.reshape(-1, 1)).flatten()

# 예측된 Growth 값을 데이터프레임에 추가
new_env_data['Predicted Growth'] = predicted_growth

# 결과를 엑셀 파일로 저장
new_env_data.to_excel('D:/Data/Predicted_growth_Final.xlsx', index=False)
print("예측된 Growth 값을 새로운 엑셀 파일로 저장했습니다.")
