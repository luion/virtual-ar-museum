import viz
import vizact
import vizinfo
import vizcam
import vizfx

viz.go()

#IDEA = hotspots para hacer trigger al cambio en lugar de callbacks
#IDEA = agregar recursos como musica y objetos a las locations con sus valores; desde el archivo
#IDEA = hacer una estructura de control para AR marks
#IDEA = hacer una estructura de control para movimiento
# HABILITAR Colisiones
# Sonido en 3d
# Baking de texturas
# Luces y sombras

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
	
def main():
	global loc_list
	global active_location
	loc_list = []
	initializer(loc_list)
	for item in loc_list:
		print item.space_name
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
	
