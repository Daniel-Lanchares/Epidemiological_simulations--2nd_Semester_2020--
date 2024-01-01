#Modelo Epidemiológico básico
from numpy import *
from scipy.integrate import solve_ivp

import matplotlib.pyplot as plt


#SEDO
#S'(t,S,I,R,M) = -tr*S*I				Susceptibles
#I'(t,S,I,R,M) = tr*S*I - (rec+mort)*I	Infectados
#R'(t,S,I,R,M) = rec*I					Recuperados
#M'(t,S,I,R,M) = mort*I					Fallecidos

#Para los escenarios del apartado 7.4.1
'''
def ftr(t): return tr*exp(-t*4e-2)
def frec(t): return rec*exp(t*1e-3)
def fmort(t): return mort*exp(-t*1e-2)
'''

'''
def ftr(t): return 0.5*tr* cos(t*1.5e-2)**2* exp(-5e-3*t) #exp(t*5e-3)
def frec(t): return 0.4*rec * sin(t*1e-2)**2 * exp(-5e-3*t) + 8e-6*t
def fmort(t): return mort*exp(-t*4e-3)
'''

'''
def ftr(t): return 3*tr * sin(t*1e-2 + 0)**2 *exp(-t*2e-3)
def frec(t): return rec*exp(t*1e-3)
def fmort(t): return mort*exp(-t*1e-2)
'''


def ftr(t): return tr*ones_like(t)
def frec(t): return rec*ones_like(t)
def fmort(t): return mort*ones_like(t)

#Función SEDO
def f(t, v): return [-ftr(t)*v[0]*v[1], ftr(t)*v[0]*v[1] - (frec(t)+fmort(t))*v[1], frec(t)*v[1], fmort(t)*v[1]]




'''Valores para evaluar sobre 10 (y no sobre 100)
tr=0.2
rec=0.2
mort=0.02
Tmax= 50

S0=9.9
I0=0.1
R0=0
M0=0
'''
#Tasas de transmisión, recuperación y mortalidad
tr=0.002
rec=0.01
mort=0.002

#Intervalo de tiempo
tmin= 0
Tmax=900
nptos= 200


#Valores iniciales (% de población)
S0=99
I0=1
R0=0
M0=0


y0=[S0, I0, R0, M0]

t_eval= linspace(tmin,Tmax, nptos)
sol = solve_ivp(fun=f, t_span=(tmin, Tmax), y0=y0,t_eval=t_eval)

#Asindotas (con t suficientemente alto muestran lim t -> Inf)
apoyo= ones_like(sol.y[0])
asin0= sol.y[0][-1]*apoyo
asin1= sol.y[1][-1]*apoyo
asin2= sol.y[2][-1]*apoyo
asin3= sol.y[3][-1]*apoyo
#Pico de infectados
infmax= max(sol.y[1]) 

#2 subfiguras, la principal y la de las tasas frente al tiempo
plt.figure(figsize=(12,6))
plt.subplot(2,1,1)
plt.title('Propagación frente al tiempo (Control)')
plt.plot(sol.t, sol.y[0], 'b-', label='Susceptibles (%4.2f)'%(sol.y[0][-1]))
plt.plot(sol.t, asin0, 'k--')

plt.plot(sol.t, sol.y[1], 'r-', label='Infectados (%4.2f)\nMáximo=(%4.2f)'%(sol.y[1][-1], infmax))
plt.plot(sol.t, asin1, 'k--')

plt.plot(sol.t, sol.y[2], 'g-', label='Recuperados (%4.2f)'%(sol.y[2][-1]))
plt.plot(sol.t, asin2, 'k--')

plt.plot(sol.t, sol.y[3], 'k-', label='Fallecidos (%4.2f)'%(sol.y[3][-1]))
plt.plot(sol.t, asin3, 'k--')


plt.axis([0, Tmax, 0, 110])

plt.ylabel('Población (%)')
plt.legend()

plt.subplot(2,1,2)
plt.plot(sol.t, ftr(sol.t), 'r-', label= 'tr')
plt.plot(sol.t, frec(sol.t), 'g-', label= 'rec')
plt.plot(sol.t, fmort(sol.t), 'k-', label= 'mort')
plt.xlabel('tiempo (unidades sin definir)')
plt.xlim((0,Tmax))
plt.legend()
plt.tight_layout()
#plt.savefig('EDO_const.png')
plt.show()

