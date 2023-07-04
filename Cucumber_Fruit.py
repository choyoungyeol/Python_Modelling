import numpy as np
import matplotlib.pyplot as plt

# 데이터 준비
x = np.arange(1, 30)  # 개화 후 날짜
y1 = 35.89 * (1 + np.exp(-((x - 8.446) / 3.794)))  # 생육 데이터 (임의로 생성)
y2 = 19.44 * (1 + np.exp(-((x - 11.09) / 5.152)))  # 생육 데이터 (임의로 생성)
y3 = 0.752 * y1 * y2**2 / (4 * np.pi)
y4 = 0.081 * y3

# 그래프 초기화
fig, ax1 = plt.subplots()
ax1.plot(x, y1, label='Length')
ax1.set_xlim(1, len(x))
ax1.set_ylim(0, max(max(y1), max(y2)))
ax1.set_xlabel('Days after flowering of the fruit')
ax1.set_ylabel('Length (cm)')

# 제2 y축 그래프 설정
ax2 = ax1.twinx()
ax2.plot(x, y2, 'r', label='Circumference')
ax2.set_ylim(0, max(y2))
ax2.set_ylabel('Circumference (cm)')

# 범례 표시
lines = [ax1.get_lines()[0], ax2.get_lines()[0]]
ax1.legend(lines, [line.get_label() for line in lines])

plt.show()
