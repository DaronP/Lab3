from SR1 import *
from math import * 
import copy
from collections import namedtuple
width = 800
x = 0.1
y = 0.1
height = 600
V2 = namedtuple('Vertex2', ['x', 'y'])
V3 = namedtuple('Vertex3', ['x', 'y', 'z'])
zbuffer = [[-99999999999 for x in range(1000)] for y in range(1000)]


def loadModelMatrix(transalte, scale, rotate):
	transalte = V3(*transalte)
	scale = V3(*scale)
	rotate = V3(*rotate)
	translate_matrix=[
		[1,0,0,transalte.x],
		[0,1,0,transalte.y],
		[0,0,1,transalte.z],
		[0,0,0,1]
		]
	scale_matrix = [
			[scale.x,0,0,0],
			[0,scale.y,0,0],
			[0,0,1,scale.z],
			[0,0,0,1]
		]

	a = rotate.x
	rotation_matrix_x =[
			[1,0,0,0],
			[0,cos(a),-sin(a),0],
			[0,sin(a),cos(a),0],
			[0,0,0,1]
		]

	a = rotate.y
	rotation_matrix_y =[
			[cos(a),0,-sin(a),0],
			[0,1,0,0],
			[-sin(a),0,cos(a),0],
			[0,0,0,1]
		]

	a = rotate.z
	rotation_matrix_z =[
			[cos(a),-sin(a),0,0],
			[sin(a),cos(a),0,0],
			[0,0,1,0],
			[0,0,0,1]
		]
	
	rotation_matrix =  mulmat(rotation_matrix_z,mulmat(rotation_matrix_y,rotation_matrix_x))
	#Model = traslate_matrix @ rotation_matrix @ scale_matrix
	model = mulmat(scale_matrix,mulmat(rotation_matrix,translate_matrix))
	
	return model
class Modelobj(object):
	def __init__(self,filename):
		with open(filename) as f:
			self.lines = f.read().splitlines()
		self.vertices = []
		self.tvertices = []
		self.faces = []
		self.normals = []
		

	def read(self):
		#global view
		for line in self.lines:
			if line:
				prefix, value = line.split(' ',1)

				if prefix == 'v':
					self.vertices.append(list(map(float,value.split(' '))))
				if prefix == 'f':
					self.faces.append([list(map(int, face.split('/'))) for face in value.split(' ')])
				if prefix == 'vt':
					self.tvertices.append(list(map(float, value.split(' '))))
				if prefix == 'vn':
					self.normals.append(list(map(float, value.split(' '))))
		
	def getverts(self):
		return self.vertices
	def getfaces(self):
		return self.faces
verts = []

def reverse(var):
	varc = []
	vat = []
	for y in range(0,len(var[0])):
		varf = []
		for x in range(0,len(var)):
			if y == 0 :
				vat.append(1)
			varf.append(var[x][y])

		varc.append(varf)

	varc.append(vat)
	return varc

def recover(mat):
    matriz = []
    for y in range(0,len(mat[0])):
        vam = []
        for x in range(0,len(mat)-1):
            vam.append(mat[x][y]/mat[3][y])
        matriz.append(vam)
    return matriz


def mulmat(mat1, mat2):
	mat3 = copy.deepcopy(mat2)
	for y in range(0,len(mat2)):
		for x in range(0,len(mat2[0])):
			mat3[y][x] = fabs(mat3[y][x]*0.0)


	for i in range(0,len(mat1)):
		for j in range(0,len(mat2[1])):
			for k in range(0,len(mat2)):
				mat3[i][j] += mat1[i][k] * mat2[k][j]
	return mat3

def loadViewMatrix(x,y,z, center):
	M = [
		[x.x, x.y, x.z, 0],
		[y.x, y.y, y.z, 0],
		[z.x, z.y, z.z, 0],
		[0,0,0,1]
		]
	O = [
		[1,0,0,-center.x],
		[0,1,0,-center.y],
		[0,0,1,-center.z],
		[0,0,0,1]
		]
	
	view = mulmat(O,M)
	
	return view

def loadProjectionMatrix(coeff):
	Projection = [
		[1,0,0,0],
		[0,1,0,0],
		[0,0,1,0],
		[0,0,coeff,1]
	]
	return Projection



def loadViewportMatrix():
	Viewport = [
		[width/500,0,0,x+width/500],
		[0,height/500,0,y + height/500],
		[0,0,16,16],
		[0,0,0,1]
		]
	return Viewport
	
def load(filename,eye,center,up,transalte, scale, rotate, texture = None, shader = None, normalMap = None):
	var = Modelobj("Poopybutthole.obj")
	var.read()
	vertices = var.getverts()
	faces = var.getfaces()
	z = normVec(restVec(eye, center))
	x = normVec(prodx(up,z))
	y = normVec(prodx(z,x))

	
	 
	matriz = mulmat(loadViewportMatrix(),mulmat(loadProjectionMatrix(-0.1),mulmat(loadViewMatrix(x,y,z, center),loadModelMatrix(transalte, scale, rotate))))
	vertices = mulmat(matriz,reverse(vertices))
	vertices = recover(vertices)
	
	scal = 0.4


	luz=V3(0,0,1)
	for face in faces:
	
		x1=round(scal*(vertices[face[0][0]-1][0]+1)*(getwidth()/2))
		y1=round(scal*(vertices[face[0][0]-1][1]+1)*(getwidth()/2))
		z1=round(scal*(vertices[face[0][0]-1][2]+1)*(getwidth()/2))
		x2=round(scal*(vertices[face[1][0]-1][0]+1)*(getwidth()/2))
		y2=round(scal*(vertices[face[1][0]-1][1]+1)*(getwidth()/2))
		z2=round(scal*(vertices[face[1][0]-1][2]+1)*(getwidth()/2))
		x3=round(scal*(vertices[face[2][0]-1][0]+1)*(getwidth()/2))
		y3=round(scal*(vertices[face[2][0]-1][1]+1)*(getwidth()/2))
		z3=round(scal*(vertices[face[2][0]-1][2]+1)*(getwidth()/2))
		n1 = face[0][2] - 1
		n2 = face[1][2] - 1
		n3 = face[2][2] - 1

		v1 = V3(x1,y1,z1)
		v2 = V3(x2,y2,z2)
		v3 = V3(x3,y3,z3)

		normal = normVec(prodx(restVec(v2,v1),restVec(v3,v1)))
		intens = prod(normal,luz)
		if intens<0:
			pass
		if not texture:
			grey = round(255 * intens)
			glColor(grey, grey, grey)
			triangle(v1,v2,v3)

		else:
			t1 = round(scal*(vertices[face[0][1] -1][0] + 1)*(getwidth()/2))
			t2 = round(scal*(vertices[face[1][1] -1][0] + 1)*(getwidth()/2))
			t3 = round(scal*(vertices[face[2][1] -1][0] + 1)*(getwidth()/2))
			t4 = round(scal*(vertices[face[3][1] -1][0] + 1)*(getwidth()/2))
			tA = V2(*var.tvertices[t1])
			tB = V2(*var.tvertices[t2])
			tC = V2(*var.tvertices[t3])
			tD = V2(*var.tvertices[t4])

			triangle(v1, v2, v3, texture = texture, texture_coords = (tA, tB, tC), intens = intens)
			triangle(v1, v2, v3, texture = texture, texture_coords=(tA, tC, tD), intens = intens)




def barycentric(A, B, C, P):
	cx, cy, cz = prodx(
		V3(B.x - A.x, C.x - A.x, A.x - P.x),
		V3(B.y - A.y, C.y - A.y, A.y - P.y)
	)

	if cz == 0:
		return -1, -1, -1
		
	u = cx/cz
	v = cy/cz
	w = 1 - (u + v)

	return w,v,u

def bbox(A, B, C):
	xs = sorted([A.x, B.x, C.x])
	ys = sorted([A.y, B.y, C.y])
	return V2(xs[0], ys[0]), V2(xs[2], ys[2])

def triangle(A, B, C, texture = None, texture_coords = (), varying_normals = (), intens = 0):
	bbox_min, bbox_max = bbox(A, B, C)

	for x in range(bbox_min.x, bbox_max.x + 1):
		for y in range(bbox_min.y, bbox_max.y + 1):
			w, v, u = barycentric(A, B, C, V2(x, y))

			if w < 0 or v < 0 or u < 0:
				pass
			else:
				if texture:
					tA, tB, tC = texture_coords
					tx = tA.x * w + tB.x * v + tC.x * u
					ty = tA.y * w + tB.y * v + tC.y * u
					
					color = gourad(triangle(A, B, C), 
							bar = (w, v, u), 
							varying_normals = varying_normals,
							texture_coords = texture_coords,
							intens = intens
							)

				z = A.z * w + B.z * v + C.z * u
				
				try:
					if z > zbuffer[x][y]:
						pointf(x, y, color)
						zbuffer[x][y] = z
				except:
						pass

	
def gourad(render, bar, **kwargs):
	w, v, u = bar

	tA, tB, tC = kwargs['texture_coords']
	tx = tA.x * w + tB.x * v + tC.x + u
	ty = tA.y * w + tB.y * v + tC.y + u

	color = render.texture.get_color(tx, ty)

	iA, iB, iC = [prod(n, render.luz) for n in kwargs['varying_normals']]

	return bytes(map(lambda b: round(b*kwargs['intens']) if b * kwargs['intens'] >0 else 0, color))



def prod(v0,v1):
	return (v0.x*v1.x)+(v0.y*v1.y)+(v0.z*v1.z)
def restVec(v0,v1):
	return V3(v0.x-v1.x,v0.y-v1.y,v0.z-v1.z)
def prodx(v0,v1):
	return V3(
	v0.y * v1.z - v0.z * v1.y,
	v0.z * v1.x - v0.x * v1.z,
	v0.x * v1.y - v0.y * v1.x
		)
def magVec(v0):
	return (v0.x**2 + v0.y**2 + v0.z**2)**0.5
def normVec(v0):
	l = magVec(v0)
	if not l:
		return V3(0, 0, 0)
	return V3(v0.x/l, v0.y/l, v0.z/l)




