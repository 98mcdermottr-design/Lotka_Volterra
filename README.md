# Lotka Volterra Equations Applied
This project implements a series of increasingly complex models focused around applying the Lotka-Volterra equations in Python. Each extension is motivated by biological realism or mathematical curiosity. From this basis, these Lotka-Volterra models can be extended even further and applied across ecology, economics, city planning and more.

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

The phase plane just merges the Lotka-Volterra equations, and instead of showing how each population changes with respect to time, you show how the predator population changes with respect to the prey population.

The rate of change of the predator population with respect to the prey population can be represented using the below formula (found simply using the chain rule):

<img width="173" height="68" alt="image" src="https://github.com/user-attachments/assets/99bb4f0c-e7a4-4438-8d62-03bb977e8a2d" />

So to plot the phase plane, you first make up a large grid of possible population values for x and y. From there you calculate the change in x and y at each of those possible values of x and y, and then you plot all of these possible movements in x and y using the streamplot function:

<img width="757" height="555" alt="image" src="https://github.com/user-attachments/assets/c99c16a3-29b6-4d81-b8b5-c35bac6e790b" />

The arrows represent the direction that the predator and prey populations go in respect to where they are right now.

The above also shows the actual trajectory of the predator and prey populations based on our actual starting populations (blue line), as well as the steady state from this model (red dot).

---

# 5_Lotka_Volterra_Bifurcation.py

The bifurcation script adds an additional element on the end, to show how the model would change as a result of change in the parameters; alpha, beta, gamma or delta.

It simply takes the input of which parameter you're looking to show variations of, and then scales it up 1.5 times, and scales it down 0.5 times. After this it runs the normal steps of odeint and then plot the results, but it shows 3 seperate models for each possible version of the parameter that's been chosen to perform bifurcation analysis for. Below is an example of the output plot from this analysis:

<img width="1619" height="888" alt="image" src="https://github.com/user-attachments/assets/c6d9c486-178e-495b-b780-3a42743d9c64" />

---

# 6_Lotka_Volterra_Parameter_Estimation.py

In each of the above models, the parameters and the starting populations were inputted by the user, but if we had a data set with predator and prey populations over a stretch of time, we could solve for the model parameters using this data set.

This is what is done in the latest iteration of the Lotka-Volterra model. The user inputs are removed, and instead we rely on an excel sheet, which we import into the python script, called "Input Data.xlsx".

So once we import the excel sheet using pd.read_excel, we must then transform this pandas dataframe, into arrays, one for the length of time, one for the prey population and one for the predator population.

Once we have done this, we setup an initial guesses for the parameters (don't worry these will be changed later in the script), and we set x0 and y0 equal to the starting populations from the "Input Data.xlsx" file.

Then there is the usual step of defining our Lotka-Volterra equations, but then we define a residuals function, which essentially runs the odeint, and then finds the difference between the output of the odeint and our actual predator and prey populations from the "Input Data.xlsx".

Using a combination of our residuals function and out initial estimate of the parameters, the least-squares function then performs an optimsiation loop, that keeps trying different parameters until it's landed on the set of paramters that minimise the sum of squared residuals. Once it has found these set of parameters, we set these equal to alpha, beta, delta, gamma and K, and we run the remaining steps as usual.

---

# 7_Lotka_Volterra_Multiple_Animals.py

The Lotka-Volterra can also be upgraded to include multiple animals. The addition of multiple animals is quite simple in theory, but it introduces many complexities in Python.

For simplicities sake, this new iteration of the Lotka-Volterra model has the parameter estimation, bifurcation, phase plane, and steady state removed. It also relies on the assumption that each predator can eat each prey.

So with multiple animals the equations change, but just with the addition of the extra predator or prey. For example with two predators and one prey, the rate of change of the prey population is now represented by the below:

<img width="215" height="72" alt="image" src="https://github.com/user-attachments/assets/14349aa4-674b-4ed1-aef4-f89fe68184da" />

where
- x is the prey population
- y is the population of the first predator
- z is the population of the second predator
- a is the birth rate of the prey population
- b is the predation rate of the first predator on the prey population
- c is the predation rate of the second predator on the prey population

But for this model we've assumed that the predation rate parameters are the same, so b = c, which means we can sum the predator populations when doing the calculation.

In this model, you're allowed to have as many prey or predators as you like, so first we define empty lists for each of the parameters, then runs a loop to get the user input for each of the parameters. Once all of these parameters are added to their respective lists, it then converts the paramter lists into arrays.

Once this is done, the lotka volterra equations need to be defined in a function. So first we redefine the parameters within the function, as usual, and set x and y equal to the starting populations for the prey and the predators. Then we create an array of 0s for dxdt (essentially an empty array for values to be added later), after this it is a matter of running a loop to calculate dxdt for each prey, so the formula for each is the birth rate for that prey times the starting population, which is all adjusted for with the carrying capacity, minus the prey population times the predation rate times the sum of the predator (remember it was noted above that we are not using specific predation rates for each predator, which means we can sum the predator population). We then apply this same approach of using a loop to calculate the rate of change of the predator population for each predator.

Once this is all complete, we run the odeint. But notice in each of the previous steps we concatenated the starting populations, as well as the rates of change, this is because odeint requires a 1D array input for the starting populations and a 1D array output for the rates of change, as the integration requires vectors. Odeint will then return a t x a matrix, where t is the number of timesteps and a is the number of prey and predator species you are analysing combined, where the first n columns, where n is the number of prey, show the prey populations over time and the m columns after that, where m is the number of predators, show the predator populations over time.

Then the results can be plotted:

<img width="869" height="545" alt="image" src="https://github.com/user-attachments/assets/df27d79a-5694-451c-aa43-87a6c96f37fa" />

---
# 🥈 Alternatives Of The Above
 - Instead of using odeint, you can actually use Euler's method, which is just a gradual step-by-step approach, however, its often less accurate and less stable than odeint, which is why we've used this intead

---

# 📑 Sources
_Youtube Videos and Wikipedia pages explaining the concepts behind the Lotka-Volterra Model_
- https://www.youtube.com/watch?v=Tc05IbqTsFM
- https://en.wikipedia.org/wiki/Lotka%E2%80%93Volterra_equations
- https://en.wikipedia.org/wiki/Competitive_Lotka%E2%80%93Volterra_equations

_Useful papers on the application of the Lotka-Volterr model, as well as one applied to market share between Samsung and Apple (recommend this read if you want to see the Lotka-Volterra equations applied outside of ecology)_
- https://mc-stan.org/learn-stan/case-studies/lotka-volterra-predator-prey.html?utm_source=chatgpt.com
- https://www.siam.org/media/oqef0fuc/s163493r.pdf
