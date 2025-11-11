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

K = float(input("Please enter the maximum for your Prey population: "))
# introduction of carrying capacity, without the possible growth of the prey population is technically infinity

params = [alpha, beta, delta, gamma, K]
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
    K = params[4]
    # define all of your variables again in the function
    dxdt = (alpha * x * (1 - (x / K))) - (beta * x * y)
    # introduction of carrying capacity into the rate of change of the prey population (K)
    # alpha is the birth rate and x is the prey population, so as x approaches the carrying capacity K
    # then the growth of the prey population will slow, and if x reaches the carrying capacity K,
    # whereby x = K, then the birth rate of the prey population will go to 0 as,
    # alpha * x * (1 - (x / x)) = alpha * x * (1 - 1) = alpha * x * 0 = 0

    dydt = (-gamma * y) + (delta * x * y)
    # Lotka-Volaterra equations
    return dxdt, dydt

y = odeint(sim, variables, t, args = (params, ))
# odeint means ODE integrator, it finds the integral of the derivative function that you have defined above
# then has the starting value, and it approximates the prey/predator population at each time steps
# the output is a txa matrix, where t is each time step and a is the number of animals that you are analysing
# you need to outline the parameters again for odeint to use, which is why they're included above

def SS(alpha, beta, delta, gamma, K):
    y0_SS = (alpha / beta) * (1 - (gamma / (delta * K)))
    # with the introduction of the carrying capacity, the steady state for the predator population changes
    x0_SS = gamma / delta
    variables_SS = [x0_SS, y0_SS]
    return variables_SS
# steady state occurs when the derivative functions are set to 0
# so if we find x and y with the derivative functions set to 0, then we find the steady state populations
variables_SS = SS(alpha, beta, delta, gamma, K)
# steady state occurs when the derivative functions are set to 0
# so if we find x and y with the derivative functions set to 0, then we find the steady state populations

y_SS = odeint(sim, variables_SS, t, args = (params, ))
# run odeint with the steady state populations

plt.figure(figsize = (10,6))
plt.subplot(2, 1, 1)
plt.plot(t, y[:,0], color = "blue", label = "Prey Population")
plt.plot(t, y_SS[:, 0], linestyle = "--", color = "grey", label = "Prey Steady State")
plt.title("Prey Population")
plt.ylabel("Population")
plt.subplot(2, 1, 2)
plt.plot(t, y[:,1], color = "red", label = "Predator Population")
plt.plot(t, y_SS[:, 1], linestyle = "--", color = "grey", label = "Predator Steady State")
plt.title("Predator Population")
plt.xlabel("Time")
plt.ylabel("Population")
plt.show()
# plot the results
