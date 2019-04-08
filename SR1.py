import struct
from collections import namedtuple

def char(c):
	return struct.pack("=c",c.encode('ascii'))
def word(c):
	return struct.pack("=h",c)
def dword(c):
	return struct.pack("=l",c)
def color(r,g,b):
	return bytes([b,g,r])



class Bitmap(object):
	def __init__(self, width,height):
		self.width = width
		self.height = height
		self.Initx = 0
		self.Inity = 0
		self.vpwidth = 0
		self.vpheight = 0
		self.r1 = 0
		self.g1 = 0
		self.b1 = 0
		self.r2 = 255
		self.g2 = 255
		self.b2 = 255
		self.framebuffer = []
		self.clear()


	def clear(self):
		self.framebuffer = [[color(self.r1,self.g1,self.b1) for x in range(self.width)] for y in range(self.height)]
	def clearColor(self,a,c,d):
		self.r1 = int(round(a *255.0)) 
		self.g1 = int(round(c *255.0))
		self.b1 = int(round(d *255.0))

	def gwidth(self):
		return self.width

	def gheight(self):
		return self.height
	def ViewPort(self,x, y, ancho, alto):
		self.Initx = x + (ancho/2)
		self.Inity = y + (alto/2)
		self.vpheight = alto/2 
		self.vpwidth = ancho/2
		
	def changeColor(self,z,x,y):
		self.r2 = int(round(z *255.0)) 
		self.g2 = int(round(x *255.0))
		self.b2 = int(round(y *255.0))
		
	def createFile(self, filename):
		f = open(filename, 'wb')

		#file header
		f.write(char('B'))
		f.write(char('M'))
		f.write(dword(54 + self.width * self.height *3))
		f.write(dword(0))
		f.write(dword(54))

		#image header 40
		f.write(dword(40))
		f.write(dword(self.width))
		f.write(dword(self.height))
		f.write(word(1))
		f.write(word(24))
		f.write(dword(0))
		f.write(dword(self.width * self.height *3))	
		f.write(dword(0))
		f.write(dword(0))
		f.write(dword(0))
		f.write(dword(0))

		for x in range(self.height):
			for y in range(self.width):
				f.write(self.framebuffer[x][y])

		f.close()
		
	def vertex(self, x, y):
		self.framebuffer[int(round((self.Inity + (y * self.vpheight))))][int(round((self.Initx + (x * self.vpheight))))] = color(self.r2,self.g2,self.b2)

	def punto(self, x, y):
		self.framebuffer[ y ][ x ] = color(self.r2,self.g2,self.b2)

	def puntofz(self, x1, y1, color):
		x1 += round(self.width/8)
		y1 -= 10
		try:
			self.framebuffer[ y1 ][ x1 ] = color
		except:
			pass

	def line_float(self,x1,y1,x2,y2):
		if x1 >=-1 and y1 >=-1 and x2 >=-1 and y2 >=-1 and x1 <=1 and y1 <=1 and x2 <=1 and y2<=1:
			x1 *= self.width/2
			x2 *= self.width/2
			y1 *= self.height/2
			y2 *= self.height/2
			x1 = round(x1)
			x2 = round(x2)
			y1 = round(y1)
			y2 = round(y2)

			x1 += round(self.width/2)
			x2 += round(self.width/2)
			y1 += (round(self.height/2)) -1
			y2 += (round(self.height/2)) -1

			dy = abs(y2-y1)
			dx = abs(x2-x1)
			
			steep = dy >dx
			
			if steep:
				x1,y1 = y1,x1
				x2,y2 = y2,x2

			if x1>x2:
				x1,x2 = x2,x1
				y1,y2 = y2,y1

			dy = abs(y2-y1)
			dx = abs(x2-x1)

			offset = 0 *2 *dx
			threshold =0.5 *2 *dx
			y = y1

			for x in range(x1,x2, +1):

				if steep:
					point(y,x)
				else:
					point(x,y)  
				offset += dy
				if offset >= threshold:
					y +=1 if y1 <y2 else -1
					threshold +=1 *dx
		else:
			print("solo puede ingresar valores entre -1 y 1")

	def line_in(self,x1,y1,x2,y2):

		dy = abs(y2-y1)
		dx = abs(x2-x1)

		steep = dy >dx

		if steep:
			x1,y1 = y1,x1
			x2,y2 = y2,x2

		if x1>x2:
			x1,x2 = x2,x1
			y1,y2 = y2,y1

		dy = abs(y2-y1)
		dx = abs(x2-x1)

		offset = 0 *2 *dx
		threshold =0.5 *2 *dx
		y = y1

		for x in range(x1,x2, +1):

			if steep:
				point(y,x)
			else:
				point(x,y)  
			offset += dy
			if offset >= threshold:
				y +=1 if y1 <y2 else -1
				threshold +=1 *dx

	def pointbz(self, x, y, color):
		self.framebuffer[x][y] = color

class Texture(object):
    def __init__(self, path):
        self.path = path
        self.read()

    def read(self):
        image = open(self.path, "rb")
        image.seek(2 + 4 + 4)
        header_size = struct.unpack("=l", image.read(4))[0]
        image.seek(2 + 4 + 4 + 4 + 4)        
        self.width = struct.unpack("=l", image.read(4))[0]
        self.height = struct.unpack("=l", image.read(4))[0]
        self.pixels = []

        image.seek(header_size)

        for y in range(self.height):
            self.pixels.append([])
            for x in range(self.width):
                b = ord(image.read(1))
                g = ord(image.read(1))
                r = ord(image.read(1))

                self.pixels[y].append(color(r,g,b))

        image.close()

    def get_color(self, tx, ty, intensity=1):
        x = int(tx * self.width)
        y = int(ty * self.height)

        return self.pixels[y][x]

var = None
def get_var():
	return var
	
def glCreateWindow(width, height):
	global var
	var = Bitmap(width,height)
	
def glViewPort(x, y, width, height):
	var.ViewPort(x,y, width, height)
	
def glClear():
	var.clear()
	
def glClearColor(r, g, b):
	var.clearColor(r,g,b)
	
def  glVertex(x, y):
	var.vertex(x,y)
	
def  glColor(r, g, b):
	var.changeColor(r,g,b)
	
def point(x,y):
	var.punto(x,y)
	
def glline_fl(x1,y1,x2,y2):
	var.line_float(x1,y1,x2,y2)
	
def glLine(x1,y1,x2,y2):
	var.line_in(x1,y1,x2,y2)


def glFinish():
	var.createFile("out.bmp")

def pointf(x, y, color):
	var.puntofz(x, y, color)
def getwidth():
	return var.gwidth()

def getheight():
	return var.gheight()
	
