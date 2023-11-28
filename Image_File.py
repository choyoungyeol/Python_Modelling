import cv2
import numpy as np
import tkinter as tk
from tkinter import Scale, Button, Entry, filedialog

def on_scale_change(event=None):
    lower_color = [hue_var.get(), sat_var.get(), val_var.get()]
    upper_color = [hue_var.get() + hue_range_var.get(), sat_var.get() + sat_range_var.get(), val_var.get() + val_range_var.get()]

    extract_flower_color(image_path, lower_color, upper_color)

def on_save():
    lower_color = [hue_var.get(), sat_var.get(), val_var.get()]
    upper_color = [hue_var.get() + hue_range_var.get(), sat_var.get() + sat_range_var.get(), val_var.get() + val_range_var.get()]

    save_path = filedialog.asksaveasfilename(defaultextension=".jpg", filetypes=[("JPEG files", "*.jpg"), ("All files", "*.*")])

    if save_path:
        save_extracted_flower_color(image_path, lower_color, upper_color, save_path)

def extract_flower_color(image_path, lower_color, upper_color):
    image = cv2.imread(image_path)
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # 색상 범위에 해당하는 부분을 추출합니다.
    mask = cv2.inRange(hsv, np.array(lower_color), np.array(upper_color))

    # 추출된 부분만 남기고 나머지는 검은색으로 만듭니다.
    result = cv2.bitwise_and(image, image, mask=mask)

    cv2.imshow('Original Image', image)
    cv2.imshow('Extracted Flower Color', result)

def save_extracted_flower_color(image_path, lower_color, upper_color, save_path):
    image = cv2.imread(image_path)
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # 색상 범위에 해당하는 부분을 추출합니다.
    mask = cv2.inRange(hsv, np.array(lower_color), np.array(upper_color))

    # 추출된 부분만 남기고 나머지는 검은색으로 만듭니다.
    result = cv2.bitwise_and(image, image, mask=mask)

    # 추출된 이미지를 저장합니다.
    cv2.imwrite(save_path, result)
    print(f"Extracted image saved at {save_path}")

# 이미지 경로를 지정합니다.
image_path = 'D:/Data/flower.jpg'

# Tkinter 창을 생성합니다.
root = tk.Tk()
root.title("Color Range Selector")

# 초기 입력값을 설정합니다.
initial_values = [
    (0, 180),  # Hue
    (0, 255),  # Saturation
    (0, 255),  # Value
]

# 변수들을 생성합니다.
hue_var = tk.IntVar()
sat_var = tk.IntVar()
val_var = tk.IntVar()
hue_range_var = tk.IntVar()
sat_range_var = tk.IntVar()
val_range_var = tk.IntVar()

# 초기값 설정
hue_var.set(initial_values[0][0])
sat_var.set(initial_values[1][0])
val_var.set(initial_values[2][0])
hue_range_var.set(initial_values[0][1] - initial_values[0][0])
sat_range_var.set(initial_values[1][1] - initial_values[1][0])
val_range_var.set(initial_values[2][1] - initial_values[2][0])

# 스크롤바 추가
hue_slider = Scale(root, from_=0, to=180, variable=hue_var, label="Hue", command=on_scale_change, orient=tk.HORIZONTAL)
sat_slider = Scale(root, from_=0, to=255, variable=sat_var, label="Saturation", command=on_scale_change, orient=tk.HORIZONTAL)
val_slider = Scale(root, from_=0, to=255, variable=val_var, label="Value", command=on_scale_change, orient=tk.HORIZONTAL)
hue_range_slider = Scale(root, from_=0, to=180, variable=hue_range_var, label="Hue Range", command=on_scale_change, orient=tk.HORIZONTAL)
sat_range_slider = Scale(root, from_=0, to=255, variable=sat_range_var, label="Saturation Range", command=on_scale_change, orient=tk.HORIZONTAL)
val_range_slider = Scale(root, from_=0, to=255, variable=val_range_var, label="Value Range", command=on_scale_change, orient=tk.HORIZONTAL)

# 스크롤바 배치
hue_slider.pack()
sat_slider.pack()
val_slider.pack()
hue_range_slider.pack()
sat_range_slider.pack()
val_range_slider.pack()

# "Save to File" 버튼 추가
save_button = Button(root, text="Save to File", command=on_save)
save_button.pack()

# 초기 이미지를 표시합니다.
initial_lower_color = [hue_var.get(), sat_var.get(), val_var.get()]
initial_upper_color = [hue_var.get() + hue_range_var.get(), sat_var.get() + sat_range_var.get(), val_var.get() + val_range_var.get()]
extract_flower_color(image_path, initial_lower_color, initial_upper_color)

root.mainloop()
