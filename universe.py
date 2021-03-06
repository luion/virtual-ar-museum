﻿import viz
import vizact
import vizinfo
import vizcam
import math

#Importar libreria de AR
ar = viz.add('artoolkit.dle')

#Importar libreria de wiimote
wii = viz.add('wiimote.dle')

viz.go()

loc_list = []
active_location = None

class location:
	def __init__(self):
		self.space_object = None
		self.space_name = None
		self.id = 0

	def removeLocation(self):
		self.space_object.remove()

	def addLocation(self):
		self.space_object = viz.add(self.space_name)
		
	def initializeLocation(self, identifier, space_name):
		self.space_name = space_name
		self.id = identifier


#Detects and ensures that the Wii NUNCHUCK is connected.
def onConnect(e):
	global should_it_run
	print "The extension device has been connected."
	if (e.extension == wii.EXT_NUNCHUK):
		print "The Wii NUNCHUCK has been pluged in."
		#Rumble wiimote for 0.5 seconds when nunchuk is connected
		e.object.setRumble(True, 0.5)
		should_it_run = True
		message_screen.visible(viz.OFF)
	else:
		print "Please plug-in the Wii NUNCHUCK."
		message_screen.texture(nunchuck_disconnect_screen)
		message_screen.visible(viz.ON)
		should_it_run = False

#Detects a disconect event and ensures that the NUNCHUCK is connected again.
def onDisconnect(e):
	global should_it_run
	print "The extension device has been disconnected."
	if (e.extension == wii.EXT_NUNCHUK):
		print "Please plug-in the Wii NUNCHUCK again."
		message_screen.texture(nunchuck_disconnect_screen)
		message_screen.visible(viz.ON)
		should_it_run = False
	else:
		print "Please plug-in the Wii NUNCHUCK."
		message_screen.texture(nunchuck_disconnect_screen)
		message_screen.visible(viz.ON)
		should_it_run = False

def moveCamera(nunchuck_wiimote, should_it_run):
	x,y,z = nunchuck_wiimote.position
	cam_x,cam_y,cam_z = viz.MainView.getEuler()
	#nunchuck_wiimote.deadZone = (0.01031,0.01031)#Zona de 0,0 sin mover
	if nunchuck_wiimote.state == 0 and should_it_run == True:
		if(math.fabs(x) > 0.025):
			viz.MainView.move([x*0.1,0,0],viz.BODY_ORI)
		if(math.fabs(y) > 0.025):
			viz.MainView.move([0,0,y*0.1],viz.BODY_ORI)
		else:
			pass
	if nunchuck_wiimote.state == wii.NUNCHUK_C and should_it_run == True:
		viz.MainView.setEuler([x,0,0],viz.BODY_ORI,viz.REL_PARENT)
		if cam_y <= 30:
			viz.MainView.setEuler([0,-y,0],viz.HEAD_ORI,viz.REL_PARENT)

def wiiButtonManager(wiimote, nunchuck_wiimote, should_it_run, message_screen):
	if wiimote.state == wii.BUTTON_HOME and wiimote.getExtension() == wii.EXT_NUNCHUK: #Button HOME con NUNCHUCK conectado
		message_screen.texture(pause_screen)
		if should_it_run:
			message_screen.visible(viz.ON)
		else:
			message_screen.visible(viz.OFF)
		should_it_run = not should_it_run
	elif should_it_run == True:
		if nunchuck_wiimote.state == wii.NUNCHUK_C:
			print "C"
		if nunchuck_wiimote.state == wii.NUNCHUK_Z:
			print "Z"
		if wiimote.state == wii.BUTTON_UP:
			print "UP"
		if wiimote.state == wii.BUTTON_DOWN:
			print "DOWN"
		if wiimote.state == wii.BUTTON_LEFT:
			print "LEFT"
		if wiimote.state == wii.BUTTON_RIGHT:
			print "RIGHT"
		if wiimote.state == wii.BUTTON_A:
			print "A"
		if wiimote.state == wii.BUTTON_B:
			print "B"
		if wiimote.state == wii.BUTTON_PLUS:
			print "+"
		if wiimote.state == wii.BUTTON_MINUS:
			print "-"
		if wiimote.state == wii.BUTTON_HOME:
			print "Home"
		if wiimote.state == wii.BUTTON_1:
			print "1"
		if wiimote.state == wii.BUTTON_2:
			print "2"

def init_settings(mainSceneWindow, cameraWindow, cameraWindowView, cam, pause_screen, nunchuck_disconnect_screen, message_screen, wiimote, nunchuck_wiimote, should_it_run):
	viz.MainWindow.visible(viz.OFF) #Hago invisible la main window
	viz.setMultiSample(8) # FSAA de 8
	viz.fogcolor = viz.BLACK # Color de sombra = negro
	viz.fog(0.15) # Agrega sombra de tipo exponencial
	viz.collision(viz.ON) # Habilita colisiones en el mundo
	viz.phys.enable() # Habilita la fisica

	#Desabilita mouse
	viz.mouse.setOverride(viz.ON)

	#Mouse invisible
	viz.mouse.setVisible(viz.OFF)

	#Subventana que renderea viz.MainWindow
	mainSceneWindow = viz.addWindow()
	mainSceneWindow.setSize(0.7,1)
	mainSceneWindow.setPosition(0,1)
	mainSceneWindow.fov(40, 1.3) # Coloca el FOV de la ventana principal en la actual con los valores de default (40 grados verticales, 1.3 aspect ratio)

	#Creando una ventana y un punto de vista para la camara
	cameraWindow = viz.addWindow(pos =[.7,1],size=(0.4,1)) #Creando la ventana
	cameraWindowView = viz.addView() #Creando un viewpoint
	cameraWindowView.setScene(2) #Poniendo la nueva ventana en la escena 2
	cameraWindow.setView(cameraWindowView) #Ligando el viewpoint con la nueva ventana

	#Vincular camara web a plugin de AR
	cam = ar.addWebCamera(window=cameraWindow) #Agregando una camara en la ventada nueva

	# Configuracion de mensajes de la pantalla
	message_screen = viz.addTexQuad(parent=viz.SCREEN, pos=[0.5,0.5,1], scale=[12.80,10.24,1]) 
	pause_screen = viz.add("PAUSA.png")
	nunchuck_disconnect_screen = viz.add("NUNCHUCK_DISCONNECTED.png")
	message_screen.texture(pause_screen)
	message_screen.visible(viz.OFF) #Cuando should_it_run sea False, viz.ON es el valor a usar.

	# Conecta al primer wiimote disponible
	wiimote = wii.addWiimote()
	# Prende el LED 1 del wiimote
	wiimote.led = wii.LED_1
	# Obten el nunchuck del wiimote
	nunchuck_wiimote = wiimote.nunchuk 

	#Determines wheter the program should run or not.
	#It will run if the Nunchuck is connected; otherwise, it won't.
	should_it_run = True

	#Ensures that the program won't run without the NUNCHUCK plug'd in.
	if(wiimote.getExtension() == wii.EXT_NUNCHUK):
		should_it_run = True
	else:
		print "Please plug-in the Wii NUNCHUCK."
		message_screen.texture(nunchuck_disconnect_screen)
		message_screen.visible(viz.ON)
		should_it_run = False
	
	return mainSceneWindow, cameraWindow, cameraWindowView, cam, pause_screen, nunchuck_disconnect_screen, message_screen, wiimote, nunchuck_wiimote, should_it_run

def initializer(loc_list):
	try:
		f = open("config.txt", "r")
		for line in f:
			line = line.split()
			a_location = location()
			a_location.initializeLocation(int(line[0]), line[1])
			loc_list.append(a_location)
			del a_location	
		f.close()
	except:
		print "Unexpected error: ", sys.exc_info()[0]
		print "File couldn't be read."
	
def arMarkerLoader(cam):
	# Creando un logo en la escena 2 (AR)
	mark = cam.addMatrixMarker(0, width=1000) #Creando la Marca
	logo = viz.add("logo.ive",viz.WORLD, 2) #Creando el logo en la escena 2
	viz.link(mark, logo) #Ligando la marca y el logo

def wiimoteInitializer(wiimote, nunchuck_wiimote, should_it_run, message_screen):
	vizact.onsensordown(wiimote, wii.BUTTON_HOME, wiiButtonManager, wiimote, nunchuck_wiimote, should_it_run, message_screen)
	vizact.onsensordown(wiimote, wii.BUTTON_UP, wiiButtonManager, wiimote, nunchuck_wiimote, should_it_run, message_screen)
	vizact.onsensordown(wiimote, wii.BUTTON_DOWN, wiiButtonManager, wiimote, nunchuck_wiimote, should_it_run, message_screen)
	vizact.onsensordown(wiimote, wii.BUTTON_LEFT, wiiButtonManager, wiimote, nunchuck_wiimote, should_it_run, message_screen)
	vizact.onsensordown(wiimote, wii.BUTTON_RIGHT, wiiButtonManager, wiimote, nunchuck_wiimote, should_it_run, message_screen)
	vizact.onsensordown(wiimote, wii.BUTTON_A, wiiButtonManager, wiimote, nunchuck_wiimote, should_it_run, message_screen)
	vizact.onsensordown(wiimote, wii.BUTTON_B, wiiButtonManager, wiimote, nunchuck_wiimote, should_it_run, message_screen)
	vizact.onsensordown(wiimote, wii.BUTTON_PLUS, wiiButtonManager, wiimote, nunchuck_wiimote, should_it_run, message_screen)
	vizact.onsensordown(wiimote, wii.BUTTON_MINUS, wiiButtonManager, wiimote, nunchuck_wiimote, should_it_run, message_screen)
	vizact.onsensordown(wiimote, wii.BUTTON_1, wiiButtonManager, wiimote, nunchuck_wiimote, should_it_run, message_screen)
	vizact.onsensordown(wiimote, wii.BUTTON_2, wiiButtonManager, wiimote, nunchuck_wiimote, should_it_run, message_screen)
	vizact.onsensordown(wiimote, wii.NUNCHUK_C, wiiButtonManager, wiimote, nunchuck_wiimote, should_it_run, message_screen)
	vizact.onsensordown(wiimote, wii.NUNCHUK_Z, wiiButtonManager, wiimote, nunchuck_wiimote, should_it_run, message_screen)
	
	#Rumble the wiimote while the B button is down
	vizact.onsensordown(wiimote,wii.BUTTON_B,wiimote.setRumble,True)
	vizact.onsensorup(wiimote,wii.BUTTON_B,wiimote.setRumble,False)

def main():
	global loc_list
	global active_location
	loc_list = []
	
	mainSceneWindow = None
	cameraWindow = None
	cameraWindowView = None
	cam = None
	pause_screen = None
	nunchuck_disconnect_screen = None
	message_screen = None
	wiimote = None
	nunchuck_wiimote = None
	should_it_run = None
	
	mainSceneWindow, cameraWindow, cameraWindowView, cam, pause_screen, nunchuck_disconnect_screen, message_screen, wiimote, nunchuck_wiimote, should_it_run = init_settings(mainSceneWindow, cameraWindow, cameraWindowView, cam, pause_screen, nunchuck_disconnect_screen, message_screen, wiimote, nunchuck_wiimote, should_it_run)
	
	vizact.ontimer(0, moveCamera, nunchuck_wiimote, should_it_run)
	viz.callback(wii.EXT_CONNECT_EVENT,onConnect)
	viz.callback(wii.EXT_DISCONNECT_EVENT,onDisconnect)
	
	initializer(loc_list)
	arMarkerLoader(cam)
	wiimoteInitializer(wiimote, nunchuck_wiimote, should_it_run, message_screen)
	
	viz.go() # Inicia VIZ
	
	for item in loc_list:
		if item.space_name == "piazza.osgb":
			active_location = item
			item.addLocation()

def removeAdd(key):
	global loc_list
	global active_location
	for item in loc_list:
		if item.id == 1:
			active_location.removeLocation()
			active_location = item
			item.addLocation()

viz.callback(viz.KEYDOWN_EVENT, removeAdd)

if __name__ == '__main__':
	main()
	