#Prueba Clases

from numpy import *
import random as ran
from vpython import *

class Paciente(box):
	
	def __init__(self, pos, size, acel, vel , color_init=color.blue, infectado=False, inmune=False, muerto=False, hospitalizado=False, hospitalizadoUCI=False, distanciamiento_social=False):
		super().__init__()
		self.pos=pos
		self.size=size
		self.acel=acel
		self.vel=vel
		self.color=color_init
		self.infectado=infectado
		self.inmune=inmune
		self.muerto=muerto
		self.hospitalizado=hospitalizado
		self.hospitalizadoUCI=hospitalizadoUCI
		self.distanciamiento_social=distanciamiento_social
		
		self.radioinf= 	sphere(pos= self.pos, radius=0 , color=color.red, opacity=0.7)
	
	def infecta(self):
		self.infectado=	True
		self.color= 	color.red
		self.dias_enfermo=		0
		self.gravedad=			ran.randint(0,3) #Estados: Asintomático, leve, grave, muy grave

	def muere(self):
		self.infectado= 		False
		self.inmune= 			True
		self.muerto= 			True
		self.color=				color.black
		self.radioinf.radius= 	0
		self.vel=				vector(0,0,0)
		self.acel=				vector(0,0,0)
		self.pos=               Cementerio.pos+vector(0,0,3)+vector(ran.uniform(0.3*nplazas+1, -0.3*nplazas+1),ran.uniform(0.3*nplazas+1, -0.3*nplazas+1), 0)
		if self.hospitalizado== True:
			self.hospitalizado= False
			hospitalizacion= True
		if self.hospitalizadoUCI== True:
			self.hospitalizadoUCI= False
		

	def recupera(self):
		self.infectado= 				False
		self.inmune=					True
		self.color=						color.green
		self.radioinf.radius= 			0
		if self.hospitalizado==True or self.hospitalizadoUCI== True:
			self.pos= 					pos[ran.randint(0, npacientes-1)]
			if self.hospitalizado==True:
				self.hospitalizado= 	False
			if self.hospitalizadoUCI==True:
				self.hospitalizadoUCI= 	False
			hospitalizacion= 			True

	def hospitaliza(self):
		
		self.vel=						vector(0,0,0)
		self.acel=						vector(0,0,0)
		self.distanciamiento_social=	False
		if self.gravedad== 2 and nplazas-r[4] != 0:
			self.hospitalizado= 		True
			self.pos= 					Hospital.pos+vector(0,0,3)+vector(ran.uniform(0.3*nplazas, -0.3*nplazas),ran.uniform(0.3*nplazas, -0.3*nplazas), 0)
			if plazas_hosp== 0: hospitalizacion = False
		if self.gravedad== 3 and uplazas-r[5] != 0:
			self.hospitalizadoUCI= 		True
			self.pos= 					UCI.pos+vector(0,0,3)+vector(ran.uniform(0.3*uplazas, -0.3*uplazas),ran.uniform(0.3*uplazas, -0.3*uplazas), 0)
			

	def aura(self): #Aura que indica área de contagio
		if self.radioinf.radius >= radmax:
			self.radioinf.radius= 	0
			self.radioinf.opacity= 	0.7
				
		else: 
			self.radioinf.radius +=  0.1 
			self.radioinf.opacity -= 0.7*0.1/radmax
	
def euler(i): #Integración de Euler para el movimiento
	i.vel += i.acel*dt		
	i.pos += i.vel*dt

def dist_soc(i): #Fuerza repulsiva
	A = vector(0,0,0)
	for j in pacientes:
		if mag(i.pos-j.pos) > 10 or i == j:continue
		else:
			aj=norm(i.pos-j.pos)/(mag(i.pos-j.pos)+0.01)
			A += potencia_dist*aj
	i.acel= A

def recuento(pacientes):
	infectados=0
	recuperados=0
	hospitalizados=0
	hospitalizadosUCI=0
	muertos=0
	for i in pacientes:
		infectados 		  += i.infectado
		recuperados 	  += (i.inmune - i.muerto)
		muertos 		  += i.muerto
		hospitalizados	  += i.hospitalizado
		hospitalizadosUCI += i.hospitalizadoUCI
	susceptibles= len(pacientes)-(infectados+recuperados+muertos)
	return[susceptibles, infectados, recuperados, muertos, 
									hospitalizados, hospitalizadosUCI]

def reset(): #Para múltiples simulaciones
	global suscep
	global infect
	global recup
	global muert
	global count
	global plazas_hosp
	global plazas_uci
	count=0
	suscep= npacientes
	infect=0
	recup=0
	muert=0
	plazas_hosp= nplazas
	plazas_uci=	 uplazas
	for i in pacientes:
		i.visible= False
		del i	
	
	
width= 					1600
height= 				800
nsimulaciones= 			10
count=					0
fps=					80  #ciclos por segundo
dt= 					0.1 #1/fps para velocidad normal
npar= 					6 #Número de parámetros a representar.	6 por S,I,R,M | H,U

#dias_simulados= (hasta que deje de haber infectados)
Velocidad= 				4 #Multiplicador de velocidad. Usar junto con ciclos_dia para aumentar rapidez de simulación
#No necesario tocar, mejor usar dt

animation = canvas( width=width, height=height)
animation.title = 'Simulador de Contagios'

#Parametros epidemia
npacientes= 			100
radmax=					3 #Radio máximo de contagio
d_pobl= 				1/250 #Habitantes/unidad^2

tinf= 					0.2 #Probabilidad de contagio a radmax unidades de distancia (aumenta más cerca)
trec= 					0.2 #Probabilidad de recuperación para un infectado de gravedad 1 que lleva 1 día enfermo
tmort=					0.1 #Probabilidad de muerte de un paciente de gravedad 1

distanciamiento_social= True
n_inf_dist= 			5 #Número de infectados para aplicar protocolo de distanciamiento
potencia_dist= 			9 #Magnitud de distanciamiento

hospitalizacion=		True
nplazas=				15
uplazas=				10
plazas_hosp=			nplazas
plazas_uci=				uplazas

dia=					0
ciclos_dia= 			100 #Ciclos del bucle que constituyen un día

#Probabilidades/ciclo
rec= 					trec/ciclos_dia
mort= 					tmort/ciclos_dia



#Localidad
area= npacientes/d_pobl
lado= sqrt(area)
ladred= (0.9*lado/2)
Suelo= box(pos=vector(0,0,-3), size= vector(lado,lado,1), color=color.white)

if hospitalizacion== True: 
	Hospital= box(pos= Suelo.pos + vector(lado/2+1.2*nplazas, 0, 0), size=vector(1.2*nplazas, 1.2*nplazas, 1), color=color.yellow)
	UCI= 	  box(pos= Hospital.pos + vector(0,1.2*nplazas+1.2*uplazas,0), size=vector(1.2*uplazas, 1.2*uplazas, 1), color= color.orange)

Cementerio=box(pos= Suelo.pos - vector(lado/2+1.2*nplazas,0,0), size=vector(1.2*nplazas+1, 1.2*nplazas+1, 1), color=color.blue)



T=[] #Será lista de tiempos que tarda la simulación
Datos=[] #Será lista de datos sin procesar
for n in range(nsimulaciones):

	#Parámetros iniciales al azar
	pos= [vector(ran.uniform(-ladred,ladred), ran.uniform(-ladred,ladred), 0) for i in range(npacientes)]
	vel= [vector(Velocidad*ran.uniform(-1,1), Velocidad*ran.uniform(-1,1), 0) for i in range(npacientes)]
	acel=[vector(0, 0, 0) for i in range(npacientes)]

	#Creación de pacientes
	pacientes= []
	for i in range(npacientes):
		paciente= Paciente(pos=pos[i], size= vector(1,1,1), acel= acel[i], vel= vel[i], distanciamiento_social=distanciamiento_social)
		pacientes.append(paciente)
	
	r=recuento(pacientes)
	a= pacientes[0].infecta() #Paciente 0

	graf= graph(width=900, height=300, title='<b>Contagios</b>', xtitle='<i>t (dias)</i>', ytitle='<i>casos</i>', foreground=color.black, background=color.white)
	f1 = gcurve(color=color.blue, label= 'Susceptibles')
	f2 = gcurve(color=color.red, label= 'Infectados')
	f3 = gcurve(color=color.green, label= 'Recuperados')
	f4 = gcurve(color=color.black, label= 'Fallecidos')
	
	#Grabado de datos
	S= []
	I= []
	R= []
	M= []
	
	H= []
	U= []
	
	while True:
		rate(fps)
		if count% ciclos_dia ==0: dia+=1
		for i in pacientes:
			
			if i.distanciamiento_social==True and i.muerto== False and r[1]> n_inf_dist: a=dist_soc(i)
			
			a= euler(i) #Atualizamos velocidad y aceleración
			#Evitar que salgan del recinto
			if i.pos.x > ladred and i.pos.x < (ladred+0.6*nplazas) or i.pos.x < -ladred and i.pos.x > -(ladred+0.6*nplazas): i.vel.x= -i.vel.x
			if i.pos.y > ladred and i.pos.y < (ladred+0.6*nplazas) or i.pos.y < -ladred and i.pos.y < (ladred+0.6*nplazas): i.vel.y= -i.vel.y
			if hospitalizacion== True and i.hospitalizado == True:
				if i.pos.x > Hospital.pos.x+0.6*nplazas or i.pos.x < Hospital.pos.x-0.6*nplazas: i.vel.x= -i.vel.x
				if i.pos.y > Hospital.pos.y+0.6*nplazas or i.pos.y < Hospital.pos.y-0.6*nplazas: i.vel.y= -i.vel.y
			if hospitalizacion== True and i.hospitalizadoUCI == True:
				if i.pos.x > UCI.pos.x+0.6*uplazas or i.pos.x < UCI.pos.x-0.6*uplazas: i.vel.x= -i.vel.x
				if i.pos.y > UCI.pos.y+0.6*uplazas or i.pos.y < UCI.pos.y-0.6*uplazas: i.vel.y= -i.vel.y
			
			
			if i.infectado == True: #Para los ya infectados
				i.radioinf.pos = i.pos
				a= i.aura()
				if hospitalizacion==True and i.gravedad >= 2 and r[1]> n_inf_dist and i.hospitalizado== False and i.hospitalizadoUCI==False: a=i.hospitaliza()
				for j in pacientes: #Infección de otros pacientes
					if mag(i.pos-j.pos) < radmax and j.infectado == False and j.inmune == False:
						p= tinf**(mag(i.pos-j.pos)/radmax)
						if ran.random() < p:
							a=j.infecta()
				#Posibilidad de que mueran o se recuperen en función de la gravedad	
				if ran.random()< rec*(i.dias_enfermo / (i.gravedad - ((i.hospitalizado+i.hospitalizadoUCI)/2) + 0.01))**(rec): a= i.recupera()
				if i.inmune== False and ran.random()< mort*(i.dias_enfermo * i.gravedad * ((i.hospitalizado+i.hospitalizadoUCI)/2))**(mort): a= i.muere()
				if count% ciclos_dia ==0: i.dias_enfermo += 1
			
		r= recuento(pacientes)
			
		s = """&nbsp;&nbsp; 		   		Día = %4i
			&nbsp;&nbsp; Pacientes = %4i
			&nbsp;&nbsp; Susceptibles = %4i
			&nbsp;&nbsp; Infectados = %4i 
			&nbsp;&nbsp; Recuperados = %4i 
			&nbsp;&nbsp; Muertos = %4i
			&nbsp;&nbsp; Hospitalizados = %4i
			&nbsp;&nbsp; Camas de hospital = %4i/%2i
			&nbsp;&nbsp; Camas de UCI = %4i/%2i
			&nbsp""" %(dia, r[0]+r[1]+r[2]+r[3], r[0], r[1], r[2], r[3], r[4]+r[5], nplazas-r[4], nplazas, uplazas-r[5], uplazas)
		animation.caption = s
		
		#gráficos en tiempo real
		f1.plot(count/ciclos_dia, r[0])	; S.append(r[0])
		f2.plot(count/ciclos_dia, r[1])	; I.append(r[1])
		f3.plot(count/ciclos_dia, r[2])	; R.append(r[2])
		f4.plot(count/ciclos_dia, r[3])	; M.append(r[3])
		
		H.append(nplazas-r[4])
		U.append(uplazas-r[5])
		
		count +=1
		if r[1]==0: break #Condición de parada de la simulación
	T.append(count)
	Datos.append(S)
	Datos.append(I)
	Datos.append(R)
	Datos.append(M)
	
	Datos.append(H)
	Datos.append(U)
	
	a=reset()
	
#Procesamiento de datos post-simulación 
#De momento hacemos una gráfica con la media de las nsimulaciones

#print(Datos) Lista de datos brutos


b=[len(Datos[i]) for i in range(len(Datos))]

datos = ones([nsimulaciones, npar, max(b)]) 
for i in range(nsimulaciones):
	for j in range(npar):
		for k in range(max(b)-len(Datos[npar*i+j])):
			Datos[npar*i+j].append(Datos[npar*i+j][-1]) 
			#Nos aseguramos de que todos los datos miden lo mismo y
			#rellenamos con el último dato
		datos[i, j]= Datos[npar*i+j]
		
#print(datos) array de datos ordenados de todas las simulaciones
medias= ones_like(datos[0])
for i in range(npar):
	c= zeros_like(datos[0,0])
	for j in range(nsimulaciones):
		c+= datos[j,i]
	medias[i] = c/nsimulaciones
#print(medias) Medias aritméticas en array ordenado
''' En obras
fi = open ('fichero.txt', 'w')
fi.write ('Datos\n')
fi.write (str(datos[0,:,0]))
fi.write ('\nMedias\n')
fi.write (str(medias))
fi.close()
#Pasamos los datos y las medias a un fichero.
'''
fi= open('%4.3f, %s, %1i, %s, %2i.txt'%(d_pobl, distanciamiento_social, potencia_dist, hospitalizacion, nplazas),'w')

#Escritura de parámetros
fi.write(str(width)+'\n')
fi.write(str(height)+'\n')
fi.write(str(nsimulaciones)+'\n')
fi.write(str(fps)+'\n')
fi.write(str(dt)+'\n')
fi.write(str(npar)+'\n')
fi.write(str(Velocidad)+'\n')

fi.write(str(npacientes)+'\n')
fi.write(str(radmax)+'\n')
fi.write(str(d_pobl)+'\n')

fi.write(str(tinf)+'\n')
fi.write(str(trec)+'\n')
fi.write(str(tmort)+'\n')

fi.write(str(distanciamiento_social)+'\n')
fi.write(str(n_inf_dist)+'\n')
fi.write(str(potencia_dist)+'\n')

fi.write(str(hospitalizacion)+'\n')
fi.write(str(nplazas)+'\n')
fi.write(str(uplazas)+'\n')

fi.write(str(max(b))+'\n')
fi.write(str(ciclos_dia)+'\n')	

#escritura de datos
for i in range(nsimulaciones):
	for j in range(max(b)):
		for k in range(npar):
			fi.write('%6.2f'%(datos[i,k,j])) #Todas las simulaciones
		fi.write('\n')
for j in range(max(b)):
	for k in range(npar):
		fi.write('%6.2f'%(medias[k,j]))
	fi.write('\n')
fi.close()


