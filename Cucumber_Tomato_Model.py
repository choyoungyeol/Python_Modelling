import tkinter as tk
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import random

def simulate_growth(selected_crop):
    if selected_crop == "Cucumber":
        leaf_length_data = [5, 6, 7, 8, 9, 10]  # 오이 엽장 데이터 (임의의 값)
        leaf_width_data = [2, 2.5, 3, 3.5, 4, 4.5]  # 오이 엽폭 데이터 (임의의 값)
        plant_height_data = [1, 1.5, 2.3, 3.5, 4.8, 6.1]

        leaf_area_data = [-30 + 0.85 * length * width for length, width in zip(leaf_length_data, leaf_width_data)]
        fresh_weight_data = [-4.72 + 0.03 * length * width for length, width in zip(leaf_length_data, leaf_width_data)]
        dry_weight_data = [-0.581 + 0.003 * length * width for length, width in zip(leaf_length_data, leaf_width_data)]

    elif selected_crop == "Tomato":
        leaf_length_data = [4, 5, 6, 7, 8, 9]  # 토마토 초장 데이터 (임의의 값)
        leaf_width_data = [3, 3.5, 4, 4.5, 5, 5.5]  # 토마토 엽폭 데이터 (임의의 값)
        plant_height_data = [1, 1.2, 1.3, 1.5, 1.8, 2.1]

        leaf_area_data = [-398 + 1.12 * height * width for height, width in zip(plant_height_data, leaf_width_data)]
        fresh_weight_data = [-16.42 + 0.02 * height ** 2 for height in plant_height_data]
        dry_weight_data = [-2.492 + 0.002 * height ** 2 for height in plant_height_data]
    else:
        print("Select Crop ?")
        return

    # 그래프 생성
    plt.figure(figsize=(10, 6))
    plt.subplot(2, 2, 1)
    plt.plot(leaf_length_data, leaf_area_data, marker='o')
    plt.xlabel("Leaf length")
    plt.ylabel("Leaf area")
    plt.title("Leaf Area")

    plt.subplot(2, 2, 2)
    plt.plot(leaf_length_data, fresh_weight_data, marker='o')
    plt.xlabel("Leaf length")
    plt.ylabel("Fresh weight")
    plt.title("Fresh weight")

    plt.subplot(2, 2, 3)
    plt.plot(leaf_length_data, dry_weight_data, marker='o')
    plt.xlabel("Leaf length")
    plt.ylabel("Dry weight")
    plt.title("Dry Weight")

    plt.tight_layout()
    plt.show()

def choose_crop():
    def select_crop():
        selected_crop = var.get()
        window.destroy()
        simulate_growth(selected_crop)

    window = tk.Tk()
    window.title("Select Crop")
    var = tk.StringVar()

    label = tk.Label(window, text="Select Crop ?:")
    label.pack()

    crops = ["Cucumber", "Tomato"]
    for crop in crops:
        rb = tk.Radiobutton(window, text=crop, variable=var, value=crop)
        rb.pack(anchor=tk.W)

    button = tk.Button(window, text="선택", command=select_crop)
    button.pack()

    window.mainloop()

choose_crop()
