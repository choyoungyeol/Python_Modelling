import tkinter as tk
import pandas as pd
from math import exp

def calculate():
    result = ""

    if var1.get() == 1:
        try:
            value = df.loc[df['Temp'].notnull(), 'Temp'].iloc[0]
            result_value = 19.071 * (1 - 1.3704 * exp(-0.0571 * value))
            result += "Gross Photosynthetic Rate = {:.2f}\n".format(result_value)
            # Break the loop after finding the first valid result
            result_var.set(result)
            return
        except IndexError:
            result = "Error: Invalid expression\n"

    if var2.get() == 1:
        try:
            value = df.loc[df['CO2'].notnull(), 'CO2'].iloc[0]
            result_value = 19.6385 * value / (401.9447 + value)
            result += "Gross Photosynthetic Rate = {:.2f}\n".format(result_value)
            # Break the loop after finding the first valid result
            result_var.set(result)
            return
        except IndexError:
            result = "Error: Invalid expression\n"

    if var3.get() == 1:
        try:
            value = df.loc[df['PPF'].notnull(), 'PPF'].iloc[0]
            result_value = 18.6884 * value / (338.672 + value)
            result += "Gross Photosynthetic Rate = {:.2f}\n".format(result_value)
            # Break the loop after finding the first valid result
            result_var.set(result)
            return
        except IndexError:
            result = "Error: Invalid expression\n"

    if var4.get() == 1:
        try:
            value = df.loc[df['N'].notnull(), 'N'].iloc[0]
            result_value = 24.747 * (1 + 6.085 * exp(-0.3689 * value))
            result += "Gross Photosynthetic Rate = {:.2f}\n".format(result_value)
            # Break the loop after finding the first valid result
            result_var.set(result)
            return
        except IndexError:
            result = "Error: Invalid expression\n"

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
