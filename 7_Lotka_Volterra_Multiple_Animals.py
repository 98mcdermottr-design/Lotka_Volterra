import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint

t = np.linspace(0, 50, 1000)
# arguments in linspace are start, end, and number of intervals in between, so the above will look like
# [0, 0.05, 0.10, .15, ....., 50]
alpha = []
beta = []
K = []
x0 = []
a = "YES"
i = 1
while a == "YES":
    alpha.append(float(input(f"Please enter the birth rate parameter for Prey number {i: .0f}: ")))
    beta.append(float(input(f"Please enter the predation rate parameter for Prey number {i: .0f}: ")))
    K.append(float(input(f"Please enter the maximum population for Prey number {i: .0f}: ")))
    x0.append(float(input(f"Please enter the starting population for Prey number {i: .0f}: ")))
    i = i + 1
    a = input("Do you have another prey to add to analysis (YES/NO): ").strip().upper()
alpha = np.array(alpha)
beta = np.array(beta)
K = np.array(K)
x0 = np.array(x0)
gamma = []
delta = []
y0 = []
g = "YES"
i = 1
while g == "YES":
    gamma.append(float(input(f"Please enter the death rate parameter for Predator number {i: .0f}: ")))
    delta.append(float(input(f"Please enter the birth rate parameter for Predator number {i: .0f}: ")))
    y0.append(float(input(f"Please enter the starting population for Predator number {i: .0f}: ")))
    i = i + 1
    g = input("Do you have another predator to add to analysis (YES/NO): ").strip().upper()
gamma = np.array(gamma)
delta = np.array(delta)
y0 = np.array(y0)
# creates a blank list for each of the paramters, then runs a loop to get the user input for each of the parameters
# once all of these parameters are added to the list, it then converts the paramter lists into arrays

params = [alpha, beta, delta, gamma, K]
variables = np.concatenate([x0, y0])
#parameters for the lotka-volterra model

def sim(variables, t, params):
    alpha = params[0]
    beta = params[1]
    delta = params[2]
    gamma = params[3]
    K = params[4]
    global n_prey
    n_prey = len(alpha)
    global n_pred
    n_pred = len(gamma)
    x = variables[:n_prey]
    # set your initial population sizes for each species
    y = variables[n_prey:]
    # define all of your variables again in the function
    dxdt = np.zeros(n_prey)
    for i in range(n_prey):
        dxdt[i] = alpha[i] * x[i] * (1 - x[i] / K[i]) - beta[i] * x[i] * np.sum(y)
    # this is a loop that ca;culates the rate of change of the prey population for each prey inputted
    # note we don't use a predation rate specific to each predator, just specific to each prey, so you can just sum the predator populations
    dydt = np.zeros(n_pred)
    for j in range(n_pred):
        dydt[j] = -gamma[j] * y[j] + delta[j] * y[j] * np.sum(x)
    # Lotka-Volaterra equations
    return np.concatenate([dxdt, dydt])

y = odeint(sim, variables, t, args = (params, ))
# odeint means ODE integrator, it finds the integral of the derivative function that you have defined above
# then has the starting value, and it approximates the prey/predator population at each time steps
# the output is a txa matrix, where t is each time step and a is the number of animals that you are analysing
# you need to outline the parameters again for odeint to use, which is why they're included above
# run odeint with the steady state populations
# note odeint requires a 1D array input for the starting populations and a 1D array output for the rates of change, for the integration

plt.figure(figsize = (10,6))
plt.subplot(2, 1, 1)
for i in range(n_prey):
    plt.plot(t, y[:,i], label = f"Prey Population {i + 1}")
plt.title("Prey Population")
plt.ylabel("Population")
plt.legend()
plt.subplot(2, 1, 2)
for j in range(n_pred):
    plt.plot(t, y[:,n_prey + j], label = f"Predator Population {j + 1}")
plt.title("Predator Population")
plt.xlabel("Time")
plt.ylabel("Population")
plt.legend()
plt.show()
# plot the results
