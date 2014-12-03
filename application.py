#coding:cp1252
"""
V 1		Version Beta
V 1.1 	Mejorado el diseño del tablero
V 1.2	Bug del comprobador de espacios arreglado
V 1.3	Faltas de ortografias, tildes y signos arregladas
"""
import random,time, os
from sys import platform,exit


#Tableros
tableroPc = [] 
tableroVsPc = [] 
tableroJugador1 = []
tableroJugador2 = []

#nombres
nombre = []

#Guardar cantidad de barcos restantes
barcosJugador1 ={}
barcosJugador2 ={}

#Puntajes, nombres y seguidos en listas
listaUsuario = []
listaPuntaje = []
listaSeguidos = []

#variable global
seguidas = 0

def leyendoArchivo():
	
	if os.path.exists("highscore.txt"):#El fichero existe
		archivo = open("highscore.txt")
		variable = archivo.read()
		archivo.close()
		cont = 0
		string = ""
		del listaUsuario[:]
		del listaPuntaje[:]
		del listaSeguidos[:]
		while (cont!=len(variable)):
			if (variable[cont]!="," and variable[cont]!="." and variable[cont]!="-"):
				string = string + variable[cont]
				cont+=1
			elif(variable[cont]=="," ):
				cont+=1
				listaUsuario.append(string)
				string = ""
			elif(variable[cont]=="-"):
				cont+=1
				listaPuntaje.append(string)
				string = ""
			elif(variable[cont]=="."):
				cont+=1
				listaSeguidos.append(string)
				string = ""

			
	else: #El fichero no existe
		archivo=open('highscore.txt','w')
		archivo.write("Sebastian,20-5.Cristobal,18-4.Ludwin,16-3.Gerardo,15-2.Oscar,14-1.")
		archivo.close()
		leyendoArchivo()
	return ""

def highscore(nombreUsuario,puntajeTotal,seguidas):
	leyendoArchivo()
	if nombreUsuario in listaUsuario: #ya ha jugado antes
		indexUsuario = listaUsuario.index(nombreUsuario)
		puntajeAnterior = listaPuntaje[indexUsuario]
		seguidosAnterior = listaSeguidos[indexUsuario]
		if int(puntajeAnterior)<=int(puntajeTotal):
			del listaUsuario[indexUsuario]
			del listaPuntaje[indexUsuario]
			del listaSeguidos[indexUsuario]
			makeItOnce = False
			contador = 0
			if int(listaPuntaje[3])>=int(puntajeTotal):# el puntaje es el menor 
				listaPuntaje.append(str(int(puntajeTotal)))
				listaUsuario.append(nombreUsuario)
				if seguidosAnterior > seguidas:
					listaSeguidos.append(seguidosAnterior)
				else:
					listaSeguidos.append(seguidas)
			else: # el puntaje no es el menor
				for x in listaPuntaje:
					if int(puntajeTotal)>= int(x) and makeItOnce==False:
						listaUsuario.insert(contador, nombreUsuario)
						listaPuntaje.insert(contador, str(int(puntajeTotal)))
						if seguidosAnterior > seguidas:
							listaSeguidos.insert(contador,seguidosAnterior)
						else:
							listaSeguidos.insert(contador,seguidas)
						makeItOnce = True
					contador+=1
		nuevoString = ""
		for x in range(5):
			nuevoString = nuevoString + str(listaUsuario[x]) + "," + str(listaPuntaje[x])+"-"+str(listaSeguidos[x])+"."
		archivo = open("highscore.txt", "w")
		archivo.write(nuevoString)
		archivo.close()
	else: #no ha jugado antes
		print u"¡Felicidades! Te haz hecho con el quinto puesto que antes le pertenecía a: " + listaUsuario[4] + "."
		del listaUsuario[4]
		del listaPuntjaje[4]
		del listaSeguidos[4]
		listaUsuario.append(nombreUsuario)
		listaPuntaje.append(puntajeTotal)
		listaSeguidos.append("1")
		nuevoString = ""
		for x in range(5):
			nuevoString = nuevoString + str(listaUsuario[x]) + "," + str(listaPuntaje[x]) + "-" + str(listaSeguidos[x]) + "."
			archivo = open("highscore.txt", "w")
			archivo.write(nuevoString)
			archivo.close()
	mostrarHighscore()

def mostrarHighscore():
	leyendoArchivo()
	print "-----------------------------------------------------------"
	print "-----------------------Top players-------------------------"
	print "-----------------------------------------------------------"
	print "  Nombre\tPuntaje\t\tVictorias seguidas\n"
	for x in range(5):
		if x == 0:
			print str(int(x)+1)+".", str(listaUsuario[x]), "\t", listaPuntaje[x], "\t\t\t", listaSeguidos[x], "\t**BEST PLAYER**"
		else:
			print str(int(x)+1)+".", str(listaUsuario[x]), "\t", listaPuntaje[x], "\t\t\t", listaSeguidos[x]
	time.sleep(3)
	
def limpiarVentana():
	if platform == "linux" or platform == "linux2":    # linux
		clear = os.system("reset")
	elif platform == "win32":    # Windows...
		clear = os.system("cls")
	return clear

def mostrarTablero(tablero):
	print u"\t",
	for x in range(10):
		print str(x+1)+"  ",
	print u"\n"
	cont = 1
	print u"\t--------------------------------------"
	for x in tablero:
		print cont,"\t",
		print u" | ".join(x)
		print u"\t--------------------------------------"
		cont += 1
def nuevoJuego():#elimina todo el contenido de todo y luego vuelve a asignarlos
	del tableroPc[:]
	del tableroVsPc[:]
	del tableroJugador1[:]
	del tableroJugador2[:]
	del nombre[:]
	barcosJugador1.clear()
	barcosJugador2.clear()
		
	for x in range(1,6):
		barcosJugador1[str(x)]=x
		barcosJugador2[str(x)]=x
		
	for x in range(0,10):
		tableroPc.append(["0"]*10)
		tableroVsPc.append(["0"]*10)
		tableroJugador1.append(["0"]*10)
		tableroJugador2.append(["0"]*10)
		
def esconderBarcos():
	#escondiendo barcos
	nuevoJuego()
	finEscondido = False
	longBarco = 5
	while (finEscondido == False):
		orientacion = random.randint(0,1)#si es 1, pone barco horizontal, si es 0, vertical
		columna = random.randint(0,(10-longBarco))
		fila = random.randint(0,(10-longBarco))
		tablero = tableroPc
		if (orientacion ==1 and comprobadorEspacios(columna, fila, orientacion, longBarco,tablero)==True and longBarco>0):
			cont =  0
			while(cont!=longBarco):
				tablero[fila][columna]=str(longBarco)
				columna+=1
				cont+=1
			longBarco-=1
		elif(orientacion == 0 and comprobadorEspacios(columna, fila, orientacion, longBarco, tablero)==True and longBarco>0):
			cont =  0
			while(cont!=longBarco):
				tablero[fila][columna]=str(longBarco)
				fila+=1
				cont+=1
			longBarco-=1
		if longBarco==0:
			finEscondido = True

def comprobadorEspacios(columna,fila,orientacion,longBarco, tablero):
	try:
		posicionFila = 0
		posicionColumna = 0
		if orientacion == 1: #horizontal
			tablero[fila][columna+(longBarco-1)] #comprobar si el barco cabe
			for x in tablero:
				if (fila == posicionFila):
					for y in x:
						if (columna==posicionColumna and longBarco!=0):
							longBarco-=1
							if (y!="0"):
								return False
						elif(longBarco!=0):
							posicionColumna +=1
				posicionFila+=1
					
		elif orientacion == 0: #vertical
			tablero[fila+(longBarco-1)][columna] #comprobar si el barco cabe
			for x in tablero:
				if posicionFila==fila and longBarco!=0:
					longBarco-=1
					if x[columna]=="1" or x[columna]=="2" or x[columna]=="3" or x[columna]=="4" or x[columna]=="5":
						return False
				elif longBarco!=0:
					posicionFila+=1
		return True
	except IndexError:
		return False

class unJugador(object):
	def __init__(self):
		pass
	def jugar(self):
		esconderBarcos()
		leyendoArchivo()
		vidas = 2
		juegoTerminado = False
		aciertos = 0
		turno = 1
		limpiarVentana()
		puntajeTotal = 0
		print u"""Instrucciones específicas:
1. Cada vez que le aciertes a alguna parte del barco, recibirás un punto.
2. Al hundir el barco, dependiendo de la longitud del barco, se te agregará esa cantidad de puntos.
3. Solamente si logras vencer a la computadora, entrarás en el listado de puntajes altos.
  3.1 Si ya haz jugado antes y estás en el listado, recuerda usar tu mismo nombre para acumular más puntos.
  3.2 Si quedas quinto, corres el riesgo de perder tu puesto, ya que si alguien más gana, tu puntaje será eliminado sin importar cuantos puntos tenías. ¡Así que asegurate de no quedar en el último puesto!
4. Por cada vez que falles, se te restara 1 punto.

		"""
		nombreUsuario = raw_input("[Ingresa tu nombre] ")
		if nombreUsuario in listaUsuario:
			print "Cargando tus datos... Espera porfavor..."
			time.sleep(1)
			indexUsuario = listaUsuario.index(nombreUsuario)
			puntajeTotal = int(listaPuntaje[indexUsuario])
			print u"¡Cargado exitosamente!"
			time.sleep(1)
		print u"Bienvenido abordo capitán", str(nombreUsuario)+"."
		print u"Procediendo a esconder los barcos... ¡No veas!"
		time.sleep(3)
		while (vidas>=0 and juegoTerminado==False):
			limpiarVentana()

			print u"Turno #", turno
						
			mostrarTablero(tableroVsPc)
			#print u"------------------------------"
			#mostrarTablero(tableroPc)
			time.sleep(1)
			print ""
			for x in barcosJugador1:
				if barcosJugador1[x]!=0:
					print u"Te falta hundir el barco de ", x,"casillas"
			try:#error si ingresa letras
				valido = False
				while valido == False:
					colusu = int(raw_input("[Ingrese columna] "))-1
					filusu = int(raw_input("[Ingrese fila] "))-1
					if colusu>=0 and filusu>=0:
						valido = True
						
					else:
						print u"¡Capitán, le recuerdo que el tablero es de 1 a 10!"
						pausa = raw_input("[Presiona enter para continuar...]")
				
				try:#error si esta afuera del rango
					if tableroVsPc[filusu][colusu]=="X" or tableroVsPc[filusu][colusu]=="*":
						print u"Capitán el mar a afectado su orientación... ¡Ya hemos tirado ahí antes! Vuelva a intentarlo..."
						time.sleep(2)
					else:
						if tableroPc[filusu][colusu]=="1":
							print u"¡KABOOOOOOM! ¡Impacto confirmado mi capitán! ¡Continue asi!"
							time.sleep(2)
							tableroVsPc[filusu][colusu]="*"
							aciertos+=1
							a = barcosJugador1["1"]
							barcosJugador1["1"]=a-1
							puntajeTotal +=1
							if barcosJugador1["1"]==0:
								print u"¡CAPITÁN! Hemos hundido el barco de 1 casilla!"
								puntajeTotal +=1
								time.sleep(2)
						elif tableroPc[filusu][colusu]=="2":
							print u"¡KABOOOOOOM! ¡Impacto confirmado mi capitán! ¡Continue así!"
							time.sleep(2)
							tableroVsPc[filusu][colusu]="*"
							aciertos+=1
							a = barcosJugador2["2"]
							barcosJugador2["2"]=a-1
							puntajeTotal += 1
							if barcosJugador2["2"]==0:
								print u"¡CAPITÁN! Hemos hundido el barco de 2 casillas!"
								puntajeTotal += 2
								time.sleep(2)
						elif tableroPc[filusu][colusu]=="3":
							print u"¡KABOOOOOOM! ¡Impacto confirmado mi capitán! ¡Continue así!"
							time.sleep(2)
							tableroVsPc[filusu][colusu]="*"
							aciertos+=1
							a = barcosJugador2["3"]
							barcosJugador2["3"]=a-1
							puntajeTotal+=1
							if barcosJugador2["3"]==0:
								print u"¡CAPITÁN! Hemos hundido el barco de 3 casillas!"
								puntajeTotal+=3
								time.sleep(2)
						elif tableroPc[filusu][colusu]=="4":
							print u"¡KABOOOOOOM! ¡Impacto confirmado mi capitán! ¡Continue así!"
							time.sleep(2)
							tableroVsPc[filusu][colusu]="*"
							aciertos+=1
							a = barcosJugador2["4"]
							barcosJugador2["4"]=a-1
							puntajeTotal+=1
							if barcosJugador2["4"]==0:
								print u"¡CAPITÁN! Hemos hundido el barco de 4 casillas!"
								puntajeTotal+=4
								time.sleep(2)
						elif tableroPc[filusu][colusu]=="5":
							print u"¡KABOOOOOOM! ¡Impacto confirmado mi capitán! ¡Continue así!"
							time.sleep(2)
							tableroVsPc[filusu][colusu]="*"
							aciertos+=1
							a = barcosJugador2["5"]
							puntajeTotal+=1
							barcosJugador2["5"]=a-1
							if barcosJugador2["5"]==0:
								print u"¡CAPITÁN! Hemos hundido el barco de 5 casillas!"
								puntajeTotal+=5
								time.sleep(2)
						elif tableroPc[filusu][colusu]=="0":
							if puntajeTotal-1>=0:
								puntajeTotal-=1
							print u"*Mensaje de la embarcación recibida*"
							time.sleep(1)
							print u"*Abriendo...*"
							time.sleep(1)
							print u"¡LERO LERO! ¡No me dieron!"
							time.sleep(2)
							vidas-=1
							print u"Te quedan:",vidas,"vidas!"
							time.sleep(2)
							tableroVsPc[filusu][colusu]="X"
						print u"Tu puntuaje actual es de:", puntajeTotal,"puntos."
						time.sleep(2)
						turno+=1
				except IndexError:
					print u"Capitán el mar a afectado su orientación... ¡Los barcos no estan por allá! Vuelva a intentarlo..."
					pausa = raw_input("[Presiona enter para continuar...]")

			except ValueError:
				print u"Capitán, no entiendo sus coordenadas... ¡Vuelva a repetirmelas porfavor!"
				pausa = raw_input("[Presiona enter para continuar...]")
			if juegoTerminado == True:
				print u"[F] [E] [L] [I] [C] [I] [D] [A] [D] [E] [S] [!]\nEres el sobreviviente de esta feroz batalla naval!"
				pausa = raw_input("[Presiona enter para continuar...]")
				seguidas+=1
				highscore(nombreUsuario,puntajeTotal,seguidas)
				menu()
			elif juegoTerminado == False and vidas == 0:
				limpiarVentana()
				seguidas = 0
				print u"¡MUAHAHAHAHAHA! ¡Haz perdido contra nuestra embarcación ninja! ¡Mejor suerte para la próxima!"
				pausa = raw_input("[Presiona enter para continuar...]")
				if nombreUsuario in listaUsuario:
					highscore(nombreUsuario,puntajeTotal, seguidas)
				else:
					mostrarHighscore()
				menu()

class dosJugadores(object):
	def __init__(self):
		pass
	def jugar(self):
		nuevoJuego()
		for jugador in range(0,2):
			longBarco = 5
			limpiarVentana()
			print u"Bienvenido capitanes, marineros y turistas al evento del siglo!!!\n\n\t\t\tBienvenidos a ¡BATALLA NAVAL!\n\n¡Ya preparamos nuestros motores, arreglamos las velas y levantemos las anclas! ¡Lo único que nos falta son los nombres de las embarcaciones!\n"

			if jugador == 0:
				finEscondido = False
				nombreJugador = raw_input(u"Como se llamara su embarcacion? ")
				nombre.append(nombreJugador)
				jugadorTablero = tableroJugador1
			elif jugador == 1:
				finEscondido = False
				nombreJugador2 = raw_input(u"Como se llamara la embarcacion contrincante? ")
				nombre.append(nombreJugador2)
				jugadorTablero = tableroJugador2
			while (finEscondido == False and longBarco>=0):
				try:
					valido = False
					while valido == False:
						valido = False
						limpiarVentana()
						print u"Marineros de la embarcación '"+str(nombre[jugador])+u"', '¡vayan a sus puestos! ¡Hora de zarpar!\nA continuación posiciona tu embarcación:\n"
						mostrarTablero(jugadorTablero)
						print u"Recuerda, la colocación se hace automaticamente. Solo especifica las coordenadas y hacia donde quieres que vaya (vertical u horizontal)\n"
						orientacion = (raw_input("Quieres poner en 'horizontal' o 'vertical' su barco de "+str(longBarco)+ " casillas? ")).lower()
						columna = int(raw_input("[Ingrese columna] "))-1
						fila = int(raw_input("[Ingrese fila] "))-1
						if columna>=0 and fila >=0:
							if orientacion =="horizontal" or orientacion == "1":
								orientacion = 1
								valido = True
							elif orientacion == "vertical" or orientacion == "0":
								orientacion = 0
								valido = True
							else:
								print u"Error, porfavor ingrese 'horizontal' o 'vertical'"
								pausa = raw_input("[Presiona enter para continuar...]")
								valido = False
						else:
							print u"Capitán, le recuerdo que el tablero es de 1 a 10!"
							pausa = raw_input("[Presiona enter para continuar...]")
							valido = False
					if(comprobadorEspacios(columna, fila, orientacion, longBarco, jugadorTablero)==False):
						print u"¡Capitán! ¡No puede colocar barcos ahí! Intente en otro lugar..."
						pausa = raw_input("[Presiona enter para continuar...]")
					elif (orientacion ==1 and longBarco>0):
						cont =  0
						while(cont!=longBarco):
							jugadorTablero[fila][columna]=str(longBarco)
							columna+=1
							cont+=1
						longBarco-=1
						
					elif(orientacion == 0 and longBarco>0):
						cont =  0
						while(cont!=longBarco):
							jugadorTablero[fila][columna]=str(longBarco)
							fila+=1
							cont+=1
						longBarco-=1
					if longBarco==0:
						finEscondido = True
					
				except (IndexError, ValueError) as e:
					print u"Ingreso incorrecto o no hay espacios suficientes, vuelva a intentarlo..."
					pausa = raw_input("[Presione enter para continuar...]")
		print u"¡Todo está listo mis capitanes! ¡Hora de zarpar hacia la batalla! ¡AAAARG!"
		pausa = raw_input("[Presiona enter para continuar...]")
	
		batallaEmpieza()

def batallaEmpieza():
	
	turno = 0
	aciertos1 = 0
	aciertos2 = 0
	while aciertos1 != 15 or aciertos2!=15:
		limpiarVentana()

		if turno%2==0:
			miTablero = tableroJugador1
			suTablero = tableroVsPc
			aciertaBarco = tableroJugador2
			listaBarcos = barcosJugador2
			aciertosJugador = aciertos1
			nombreUsuario = nombre[0]

		if turno%2!=0:
			miTablero = tableroJugador2
			suTablero = tableroPc
			aciertaBarco = tableroJugador1
			listaBarcos = barcosJugador1
			aciertosJugador = aciertos2
			nombreUsuario = nombre[1]
		print "Mi tablero: "
		mostrarTablero(miTablero)
		print u"///////////////////////////"
		print "Tablero enemigo: "
		mostrarTablero(suTablero)
		print u"Turno #", int(round((turno/float(2)),0))
		print u"¡Es el turno de la tripulación '", nombreUsuario, "' para tirar!\n"
		for x in listaBarcos:
			if listaBarcos[x]!=0:
				print u"Te falta hundir el barco de ", x,"casillas"
		time.sleep(1)
		try:#error si ingresa letras
			valido = False
			while valido == False:
				colusu = int(raw_input("[Ingrese columna] "))-1
				filusu = int(raw_input("[Ingrese fila] "))-1
				if colusu>=0 and filusu >=0:
					valido = True
				else:
					print u"Capitán, le recuerdo que el tablero es de 1 a 10!"
					pausa = raw_input("[Presiona enter para continuar...]")

			try:#error si esta afuera del rango
				if suTablero[filusu][colusu]=="X" or tableroVsPc[filusu][colusu]=="*":
					print u"Capitán el mar a afectado su orientación... Ya hemos tirado ahi antes! Vuelva a intentarlo..."
					time.sleep(2)
				else:
					if aciertaBarco[filusu][colusu]=="1":
						print u"¡KABOOOOOOM! ¡Impacto confirmado mi capitán! ¡Continue así!"
						time.sleep(2)
						suTablero[filusu][colusu]="*"
						aciertaBarco[filusu][colusu]="*"
						aciertosJugador+=1
						a = listaBarcos["1"]
						listaBarcos["1"]=a-1
						if listaBarcos["1"]==0:
							print u"¡CAPITÁN! Hemos hundido el barco de 1 casilla!"
							time.sleep(2)
					elif aciertaBarco[filusu][colusu]=="2":
						print u"¡KABOOOOOOM! ¡Impacto confirmado mi capitán! ¡Continue así!"
						time.sleep(2)
						suTablero[filusu][colusu]="*"
						aciertaBarco[filusu][colusu]="*"
						aciertosJugador+=1
						a = listaBarcos["2"]
						listaBarcos["2"]=a-1
						if listaBarcos["2"]==0:
							print u"¡CAPITÁN! Hemos hundido el barco de 2 casillas!"
							time.sleep(2)
					elif aciertaBarco[filusu][colusu]=="3":
						print u"¡KABOOOOOOM! ¡Impacto confirmado mi capitán! ¡Continue así!"
						time.sleep(2)
						suTablero[filusu][colusu]="*"
						aciertaBarco[filusu][colusu]="*"
						aciertosJugador+=1
						a = listaBarcos["3"]
						listaBarcos["3"]=a-1
						if listaBarcos["3"]==0:
							print u"¡CAPITÁN! Hemos hundido el barco de 3 casillas!"
							time.sleep(2)
					elif aciertaBarco[filusu][colusu]=="4":
						print u"¡KABOOOOOOM! ¡Impacto confirmado mi capitán! ¡Continue así!"
						time.sleep(2)
						suTablero[filusu][colusu]="*"
						aciertaBarco[filusu][colusu]="*"
						aciertosJugador+=1
						a = listaBarcos["4"]
						listaBarcos["4"]=a-1
						if listaBarcos["4"]==0:
							print u"¡CAPITÁN! Hemos hundido el barco de 4 casillas!"
							time.sleep(2)
					elif aciertaBarco[filusu][colusu]=="5":
						print u"¡KABOOOOOOM! ¡Impacto confirmado mi capitán! ¡Continue así!"
						time.sleep(2)
						suTablero[filusu][colusu]="*"
						aciertaBarco[filusu][colusu]="*"
						aciertosJugador+=1
						a = listaBarcos["5"]
						listaBarcos["5"]=a-1
						if listaBarcos["5"]==0:
							print u"¡CAPITÁN! Hemos hundido el barco de 5 casillas!"
							time.sleep(2)
					elif aciertaBarco[filusu][colusu]=="0":
						print u"*Mensaje de la embarcación enemiga recibida*"
						time.sleep(1)
						print u"*Abriendo...*"
						time.sleep(2)
						print u"¡LERO LERO! ¡No me dieron!"
						time.sleep(1)
						suTablero[filusu][colusu]="X"
						aciertaBarco[filusu][colusu]="X"
						turno+=1
					contBarcos = 0
					for x in listaBarcos:
						if listaBarcos[x] == 0:
							contBarcos+=1
							if contBarcos==5:
								print u"¡Felicidades a la tripulación '",nombreUsuario,u"'. ¡Son los sobrevivientes de esta batalla naval!"
								pausa = raw_input("[Presiona enter para continuar...]")
								menu()

			except IndexError:
				print u"¡CAPITÁN! ¡¿Acaso se ha pasado de copas?! ¡Por allá no estan los barcos! Vuelva a intentarlo..."
				pausa = raw_input("[Presiona enter para continuar...]")
		except ValueError:
			print u"¡Solo se permiten números!"
			pausa = raw_input("[Presiona enter para continuar...]")
musicaFondoUnaVez = False
def menu():

	limpiarVentana()
	print"""
                                     # #  ( )
                                  ___#_#___|__
                              _  |____________|  _
                       _=====| | |            | | |==== _
                 =====| |.---------------------------. | |====
   <--------------------'   .  .  .  .  .  .  .  .   '--------------/
     \                PROYECTO FINAL - BATALLA NAVAL               /
      \                     POR FRANK SAM HU                      /
       \_________________________________________________________/
  wwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww
wwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww
   wwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww 
"""
	time.sleep(5)
	limpiarVentana()
	print u"""
Instrucciones:
-El objetivo de este juego es hundir los barcos del contrincante, escondidos en alguna parte del tablero de 10 por 10.
-Los barcos tienen diferentes dimensiones, siendo el mas grande de 5 casillas, y el mas pequeño de 1 casilla.
-Para darle a un barco, debes dar las coordenadas 'X' (columna) y 'Y' (fila). 
-Si hay un barco en dicha posición, aparecerá un asterisco (*) en el tablero.
-Si no hay un barco en esa posición, aparecerá una equis (X) en el tablero.
-Para colocar los barcos, solamente debes establecer en que coordenada quieres que este la proa y hacia que direccion (vertical u horizontal).

Por favor, elija una opción:
1. Un jugador
2. Dos jugadores
3. Mostrar puntajes
4. Salir
"""
	try:
		opcionesMenu = {"un jugador":unJugador, "dos jugadores":dosJugadores}
		print u"Ingrese opción: "
		opcion = raw_input().lower()
		if opcion == "1":
			opcion = "un jugador"
		elif opcion == "2":
			opcion = "dos jugadores"
		elif opcion=="3":
			mostrarHighscore()
			menu()
		elif opcion == "4" or opcion == "salir":
			print u"¿Qué? ¿Tan pronto se retiran? Bueno... ¡Hasta la proxima será!"
			raw_input("Presione enter para salir...")
			exit(0)
		varialbe = opcionesMenu[opcion]() 
		varialbe.jugar()
	except KeyError:
		pausa = raw_input("Error, opcion no válida. Intente nuevamente.\nPresione enter para continuar...")
		menu()
try:
	limpiarVentana()
	import pygame
	if musicaFondoUnaVez == False:
		musicaFondoUnaVez = True
		pygame.init()
		pygame.display.set_mode((1,1))
		pygame.mixer.music.load("backgroundmusic.mp3")
		pygame.mixer.music.play(-1)
except ImportError:
	print "Error. No se encontro la libreria pygame. Procediendo a ejecutar el juego sin musica..."
	time.sleep(3)
	limpiarVentana()

menu()

