import numpy as np
import customtkinter as ctk
from functions import *
from color_simulate_functions import *
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.patches import Rectangle
from solver import dimensionless_system
from scipy.integrate import solve_ivp
from tkinter import messagebox as mb, Canvas

# ctk.set_appearance_mode("dark")
# ctk.set_default_color_theme("blue")

root = ctk.CTk()
root.geometry("1000x800")
root.configure(fg_color="#1e2124")

root.attributes("-fullscreen", True)

for i in range(1, 15):
    root.grid_rowconfigure(i, weight=1)

label = ctk.CTkLabel(root, text="Initial Concentrations", font=("Roboto", 20), text_color="#F5F5F5")
label.grid(row=1, column=1, padx=20, pady=0)

e1 = createEntry(root, "[BrO3-]", 2, 1, entryText="0.2")
e2 = createEntry(root, "[HBrO2]", 3, 1, entryText="0.001")
e3 = createEntry(root, "[Br-]", 4, 1, entryText="0.001")
e4 = createEntry(root, "[Fe3+]", 5, 1, entryText="0.04")

label = ctk.CTkLabel(root, text="Rate Constants", font=("Roboto", 20), text_color="#F5F5F5")
label.grid(row=6, column=1, padx=0)

k1 = createEntry(root, "k1", 7, 1, entryText="2")
k2 = createEntry(root, "k2", 8, 1, entryText="300000")
k3 = createEntry(root, "k3", 9, 1, entryText="66")
k4 = createEntry(root, "k4", 10, 1, entryText="3000")
k5 = createEntry(root, "k5", 11, 1, entryText="0.06")

methods = ["RK23", "LSODA"]
currMethod = methods[0]

defaultParameterSets = ["Option 1", "Option 2", "Option 3", "Option 4"]
currParameterSet = defaultParameterSets[0]

def setMethod(method):
    currMethod = method

def setParameterSet(parameterSet):
    currParameterSet = parameterSet

    if parameterSet == "Option 1":
        k1[1].configure(textvariable=ctk.StringVar(value="2"))
        k2[1].configure(textvariable=ctk.StringVar(value="300000"))
        k3[1].configure(textvariable=ctk.StringVar(value="66"))
        k4[1].configure(textvariable=ctk.StringVar(value="3000"))
        k5[1].configure(textvariable=ctk.StringVar(value="0.06"))
    if parameterSet == "Option 2":
        k1[1].configure(textvariable=ctk.StringVar(value="1.28"))
        k2[1].configure(textvariable=ctk.StringVar(value="300000"))
        k3[1].configure(textvariable=ctk.StringVar(value="33.6"))
        k4[1].configure(textvariable=ctk.StringVar(value="3000"))
        k5[1].configure(textvariable=ctk.StringVar(value="1"))
    if parameterSet == "Option 3":
        k1[1].configure(textvariable=ctk.StringVar(value="2"))
        k2[1].configure(textvariable=ctk.StringVar(value="300000"))
        k3[1].configure(textvariable=ctk.StringVar(value="42"))
        k4[1].configure(textvariable=ctk.StringVar(value="3000"))
        k5[1].configure(textvariable=ctk.StringVar(value="1"))
    if parameterSet == "Option 4":
        k1[1].configure(textvariable=ctk.StringVar(value="2"))
        k2[1].configure(textvariable=ctk.StringVar(value="2000000000"))
        k3[1].configure(textvariable=ctk.StringVar(value="10000"))
        k4[1].configure(textvariable=ctk.StringVar(value="40000000"))
        k5[1].configure(textvariable=ctk.StringVar(value="0.6"))

methodDropdown = ctk.CTkComboBox(root, values=methods, command=setMethod)
methodDropdown.grid(row=12, column=1)

parametersDropdown = ctk.CTkComboBox(root, values=defaultParameterSets, command=setParameterSet)
parametersDropdown.grid(row=12, column=2)

root.grid_columnconfigure(3, weight=1)
root.grid_columnconfigure(4, weight=1)
root.grid_columnconfigure(5, weight=1)

plot_frame = ctk.CTkFrame(root, fg_color='')
plot_frame.grid(row=1, column=3, padx=20, pady=0, sticky="nsew", rowspan=6, columnspan=3)

plot_frame2 = ctk.CTkFrame(root, fg_color='')
plot_frame2.grid(row=7, column=3, padx=20, pady=0, sticky="nsew", rowspan=6,  columnspan=3)

figure = plt.Figure(figsize=(8, 3))
subplot = figure.add_subplot(111)
canvas = FigureCanvasTkAgg(figure, plot_frame)

figure2 = plt.Figure(figsize=(8, 3))
subplot2 = figure2.add_subplot(111)
canvas2 = FigureCanvasTkAgg(figure2, plot_frame2)

def plotGraph():
    try:
        solution = solve_ivp(dimensionless_system, (0, 50), [float(e2[1].get()), float(e3[1].get()), float(e4[1].get())], args=(float(k1[1].get()), float(k2[1].get()), float(k3[1].get()), float(k4[1].get()), float(k5[1].get()), float(e1[1].get()), 0.75), method=currMethod, t_eval=np.linspace(0, 50, 100000))
        # print(float(e1[1].get()) >= 0 and float(e2[1].get()) >= 0 and float(e3[1].get()) >= 0 and float(e4[1].get()) >= 0 and float(k1[1].get()) >= 0 and float(k2[1].get()) >= 0 and float(k3[1].get()) >= 0 and float(k4[1].get()) >= 0 and float(k5[1].get()) >= 0)

        subplot.clear()
        subplot2.clear()
        subplot.plot(solution.t, np.log10(solution.y[0]), label='log10([HBrO2])', color='blue')
        subplot.plot(solution.t, np.log10(solution.y[1]), label='log10([Br-])', color='green')
        subplot.plot(solution.t, np.log10(solution.y[2]), label='log10([Fe3+])', color='red')
        subplot.set_xlabel('Time')
        subplot.set_ylabel('log10(Concentration)')
        subplot.set_xlim(0, max(solution.t))
        subplot.legend()

        mat_color_over_time = color_over_time_fxn(solution)
        plot_rgb_line_on_subplot(subplot2, solution.t, mat_color_over_time)

        canvas.draw()
        canvas.get_tk_widget().pack(expand=True, fill="both")

        canvas2.draw()
        canvas2.get_tk_widget().pack(expand=True, fill="both")
    except ValueError:
        mb.showerror(title = "Invalid Input", message = "Please enter a numeric value for all fields.")
    except AssertionError:
        mb.showerror(title = "Invalid Input", message = "Please enter a positive number.")

storeInitialValuesButton = ctk.CTkButton(root, text="Calculate", command=plotGraph)
storeInitialValuesButton.grid(row=13, column=1, pady=0)

root.mainloop()
