import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint

import pandas as pd
from scipy.optimize import least_squares

data = pd.read_excel("Input Data.xlsx")
time = data["Time"].values
t = np.linspace(0, len(data["Time"]), len(data["Time"]))
x_real = data["Prey Population"].values
y_real = data["Predator Population"].values

initial_guess = [1.0, 0.1, 0.1, 0.1, 100]

x0 = x_real[0]
y0 = y_real[0]
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

def residuals(params):
    y = odeint(sim, variables, t, args = (params, ))
    residuals = np.concatenate([(y[:, 0] - x_real), (y[:, 1] - y_real)])
    return residuals
    # setting up what the difference between our estimated population values would be from our parameter estimates and the actual values
result = least_squares(residuals, initial_guess)
# runs an optimsiation loop, that keeps trying different parameters until it's landed on the set of paramters that minimise the sum of squared residuals
alpha, beta, delta, gamma, K = result.x
params = [alpha, beta, delta, gamma, K]

y = odeint(sim, variables, t, args = (params, ))
# odeint means ODE integrator, it finds the integral of the derivative function that you have defined above
# then has the starting value, and it approximates the prey/predator population at each time steps
# the output is a txa matrix, where t is each time step and a is the number of animals that you are analysing
# you need to outline the parameters again for odeint to use, which is why they're included above
def SS(alpha, beta, delta, gamma, K):
    global y0_SS
    # use global so that this variable is defined inside and outside of the function
    y0_SS = (alpha / beta) * (1 - (gamma / (delta * K)))
    # with the introduction of the carrying capacity, the steady state for the predator population changes
    global x0_SS
    x0_SS = gamma / delta
    variables_SS = [x0_SS, y0_SS]
    return variables_SS
# steady state occurs when the derivative functions are set to 0
# so if we find x and y with the derivative functions set to 0, then we find the steady state populations
variables_SS = SS(alpha, beta, delta, gamma, K)
y_SS = odeint(sim, variables_SS, t, args = (params, ))
# run odeint with the steady state populations

plt.figure(figsize = (10,6))
plt.subplot(2, 1, 1)
plt.plot(time, y[:,0], color = "blue", label = "Prey Population")
plt.plot(time, y_SS[:, 0], linestyle = "--", color = "grey", label = "Prey Steady State")
plt.title("Prey Population")
plt.ylabel("Population")
plt.subplot(2, 1, 2)
plt.plot(time, y[:,1], color = "red", label = "Predator Population")
plt.plot(time, y_SS[:, 1], linestyle = "--", color = "grey", label = "Predator Steady State")
plt.title("Predator Population")
plt.xlabel("Time")
plt.ylabel("Population")
plt.show()
# plot the results

x_vals = np.linspace(0, 2 * y[:,0].max(), 400)
y_vals = np.linspace(0, 2 * y[:,1].max(), 400)
X, Y = np.meshgrid(x_vals, y_vals)
# creates grid for phaseplane

DX = (alpha * X * (1 - (X / K))) - (beta * X * Y)
DY = (-gamma * Y) + (delta * X * Y)
# make derivative functions again outside of sim function
# global within sim function doesn't work, as global stores the variables as a single scalar, but streamplot requires the full vector field

plt.figure(figsize=(8, 6))
plt.streamplot(X, Y, DX, DY, color = "grey")
# plots the direction that each population moves at each point on grid
plt.plot(y[:,0], y[:,1], color="blue", label="Trajectory")
# plots actual direction of the above defined Lotka-Volterra model
plt.plot(x0_SS, y0_SS, "ro", label="Steady State")
# plots steady state point, at red circle
plt.title("Phase Plane")
plt.xlabel("Prey Population")
plt.ylabel("Predator Population")
plt.show()

update = input("""What parameter do you want to perform bifurcation analysis for?
\nPrey Birth / Prey Predation / Predator Birth / Predator Death: """).strip().upper()

def bifurcation_plot():
    plt.subplot(2, 1, 1)
    plt.title("Prey Population")
    plt.ylabel("Population")
    plt.legend()
    plt.subplot(2, 1, 2)
    plt.title("Predator Population")
    plt.xlabel("Time")
    plt.ylabel("Population")
    plt.legend()
    plt.show()

if update == "PREY BIRTH":
    alpha_vals = np.linspace(alpha/2, alpha*1.5, 3)
    for alpha in alpha_vals:
        params = [alpha, beta, delta, gamma, K]
        y = odeint(sim, variables, t, args = (params, ))
        variables_SS = SS(alpha, beta, delta, gamma, K)
        y_SS = odeint(sim, variables_SS, t, args = (params, ))
        plt.subplot(2, 1, 1)
        plt.plot(time, y[:,0], label = f"Prey Population for alpha = {alpha: .2f}")
        plt.plot(time, y_SS[:, 0], linestyle = "--", label = f"Prey Steady State for alpha = {alpha: .2f}")
        plt.subplot(2, 1, 2)
        plt.plot(time, y[:,1], label = f"Predator Population for alpha = {alpha: .2f}")
        plt.plot(time, y_SS[:, 1], linestyle = "--", label = f"Prey Steady State for alpha = {alpha: .2f}")
        plt.ylabel("Population")
    bifurcation_plot()
elif update == "PREY PREDATION":
    beta_vals = np.linspace(beta/2, beta*1.5, 3)
    for beta in beta_vals:
        params = [alpha, beta, delta, gamma, K]
        y = odeint(sim, variables, t, args = (params, ))
        variables_SS = SS(alpha, beta, delta, gamma, K)
        y_SS = odeint(sim, variables_SS, t, args = (params, ))
        plt.subplot(2, 1, 1)
        plt.plot(time, y[:,0], label = f"Prey Population for beta = {beta: .2f}")
        plt.plot(time, y_SS[:, 0], linestyle = "--", label = f"Prey Steady State for beta = {beta: .2f}")
        plt.subplot(2, 1, 2)
        plt.plot(time, y[:,1], label = f"Predator Population for beta = {beta: .2f}")
        plt.plot(time, y_SS[:, 1], linestyle = "--", label = f"Prey Steady State for beta = {beta: .2f}")
        plt.ylabel("Population")
    bifurcation_plot()
elif update == "PREDATOR BIRTH":
    delta_vals = np.linspace(delta/2, delta*1.5, 3)
    for delta in delta_vals:
        params = [alpha, beta, delta, gamma, K]
        y = odeint(sim, variables, t, args = (params, ))
        variables_SS = SS(alpha, beta, delta, gamma, K)
        y_SS = odeint(sim, variables_SS, t, args = (params, ))
        plt.subplot(2, 1, 1)
        plt.plot(time, y[:,0], label = f"Prey Population for delta = {delta: .2f}")
        plt.plot(time, y_SS[:, 0], linestyle = "--", label = f"Prey Steady State for delta = {delta: .2f}")
        plt.subplot(2, 1, 2)
        plt.plot(time, y[:,1], label = f"Predator Population for delta = {delta: .2f}")
        plt.plot(time, y_SS[:, 1], linestyle = "--", label = f"Prey Steady State for delta = {delta: .2f}")
        plt.ylabel("Population")
    bifurcation_plot()
elif update == "PREDATOR DEATH":
    gamma_vals = np.linspace(gamma/2, gamma*1.5, 3)
    for gamma in gamma_vals:
        params = [alpha, beta, delta, gamma, K]
        y = odeint(sim, variables, t, args = (params, ))
        variables_SS = SS(alpha, beta, delta, gamma, K)
        y_SS = odeint(sim, variables_SS, t, args = (params, ))
        plt.subplot(2, 1, 1)
        plt.plot(time, y[:,0], label = f"Prey Population for gamma = {gamma: .2f}")
        plt.plot(time, y_SS[:, 0], linestyle = "--", label = f"Prey Steady State for gamma = {gamma: .2f}")
        plt.subplot(2, 1, 2)
        plt.plot(time, y[:,1], label = f"Predator Population for gamma = {gamma: .2f}")
        plt.plot(time, y_SS[:, 1], linestyle = "--", label = f"Prey Steady State for gamma = {gamma: .2f}")
        plt.ylabel("Population")
    bifurcation_plot()
else:
    print("\nNo Bifurcation Analysis")
