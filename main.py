#!/usr/bin/env python
# -*- conding: utf-8 -*-

import random
import pygame

class GameObject:
	def __init__ (self):
		self.x = False
		self.y = False

class Bird (GameObject):
	def __init__  (self):
		try:
			self.bird_pic = pygame.image.load("./assets/pepe_40x40_02.png")
		except RuntimeError:
			print("Could not find assets!")
			raise RuntimeError
		self.acceleration = 40
		self.speed_y = False
		self.x = 100

	def fly (self, speed_y=10):
		self.speed_y -= float(self.acceleration) * 1/framerate
		if self.y > 0:
			self.y -= int(self.speed_y)
		self.coords = pygame.Rect(self.x, self.y, 40, 40)

	def fall (self):
		if self.y < window_dimensions[1] - (50 + 30):
			self.speed_y += float(self.acceleration) * 1/framerate
			self.y += int(self.speed_y)
		else:
			self.y = window_dimensions[1] - (50 + 30)
		self.coords = pygame.Rect(self.x, self.y, 40, 40)

	def draw_bird (self):
		screen.blit(self.bird_pic, (self.x, self.y))

class Obstacle (GameObject):
	def __init__ (self):
		try:
			self.obstacleBottom = pygame.image.load("./assets/bottom.png").convert()
			self.obstacleTop = self.obstacleBottom # pygame.image.load("./assets/top.png").convert()
		except RuntimeError:
			print("Could not find assets!")
			raise RuntimeError
		self.active = True

	def draw_bottom (self):
		screen.blit(self.obstacleBottom, (self.x, self.y))

	def draw_top (self):
		screen.blit(self.obstacleTop, (self.x, self.y))

	@staticmethod
	def move(bottom_list, top_list, speed):
		for v in range(4):
			if bottom_list[v].x <= -98:
				bottom_list[v].x = window_dimensions[0] + (window_dimensions[0]/4) - (abs(bottom_list[v].x)-98)	# works but not consistent
				bottom_list[v].y = random.randrange(window_dimensions[1] - 361, window_dimensions[1] - 120, 20)
				bottom_list[v].active = True
				top_list[v].x = bottom_list[v].x
				top_list[v].y = bottom_list[v].y - 630

			bottom_list[v].x -= speed
			top_list[v].x -= speed
			bottom_list[v].draw_bottom()
			top_list[v].draw_top()

class Score (GameObject):
	def __init__ (self):
		self.points = 0
		self.font = "helvetica"
		self.dimensions = 54
		self.colour = 255, 255, 255

	def write (self):
		font = pygame.font.SysFont(self.font, self.dimensions, bold=True)
		text = font.render(str(self.points), True, self.colour)
		self.position = text.get_rect()
		self.position.centerx = screen.get_rect().centerx
		self.position.y = 10
		screen.blit(text, self.position)

class Ground (GameObject):
	def __init__ (self):
		try:
			self.ground_pic = pygame.image.load("./assets/ground840.png").convert()
		except RuntimeError:
			print("Could not find assets!")
			raise RuntimeError

	def draw (self):
		screen.blit(self.ground_pic, (self.x, (window_dimensions[1] - 50) ))

	# For an eventual mooving ground
	@staticmethod
	def move(ground_list, speed):
		for ground in ground_list:
			ground.x -= speed
			if ground.x <= -window_dimensions[0]:
				ground.x = window_dimensions[0] - (window_dimensions[0] - abs(ground.x))

def initial_screen (score_displayed):

	score = Score()
	score.points = score_displayed

	try:
		splash_screen = pygame.image.load("./assets/splash_840x548.png").convert()
	except RuntimeError:
		print("Could not find assets!")
		raise RuntimeError

	while True:
		for event in pygame.event.get():
				if event.type == pygame.QUIT:
					exit()

				if event.type == pygame.KEYDOWN and event.key in (pygame.K_SPACE, pygame.K_UP):
					main()

		screen.blit(splash_screen, (0, 0))
		score.write()

		pygame.display.update()
		pygame.time.Clock().tick(15)

def main():
	pepe = Bird()
	pepe.y = (window_dimensions[1] / 2) - 32
	gravity_active = True

	bottom_obstacle1 = Obstacle()
	bottom_obstacle2 = Obstacle()
	bottom_obstacle3 = Obstacle()
	bottom_obstacle4 = Obstacle()

	bottom_list = [bottom_obstacle1, bottom_obstacle2, bottom_obstacle3, bottom_obstacle4]
	salt = window_dimensions[0] / 3
	for obstacle in bottom_list:
		obstacle.x = window_dimensions[0] + salt
		obstacle.y = random.randrange(window_dimensions[1] - 361, window_dimensions[1] - 120, 20)
		salt += window_dimensions[0] / 3

	top_obstacle1 = Obstacle()
	top_obstacle2 = Obstacle()
	top_obstacle3 = Obstacle()
	top_obstacle4 = Obstacle()

	ground_rect = pygame.Rect(0, window_dimensions[1]-50, window_dimensions[0], 50)

	top_list = [top_obstacle1, top_obstacle2, top_obstacle3, top_obstacle4]
	pointer = False
	collided = False
	for obstacle in [top_obstacle1, top_obstacle2, top_obstacle3, top_obstacle4]:
		obstacle.x = bottom_list[pointer].x
		obstacle.y = bottom_list[pointer].y - 630
		pointer += True

	ground1 = Ground()
	ground1.x = False

	score = Score()
	score.points = 0

	try:
		background = pygame.image.load("./assets/pepe_bg.png").convert()
	except RuntimeError:
		print("Could not find assets!")
		raise RuntimeError

	global_speed = 5
	timer = False

	while True:
		for event in pygame.event.get():
				if event.type == pygame.QUIT:
					exit()

				if event.type == pygame.KEYDOWN and event.key in (pygame.K_SPACE, pygame.K_UP):
					gravity_active = False
					pepe.speed_y = 10

		screen.blit(background, (0, 0))

		if not gravity_active and not collided:
			if pepe.speed_y < 1:
				gravity_active = True
			else:
				pepe.fly()
		else:
			pepe.fall()

		bottom_list = [bottom_obstacle1, bottom_obstacle2, bottom_obstacle3, bottom_obstacle4]
		top_list = [top_obstacle1, top_obstacle2, top_obstacle3, top_obstacle4]


		for p in range(4):
			hitboxt = pygame.Rect(top_list[p].x, top_list[p].y, 98, 500)
			hitboxb = pygame.Rect(bottom_list[p].x, bottom_list[p].y, 98, 500)
			if pepe.coords.colliderect(hitboxt) or pepe.coords.colliderect(hitboxb) or pepe.coords.colliderect(ground_rect):
				global_speed = False
				collided = True
				break

			if bottom_list[p].x < pepe.x and bottom_list[p].active:
				score.points += 1
				bottom_list[p].active = False

		if pepe.y == window_dimensions[1] - (50 + 30):
			timer += True
			if timer == framerate:
				initial_screen(score.points)

		Obstacle.move(bottom_list, top_list, global_speed)

		ground1.draw()
		pepe.draw_bird()
		score.write()

		pygame.display.update()
		# pygame.time.Clock().tick(framerate)
		pygame.time.Clock().tick_busy_loop(framerate)



window_dimensions = 840, 548
framerate = 60

# Initialise Pygame
pygame.init()
screen = pygame.display.set_mode(window_dimensions)
screen.fill((255, 255, 255))
pygame.display.set_caption("Flappy Pepe")

try:
	icon = pygame.image.load("./assets/icon.png")
except RuntimeError:
	print("Could not find assets!")
	raise RuntimeError

pygame.display.set_icon(icon)


if __name__ == "__main__":
	initial_screen(0)
