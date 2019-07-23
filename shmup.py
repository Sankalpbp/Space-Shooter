# pygame template - skeleton for a new pygame project

# Frozen Jam by tgfcoder <https://twitter.com/tgfcoder> licensed under CC-BY-3 
# Art from Kenny.nl

import pygame
import random
from os import path
import time


img_dir = path.join(path.dirname(__file__), 'img')
snd_dir = path.join(path.dirname(__file__), 'snd')

# constants for our window

WIDTH = 480
HEIGHT = 600
FPS = 60
POWERUP_TIME = 5000

# defining some colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# initializing pygame
pygame.init()

# initializing the music stuff
pygame.mixer.init()

# initializing screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# The title for window
pygame.display.set_caption("Shmup!")

# the clock
clock = pygame.time.Clock()

# now our window is ready for running

# drawing text on the screen

# this is used for telling the python that use any of the fonts present in the system, which "matches" with the name 'arial'
font_name = pygame.font.match_font('arial')

def draw_text(surf, text, size, x, y):
	"""
	The function will use the surface(the screen here), the text we want to put in, the size and the coordinates 
	where we want to put that.
	"""	
	font = pygame.font.Font(font_name, size)
	# loads a new font from a given file object, with the given font_name and the given size
	text_surface = font.render(text, True, WHITE)
	# This creates a new Surface with the specified text rendered on it. pygame provides no way to directly draw
	#  text on an existing Surface: instead you must use Font.render() to create an image (Surface) of the text, 
	#  then blit this image onto another Surface.
	# "True" argument is for aliasing the text or anti-aliasing it.
	text_rect = text_surface.get_rect()
	text_rect.midtop = (x, y)
	surf.blit(text_surface, text_rect)


# making a new mob

def newmob():
	m = Mob()
	all_sprites.add(m)
	mobs.add(m)


# drawing the bar for shield
def draw_shield_bar(surf, x, y, pct):

	if pct < 0:
		pct = 0

	BAR_LENGTH = 100
	BAR_HEIGHT = 10

	fill = (pct / 100) * BAR_LENGTH
	outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
	fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
	pygame.draw.rect(surf, GREEN, fill_rect)
	pygame.draw.rect(surf, WHITE, outline_rect, 2)


def draw_lives(surf, x, y, lives, img):
	
	for i in range(lives):
		img_rect = img.get_rect()
		img_rect.x = x + 30 * i
		img_rect.y = y
		surf.blit(img, img_rect)


# the player class

class Player(pygame.sprite.Sprite):
	
	def __init__(self):

		pygame.sprite.Sprite.__init__(self)

		self.image = pygame.transform.scale(player_img, (50, 38))
		self.image.set_colorkey(BLACK)
		self.rect = self.image.get_rect()
		self.radius = 20
		#pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
		self.rect.centerx = WIDTH/2
		self.rect.bottom = HEIGHT - 10
		self.speedx = 0
		self.shield = 100
		self.shoot_delay = 250
		self.last_shot = pygame.time.get_ticks()
		self.lives = 3
		self.hidden = False
		self.hide_timer = pygame.time.get_ticks()
		self.power_level = 1
		self.power_timer = pygame.time.get_ticks()


	def update(self):


		# timeout for powerups
		if self.power_level >= 2 and pygame.time.get_ticks() - self.power_timer > POWERUP_TIME:
			self.power_level -= 1
			self.power_timer = pygame.time.get_ticks()

		# unhide if hidden
		if self.hidden and pygame.time.get_ticks() - self.hide_timer > 1000:
			self.hidden = False
			self.rect.centerx = WIDTH / 2
			self.rect.bottom = HEIGHT - 10

		self.speedx = 0
		keystate = pygame.key.get_pressed()
		# the statement above will return the list of all the keys that are pressed
		# and then we can check, each of them like shown below
		if keystate[pygame.K_LEFT]:
			self.speedx = -5
		if keystate[pygame.K_RIGHT]:
			self.speedx = 5
		if keystate[pygame.K_SPACE]:
			self.shoot()
		self.rect.x += self.speedx

		if self.rect.right > WIDTH:
			self.rect.right = WIDTH
		if self.rect.left < 0:
			self.rect.left = 0


	def powerup(self):
		self.power_level += 1
		self.power_timer = pygame.time.get_ticks()

	def shoot(self):

		now = pygame.time.get_ticks()
		if now - self.last_shot > self.shoot_delay:
			self.last_shot = now
			if self.power_level == 1:
				bullet = Bullet(self.rect.centerx, self.rect.top)
				all_sprites.add(bullet)
				bullets.add(bullet)
				shoot_sound.play()

			if self.power_level >= 2:
				bullet1 = Bullet(self.rect.left, self.rect.centery)
				bullet2 = Bullet(self.rect.right, self.rect.centery)
				all_sprites.add(bullet1)
				all_sprites.add(bullet2)
				bullets.add(bullet1)
				bullets.add(bullet2)
				shoot_sound.play()

	def hide(self):

		# hide the player temporarily
		self.hidden = True
		self.hide_timer = pygame.time.get_ticks()
		self.rect.center = (WIDTH / 2, WIDTH + 300)


class Mob(pygame.sprite.Sprite):

	def __init__(self):
		
		pygame.sprite.Sprite.__init__(self)

		self.image_original = random.choice(meteor_images)
		self.image_original.set_colorkey(BLACK)
		self.image = self.image_original.copy()
		self.rect = self.image.get_rect()
		self.radius = int(self.rect.width * 0.85 / 2)
		#pygame.draw.circle(self.image, RED, self.rect.center, self.radius)

		# positionaing all the mob(as we'll have a lot of them)
		# it will randomly be positioned on all of the x axis
		self.rect.x = random.randrange(0, WIDTH - self.rect.width)
		self.rect.y = random. randrange(-150, -100)
		self.speedy = random.randrange(1, 8)
		self.speedx = random.randrange(-3, 3)
		self.rotation = 0
		self.rotation_speed = random.randrange(-8, 8)
		self.last_update = pygame.time.get_ticks()

	def rotate(self):
		now = pygame.time.get_ticks()
		if now - self.last_update > 50:
			self.last_update = now
			self.rotation = (self.rotation + self.rotation_speed) % 360
			new_image = pygame.transform.rotate(self.image_original, self.rotation)
			old_center = self.rect.center
			self.image = new_image
			self.rect = self.image.get_rect()
			self.rect.center = old_center


	def update(self):

		self.rotate()
		self.rect.y += self.speedy
		self.rect.x += self.speedx

		if self.rect.top > HEIGHT + 10 or self.rect.left < -25 or self.rect.right > WIDTH + 30:
			self.rect.x = random.randrange(0, WIDTH - self.rect.width)
			self.rect.y = random.randrange(-100, -40)
			self.speedy = random.randrange(1, 8)


class Bullet(pygame.sprite.Sprite):

	def __init__(self, x, y):

		pygame.sprite.Sprite.__init__(self)
		
		self.image = bullet_img
		self.image.set_colorkey(BLACK)
		self.rect = self.image.get_rect()
		self.rect.bottom = y
		self.rect.centerx = x
		self.speedy = -10


	def update(self):
		self.rect.y += self.speedy
		# kill if it moves off the top of the screen
		if self.rect.bottom < 0:
			self.kill()

# Powerups class

class Power(pygame.sprite.Sprite):

	def __init__(self, center):

		pygame.sprite.Sprite.__init__(self)
		
		self.type = random.choice(['shield', 'gun'])
		self.image = powerup_images[self.type]
		self.image.set_colorkey(BLACK)
		self.rect = self.image.get_rect()
		self.rect.center = center
		self.speedy = 4


	def update(self):
		self.rect.y += self.speedy
		# kill if it moves off the top of the screen
		if self.rect.top > HEIGHT:
			self.kill()


# Explosion sprite

class Explosion(pygame.sprite.Sprite):

	def __init__(self, center, size):

		pygame.sprite.Sprite.__init__(self)
		self.size = size
		self.image = explosion_animation[self.size][0]
		self.rect = self.image.get_rect()
		self.rect.center = center
		self.frame = 0
		self.last_update = pygame.time.get_ticks()
		self.frame_rate = 75

	def update(self):
		now = pygame.time.get_ticks()
		if now - self.last_update > self.frame_rate:
			self.last_update = now
			self.frame += 1

			if self.frame == len(explosion_animation[self.size]):
				self.kill()
			else:
				center = self.rect.center
				self.image = explosion_animation[self.size][self.frame]
				self.rect = self.image.get_rect()
				self.rect.center = center


def show_game_over_screen():

	screen.blit(background, background_rect)
	draw_text(screen, "SHMUP!", 64, WIDTH / 2, HEIGHT / 4)
	draw_text(screen, "Arrow keys move, Space to fire", 22, WIDTH / 2, HEIGHT / 2)
	draw_text(screen, "Press a key to begin", 18, WIDTH / 2, HEIGHT * 3 / 4)
	pygame.display.flip()
	waiting = True

	while waiting:
		clock.tick(FPS)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
			if event.type == pygame.KEYUP:
				waiting = False

# load all game graphics
background = pygame.image.load(path.join(img_dir, "starfield.png")).convert()
background_rect = background.get_rect()

player_img  = pygame.image.load(path.join(img_dir, "player.png")).convert()
player_mini_img = pygame.transform.scale(player_img, (25, 19))
player_mini_img.set_colorkey(BLACK)
bullet_img = pygame.image.load(path.join(img_dir, "laserRed.png")).convert()

meteor_images = []
meteor_list = ['meteorBig.png', 'meteorSmall.png']

for img in meteor_list:
	meteor_images.append(pygame.image.load(path.join(img_dir, img)).convert())


explosion_animation = {}
explosion_animation['large'] = []
explosion_animation['small'] = []
explosion_animation['player'] = []

for i in range(9):
	filename = 'regularExplosion0{}.png'.format(i)
	img = pygame.image.load(path.join(img_dir, filename)).convert()
	img.set_colorkey(BLACK)
	img_large = pygame.transform.scale(img, (75, 75))
	explosion_animation['large'].append(img_large)
	img_small = pygame.transform.scale(img, (32, 32))
	explosion_animation['small'].append(img_small)
	filename = 'sonicExplosion0{}.png'.format(i)
	img = pygame.image.load(path.join(img_dir, filename)).convert()
	img.set_colorkey(BLACK)
	explosion_animation['player'].append(img)

powerup_images = {}
powerup_images['shield'] = pygame.image.load(path.join(img_dir, 'shield_gold.png')).convert()
powerup_images['gun'] = pygame.image.load(path.join(img_dir, 'bolt_gold.png')).convert()


# load all game sounds
shoot_sound = pygame.mixer.Sound(path.join(snd_dir, 'shoot.wav'))
shield_sound = pygame.mixer.Sound(path.join(snd_dir, 'shield.wav'))
gun_sound = pygame.mixer.Sound(path.join(snd_dir, 'gun.wav'))

explosion_sounds = []
for snd in ['explosion.wav', 'explosion2.wav']:
	explosion_sounds.append(pygame.mixer.Sound(path.join(snd_dir, snd)))

player_die_sound = pygame.mixer.Sound(path.join(snd_dir, 'rumble1.ogg'))
pygame.mixer.music.load(path.join(snd_dir, 'background_music.ogg'))


# in order to stop the game, we make "running"
running = True

# to pause the game
pause = False

# play the background music
pygame.mixer.music.play(loops=-1)


game_over = True

# GAME LOOP
while running:

	if game_over:
		show_game_over_screen()
		game_over = False
		all_sprites = pygame.sprite.Group()
		# creating mobs
		mobs = pygame.sprite.Group()
		# creating bullets group
		bullets = pygame.sprite.Group()
		# ADDING powerups sprites
		powerups = pygame.sprite.Group()
		# Player object created
		player = Player()
		all_sprites.add(player)
		for i in range(0, 8):
			newmob()
		# the score for the player
		score = 0

	# keep loop running at the right speed
	clock.tick(FPS)


# process input (events)
	for event in pygame.event.get():
		# check for closing the window
		if event.type == pygame.QUIT:
			running = False

		# elif event.type == pygame.KEYDOWN:
		# 	if event.key == pygame.K_u:
		# 		running = False
	
# update

	# if pause is True, sleep the game
	if pause:
		time.sleep(.200)


	# just using one statement, all sprites will be updated
	all_sprites.update()

	# this one is a little different from the player and the mobs because, here we have a
	# group of bullets and the group of mobs. Any of those bullets may hit any of those mobs
	hits = pygame.sprite.groupcollide(mobs, bullets, True, True)
	# then, delete all of mobs

	for hit in hits:
		score += 50 - hit.radius
		random.choice(explosion_sounds).play()
		expl = Explosion(hit.rect.center, 'large')
		all_sprites.add(expl)
		if random.random() > 0.92:
			power = Power(hit.rect.center)
			all_sprites.add(power)
			powerups.add(power)
		newmob()



	# CHECK to see if a mob hit the player
	hits = pygame.sprite.spritecollide(player, mobs, True, pygame.sprite.collide_circle)
	# spritecollide function with arguments - (the sprite, the sprite group, the bool value
	# which will ask for if the mobs member which gets hit on the sprite should be deleted or not)
	# the function will return a list of the mobs that have hit the player

	for hit in hits:	# list of all those who hit us and then do the damage to the shield accordingly
		player.shield -= hit.radius * 2
		expl = Explosion(hit.rect.center, 'small')
		all_sprites.add(expl)
		newmob()
		if player.shield <= 0:
			player_die_sound.play()
			death_explosion = Explosion(player.rect.center, 'player')
			all_sprites.add(death_explosion)
			player.hide()
			player.lives -= 1
			player.shield = 100


	# check if the player hit a powerup
	hits = pygame.sprite.spritecollide(player, powerups, True)
	for hit in hits:

		if hit.type == 'shield':
			player.shield += random.randrange(10, 30)
			shield_sound.play()
			if player.shield >= 100:
				player.shield = 100

		if hit.type == 'gun':
			gun_sound.play()
			player.powerup()			

	# if the player died and the explosion had finished
	if player.lives == 0 and not death_explosion.alive():
		game_over = True # game over

# draw / render

	# filling the color on the screen
	screen.fill(BLACK)
	screen.blit(background, background_rect)
	# blit means copy the functions of one thing on another thing
	all_sprites.draw(screen)

	# drawing text
	draw_text(screen, str(score), 18, WIDTH/2, 10)

	# drawing the shield bar
	draw_shield_bar(screen, 5, 5, player.shield)

	# drawing the lives the small ships at the top
	draw_lives(screen, WIDTH - 100, 5, player.lives, player_mini_img)
	# *after* drawing everything, flip the display
	pygame.display.flip()


pygame.quit()
quit()