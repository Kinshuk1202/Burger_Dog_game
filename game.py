import pygame , random

pygame.init()

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600

screen = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))
pygame.display.set_caption("Burger Dog")

#fps n clock
FPS = 70
clock = pygame.time.Clock()
#values
PLAYER_ST_LIVES = 3
PLAYER_NORMAL_VEL = 5
PLAYER_BOOST_VEL = 10
ST_BOOST_LVL = 100
ST_BURGER_VEL = 3
BURGER_ACC = 0.5

score = 0
burger_points = 0
burgers_eaten = 0

player_lives = PLAYER_ST_LIVES
player_vel = PLAYER_NORMAL_VEL
boost_lvl = ST_BOOST_LVL
burger_vel = ST_BURGER_VEL
BUFFER_DIS = 100
#font

font = pygame.font.Font("burger_dog_assets/WashYourHand.ttf",32)


#colors
ORANGE = (246,170,54)
BLACK = (0,0,0)
WHITE = (255,255,255)
#txt

points_txt = font.render("Burger Points: " + str(burger_points),True,ORANGE)
points_rect = points_txt.get_rect(topleft = (10,10))

score_txt = font.render("Burger Score: " + str(score),True,ORANGE)
score_rect = score_txt.get_rect(topleft = (10,50))

title_txt = font.render("Burger Dog" , True,ORANGE)
title_rect = title_txt.get_rect()
title_rect.centerx = WINDOW_WIDTH//2
title_rect.centery= 15

eaten_txt = font.render("Burgers Eaten: " + str(burgers_eaten) , True,ORANGE)
eaten_rect = eaten_txt.get_rect()
eaten_rect.centerx = WINDOW_WIDTH//2
eaten_rect.centery = 50

lives_txt = font.render("Lives: " + str(player_lives),True,ORANGE)
lives_rect = lives_txt.get_rect(topright = (WINDOW_WIDTH-10,10))

boost_txt = font.render("Boost: " + str(boost_lvl),True,ORANGE)
boost_rect = boost_txt.get_rect(topright = (WINDOW_WIDTH-10,50))

game_ovr_txt = font.render("FINAL SCORE: "+str(score),True,ORANGE)
game_ovr_rect = game_ovr_txt.get_rect(center = (WINDOW_WIDTH//2,WINDOW_HEIGHT//2))

continue_txt = font.render("Press any key to play again",True,ORANGE)
continue_rect = continue_txt.get_rect(center = (WINDOW_WIDTH//2,WINDOW_HEIGHT//2 + 64))
#music

bark_snd = pygame.mixer.Sound("burger_dog_assets/bark_sound.wav")
miss_snd = pygame.mixer.Sound("burger_dog_assets/miss_sound.wav")
pygame.mixer.music.load("burger_dog_assets/bd_background_music.wav")
#imgs

dog_lft = pygame.image.load("burger_dog_assets/dog_left.png")
dog_right = pygame.image.load("burger_dog_assets/dog_right.png")

dog_img = dog_lft

dog_rect = dog_img.get_rect(centerx = WINDOW_WIDTH//2)
dog_rect.bottom = WINDOW_HEIGHT

burger_img = pygame.image.load("burger_dog_assets/burger.png")
burger_rect = burger_img.get_rect()
burger_rect.topleft = (random.randint(0,WINDOW_WIDTH-32),-BUFFER_DIS)

running = True
pygame.mixer.music.play()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and dog_rect.left>0:
        dog_rect.x -= player_vel
        dog_img = dog_lft
    if (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and dog_rect.right<WINDOW_WIDTH:
        dog_rect.x += player_vel
        dog_img = dog_right
    if (keys[pygame.K_UP] or keys[pygame.K_w]) and dog_rect.top>100:
        dog_rect.y -= player_vel
    if (keys[pygame.K_DOWN] or keys[pygame.K_s]) and dog_rect.bottom<WINDOW_HEIGHT:
        dog_rect.y += player_vel
        
    #boost
    if keys[pygame.K_SPACE] and boost_lvl>0:
        player_vel = PLAYER_BOOST_VEL
        boost_lvl -= 1
    else:
        player_vel = PLAYER_NORMAL_VEL
    
    #burger
    burger_rect.y += burger_vel
    burger_points = int((WINDOW_HEIGHT-burger_rect.y + 100)*burger_vel)

    #burger missed
    if burger_rect.y>WINDOW_HEIGHT:
        player_lives -= 1
        miss_snd.play()
        burger_rect.topleft = (random.randint(0,WINDOW_WIDTH-32),-BUFFER_DIS-100)
        burger_vel = ST_BURGER_VEL
        dog_rect.centerx = WINDOW_WIDTH//2
        dog_rect.bottom = WINDOW_HEIGHT
        boost_lvl = ST_BOOST_LVL
    
    #collision
    if dog_rect.colliderect(burger_rect):
        score += burger_points
        burgers_eaten += 1
        bark_snd.play()
        burger_rect.topleft = (random.randint(0,WINDOW_WIDTH-32),-BUFFER_DIS-100)
        burger_vel += BURGER_ACC
        boost_lvl += 25
        if boost_lvl>ST_BOOST_LVL:
            boost_lvl = ST_BOOST_LVL
    
    points_txt = font.render("Burger Points: " + str(burger_points),True,ORANGE)
    score_txt = font.render("Burger Score: " + str(score),True,ORANGE)
    eaten_txt = font.render("Burgers Eaten: " + str(burgers_eaten) , True,ORANGE)
    lives_txt = font.render("Lives: " + str(player_lives),True,ORANGE)
    boost_txt = font.render("Boost: " + str(boost_lvl),True,ORANGE)

    if player_lives == 0:
        game_ovr_txt = font.render("FINAL SCORE: "+str(score),True,ORANGE)
        screen.blit(game_ovr_txt,game_ovr_rect)
        screen.blit(continue_txt,continue_rect)
        pygame.display.update()
        pygame.mixer.music.stop()
        is_paused = True
        while is_paused:
            for ev in pygame.event.get():
                if ev.type == pygame.KEYDOWN:
                    running = True
                    is_paused = False
                    score = 0
                    burgers_eaten = 0
                    player_lives = PLAYER_ST_LIVES
                    boost_lvl = ST_BOOST_LVL
                    burger_vel = ST_BURGER_VEL
                    burger_rect.topleft = (random.randint(0,WINDOW_WIDTH-32),-BUFFER_DIS-100)
                    pygame.mixer.music.play()
                    dog_rect.centerx = WINDOW_WIDTH//2
                    dog_rect.bottom = WINDOW_HEIGHT
                if ev.type == pygame.QUIT:
                    running = False
                    is_paused = False
    screen.fill(BLACK)
    screen.blit(points_txt,points_rect)
    screen.blit(score_txt,score_rect)
    screen.blit(title_txt,title_rect)
    screen.blit(eaten_txt,eaten_rect)
    screen.blit(lives_txt,lives_rect)
    screen.blit(boost_txt,boost_rect)
    pygame.draw.line(screen,WHITE,(0,100),(WINDOW_WIDTH,100),3)

    screen.blit(dog_img,dog_rect)
    screen.blit(burger_img,burger_rect)

    pygame.display.update()
    clock.tick(FPS)

pygame.quit()