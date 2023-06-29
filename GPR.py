import tkinter as tk
import pandas as pd
from math import exp
import matplotlib.pyplot as plt
import numpy as np


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

    if len(selected_columns) >= 1:
        try:
            result += "Gross Photosynthetic Rates:\n"

            values = df.loc[df[selected_columns].notnull().all(axis=1), selected_columns]

            if len(values) == 0:
                result = "Error: No valid data points for calculation\n"
            else:
                result_values = calculate_formula(values, selected_columns)

                if len(result_values) > 0:
                    # Plotting the values
                    if None not in result_values:
                        if len(selected_columns) > 1:
                            plt.scatter(np.arange(len(result_values)), result_values, label="Calculated")
                            result += f"Calculated: Based on {', '.join(selected_columns)}\n"
                        else:
                            plt.scatter(np.arange(len(result_values)), result_values, label="Calculated")
                            result += f"{selected_columns[0]}: Calculated\n"

                        plt.xlabel('Counts')
                        plt.ylabel('Gross Photosynthetic Rate')
                        plt.title('Gross Photosynthetic Rate vs. Counts')
                        plt.legend()
                        plt.show()
                    else:
                        result = "Error: No calculated values\n"

                else:
                    result = "Error: No calculated values\n"

        except ValueError as e:
            result = str(e)  # Update the result with the error message

    else:
        result = "Error: Select at least one column for calculation\n"

    # Update the result variable
    result_var.set(result)


def calculate_formula(values, columns):
    result_values = []

    for _, row in values.iterrows():
        result = None
        calculated = False  # Variable to check if any calculation is performed for a row

        if 'Temp' in columns:
            result = 19.071 * (1 - 1.3704 * exp(-0.0571 * row['Temp']))
            calculated = True
        if 'CO2' in columns:
            result = 19.6385 * row['CO2'] / (401.9447 + row['CO2'])
            calculated = True
        if 'PPF' in columns:
            result = 18.6884 * row['PPF'] / (338.672 + row['PPF'])
            calculated = True
        if 'N' in columns:
            result = 24.747 * (1 + 6.085 * exp(-0.3689 * row['N']))
            calculated = True

        # Additional calculation formulas
        if len(columns) > 1:
            if 'Temp' in columns and 'CO2' in columns and 'PPF' in columns and 'N' in columns:
                result += 56.046 * (1 - 4.1942 * exp(-0.226 * row['Temp'])) * (row['PPF'] / (253.993 + row['PPF'])) * (
                    row['CO2'] / (373.663 + row['CO2'])) * (1 / (1 + 5.345 * exp(-0.423 * row['N'])))
                calculated = True
            elif 'Temp' in columns and 'CO2' in columns and 'PPF' in columns:
                result += 38.878 * (1 - 4.1942 * exp(-0.226 * row['Temp'])) * (row['PPF'] / (253.993 + row['PPF'])) * (
                    row['CO2'] / (373.663 + row['CO2']))
                calculated = True
            elif 'Temp' in columns and 'CO2' in columns:
                result += 20.214 * (1 - 9.081 * exp(-0.3211 * row['Temp'])) * (row['CO2'] / (363.3 + row['CO2']))
                calculated = True
            elif 'Temp' in columns and 'PPF' in columns:
                result += 4.1485 * (1 - 409673 * exp(-0.4552 * row['Temp'])) * (
                    1 - 0.8493 * exp(-0.0027 * row['PPF']))
                calculated = True
            elif 'CO2' in columns and 'PPF' in columns:
                result += 50.149 * row['CO2'] * (501.437 + row['CO2']) * (row['PPF'] * (316.114 + row['PPF']))
                calculated = True
            else:
                result_values.append(None)
        if not calculated:
            result_values.append(None)
        else:
            result_values.append(result)

    return result_values


# 예시 데이터 프레임
df = pd.read_excel('D:/Data/GPR_data.xlsx')

# GUI 생성
root = tk.Tk()
root.title("Calculate")

# 체크박스 생성
var1 = tk.IntVar()
check1 = tk.Checkbutton(root, text="Temp", variable=var1)
check1.pack()

var2 = tk.IntVar()
check2 = tk.Checkbutton(root, text="CO2", variable=var2)
check2.pack()

var3 = tk.IntVar()
check3 = tk.Checkbutton(root, text="PPF", variable=var3)
check3.pack()

var4 = tk.IntVar()
check4 = tk.Checkbutton(root, text="N", variable=var4)
check4.pack()

# 계산 버튼 생성
calculate_button = tk.Button(root, text="Calculate", command=calculate)
calculate_button.pack()

# 결과 텍스트 상자 생성
result_var = tk.StringVar()
result_label = tk.Label(root, textvariable=result_var)
result_label.pack()

root.mainloop()
