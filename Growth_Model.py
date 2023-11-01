import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from xgboost import XGBRegressor
import joblib
from sklearn.preprocessing import MinMaxScaler

# 데이터 불러오기 (날짜 열 제외)
data = pd.read_excel('D:/Data/Growth2.xlsx', parse_dates=['Date'])  # Date 열을 날짜 형식으로 불러옴

# 결측값 보간 (linear 방법 사용)
data['Growth'].interpolate(method='linear', inplace=True)

# Growth 값 추출
y_growth = data['Growth'].values

# 환경 변수(Temp, RH, VPD, CO2) 추출
X_env = data[['Temp', 'RH', 'VPD', 'CO2']].values

# 데이터 스케일링 (StandardScaler 사용)
scaler_X_env = StandardScaler()
scaler_y_growth = StandardScaler()

X_env_scaled = scaler_X_env.fit_transform(X_env)
y_growth_scaled = scaler_y_growth.fit_transform(y_growth.reshape(-1, 1)).flatten()

# XGBoost 모델 생성
model = XGBRegressor(n_estimators=400, learning_rate=0.1, random_state=42)

# 모델 학습
model.fit(X_env_scaled, y_growth_scaled)

# 예측
predicted_growth_scaled = model.predict(X_env_scaled)

# 예측 결과 역정규화
predicted_growth = scaler_y_growth.inverse_transform(predicted_growth_scaled.reshape(-1, 1)).flatten()

# 예측된 Growth 값 출력
print("예측된 Growth 값:")
print(predicted_growth)

# 예측된 Growth 값을 데이터프레임에 추가
data['Predicted Growth'] = predicted_growth

# 결과를 엑셀 파일로 저장
data.to_excel('D:/Data/데이터_완성본_XGBoost.xlsx', index=False)
print("예측된 Growth 값을 엑셀 파일로 저장했습니다.")

# 모델 저장
joblib.dump(model, 'D:/Data/xgboost_model.pkl')
joblib.dump(scaler_X_env, 'D:/Data/scaler_X_env.pkl')
joblib.dump(scaler_y_growth, 'D:/Data/scaler_y_growth.pkl')

print("모델을 파일로 저장했습니다.")
