import tkinter as tk
import pandas as pd
from math import exp
import matplotlib.pyplot as plt

def calculate():
    result = ""

    selected_columns = []
    if var1.get() == 1:
        selected_columns.append('Temp')
    if var2.get() == 1:
        selected_columns.append('CO2')
    if var3.get() == 1:
        selected_columns.append('PPF')
    if var4.get() == 1:
        selected_columns.append('N')

    for column in selected_columns:
        try:
            values = df.loc[df[column].notnull(), column]
            result_values = []

            if column == 'Temp':
                result_values = 19.071 * (1 - 1.3704 * values.apply(lambda x: exp(-0.0571 * x)))
            elif column == 'CO2':
                result_values = 19.6385 * values / (401.9447 + values)
            elif column == 'PPF':
                result_values = 18.6884 * values / (338.672 + values)
            elif column == 'N':
                result_values = 24.747 * (1 + 6.085 * values.apply(lambda x: exp(-0.3689 * x)))

            result += f"Gross Photosynthetic Rate for {column}:\n"

            # Plotting the values
            plt.plot(values, result_values, label=column)
            plt.xlabel(column)
            plt.ylabel('Gross Photosynthetic Rate')
            plt.title(f"Gross Photosynthetic Rate vs. {column}")
            plt.legend()
            plt.show()

        except IndexError:
            result += f"Error: Invalid expression for {column}\n"

    # Update the result variable
    result_var.set(result)

# Load data from Excel file
df = pd.read_excel('D:/Data/GPR_data.xlsx')

window = tk.Tk()
window.title("Math Calculation")
window.geometry("400x500")

var1 = tk.IntVar()
var2 = tk.IntVar()
var3 = tk.IntVar()
var4 = tk.IntVar()

check1 = tk.Checkbutton(window, text="Temp", variable=var1, font=("Arial", 12))
check1.pack()
check2 = tk.Checkbutton(window, text="CO2", variable=var2, font=("Arial", 12))
check2.pack()
check3 = tk.Checkbutton(window, text="PPF", variable=var3, font=("Arial", 12))
check3.pack()
check4 = tk.Checkbutton(window, text="N", variable=var4, font=("Arial", 12))
check4.pack()

calculate_button = tk.Button(window, text="Calculate", command=calculate, font=("Arial", 12))
calculate_button.pack(pady=10)

result_var = tk.StringVar()
result_label = tk.Label(window, textvariable=result_var, font=("Arial", 12))
result_label.pack()

window.mainloop()
