import pygame
import time

pygame.init()
screen = pygame.display.set_mode((618, 359),) # flags=pygame.NOFRAME размер окна
pygame.display.set_caption("Ночное приключение Адольфа") # имя приложение 
icon = pygame.image.load('img/icon/ico.png') # подгрузить изображение
pygame.display.set_icon(icon) # иконка приложения

#обьекты
bg = pygame.image.load('img/bg/bg.png') #задний фон 
ghost = pygame.image.load('img/ghost/ghost.jpg') # враги

#игрок \/
walk_right = [
	pygame.image.load('img/player right/0.png'),
	pygame.image.load('img/player right/1.png'), 
	pygame.image.load('img/player right/3.png'), 
	pygame.image.load('img/player right/4.png'), 
]
walk_left = [
	pygame.image.load('img/player left/0.png'),
	pygame.image.load('img/player left/1.png'), 
	pygame.image.load('img/player left/2.png'), 
	pygame.image.load('img/player left/3.png'), 
]

#переменые
player_anim_count = 0
bg_x = 0 

player_speed = 5
player_x = 150
player_y = 250

is_jump = False
jump_count = 8
gameplay = True

ghost_timer = pygame.USEREVENT + 1
pygame.time.set_timer(ghost_timer, 2500)
ghost_list_in_game = []

bullet = pygame.image.load('img/bullets/bullets.jpg')
bullets =[] 
bullets_left = 30

#надписи для счета
font = pygame.font.Font('font/Lumanosimo-Regular.ttf', 20)

#надписи для пройгрыша
text_lose = font.render('You lost press Q to quit the game', False, 'Red')	# создание текстовой натписи пройгрыша
text_lose1 = font.render('or press R to restart the game', False, 'Red')

#звуки
bg_sound = pygame.mixer.Sound('sounds/bg sound/4.mp3')
bg_sound.play()
jump_mp3 = pygame.mixer.Sound('sounds/player sounds/player jump sours/jump.mp3')

#бескноечный цикл
running = True
while running:
	time.sleep(0.060)

	screen.blit(bg, (bg_x, 0))
	screen.blit(bg, (bg_x + 618, 0))

	
	keys = pygame.key.get_pressed()

	if gameplay:
		player_rect = walk_left[0].get_rect(topleft=(player_x, player_y))
		
		if ghost_list_in_game:
			for (i, el) in enumerate(ghost_list_in_game):
				screen.blit(ghost, el)
				el.x -= 10

				if el.x < -10:
					ghost_list_in_game.pop(i) #унечтожение обьекта
				if player_rect.colliderect(el):
						gameplay = False
		#считывание на что нажал игрок
		
		if keys[pygame.K_LEFT]:
			screen.blit(walk_right[player_anim_count], (player_x, player_y))
		else:
			screen.blit(walk_left[player_anim_count], (player_x, player_y))

		if keys[pygame.K_LEFT] and player_x > 50:
			player_x -= player_speed

		elif keys[pygame.K_RIGHT] and player_x < 300:
			player_x += player_speed

		if not is_jump:
			if keys[pygame.K_SPACE]:
				jump_mp3.play()
				is_jump = True 
		else:
			if jump_count >= -8:
				if jump_count > 0:
					player_y -= (jump_count ** 2) / 2
				else:
					player_y += (jump_count ** 2) / 2
				jump_count -= 1
			else:
				is_jump = False
				jump_count = 8

		if player_anim_count == 3:
			player_anim_count = 0
		else:
			player_anim_count += 1

		bg_x -= 2
		if bg_x == -618:
			bg_x = 0
		if keys[pygame.K_g] and bullets_left > 0:
			bullets.append(bullet.get_rect(topleft=(player_x + 30, player_y)))
			print("bullets: ", bullets_left)
			bullets_left -= 1
			
		 	
		if bullets:
			for (iw,elen) in enumerate(bullets):
				screen.blit(bullet, (elen.x, elen.y))
				elen.x += 4 
				if elen.x > 630:
					bullets.pop()
					bullets.clear()
					time.sleep(0.1)

				if ghost_list_in_game:
					for (index,ghost1) in enumerate(ghost_list_in_game):
						if elen.colliderect(ghost1):
							ghost_list_in_game.pop(index)
							bullets.pop(iw)	

	else:
		screen.fill((87,88,89))
		bg_sound.stop()

		screen.blit(text_lose,(100, 0)) 
		screen.blit(text_lose1,(100, 30))

		if keys[pygame.K_q]:
			running = False
		if keys[pygame.K_r]:
			bullets_left = 30
			bullets.clear()
			ghost_list_in_game.clear()
			player_x = 50
			bg_sound.play()
			gameplay = True
		
	pygame.display.update() #обновлять экран

	for event in pygame.event.get(): # считывание нажатия на крестик
		if event.type == pygame.QUIT:
	 		running = False 

		if event.type == ghost_timer:
			ghost_list_in_game.append(ghost.get_rect(topleft=(620, 250))) 
