import viz
import vizact
import vizinfo
import vizcam

# SETTINGS INICIALES #

viz.MainWindow.visible(viz.OFF) #Hago invisible la main window
viz.setMultiSample(8) # FSAA de 8
viz.fogcolor = viz.BLACK # Color de sombra = negro
viz.fog(0.15) # Agrega sombra de tipo exponencial
viz.collision(viz.ON) # Habilita colisiones en el mundo

#Subventana que renderea viz.MainWindow
mainSceneWindow = viz.addWindow()
mainSceneWindow.setSize(0.7,1)
mainSceneWindow.setPosition(0,1)
mainSceneWindow.fov(viz.MainWindow.getVerticalFOV()) # Coloca el FOV de la ventana principal en la actual

#Creando una ventana y un punto de vista para la camara
cameraWindow = viz.addWindow(pos =[.7,1],size=(0.4,1)) #Creando la ventana
cameraWindowView = viz.addView() #Creando un viewpoint
cameraWindowView.setScene(2) #Poniendo la nueva ventana en la escena 2
cameraWindow.setView(cameraWindowView) #Ligando el viewpoint con la nueva ventana

#Importar libreria de AR
ar = viz.add('artoolkit.dle')

#Vincular camara web a plugin de AR
cam = ar.addWebCamera(window=cameraWindow) #Agregando una camara en la ventada nueva

#Fullscreen no funciona en version trial
#viz.window.setFullscreen(mode = viz.ON)
#viz.go(viz.FULLSCREEN)

viz.go()

# FIN DE SETTINGS INICIALES #

#IDEA = hotspots para hacer trigger al cambio en lugar de callbacks
#IDEA = agregar recursos como musica y objetos a las locations con sus valores; objetos tienen sus propios atributos como musica, nombre, posicion inicial; desde el archivo
#IDEA = hacer una estructura de control para AR marks
#IDEA = hacer una estructura de control para movimiento
# HABILITAR Colisiones
# Sonido en 3d
# Baking de texturas
# Luces y sombras
# todo lo que se agrega en una localidad se debe retirar incluyendo objetos y musica antes de agregar el otro

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
	
def arMarkerLoader():
	# Creando un logo en la escena 2 (AR)
	mark = cam.addMatrixMarker(0, width=1000) #Creando la Marca
	logo = viz.add("logo.ive",viz.WORLD, 2) #Creando el logo en la escena 2
	viz.link(mark, logo) #Ligando la marca y el logo

def main():
	global loc_list
	global active_location
	loc_list = []
	initializer(loc_list)
	arMarkerLoader()
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
	