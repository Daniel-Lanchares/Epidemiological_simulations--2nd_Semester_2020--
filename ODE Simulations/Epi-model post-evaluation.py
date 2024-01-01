#Modelo Epidemiológico básico
from numpy import *
from scipy.integrate import solve_ivp

import matplotlib.pyplot as plt


#SEDO
#0 S' = mu*Nt + tau*C -(tr/Nt)*S*I -(mu+prot)*S		Susceptibles
#1 C' = prot*S -(tau+mu)*C							Confinados
#2 E' = (tr/Nt)*S*I - (gamma+mu)*E 					Expuestos
#3 I' = gamma*E - (delta+mu)*I						Infectados (Asintomáticos)
#4 A' = delta*I - (rec(t)+mort(t)+mu)*Q				Aislados   (Sintomáticos)
#5 R' = rec(t)*I - mu*R								Recuperados
#6 M' = mort(t)*Q									Fallecidos




def rec(t): return rec0*(1-exp(-rec1*t))
def mort(t): return mort0*exp(-mort1*t)

def prot(A): return prot0*log(A+2)		#exp(-prot1*(I+prot2)**2)
def tau(A):  return prot0*exp(-0.05*A)

#Función SEDO
def f(t, v): 
	I= 												  gamma*v[2] - delta*v[3]
	A= 															  delta*v[3] - (rec(t)+mort(t))*v[4]
	S=  tau(A)*v[1] -(tr/Nt)*v[0]*v[3] -prot(A)*v[0] 												+ mu*Nt
	C= -tau(A)*v[1] 				   +prot(A)*v[0]
	E= 				 (tr/Nt)*v[0]*v[3] 				 -gamma*v[2]	
	
	R= 																			rec(t)*v[3]
	M= 																		    mort(t)*v[4] 		#+ mu*v[6]
	return [S, C, E, I, A, R, M] 																	#- mu*v




#Parámetros del modelo
Nt= 10e+2
mu=  	1/(80*365)		#Mortalidad habitual

prot0= 		0.028		#Protección (Max)
tr=			1.133		#Transmisión
gamma=		0.890  		#Incubación
delta= 		0.539		#Aislamiento
#tau= 	(1+0.5)*prot0	#Deconfinamiento

rec0= 		0.072
rec1= 		0.040
mort0=		0.070
mort1=		0.145



#Intervalo de tiempo
tmin= 0
Tmax=300
ppt=0.5
nptos= int(ppt*Tmax)


#Valores iniciales (% de población)
S0=Nt-1
C0=0
E0=0
I0=1
A0=0
R0=0
M0=0


y0=[S0, C0, E0, I0, A0, R0, M0]

t_eval= linspace(tmin,Tmax, nptos)
sol = solve_ivp(fun=f, t_span=(tmin, Tmax), y0=y0,t_eval=t_eval)

print(2)
#Asindotas (con t suficientemente alto muestran lim t -> Inf)
apoyo= ones_like(sol.y[0])
asin0= sol.y[0][-1]*apoyo
asin1= sol.y[1][-1]*apoyo
asin2= sol.y[2][-1]*apoyo
asin3= sol.y[3][-1]*apoyo
asin4= sol.y[4][-1]*apoyo
asin5= sol.y[5][-1]*apoyo
asin6= sol.y[6][-1]*apoyo

#Pico de infectados
infmax= max(sol.y[3]) 
aismax= max(sol.y[4])

#2 subfiguras, la principal y la de las tasas frente al tiempo
plt.figure(figsize=(16,8))
plt.subplot(2,1,1)
plt.title('Propagación frente al tiempo (Control)')

plt.plot(sol.t, sol.y[0], 'b-', label='Susceptibles (%4.2f)'%(sol.y[0][-1]))
plt.plot(sol.t, asin0, 'k--')

plt.plot(sol.t, sol.y[1], 'b--', label='Confinados (%4.2f)'%(sol.y[1][-1]))
plt.plot(sol.t, asin1, 'k--')

plt.plot(sol.t, sol.y[2], 'y-', label='Expuestos (%4.2f)'%(sol.y[2][-1]))
plt.plot(sol.t, asin2, 'k--')

plt.plot(sol.t, sol.y[3], 'r-', label='Infectados (%4.2f)\nMáximo=(%4.2f)'%(sol.y[3][-1], infmax))
plt.plot(sol.t, asin3, 'k--')

plt.plot(sol.t, sol.y[4], 'r--', label='Aislados (%4.2f)\nMáximo=(%4.2f)'%(sol.y[4][-1], aismax))
plt.plot(sol.t, asin4, 'k--')

plt.plot(sol.t, sol.y[5], 'g-', label='Recuperados (%4.2f)'%(sol.y[5][-1]))
plt.plot(sol.t, asin5, 'k--')

plt.plot(sol.t, sol.y[6], 'k-', label='Fallecidos (%4.2f)'%(sol.y[6][-1]))
plt.plot(sol.t, asin6, 'k--')


plt.axis([0, Tmax, 0, 1.1*Nt])

plt.ylabel('Población (%)')
plt.legend()

plt.subplot(2,1,2)

plt.plot(sol.t, prot(sol.y[4]), 'b-', label= 'protección')
plt.plot(sol.t, tau(sol.y[4]), 'b--', label= 'deconfinaimento')
plt.plot(sol.t, rec(sol.t), 'g-', label= 'rec')
plt.plot(sol.t, mort(sol.t), 'k-', label= 'mort')
plt.xlabel('tiempo (unidades sin definir)')
plt.xlim((0,Tmax))
plt.legend()
plt.tight_layout()
#plt.savefig('EDO_const.png')

plt.show()

