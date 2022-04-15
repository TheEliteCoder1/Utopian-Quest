import pygame
import csv
from gamelib import *
pygame.init()
pygame.mixer.init()


screen_width, screen_height = 600, 500
screen = pygame.display.set_mode((600, 500))
screen_constants = get_usefull_constants(screen)
running = True
fps = 30
clock = pygame.time.Clock()
bg_img = 'assets/images/bg_shroom.png'
background = pygame.image.load(bg_img).convert()
GRAVITY = 0.2
ROWS = 16
TILE_SIZE = screen_height // ROWS
bg_scroll = 0
screen_scroll = 0
SCROLL_THRESH = 250
COLS = 200
level = 0
MAX_LEVELS = 10

# define player action variables
moving_left = False
moving_right = False

# music and fx
song_on = True
pygame.mixer.music.load('assets/music/woods.mp3')
pygame.mixer.music.play(-1)

coin_fx = pygame.mixer.Sound('assets/music/coin.mp3')
coin_fx.set_volume(0.5)

explosive_fx = pygame.mixer.Sound('assets/music/explosive.wav')
explosive_fx.set_volume(2)


class Player(pygame.sprite.Sprite):
	def __init__(self, screen, x, y, character, scale, speed):
		pygame.sprite.Sprite.__init__(self)
		self.alive = True
		self.speed = speed
		self.shoot_cooldown = 0
		self.direction = 1
		self.hearts = 3
		self.vel_y = 0
		self.jump = False
		self.react_to_explosion = False
		self.in_air = True
		self.flip = False
		self.animation_list = []
		self.frame_index = 0
		self.action = 0
		self.update_time = pygame.time.get_ticks()
		#ai specific variables
		self.move_counter = 0
		self.vision = pygame.Rect(0, 0, 150, 20)
		self.idling = False
		self.idling_counter = 0
		
		#load all images for the players
		animation_types = ['Idle', 'Run', 'Death']
		for animation in animation_types:
			#reset temporary list of images
			temp_list = []
			#count number of files in the folder
			num_of_frames = len(os.listdir(f'assets/player/{character}/{animation}'))
			for i in range(num_of_frames):
				img = pygame.image.load(f'assets/player/{character}/{animation}/{i}.png').convert_alpha()
				img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
				temp_list.append(img)
			self.animation_list.append(temp_list)

		self.image = self.animation_list[self.action][self.frame_index]
		self.rect = self.image.get_rect()
		self.rect.center = (x, y)
		self.width = self.image.get_width()
		self.height = self.image.get_height()


	def update(self):
		self.update_animation()
		self.check_alive()

	def move(self, moving_left, moving_right):
		#reset movement variables
		screen_scroll = 0
		dx = 0
		dy = 0

		#assign movement variables if moving left or right
		if moving_left:
			dx = -self.speed
			self.flip = True
			self.direction = -1
		if moving_right:
			dx = self.speed
			self.flip = False
			self.direction = 1

		#jump
		if self.jump == True and self.in_air == False:
			self.vel_y = -7
			self.jump = False
			self.in_air = True
		if self.react_to_explosion == True and self.in_air == False:
			self.vel_y = -11
			self.react_to_explosion = False
			self.in_air = True

		#apply gravity
		self.vel_y += GRAVITY*2
		if self.vel_y > 6:
			self.vel_y
		dy += self.vel_y

		#check for collision
		for tile in world.objects_list:
			if tile[2] == 'Block':
				#check collision in the x direction
				if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
					dx = 0
				#check for collision in the y direction
				if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
					#check if below the ground, i.e. jumping
					if self.vel_y < 0:
						self.vel_y = 0
						dy = tile[1].bottom - self.rect.top
					#check if above the ground, i.e. falling
					elif self.vel_y >= 0:
						self.vel_y = 0
						self.in_air = False
						dy = tile[1].top - self.rect.bottom
			elif tile[2] == 'Currency':
				if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height) or tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
					coin_fx.play()
					world.objects_list.remove(tile)
			elif tile[2] == 'Explodable':
				if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height) or tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
					explosive_fx.play()
					self.react_to_explosion = True
					self.hearts -= 1
					world.objects_list.remove(tile)


		# #check for collision with water
		# if pygame.sprite.spritecollide(self, water_group, False):
		# 	self.health = 0

		#check for collision with exit
		level_complete = False
		# if pygame.sprite.spritecollide(self, exit_group, False):
		# 	level_complete = True

		#check if fallen off the map
		if self.rect.bottom > screen_height:
			self.hearts = 0


		#check if going off the edges of the screen
		if self.rect.left + dx < 0 or self.rect.right + dx > screen_width:
			dx = 0

		#update rectangle position
		self.rect.x += dx
		self.rect.y += dy

		#update scroll based on player position
		if (self.rect.right > screen_width - SCROLL_THRESH and bg_scroll < (world.level_length * TILE_SIZE) - screen_width)\
			or (self.rect.left < SCROLL_THRESH and bg_scroll > abs(dx)):
			self.rect.x -= dx
			screen_scroll = -dx

		return screen_scroll, level_complete
		
	def update_animation(self):
		#update animation
		ANIMATION_COOLDOWN = 100
		#update image depending on current frame
		self.image = self.animation_list[self.action][self.frame_index]
		#check if enough time has passed since the last update
		if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
			self.update_time = pygame.time.get_ticks()
			self.frame_index += 1
		#if the animation has run out the reset back to the start
		if self.frame_index >= len(self.animation_list[self.action]):
			if self.action == 3:
				self.frame_index = len(self.animation_list[self.action]) - 1
			else:
				self.frame_index = 0

	def update_action(self, new_action):
		#check if the new action is different to the previous one
		if new_action != self.action:
			self.action = new_action
			#update the animation settings
			self.frame_index = 0
			self.update_time = pygame.time.get_ticks()



	def check_alive(self):
		if self.hearts <= 0:
			self.health = 0
			self.speed = 0
			self.alive = False
			self.update_action(3)


	def draw(self):
		screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)

# store tiles in list
img_list = []
for x in list(LEVEL_OBJECTS.keys()):
	img = pygame.transform.scale(pygame.image.load(
		LEVEL_OBJECTS[x]["image"]), LEVEL_OBJECTS[x]["size"])
	img_list.append(img)


def draw_bg(screen, background):
	screen.fill((255, 255, 255))
	width = background.get_width()
	for x in range(5):
		screen.blit(background, ((x * width) - bg_scroll * 0.5, 0))


def reset_level():
	# enemy_group.empty()
	# bullet_group.empty()
	# grenade_group.empty()
	# explosion_group.empty()
	# item_box_group.empty()
	# decoration_group.empty()
	# water_group.empty()
	# exit_group.empty()

	# create empty tile list
	data = []
	for row in range(ROWS):
		r = [-1] * COLS
		data.append(r)

	return data


class World():
	def __init__(self):
		self.objects_list = []
		
	def process_data(self, data):
		self.level_length = len(data[0])
		# iterate through each value in level data file
		# print(data)
		for y, row in enumerate(data):
			for x, tile in enumerate(row):
				if tile >= 0:
					img = pygame.transform.scale(pygame.image.load(LEVEL_OBJECTS[tile]["image"]), LEVEL_OBJECTS[tile]["size"])
					img_rect = img.get_rect()
					img_rect.x = x * TILE_SIZE
					img_rect.y = y * TILE_SIZE
					tile_data = (img, img_rect, LEVEL_OBJECTS[tile]["descriptor"])
					self.objects_list.append(tile_data)

	def draw(self):
		for tile in self.objects_list:
			tile[1][0] += screen_scroll
			screen.blit(tile[0], tile[1])


#create empty tile list
world_data = []
for row in range(ROWS):
	r = [-1] * COLS
	world_data.append(r)
#load in level data and create world
with open(f'levels/{level}.csv', newline='') as csvfile:
	reader = csv.reader(csvfile, delimiter=',')
	for x, row in enumerate(reader):
		for y, tile in enumerate(row):
			world_data[x][y] = int(tile)

world = World()
world.process_data(world_data)
player = Player(screen, 30, 0, "Boro", 0.5, 5)

# Player
# player = Player(screen, 20, screen_constants['bottom_y'], player_character, selected_level.rect_list)

while running:
	clock.tick(fps)
	if song_on != True:
		pygame.mixer.music.stop()
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
			pygame.quit()
			quit()
		
		#keyboard presses
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_a:
				moving_left = True
			if event.key == pygame.K_d:
				moving_right = True
			if event.key == pygame.K_w and player.alive:
				player.jump = True
		
		#keyboard button released
		if event.type == pygame.KEYUP:
			if event.key == pygame.K_a:
				moving_left = False
			if event.key == pygame.K_d:
				moving_right = False

		if event.type == pygame.MOUSEMOTION:
			# When mouse is hovering
			pass

		if event.type == pygame.MOUSEBUTTONDOWN:
			# When mouse is clicking
			pass

	# draw game every frame.
	draw_bg(screen, background)
	world.draw()
	player.update()
	player.draw()
	draw_text(screen, FONTS['game_info'], "LEVEL: " + str(level), 30, (255, 213, 128), (75, screen_constants['margin_y']-30))
	try:
		for x in range(player.hearts):
			img = pygame.transform.smoothscale(pygame.image.load("assets/images/heart.png"), (30, 30))
			screen.blit(img, (x*30+500, 5))
	except:
		pass
	if player.alive:
		if player.in_air:
			player.update_action(2)#2: jump
		elif moving_left or moving_right:
			player.update_action(1)#1: run
		else:
			player.update_action(0)#0: idle
		screen_scroll, level_complete = player.move(moving_left, moving_right)
		bg_scroll -= screen_scroll
	else:
		bg_scroll = 0
		world_data = reset_level()
		#load in level data and create world
		with open(f'levels/{level}.csv', newline='') as csvfile:
			reader = csv.reader(csvfile, delimiter=',')
			for x, row in enumerate(reader):
				for y, tile in enumerate(row):
					world_data[x][y] = int(tile)
		world = World()
		world.process_data(world_data)
		player = Player(screen, 30, 0, "Boro", 0.5, 5)
		
	pygame.display.update()
