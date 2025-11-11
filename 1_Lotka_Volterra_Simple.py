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

y = odeint(sim, variables, t, args = (params, ))
# odeint means ODE integrator, it finds the integral of the derivative function that you have defined above
# then has the starting value, and it approximates the prey/predator population at each time steps
# the output is a txa matrix, where t is each time step and a is the number of animals that you are analysing
# you need to outline the parameters again for odeint to use, which is why they're included above

plt.figure(figsize = (10,6))
plt.subplot(2, 1, 1)
plt.plot(t, y[:,0], color = "blue", label = "Prey Population")
plt.title("Prey Population")
plt.ylabel("Population")
plt.subplot(2, 1, 2)
plt.plot(t, y[:,1], color = "red", label = "Predator Population")
plt.title("Predator Population")
plt.xlabel("Time")
plt.ylabel("Population")
plt.show()

plt.show()
# plot the results
