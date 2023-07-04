import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# 데이터 준비
x = np.arange(1, 15)  # 개화 후 날짜
y1 = 35.89 / (1 + np.exp(-((x - 8.446) / 3.794)))   # 생육 데이터 (임의로 생성)
y2 = 19.44 / (1 + np.exp(-((x - 11.09) / 5.152))) # 생육 데이터 (임의로 생성)
y3 = 0.752 * y1 * y2**2 / (4 * np.pi)
y4 = 0.081 * y3

# 그래프 초기화
fig, (ax1, ax2, ax3, ax4) = plt.subplots(nrows=4, figsize=(8, 12))

# 축 범위 설정
ax1.set_xlim(1, 15)
ax1.set_ylim(0, max(y1))
ax2.set_xlim(1, 15)
ax2.set_ylim(0, max(y2))
ax3.set_xlim(1, 15)
ax3.set_ylim(0, max(y3))
ax4.set_xlim(1, 15)
ax4.set_ylim(0, max(y4))

# 축 레이블 설정
ax1.set_xlabel('Days after flowering of the fruit', fontsize=12)
ax1.set_ylabel('Length (cm)', fontsize=12)
ax2.set_ylabel('Circumference (cm)', fontsize=12)
ax3.set_xlabel('Days after flowering of the fruit', fontsize=12)
ax3.set_ylabel('Fresh weight (g)', fontsize=12)
ax4.set_ylabel('Dry weight (g)', fontsize=12)

# 그래프 객체 초기화
line1, = ax1.plot([], [], label='Length', color='steelblue')
line2, = ax2.plot([], [], 'r', label='Circumference')
line3, = ax3.plot([], [], 'g', label='Fresh weight', linewidth=2)
line4, = ax4.plot([], [], 'm', label='Dry weight', linewidth=2)
lines = [line1, line2, line3, line4]

# 범례 표시
ax1.legend(loc='upper left', fontsize=10)
ax2.legend(loc='upper left', fontsize=10)
ax3.legend(loc='upper left', fontsize=10)
ax4.legend(loc='upper left', fontsize=10)

# 그래프 갱신 함수
def update_graph(frame):
    if frame >= len(x):
        return

    line1.set_data(x[:frame+1], y1[:frame+1])
    line2.set_data(x[:frame+1], y2[:frame+1])
    line3.set_data(x[:frame+1], y3[:frame+1])
    line4.set_data(x[:frame+1], y4[:frame+1])

# 애니메이션 생성
ani = FuncAnimation(fig, update_graph, frames=len(x)+1, interval=500, blit=False)

plt.show()
