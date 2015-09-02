#!/usr/bin/env python3
# basic moving ship

import turtle
import engine
import random
import math
import time

WIDTH = 640
HEIGHT = 480
speed = 0 # vitesse
countreac = 0 # compteur de frames du réacteur
basesize = 15
sundiam = 150
shiphead = 0 # tilt du vaisseau

xspeed = 0
yspeed = 0

class Ground(engine.GameObject):
	def __init__(self):
		super().__init__(0, -HEIGHT/2, 0, 0, 'ground', '#8B4513')
	def heading(self):
		return 90

class Sun(engine.GameObject):
	def __init__(self):
		super().__init__(0, HEIGHT/2, 0, 0, 'sun', 'yellow')


class Fusee(engine.GameObject):
	def __init__(self):
		super().__init__(0, 0, 0, 0, 'fusee', 'black')
	def heading(self):
		return shiphead
	def move(self):
		global speed
		global xspeed
		global yspeed
		global lost
		global ship
		global countreac
		if self.y >= HEIGHT / 2. - 3 * basesize - sundiam / 2:
			speed = 0
			banner("Burnt!")
			lost = True
			engine.exit_engine()
		elif self.y > (-1 * HEIGHT / 2 + basesize + speed + 20) or speed < 0: 
			# le zéro de la fusée est au coin supérieur droit du réacteur gauche
			# ceci est À CHANGER IMPÉRATIVEMENT mais je suis un gros feignant
			self.y += yspeed
			self.x += xspeed
			
			xspeed = 0.99 * xspeed # histoire qu'il ne file pas à l'infini
			yspeed = 0.99 * yspeed - 0.02 # gravité
			
		else:
			if abs(math.sqrt(xspeed ** 2 + yspeed ** 2)) > 2 or abs(shiphead) >= 15:
				banner("Crashed!")
			else:
				banner("Landed!")
			self.y = -1 * HEIGHT / 2 + basesize
			speed = 0
			engine.exit_engine()
		countreac += 1
		if countreac > 20:
			ship.color = "black"


def keyboard_cb(key):
	global speed
	global xspeed
	global yspeed
	global ship
	global countreac
	global shiphead
	if key == 'space' or key == 'Up':
		xspeed = xspeed + math.sin(-3.1415926535 * shiphead / 180) * 0.2
		yspeed = yspeed + math.cos(3.1415926535 * shiphead / 180) * 0.2
		
		ship.color = "red"
		countreac = 0
	elif key == 'Escape':
		print("Au revoir...")
		engine.exit_engine()
	elif key == 'Right':
		shiphead -= 2
	elif key == 'Left':
		shiphead += 2
	else:
		print(key)

def drawfus(): # spaceship!
	global basesize
	B = basesize
	turtle.begin_poly()
	#turtle.fd(-1.5 * B)
	turtle.fd(B)
	turtle.rt(90)
	turtle.fd(B)
	turtle.rt(90)
	turtle.fd(B)
	turtle.rt(90)
	turtle.fd(B)
	turtle.fd(2.25 * B)
	turtle.rt(90)
	turtle.fd(B)
	turtle.rt(90)
	turtle.fd(B)
	turtle.rt(90)
	turtle.fd(B)
	turtle.fd(3 * B)
	turtle.rt(-90)
	turtle.fd(1.25 * B)
	
	turtle.end_poly()
	poly = turtle.get_poly() # c'est le poly... yveslemaire.poly
	turtle.register_shape('fusee', poly)

def banner(s):
	turtle.home()
	turtle.color('black')
	turtle.write(s, True, align='center', font=('Arial', 48, 'italic'))
	time.sleep(3)
	#turtle.undo()


def drawsun():
	global sundiam
	turtle.begin_poly()
	turtle.setpos(-sundiam/2,0)
	turtle.circle(sundiam/2, None, None)
	turtle.end_poly()
	circ = turtle.get_poly()
	turtle.register_shape('sun',circ)

def drawground():
	s = turtle.Shape("compound")
	ground = ((-320, 120), (-280, 41), (-240, 27),
		   (-200, 59), (-160, 25), (-120, 43), (-80, 56),
		   (-40, 20), (0, 20), (40, 20), (80, 44),
		(120, 28), (160, 66), (200, 29), (240, 64),
		(280, 34), (320, 140), (320, 0), (-320,0) ) 
	s.addcomponent(ground, "#8B4513", "#8B4513")
	turtle.register_shape('ground', s)

if __name__ == '__main__':
	engine.init_screen(WIDTH, HEIGHT)
	engine.init_engine()
	engine.set_keyboard_handler(keyboard_cb)
	drawground()
	drawfus()
	drawsun()

	ship = Fusee()
	gnd = Ground()
	sun = Sun()
	engine.add_obj(gnd)
	engine.add_obj(sun)	
	engine.add_obj(ship)
	engine.engine()

