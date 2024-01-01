#Lector de datos
from numpy import *
import matplotlib.pyplot as plt

cont= 'S'
while cont== 'S':
	a= input('Introduzca nombre de fichero (sin .txt): ')

	fi= open(str(a)+'.txt', 'r')
	
#Lectura de parámetros
	width= 					eval(fi.readline())
	height= 				eval(fi.readline())
	nsimulaciones= 			eval(fi.readline())
	fps= 					eval(fi.readline())
	dt= 					eval(fi.readline())
	npar= 					eval(fi.readline())
	Velocidad=				eval(fi.readline())

	npacientes= 			eval(fi.readline())
	radmax= 				eval(fi.readline())
	d_pobl= 				eval(fi.readline())

	tinf= 					eval(fi.readline())
	trec= 					eval(fi.readline())
	tmort= 					eval(fi.readline())

	distanciamiento_social= eval(fi.readline())
	n_inf_dist= 			eval(fi.readline())
	potencia_dist=			eval(fi.readline())

	hopitalizacion=			eval(fi.readline())
	nplazas= 				eval(fi.readline())
	uplazas= 				eval(fi.readline())

	max_b= 					eval(fi.readline())
	ciclos_dia= 			eval(fi.readline())

#Creación del array con todas las simulaciones (No usado para el informe)
	datos= ones([nsimulaciones, npar, max_b])
	for i in range(nsimulaciones):
		for j in range(max_b):
			x=fi.readline()
			for k in range(npar):
				datos[i,k,j] = eval(x[6*k : 6*k+6])	
	#print(datos)

#Creación del array de medias usado para las figuras del informe
	medias= ones([npar, max_b])
	for j in range(max_b):
		x=fi.readline()
		for k in range(npar):
			medias[k,j] = eval(x[6*k : 6*k+6])
	fi.close()
	#print(medias)

	t=linspace(0, max_b/ciclos_dia, max_b)
	apoyo= ones_like(t) #Para las asísdotas de apoyo

#Crea 2 subfiguras, la principal y la de ocupación hospitalaria

	f=plt.figure(figsize=(12,6))
	plt.subplot(2,1,1)
	plt.plot(t, medias[0], 'b-', label='susceptibles\n(%5.2f)'%medias[0][-1])
	plt.plot(t, medias[0][-1]*apoyo, 'k--')
	plt.plot(t, medias[1], 'r-', label=u'infectados\nMaximo: %5.2f'%(max(medias[1])))
	plt.plot(t, medias[1][-1]*apoyo, 'k--')
	plt.plot(t, medias[2], 'g-', label='recuperados\n(%5.2f)'%medias[2][-1])
	plt.plot(t, medias[2][-1]*apoyo, 'k--')
	plt.plot(t, medias[3], 'k-', label='fallecidos\n(%5.2f)'%medias[3][-1])
	plt.plot(t, medias[3][-1]*apoyo, 'k--')
	plt.title('Media de %2i simulaciones'%(nsimulaciones))
	plt.xlabel('t (dias)') ; plt.ylabel('Casos')
	plt.legend(loc='right')

	plt.subplot(2,1,2)
	plt.plot(t, medias[4], 'b-', label='Plazas Hospital\n(%3i)\nMínimo: %5.2f'%(medias[4][-1], min(medias[4])))
	plt.plot(t, nplazas*apoyo, 'k--')
	plt.plot(t, medias[5], 'r-', label='Plazas UCI\n(%3i)\nMínimo: %5.2f'%(medias[5][-1], min(medias[5])))
	plt.plot(t, uplazas*apoyo, 'k--')
	plt.xlabel('t (dias)') ; plt.ylabel('Plazas Libres')
	plt.ylim(bottom=0)
	plt.legend(loc='right')

	plt.tight_layout()
	plt.savefig(str(a)+'.png') #Guarda con el mismo nombre que el fichero
	plt.show()
	cont= input('¿Continuamos? (S/N): ')
