from Modelobj import *

cont = 0

print('1. medium shot')
print('2. low angle shot')
print('3. high angle shot')
print('4. dutch angle shot')
respuesta = int(input())


if respuesta == 1:
	glCreateWindow(800,600)
	val = get_var()
	t = Texture('Poopy.bmp')
	load("Poopybutthole.obj",eye=V3(0,0,0.5),center=V3(0.2,0,0),up=V3(0,1,0),transalte=(-3.8,-0.3,4), scale=(1,1,1), rotate=(0,-0.1,0), texture = t)
	glFinish()
if respuesta == 2:
	glCreateWindow(800,600)
	val = get_var()
	t = Texture('Poopy.bmp')
	load("Poopybutthole.obj",eye=V3(0,0,0.5),center=V3(0,0.2,0),up=V3(0,1,0),transalte=(-0.5,0,0), scale=(1,1,1), rotate=(0,-0.1,0), texture = t)
	glFinish()
if respuesta == 3:
	glCreateWindow(800,600)
	val = get_var()
	t = Texture('Poopy.bmp')
	load("Poopybutthole.obj",eye=V3(0,0,0.5),center=V3(0,-1.3,0),up=V3(0,1,0),transalte=(-0.5,-1.5,0), scale=(1,1,1), rotate=(0,0,0), texture = t)
	glFinish()
if respuesta == 4:
	glCreateWindow(800,600)
	val = get_var()
	t = Texture('Poopy.bmp')
	load("Poopybutthole.obj",eye=V3(0,0,0.5),center=V3(0,0,0),up=V3(0.3,1,0),transalte=(-0.5,-0,0), scale=(1,1,1), rotate=(0,0,0), texture = t)
	glFinish()
