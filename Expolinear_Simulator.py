import tkinter as tk
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

# Graph data generation
x = np.linspace(0, 60, 100)

def simulate_graph(cm, rm, tb):
    # Graph simulation
    y = cm / rm * np.log(1 + np.exp(rm * (x - tb)))
    return y

def update_graph():
    # Update the graph
    cm = cm_var.get()
    rm = rm_var.get()
    tb = tb_var.get()
    y = simulate_graph(cm, rm, tb)

    ax.clear()
    ax.plot(x, y)
    ax.set_xlabel('Days after transplant (DAT)')
    ax.set_ylabel('Dry weight (g/m2)')
    ax.set_title('Graph')
    ax.set_ylim(0, np.max(y)*1.1)  # Set y-axis limit to 0 and max value of y
    ax.grid(True)
    canvas.draw()

def reset_values():
    # Reset input values
    cm_var.set(0.2)
    rm_var.set(0.03)
    tb_var.set(10)
    y_var.set(8)
    result_var.set("")

# Create the window
window = tk.Tk()
window.title("Graph Simulation")
window.geometry("600x900")
window.configure(bg="#F0F0F0")

# Initialize the graph
fig, ax = plt.subplots()
y = simulate_graph(0.2, 0.03, 10)
line, = ax.plot(x, y)
ax.set_xlabel('Days after transplant (DAT)')
ax.set_ylabel('Dry weight (g/m2)')
ax.set_title('Graph')
ax.set_ylim(0, np.max(y)*1.1)  # Set y-axis limit to 0 and max value of y
ax.grid(True)

canvas = FigureCanvasTkAgg(fig, master=window)
canvas.get_tk_widget().pack()

# Crop growth rate input field
cm_label = tk.Label(window, text="Crop growth rate (g/g/d)", bg="#F0F0F0", font=("Arial", 12))
cm_label.pack()

cm_var = tk.DoubleVar(value=0.2)
cm_scale = tk.Scale(window, variable=cm_var, from_=0.1, to=1, resolution=0.1, orient=tk.HORIZONTAL, length=200)
cm_scale.pack()

# Relative growth rate input field
rm_label = tk.Label(window, text="Relative growth rate (g/g/d)", bg="#F0F0F0", font=("Arial", 12))
rm_label.pack()

rm_var = tk.DoubleVar(value=0.03)
rm_scale = tk.Scale(window, variable=rm_var, from_=0.01, to=0.1, resolution=0.01, orient=tk.HORIZONTAL, length=200)
rm_scale.pack()

# tb input field
tb_label = tk.Label(window, text="tb (d)", bg="#F0F0F0", font=("Arial", 12))
tb_label.pack()

tb_var = tk.DoubleVar(value=10)
tb_scale = tk.Scale(window, variable=tb_var, from_=1, to=30, orient=tk.HORIZONTAL, length=200)
tb_scale.pack()

# Weight input field
y_label = tk.Label(window, text="Harvest weight (g/m2)", bg="#F0F0F0", font=("Arial", 12))
y_label.pack()

y_var = tk.DoubleVar(value=8)
y_scale = tk.Scale(window, variable=y_var, from_=1, to=20, orient=tk.HORIZONTAL, length=200)
y_scale.pack()

# Result text display
result_var = tk.StringVar()
result_label = tk.Label(window, text="", font=("Arial", 12))
result_label.pack()


# Button frame
button_frame = tk.Frame(window, bg="#F0F0F0")
button_frame.pack()

# Buttons
is_running = True  # Flag to indicate if the graph animation is running

def stop_animation():
    global is_running
    is_running = False

def animate_graph():
    global is_running

    # 결과 레이블 초기화
    result_label.config(text="")

    cm = cm_var.get()
    rm = rm_var.get()
    tb = tb_var.get()
    y = simulate_graph(cm, rm, tb)

    ax.clear()
    ax.set_xlabel('Days after transplant (DAT)')
    ax.set_ylabel('Dry weight (g/m2)')
    ax.set_title('Graph')
    ax.set_ylim(0, np.max(y) * 1.1)  # Set y-axis limit to 0 and max value of y
    ax.grid(True)

    is_running = True
    frame = 0
    while frame <= len(y) and y[frame] < y_var.get():
        ax.plot(x[:frame], y[:frame], 'r-')
        canvas.draw()
        frame += 1
        plt.pause(0.1)

        # 결과 레이블 업데이트
        result_label.config(text=f"Days after transplanting (DAT): {x[frame - 1]:.1f}\n"
                                 f"Crop growth rate: {cm}\n"
                                 f"Relative growth rate: {rm}\n"
                                 f"tb: {tb}")

    is_running = False

    # 그래프 초기화
    ax.clear()
    y_init = simulate_graph(cm_var.get(), rm_var.get(), tb_var.get())
    ax.plot(x, y_init)
    ax.set_xlabel('Days after transplant (DAT)')
    ax.set_ylabel('Dry weight (g/m2)')
    ax.set_title('Graph')
    ax.set_ylim(0, np.max(y_init) * 1.1)
    ax.grid(True)
    canvas.draw()

start_button = tk.Button(button_frame, text="Start", command=animate_graph, font=("Arial", 12))
start_button.pack(side=tk.LEFT, padx=5, pady=10)

stop_button = tk.Button(button_frame, text="Stop", command=stop_animation, font=("Arial", 12))
stop_button.pack(side=tk.LEFT, padx=5, pady=10)

reset_button = tk.Button(button_frame, text="Reset", command=reset_values, font=("Arial", 12))
reset_button.pack(side=tk.LEFT, padx=5, pady=10)

# Run the window
window.mainloop()

