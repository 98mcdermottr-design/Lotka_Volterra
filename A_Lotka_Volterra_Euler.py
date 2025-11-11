import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint

t = np.linspace(0, 50, 1000)
# arguments in linspace are start, end, and number of intervals in between, so the above will look like
# [0, 0.05, 0.10, .15, ....., 50]

alpha = float(input("Please enter the birth rate parameter for your Prey population: "))
gamma = float(input("Please enter the death rate parameter for your Predator population: "))
beta = float(input("Please enter the predation rate parmeter for your Prey population: "))
delta = float(input("Please enter the birth rate parmeter for your Predator population: "))
# enter in your parameters for the Lotka_Volterra model

params = [alpha, beta, delta, gamma]
#parameters for the lotka-volterra model

x0 = float(input("What is the starting population for your Prey? "))
y0 = float(input("What is the starting population for your Predator? "))
variables = [x0, y0]
# starting populations for your prey and you predators

def sim(variables, t, params):
    x = variables[0]
    y = variables[1]
    alpha = params[0]
    beta = params[1]
    delta = params[2]
    gamma = params[3]
    # define all of your variables again in the function
    dxdt = (alpha * x) - (beta * x * y)
    dydt = (-gamma * y) + (delta * x * y)
    # Lotka-Volaterra equations
    return dxdt, dydt

# Initialize arrays
x_vals = np.zeros(len(t))
y_vals = np.zeros(len(t))
x_vals[0] = x0
y_vals[0] = y0

dt = t[1] - t[0]  # time step size

# Euler integration loop
for i in range(1, len(t)):
    dxdt, dydt = sim([x_vals[i-1], y_vals[i-1]], t[i-1], params)
    x_vals[i] = x_vals[i-1] + dxdt * dt
    y_vals[i] = y_vals[i-1] + dydt * dt

plt.figure(figsize = (10,6))
plt.subplot(2, 1, 1)
plt.plot(t, x_vals, color = "blue", label = "Prey Population")
plt.title("Prey Population")
plt.ylabel("Population")
plt.subplot(2, 1, 2)
plt.plot(t, y_vals, color = "red", label = "Predator Population")
plt.title("Predator Population")
plt.xlabel("Time")
plt.ylabel("Population")
plt.show()

plt.show()
# plot the results
