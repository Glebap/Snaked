import pygame
import sys
import random


class Snake():

	def __init__(self):
		self.reset()
		self.mode = 0
		self.color = (255, 0, 0)

	def get_head_position(self):
		return self.positions[0]

	def turn(self, point):
		if self.length > 1 and (point[0]*-1, point[1]*-1) == self.direction:
			return
		else:
			self.direction = point

	def move(self):
		cur = self.get_head_position()
		x,y = self.direction
		new = ((cur[0]+(x*GRIDSIZE))%WIDTH, (cur[1]+(y*GRIDSIZE))%HEIGHT)
		if len(self.positions) > 2 and new in self.positions[2:]:
			self.reset()
		else:
			self.positions.insert(0,new)
			if len(self.positions) > self.length:
				self.positions.pop()


	def reset(self):
		self.length = 1
		self.positions = [(GRIDSIZE*4, GRIDSIZE*4)]
		self.direction = random.choice(DIRS)
		self.set_high_score()
		self.score = 0  
		self.run = 0
	def set_high_score(self):
		try:
			if self.high_score >= self.score:
				self.high_score = self.high_score
			else:
				with open('./data/stats.txt', 'w') as s:
					self.high_score = self.score
					s.write(str(self.score))
		except:
			with open('./data/stats.txt', 'r') as s:
				self.high_score = int(s.readline())

	def draw(self,surface):
		global SNAKE_POSITIONS
		SNAKE_POSITIONS = self.positions

		if self.mode == 1:
			self.color = tuple(random.choices(range(256), k=3))
		else:
			self.color = (255, 0, 0)

		for p in self.positions:
			r = pygame.Rect((p[0], p[1]), GRID)
			pygame.draw.rect(surface, self.color, r)
			pygame.draw.rect(surface, (10, 10, 10), r, 1)

	def keys_handler(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_r:
					if self.mode == 0:
						self.mode = 1
					else:
						self.mode = 0
				elif event.key == pygame.K_p or event.key == pygame.K_ESCAPE:
					self.run = "pause"
				else:
					self.run = "run"
					if event.key == pygame.K_UP or event.key == pygame.K_w:
						self.turn(UP)
					if event.key == pygame.K_DOWN or event.key == pygame.K_s:
						self.turn(DOWN)
					if event.key == pygame.K_LEFT or event.key == pygame.K_a:
						self.turn(LEFT)
					if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
						self.turn(RIGHT)

class Food():

	def __init__(self):
		self.position = (0, 0)
		self.color = (0, 255, 255)
		self.rand_position()


	def rand_position(self):
		global SNAKE_POSITIONS
		empty = [grid for grid in ALL_GRIDS if grid not in SNAKE_POSITIONS]
		self.position = (random.choice(empty))

	def draw(self, surface):
		r = pygame.Rect((self.position[0], self.position[1]), (GRID))
		pygame.draw.rect(surface, self.color, r)
		pygame.draw.rect(surface, (10, 10, 10), r, 1)

def draw_grid(surface):
	for y in range(0, int(GRID_HEIGHT)):
		for x in range(0, int(GRID_WIDTH)):
			r = pygame.Rect((x*GRIDSIZE, y*GRIDSIZE), (GRID))
			if (x + y) % 2 == 0:
				pygame.draw.rect(surface, (10, 10, 10), r)
			else:
				pygame.draw.rect(surface, (0, 0, 0), r)

WIDTH = HEIGHT = 576

GRIDSIZE = 64
ALL_GRIDS = [(x, y) for x in range(0, WIDTH, GRIDSIZE) for y in range(0, HEIGHT, GRIDSIZE)]
SNAKE_POSITIONS = []
GRID = (GRIDSIZE, GRIDSIZE)
GRID_WIDTH = WIDTH/GRIDSIZE
GRID_HEIGHT = HEIGHT/GRIDSIZE
UP = (0,-1)
DOWN = (0,1)
LEFT = (-1,0)
RIGHT = (1,0)

DIRS = [UP, DOWN, LEFT, RIGHT]

def main():
	pygame.init()

	clock = pygame.time.Clock()
	WIN = pygame.display.set_mode((WIDTH, HEIGHT))

	pygame.display.set_caption("Snaked")
	pygame.display.set_icon(pygame.image.load("./data/images/icon.png"))

	surface = pygame.Surface(WIN.get_size())
	surface = surface.convert()

	snake = Snake()
	food = Food()

	def text_display():
		score_font = pygame.font.Font('./data/font/Psilent.otf', 18)
		start_font = pygame.font.Font('./data/font/Psilent.otf', 120)
		menu_font = pygame.font.Font('./data/font/Psilent.otf', 40)
		high_font = pygame.font.Font('./data/font/Psilent.otf', 22)

		if snake.run == "run":
			game_score  = score_font.render(f"Score: {snake.score}", 1, (200, 200, 200))
			WIN.blit(game_score, (5, 10))
		elif snake.run == "pause":
			pause_l = pygame.Rect((192, 192), (64, 192))
			pause_ll = pygame.Rect((320, 192), (64, 192))
			pygame.draw.rect(surface, (200, 200, 200), pause_l)
			pygame.draw.rect(surface, (200, 200, 200), pause_ll)	
		else:
			snaked = start_font.render(f"Snaked", 1, (200, 200, 200))
			main_menu = menu_font.render(f"Use keyboard to play", 1, (200, 200, 200))
			h_s = high_font.render(f"High score: {snake.high_score}", 1, (200, 200, 200))
			WIN.blit(snaked, (78, 40))
			WIN.blit(main_menu, (78, 400))
			WIN.blit(h_s, (220, 170))

	while 1:
		clock.tick(8)
		snake.keys_handler()

		if snake.run == "run":
			draw_grid(surface)
			snake.move()
			#snake.change_color()
			if snake.get_head_position() == food.position:
				snake.length += 1
				snake.score += 1
				food.rand_position()
			snake.draw(surface)
			food.draw(surface)
			WIN.blit(surface, (0, 0))
			text_display()
		elif snake.run == "pause":
			draw_grid(surface)
			snake.draw(surface)
			food.draw(surface)
			text_display()
			WIN.blit(surface, (0, 0))
		else:
			food.rand_position()
			draw_grid(surface)
			snake.draw(surface)
			WIN.blit(surface, (0, 0))
			text_display()

		pygame.display.update()
		
	pygame.quit()



if __name__ == '__main__':
	main()
