import pygame
import random


pygame.init()
screen = pygame.display.set_mode((400, 600))
pygame.display.set_caption('Gunfight')

gunspeed = 30
gunx = 200
playery = -3

#проигрыш
play=0
label=pygame.font.Font('Times.ttf',40)
lose_label=label.render('Вы проиграли!!!',False,'red')
label=pygame.font.Font('Times.ttf',20)
restart_label=label.render('переиграть',False,'red')
restart_label_rect=restart_label.get_rect(topleft=(70,260))
label=pygame.font.Font('Times.ttf',20)
back_label=label.render('назад',False,'red')
back_label_rect=back_label.get_rect(topleft=(300,260))

#выигрыш
label=pygame.font.Font('Times.ttf',40)
win_label=label.render('Вы выиграли!!!',False,'red')

#установка времени
clock = pygame.time.Clock()
clock1 = pygame.time.Clock()
player_timer = pygame.USEREVENT + 1
pygame.time.set_timer(player_timer, 1500)

#анимация
bum=pygame.image.load('пуля.png').convert_alpha()
bums=[]
bg = pygame.image.load('фон-снег.jpg').convert_alpha()
gun = pygame.image.load('пушка1.png').convert_alpha()
player = [
    pygame.image.load('солдат_снег_1.png').convert_alpha(),
    pygame.image.load('солдат_снег_2.png').convert_alpha(),
    pygame.image.load('солдат_снег_3.png').convert_alpha(),
    pygame.image.load('солдат_снег_4.png').convert_alpha(),
]
player_list=[]
count_walking = 0
running = True
k = 0
kol=0
kol_bums=30
while running:
    #вывод на экран
    wall_rect = pygame.draw.rect(screen, (133, 116, 105), (0, 500, 400, 100), 1)
    screen.blit(bg, (0, 0))
    screen.blit(gun, (gunx, 470))

    # игровые характеристики
    label = pygame.font.Font('arial.otf', 10)
    text='lifes:'+str(3-play)+'/'+'3'
    life_label = label.render(text,False,'black')
    screen.blit(life_label, (340, 10))
    text = 'bulles:' + str(kol_bums) + '/' + '30'
    bums_label = label.render(text, False, 'black')
    screen.blit(bums_label, (323, 20))
    text = 'kills:' + str(kol) + '/' + '29'
    kills_label = label.render(text, False, 'black')
    screen.blit(kills_label, (335, 30))

    if play<3 and kol<29:
        #автоматический вывод солдат
        if player_list:
            for (i,e) in enumerate(player_list):
                screen.blit(player[count_walking],e)
                e.y+=7
                if wall_rect.colliderect(e):
                    play += 1
                if e.y>400:
                    player_list.pop(i)
        playery += 10

        #вдижение пушки
        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT] and gunx > 0:
            gunx -= gunspeed
        elif key[pygame.K_RIGHT] and gunx < 325:
            gunx += gunspeed

        #анимация солдата
        if count_walking == 3:
            count_walking = 0
        else:
            count_walking += 1

        #стрельбa
        if bums:
            for (i,e) in enumerate(bums):
                screen.blit(bum,(e.x+21,e.y-15))
                e.y-=10
                if e.y<-40:
                    bums.pop(i)
                if player_list:
                    for (ind,el) in enumerate(player_list):
                        if e.colliderect(el):
                            kol+=1
                            player_list.pop(ind)
                            bums.pop(i)

    elif play>=3:
        screen.fill('grey')
        screen.blit(lose_label,(70,200))
        screen.blit(restart_label, restart_label_rect)
        screen.blit(back_label, back_label_rect)

        #перезапуск
        mouse=pygame.mouse.get_pos()
        if restart_label_rect.collidepoint(mouse) and pygame.mouse.get_pressed()[0]:
            play=0
            gunx=200
            player_list.clear()
            bums.clear()

        #заново
        if back_label_rect.collidepoint(mouse) and pygame.mouse.get_pressed()[0]:
            None

    elif kol>=29:
        screen.fill('grey')
        screen.blit(win_label, (70, 200))
        screen.blit(back_label,back_label_rect)
        mouse = pygame.mouse.get_pos()
        # заново
        if back_label_rect.collidepoint(mouse) and pygame.mouse.get_pressed()[0]:
            None

    pygame.display.update()

    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False
            pygame.quit()
        if e.type == player_timer:
            player_list.append(player[0].get_rect(topleft=(random.randint(10,350),-70)))
        if play<5 and e.type==pygame.KEYUP and e.key==pygame.K_SPACE and kol_bums>0:
            bums.append(bum.get_rect(topleft=(gunx,460)))
            kol_bums-=1
    clock.tick(10)
