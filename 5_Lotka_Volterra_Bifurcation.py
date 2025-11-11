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
    global y0_SS
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
        plt.plot(t, y[:,0], label = f"Prey Population for alpha = {alpha: .2f}")
        plt.plot(t, y_SS[:, 0], linestyle = "--", label = f"Prey Steady State for alpha = {alpha: .2f}")
        plt.subplot(2, 1, 2)
        plt.plot(t, y[:,1], label = f"Predator Population for alpha = {alpha: .2f}")
        plt.plot(t, y_SS[:, 1], linestyle = "--", label = f"Prey Steady State for alpha = {alpha: .2f}")
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
        plt.plot(t, y[:,0], label = f"Prey Population for beta = {beta: .2f}")
        plt.plot(t, y_SS[:, 0], linestyle = "--", label = f"Prey Steady State for beta = {beta: .2f}")
        plt.subplot(2, 1, 2)
        plt.plot(t, y[:,1], label = f"Predator Population for beta = {beta: .2f}")
        plt.plot(t, y_SS[:, 1], linestyle = "--", label = f"Prey Steady State for beta = {beta: .2f}")
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
        plt.plot(t, y[:,0], label = f"Prey Population for delta = {delta: .2f}")
        plt.plot(t, y_SS[:, 0], linestyle = "--", label = f"Prey Steady State for delta = {delta: .2f}")
        plt.subplot(2, 1, 2)
        plt.plot(t, y[:,1], label = f"Predator Population for delta = {delta: .2f}")
        plt.plot(t, y_SS[:, 1], linestyle = "--", label = f"Prey Steady State for delta = {delta: .2f}")
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
        plt.plot(t, y[:,0], label = f"Prey Population for gamma = {gamma: .2f}")
        plt.plot(t, y_SS[:, 0], linestyle = "--", label = f"Prey Steady State for gamma = {gamma: .2f}")
        plt.subplot(2, 1, 2)
        plt.plot(t, y[:,1], label = f"Predator Population for gamma = {gamma: .2f}")
        plt.plot(t, y_SS[:, 1], linestyle = "--", label = f"Prey Steady State for gamma = {gamma: .2f}")
        plt.ylabel("Population")
    bifurcation_plot()
else:
    print("\nNo Bifurcation Analysis")
