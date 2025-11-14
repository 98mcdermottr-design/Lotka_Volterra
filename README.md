# Lotka_Volterra
Series of Lotka-Volterra models applied in Python, with each model having an additional extension.

---

# 1_Lotka_Volterra_Simple.py
The Lotka-Volterra model in itself, is quite simple, it estimates how predator and prey populations change over time, and it revolves around the below two equations:

<img width="179" height="102" alt="image" src="https://github.com/user-attachments/assets/0646947e-b69e-423a-bc43-3c32b2a0cc9f" />

where
- x represents the prey population
- y represents the predator population
- $dx/dt$ and $dy/dt$ are the change in each of these populations with respect to time
- alpha is the birth rate for the prey population
- beta is the predation rate for the prey population, or the rate at which prey are being killed by the predators
- gamma is the death rate for the predator population
- delta is the birth rate for the predator population

So these equations form the foundation of this Lotka-Volterra model in Python.

This version is quite simple and uses user inputted estimates of the birth/death rates, as well as the starting populations for each species (prey/predator).

So with the function defined (which includes the above equations), the starting populations, and the parameters of the equations, you can use each of these as inputs in the odeint function from the scipy.integrate package in Python.

The odeint function stands for Ordinary Differential Equation Integrator. How it works is that it starts with your ODEs, i.e. the two Lotka-Volterra equations, the initial population sizes, and the time lengths (which was definied using the linspace function). From there it does a sort of dynamic time step, sort of like Euler's method, but Euler's method uses a fixed time step. Determining what the dynamic step is is quite complex, but to boil it down into a brief few sentences is that it starts with the Adams-Bashforth method to predict the next population value (value right after the starting population), using this, it calculates the corrected predicted value using the Adams-Moulton method, and the difference between the corrected and predicted values equal the local truncation error. If the local truncation error is within the tolerance (tolerance can be specified within the odeint function, but if not specified it just defaults to a relative tolerance and absolute tolerance of 1.49012 x $10e-8$), then it accepts the time step, if not, then it reduces the time step and tries again. If it keeps retrying, to no avail then it switches to the Backward Differentiation Formula to determine the next population value. This is for when stiffness is detected (non-stiff systems are when all the variables evolve on roughly the same time scale, stiff systems have variables that change on different scales, which can cause instability). The result of this is an array where the rows represent each time step and the columns represent the prey and predator populations.

Once you've run odeint and solved for this array, then you can just plot the results, which will show the two populations oscillating, as an increase in the prey population will result in more predators, which in turn will increase predation of prey This will then reduce the prey population, which will cause a reduction in predator population, as there is less food. The predation rate will then decrease, causing the prey population to increase, and then the cycle will just repeat.

<img width="912" height="568" alt="image" src="https://github.com/user-attachments/assets/63058b30-9843-43f2-95a3-6680646281c3" />

---

# 2_Lotka_Volterra_Steady_State.py

In this next iteration, I've incorporated the steady state. The steady state is the population at which neither the prey nor predator populations change over time. To solve for this you just set the two Lotka-Volterra equations equal to 0, which gives you the below formulae:

$y = alpha / beta$

$x = gamma / delta$

You can then set these values for x and y as your starting populations, and then use odeint and matplotlib to plot the prey and predator populations over time, starting with the steady state populations for each (grey dotted line in the below plots represent this):

<img width="879" height="566" alt="image" src="https://github.com/user-attachments/assets/9d853903-09e9-4161-8e8c-ec164db24b7f" />

As you can see, the populations do not oscillate when you start at the steady state populations and they just remain flat over time.

---

# 3_Lotka_Volterra_Carrying_Capacity.py

One limitation of the above model is that it relies on simple exponential growth for each of the populations, based off of the above, the prey population could grow forever without the predators involved, but this is not the case in reality. 

In reality the prey population itself can run out of food and resources. Considering this we adapt the model to follow logistic growth, by introducing a carrying capacity.

To do this, we simply add a variable K, which represents the maximum prey population, into the formula for the rate of change of the prey population:

<img width="196" height="66" alt="image" src="https://github.com/user-attachments/assets/839655af-27a5-4de6-b6ce-c4467875647f" />

This will also impact the steady state for the predator population, as it now becomes:

$y = (alpha / beta) x (1 - (gamma / (delta x K)))$

But the remainder of the process remains the same, use the odeint function and then plot the results, but you'll notice one significant change in the output charts:

<img width="904" height="546" alt="image" src="https://github.com/user-attachments/assets/cf2019b6-4db5-4a30-8659-56df3453f470" />

How the carrying capacity works, is that once the prey population gets close to the maximum prey population, it slows the birth rate for the prey, and if the prey population is far away from the maximum population, then you have essentially have the birth rate parameter working in full effect (doesn't speed up the birth rate, it just doesn't slow it down). But at all times the birth rate is somewhat slowed, which in turn affects the predator population. All of this results in a dampening of the oscillations, as the population highs aren't as high and the lows aren't as low. But the dampening keeps happening overtime, so the oscillations get smaller and smaller until they converge and become a flat line. The flat line they converge on is the steady state, because as the oscillations get smaller and smaller the populations get closer and closer to the steady state, until the populations then reach the steady state values and then they remain at this.

---


# 4_Lotka_Volterra_Phase_Plane.py

The phase plane just merges the Lotka-Volterra equations, and instead of showing how each population changes with respect to time, you show how the prey population changes with respect to the predator population.

---

# 5_Lotka_Volterra_Parameter_Estimation.py

---

# 6_Lotka_Volterra_Phase_Plane_Nullclines.py

---
# 🥈 Alternatives Of The Above
 - Instead of using odeint, you can actually use Euler's method, which is just a gradual step-by-step approach, however, its often less accurate and less stable than odeint, which is why we've used this intead

---

# 📑 Sources
- https://www.youtube.com/watch?v=Tc05IbqTsFM
- https://en.wikipedia.org/wiki/Lotka%E2%80%93Volterra_equations
- https://en.wikipedia.org/wiki/Competitive_Lotka%E2%80%93Volterra_equations
