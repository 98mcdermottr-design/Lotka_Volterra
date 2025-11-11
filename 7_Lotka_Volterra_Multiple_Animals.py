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
# enter in your parameters for the Lotka_Volterra model

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
    y = variables[n_prey:]
    # define all of your variables again in the function
    dxdt = np.zeros(n_prey)
    for i in range(n_prey):
        dxdt[i] = alpha[i] * x[i] * (1 - x[i] / K[i]) - beta[i] * x[i] * np.sum(y)
    # introduction of carrying capacity into the rate of change of the prey population (K)
    # alpha is the birth rate and x is the prey population, so as x approaches the carrying capacity K
    # then the growth of the prey population will slow, and if x reaches the carrying capacity K,
    # whereby x = K, then the birth rate of the prey population will go to 0 as,
    # alpha * x * (1 - (x / x)) = alpha * x * (1 - 1) = alpha * x * 0 = 0
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
