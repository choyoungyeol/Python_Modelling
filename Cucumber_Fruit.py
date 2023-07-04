import numpy as np
import matplotlib.pyplot as plt

# 데이터 준비
x = np.arange(1, 15)  # 개화 후 날짜
y1 = 35.89 / (1 + np.exp(-((x - 8.446) / 3.794)))   # 생육 데이터 (임의로 생성)
y2 = 19.44 / (1 + np.exp(-((x - 11.09) / 5.152))) # 생육 데이터 (임의로 생성)
y3 = 0.752 * y1 * y2**2 / (4 * np.pi)
y4 = 0.081 * y3

# 그래프 초기화
fig, (ax1, ax3) = plt.subplots(nrows=2, figsize=(8, 8))

# y1, y2 그래프
ax1.plot(x, y1, label='Length', color='steelblue')
ax1.set_ylim(0, max(y1))
ax1.set_xlabel('Days after flowering of the fruit', fontsize=12)
ax1.set_ylabel('Length (cm)', fontsize=12)

ax2 = ax1.twinx()
ax2.plot(x, y2, 'r', label='Circumference')
ax2.set_ylim(0, max(y2))
ax2.set_ylabel('Circumference (cm)', fontsize=12)

# y3, y4 그래프
ax3.plot(x, y3, 'g', label='Fresh weight', linewidth=2)
ax3.set_ylim(0, max(y3))
ax3.set_xlabel('Days after flowering of the fruit', fontsize=12)
ax3.set_ylabel('Fresh weight (g)', fontsize=12)

ax4 = ax3.twinx()
ax4.plot(x, y4, 'm', label='Dry weight', linewidth=2)
ax4.set_ylim(0, max(y4))
ax4.set_ylabel('Dry weight (g)', fontsize=12)

# 범례 표시
lines1 = ax1.get_lines() + ax2.get_lines()
lines2 = ax3.get_lines() + ax4.get_lines()
labels1 = [line.get_label() for line in lines1]
labels2 = [line.get_label() for line in lines2]

ax1.legend(lines1, labels1, loc='upper left', fontsize=10)
ax3.legend(lines2, labels2, loc='upper left', fontsize=10)

# 그래프 간격 조정
fig.tight_layout()

# 배경 그리드 제거
ax1.grid(False)
ax2.grid(False)
ax3.grid(False)
ax4.grid(False)

# 축 레이블 크기 조정
ax1.tick_params(labelsize=10)
ax2.tick_params(labelsize=10)
ax3.tick_params(labelsize=10)
ax4.tick_params(labelsize=10)

plt.show()
