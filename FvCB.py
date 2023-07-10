import pandas as pd
import numpy as np
import math
import matplotlib.pyplot as plt
from datetime import datetime

def calculate_photosynthesis(T, Ci, PPFD):
    # 모델에 필요한 매개 변수 설정
    phi = 0.8
    Kc25 = 30.0
    Ko25 = 300.0
    O = 210.0
    Gamma = 0.0
    Rd25 = 1.5
    Q10 = 2.0
    T_ref = 25.0
    S_J = 65.0

    # 온도 보정
    Q10_value = Q10 ** ((T - T_ref) / 10.0)

    # Rubisco 활성화 상태 계산
    Kc = Kc25 * Q10_value
    Ko = Ko25 * Q10_value
    Rd = Rd25 * Q10_value

    # Jmax 계산 모델식
    Jmax = 25.0 * Q10_value ** ((T - 25.0) / 10.0)

    # RuBP 재생 속도 계산
    J = Jmax * (1 - math.exp(-phi * PPFD / Jmax)) * (math.exp(S_J * T / T_ref) / math.exp(S_J * T_ref / T_ref))

    # 탄산화 속도와 산화 속도 계산
    Vcmax = J / 2.0
    f_J = J / (J + 4.0)
    f_Ci = (Ci - Gamma) / (Ci + Kc * (1 + O / Ko) - Gamma)

    # 광합성 속도 계산
    A = Vcmax * f_J * f_Ci - Rd

    return A

# 엑셀 파일에서 데이터 읽어오기
df = pd.read_excel('D:/Data/Paprika_Input.xlsx')
temperatures = df['Temp'].tolist()
CO2_concentrations = df['CO2'].tolist()
PPFD_values = df['PAR'].tolist()
dates = df['Date'].tolist()

# 날짜를 datetime 형식으로 변환
dates = [datetime.strptime(str(date), "%Y-%m-%d %H:%M:%S") for date in dates]

# 광합성 예측 결과 계산
photosynthesis_rates = []
cumulative_photosynthesis = 0.0  # 누적 광합성량
cumulative_photosynthesis_list = []  # 누적 광합성량 리스트
for i in range(len(temperatures)):
    T = temperatures[i]
    Ci = CO2_concentrations[i]
    PPFD = PPFD_values[i]
    photosynthesis_rate = calculate_photosynthesis(T, Ci, PPFD)
    cumulative_photosynthesis += photosynthesis_rate
    photosynthesis_rates.append(photosynthesis_rate)
    cumulative_photosynthesis_list.append(cumulative_photosynthesis)

# 예측 결과를 엑셀 파일로 저장
df['Photosynthesis Rate'] = photosynthesis_rates
df['Cumulative Photosynthesis'] = cumulative_photosynthesis_list
df.to_excel('D:/Data/output.xlsx', index=False)

# 날짜를 x축으로 하는 그래프로 시각화
plt.plot(dates, photosynthesis_rates, label='Photosynthesis Rate')
plt.plot(dates, cumulative_photosynthesis_list, label='Cumulative Photosynthesis')
plt.xlabel('Date')
plt.ylabel('Photosynthesis')
plt.title('Photosynthesis Rate and Cumulative Photosynthesis over Time')
plt.xticks(rotation=45)
plt.legend()
plt.tight_layout()
plt.show()
