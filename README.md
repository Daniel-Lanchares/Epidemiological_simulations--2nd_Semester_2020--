# Epidemiological_simulations--2nd_Semester_2020--
Final assignment of the "Introduction to Computational Physics" course. 2nd semester of the 2019/2020 school-year.

Comparison between ODE and stochastic based simulations of epidemiological contagion.

Modelling is achieved through parameter alteration (and in cases addition of time-dependence) for the ODE and achieved through phenomenological simulation for the stochastic methods.

Here the stochastic simulator is presented mid-simulation (no, the lonely blue fellow did not survive for long). The various boards in which agents can move represent the living area (grey), hospital (yellow), intensive care (orange) & morgue (blue):

![simulator](https://raw.githubusercontent.com/Daniel-Lanchares/Epidemiological_simulations--2nd_Semester_2020--/main/Stochastic_Simulations/Simulation_example.png?raw=true)

As indicated by the red auras, contagion probability decreases with distance up to a customizable amount. Social distancing can be imposed as a controllable repulsive force.

The program plots real time SIRD[¹] curves that permit the evaluation of measures to take in the -completely implausible- event of a global pandemic. It also tracks available hospital beds.

![simulator curves](https://raw.githubusercontent.com/Daniel-Lanchares/Epidemiological_simulations--2nd_Semester_2020--/main/Stochastic_Simulations/Example.png)

In contrast, the ODE simulator numerically integrates the SIRD equations (shown bellow) to directly produce its data. In this example both transmission, recuperation and mortality rates have been promoted to time-dependant parameters to model an upturn in cases (two wave scenario).

$$
\begin{align*}
S'(t,S,I,R,D) &= -tr \cdot S \cdot I\\
I'(t,S,I,R,D) &=  tr \cdot S \cdot I - (rec+mort)\cdot I\\
R'(t,S,I,R,D) &= rec \cdot I\\
D'(t,S,I,R,D) &= mort \cdot I
\end{align*}
$$

![simulator curves](https://raw.githubusercontent.com/Daniel-Lanchares/Epidemiological_simulations--2nd_Semester_2020--/main/ODE_Simulations/Example.png)


[1]: **S**usceptible **I**nfected **R**ecovered **D**eceased.
