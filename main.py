import  pygame
from pygame import mixer
import asyncio

async def main():

    pygame.init()


    screen = pygame.display.set_mode((700,800))

    pygame.display.set_caption("Doremon Jump")

    # Force initial render
    screen.fill((255,255,255))
    pygame.display.flip()

    mixer.music.load('assets/sounds/zindegi.ogg')
    mixer.music.play(-1)
    mixer.music.set_volume(0.3)

    bamboo = pygame.image.load('assets/images/bamboo.png')
    bambooY = 0
    bamboo1X = 100
    bamboo2X = 300
    bamboo3X = 500


    def bambooXY1(x,y):
        screen.blit(bamboo,(x,y))
    def bambooXY2(x,y):
        screen.blit(bamboo,(x,y))
    def bambooXY3(x,y):
        screen.blit(bamboo,(x,y))



    dorileft = pygame.image.load('assets/images/dori2.png')
    doriright = pygame.image.load('assets/images/dori1.png')

    doriX = 60
    doriY = 300

    def dorileftXY(x,y):
        screen.blit(dorileft,(x,y))
    def dorirightXY(x,y):
        screen.blit(doriright,(x,y))

    #variable
    left_show = True
    right_show = False
    key_down = False
    y_cng = 0

    #mouse
    mouseleft = pygame.image.load('assets/images/mouse2.png')
    mouseright = pygame.image.load('assets/images/mouse1.png')

    mouse_lx1 = 75 #fixed
    mouse_lx2 = 275 #fixed
    mouse_lx3 = 475 #fixed


    def mouselXY1(x,y):
        screen.blit(mouseleft,(x,y))
    def mouselXY2(x,y):
        screen.blit(mouseleft,(x,y))
    def mouselXY3(x,y):
        screen.blit(mouseleft,(x,y))

    mouse_rx1 = 147 #fixed
    mouse_rx2 = 347 #fixed
    mouse_rx3 = 547 #fixed

    mouse_ly1 = -50
    mouse_ly2 = -250
    mouse_ly3 = -400

    mouse_ry1 = -400
    mouse_ry2 = -50
    mouse_ry3 = -200

    def mouserXY1(x,y):
        screen.blit(mouseright,(x,y))
    def mouserXY2(x,y):
        screen.blit(mouseright,(x,y))
    def mouserXY3(x,y):
        screen.blit(mouseright,(x,y))

    #mouseVariable
    my_cng = 3 #change
    last_speed_milestone = 0

    #gameOver
    gameOver = False
    gmusic = False
    fln_dori = 5 #change
    gfont = pygame.font.SysFont('freesansbold.ttf',128)

    def gameXY(x,y):
        game = gfont.render('GAME OVER',True,(110,0,0))
        screen.blit(game,(x,y))

    score_value = 0
    sfont = pygame.font.SysFont('freesansbold.ttf',40)

    def scoreXY(x,y,score_value):
        score = sfont.render('SCORE: '+str(score_value),True,(100,0,100))
        screen.blit(score,(x,y))

    def wait_text(x,y):
        wait_font = pygame.font.SysFont('freesansbold.ttf', 32)
        text = wait_font.render("Please wait to see the top 5 scores...", True, (0, 0, 150))
        screen.blit(text, (x,y))


    # user interface
    gameStart = False
    button_start = pygame.Rect(200, 690, 250, 80)
    button_pad = pygame.Rect(0, 600, 700, 200)  # x,y,w,h
    button_left = pygame.Rect(470, 660, 100, 80)
    button_right = pygame.Rect(580, 660, 100, 80)
    button_up = pygame.Rect(30,630,100,70)
    button_down = pygame.Rect(30,710,100,70)
    button_continue = pygame.Rect(200, 640, 270, 80)

    font_btn= pygame.font.SysFont('freesansbold.ttf', 40)

    def draw_start_button():
        pygame.draw.rect(screen, (10, 200, 10), button_start, border_radius=20)
        text = font_btn.render("START", True, (0, 0, 0))
        screen.blit(text, (button_start.x + 50, button_start.y + 20))
    def draw_button_pad():
        pygame.draw.rect(screen, (200, 150, 200), button_pad)
    def draw_buttons():
        pygame.draw.rect(screen, (100, 100, 100), button_left, border_radius= 20)
        text = font_btn.render("<<", True, (0, 0, 0))
        screen.blit(text, (button_left.x + 30, button_left.y + 20))

        pygame.draw.rect(screen, (100, 100, 100), button_right, border_radius=20)
        text = font_btn.render(">>", True, (0, 0, 0))
        screen.blit(text, (button_right.x + 35, button_right.y + 20))

        pygame.draw.rect(screen, (100, 100, 100), button_up, border_radius=20)
        text = font_btn.render("up", True, (0, 0, 0))
        screen.blit(text, (button_up.x + 25, button_up.y + 20))

        pygame.draw.rect(screen, (100, 100, 100), button_down, border_radius=20)
        text = font_btn.render("down", True, (0, 0, 0))
        screen.blit(text, (button_down.x + 15, button_down.y + 20))

    def draw_continue_button():
        pygame.draw.rect(screen, (250, 100, 10), button_continue, border_radius=30)
        text = font_btn.render("Continue", True, (0, 0, 0))
        screen.blit(text, (button_continue.x + 40, button_continue.y + 20))

    #name box
    name_font = pygame.font.SysFont('freesansbold.ttf', 50)

    input_box = pygame.Rect(150, 350, 400, 60)  # x, y, width, height
    color_inactive = (100, 100, 100)
    color_active = (0, 200, 0)
    color = color_inactive
    active = False
    player_name = ""
    done = False

    #top5 score:

    import requests

    score_board = False

    # তোমার Google Apps Script Web App URL
    WEB_APP_URL = "https://script.google.com/macros/s/AKfycbyvf5T0B07HFGU6u7nLOoCTeS749wh6U068C4A5o1c8zHaQSrQEk4GrnFmjFsKY-AlEcA/exec"

    def save_score(player_name, score_value):
        """Send player score to Google Sheets via Web App"""
        try:
            data = {"name": player_name, "score": score_value}
            res = requests.post(WEB_APP_URL, json=data)
            if res.status_code == 200:
                print("Score saved successfully!")
            else:
                print("Failed to save score:", res.text)
        except Exception as e:
            print("Error saving score:", e)

    def load_scores():
        """Load top scores from Google Sheets"""
        try:
            res = requests.get(WEB_APP_URL)
            if res.status_code == 200:
                scores = res.json()  # [{"name": "Arafat", "score": 150, "time": "..."} , ...]
                # Sort by score descending and take top 5
                scores.sort(key=lambda x: x["score"], reverse=True)
                return scores[:5]
            else:
                print("Failed to load scores:", res.text)
                return []
        except Exception as e:
            print("Error loading scores:", e)
            return []

    def get_rank_str(index):
        if index == 0:
            return "1st"
        elif index == 1:
            return "2nd"
        elif index == 2:
            return "3rd"
        else:
            return f"{index+1}th"

    # On-screen keyboard
    keys_rows = [
        ["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P"],
        ["A", "S", "D", "F", "G", "H", "J", "K", "L"],
        ["Z", "X", "C", "V", "B", "N", "M", "DEL", "ENT"]
    ]

    key_buttons = []
    key_width = 60
    key_height = 60
    padding = 5
    start_x = 50
    start_y = 450

    for row_idx, row in enumerate(keys_rows):
        for col_idx, k in enumerate(row):
            rect = pygame.Rect(
                start_x + col_idx * (key_width + padding),
                start_y + row_idx * (key_height + padding),
                key_width, key_height
            )
            key_buttons.append((k, rect))

    clock = pygame.time.Clock()
    running = True

    while running:
        screen.fill((255,255,255))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and gameOver == False:

                if event.key == pygame.K_RIGHT and doriX<= 523 and gameStart == True:
                    jump_s = mixer.Sound('assets/sounds/coinS.ogg')
                    jump_s.play()
                    key_down = True
                    if (doriX == 60 or doriX == 261 or doriX == 462 ) and key_down == True: #doriX60 to 523
                        doriX+=61  #fixed
                        left_show = False
                        right_show = True
                        key_down = False
                    if (doriX == 121 or doriX == 322 ) and key_down == True: #doriX60t0523
                        doriX+= 140 #fixed
                        left_show = True
                        right_show = False
                        key_down = False

                if event.key == pygame.K_LEFT and doriX>=121 and gameStart == True:
                    jump_s = mixer.Sound('assets/sounds/coinS.ogg')
                    jump_s.play()
                    key_down = True
                    if (doriX == 60 or doriX == 261 or doriX == 462 ) and key_down == True: #doriX60 to 523
                        doriX-=140 #fixed
                        left_show = False
                        right_show = True
                        key_down = False
                    if (doriX == 121 or doriX == 322 or doriX == 523) and key_down == True: #doriX60 to 523
                        doriX-= 61 #fixed
                        left_show = True
                        right_show = False
                        key_down = False

                if event.key == pygame.K_UP and gameStart == True:
                    y_cng = -3 #change
                if event.key == pygame.K_DOWN and gameStart == True:
                    y_cng = 3 #change
                if active and gameStart == False:
                    if active:
                        if event.key == pygame.K_RETURN:
                            gameStart = True  # start game after name entered
                        elif event.key == pygame.K_BACKSPACE:
                            player_name = player_name[:-1]
                        else:
                            if len(player_name) < 16:
                                player_name += event.unicode
            if event.type == pygame.KEYUP:
                y_cng = 0

            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_box.collidepoint(event.pos):
                    active = True
                else:
                    active = False
                color = color_active if active else color_inactive
                if button_start.collidepoint(event.pos) and gameStart == False:
                    if player_name.strip() != "": #name input na deya porjonto game start hobe na
                        gameStart = True
                if button_right.collidepoint(event.pos) and doriX<= 523 and gameStart == True:
                    jump_s = mixer.Sound('assets/sounds/coinS.ogg')
                    jump_s.play()
                    key_down = True
                    if (doriX == 60 or doriX == 261 or doriX == 462) and key_down == True:  # doriX60 to 523
                        doriX += 61  # fixed
                        left_show = False
                        right_show = True
                        key_down = False
                    if (doriX == 121 or doriX == 322) and key_down == True:  # doriX60t0523
                        doriX += 140  # fixed
                        left_show = True
                        right_show = False
                        key_down = False
                if button_left.collidepoint(event.pos) and doriX>=121 and gameStart == True:
                    jump_s = mixer.Sound('assets/sounds/coinS.ogg')
                    jump_s.play()
                    key_down = True
                    if (doriX == 60 or doriX == 261 or doriX == 462) and key_down == True:  # doriX60 to 523
                        doriX -= 140  # fixed
                        left_show = False
                        right_show = True
                        key_down = False
                    if (doriX == 121 or doriX == 322 or doriX == 523) and key_down == True:  # doriX60 to 523
                        doriX -= 61  # fixed
                        left_show = True
                        right_show = False
                        key_down = False
                if button_up.collidepoint(event.pos) and gameStart == True:
                    y_cng = -3  # change
                if button_down.collidepoint(event.pos) and gameStart == True:
                    y_cng = 3  # change
                if gameStart == False:  # only during name entry
                    for k, rect in key_buttons:
                        if rect.collidepoint(event.pos):
                            if k == "DEL":  # backspace
                                player_name = player_name[:-1]
                            elif k == "ENT":  # start game
                                if player_name.strip() != "":
                                    gameStart = True
                            else:  # regular letter
                                if len(player_name) < 16:
                                    player_name += k

            if event.type == pygame.MOUSEBUTTONUP:
                y_cng = 0

        #gameline
        if gameOver == False and gameStart == True:
            doriY+=y_cng
            if doriY<=100:
                doriY = 100
            if doriY>= 480:
                doriY = 480

            mouse_ly1+= my_cng
            if mouse_ly1 >= 650:
                mouse_ly1 = -30
                score_value+=1
            mouse_ly2 += my_cng
            if mouse_ly2 >= 650:
                mouse_ly2 = -30
                score_value += 1
            mouse_ly3 += my_cng
            if mouse_ly3 >= 650:
                mouse_ly3 = -30
                score_value += 1

            mouse_ry1 += my_cng
            if mouse_ry1 >= 650:
                mouse_ry1 = -30
                score_value += 1
            mouse_ry2 += my_cng
            if mouse_ry2 >= 650:
                mouse_ry2 = -30
                score_value += 1
            mouse_ry3 += my_cng
            if mouse_ry3 >= 650:
                mouse_ry3 = -30
                score_value += 1

            #increase mouse speed according to scores
            speed_milestone = score_value // 20
            if speed_milestone > last_speed_milestone:
                my_cng += 1
                last_speed_milestone = speed_milestone
        #gmeover
        if doriX == 60 and doriY <= mouse_ly1+20 <= doriY+100 :
            gameOver = True
        if doriX == 261 and doriY <= mouse_ly2 + 20 <= doriY + 100:
            gameOver = True
        if doriX == 462 and doriY <= mouse_ly3 + 20 <= doriY + 100:
            gameOver = True

        if doriX == 121 and doriY <= mouse_ry1+20 <= doriY+100 :
            gameOver = True
        if doriX == 322 and doriY <= mouse_ry2 + 20 <= doriY + 100:
            gameOver = True
        if doriX == 523 and doriY <= mouse_ry3 + 20 <= doriY + 100:
            gameOver = True

        if gameOver == True and gmusic == False:
            mixer.music.stop()
            gover_s = mixer.Sound('assets/sounds/falling-game-over.ogg')
            gover_s.play()
            if doriX == 60:
                doriX = 45
            if doriX == 261:
                doriX = 246
            if doriX == 462:
                doriX = 447
            if doriX == 121:
                doriX = 136
            if doriX == 322:
                doriX = 338
            if doriX == 523:
                doriX = 538
            gmusic = True

        #dorifalln

        bambooXY1(bamboo1X,bambooY)
        bambooXY2(bamboo2X, bambooY)
        bambooXY3(bamboo3X, bambooY)

        mouselXY1(mouse_lx1,mouse_ly1)
        mouselXY2(mouse_lx2, mouse_ly2)
        mouselXY3(mouse_lx3, mouse_ly3)

        mouserXY1(mouse_rx1,mouse_ry1)
        mouserXY2(mouse_rx2, mouse_ry2)
        mouserXY3(mouse_rx3, mouse_ry3)

        #doreamon
        if left_show == True:
            dorileftXY(doriX,doriY)
        if right_show == True:
            dorirightXY(doriX,doriY)


        scoreXY(520,10,score_value)
        draw_button_pad()

        if gameOver:
            # ১. ডোরিমন নিচে পড়ার animation
            if doriY < 650:  # screen নিচে পর্যন্ত যাবে
                doriY += fln_dori
            else:
                doriY = 650  # final position

            # ২. শুধু একবার sound & score save
            if not gmusic:
                mixer.music.stop()
                gover_s = mixer.Sound('assets/sounds/falling-game-over.ogg')
                gover_s.play()
                gmusic = True
            if score_board==False and doriY>=650:
                save_score(player_name, score_value)
                score_board = True

            # ৩. GAME OVER text
            gameXY(100, 250)
            wait_text(180,600)

            # ৪. leaderboard একবার show করবে
            if score_board == True:
                top_scores = load_scores()  # Google Sheets থেকে top 5
                y_offset = 630
                score_font = pygame.font.SysFont('freesansbold.ttf', 35)
                for idx, entry in enumerate(top_scores):
                    name = entry["name"]
                    score = entry["score"]
                    rank = get_rank_str(idx)
                    text = score_font.render(f"{rank}: {name} - {score}", True, (0, 0, 150))
                    screen.blit(text, (180, y_offset))
                    y_offset += 30

        if gameStart == True:
            draw_buttons()
        if gameStart == False:
            draw_start_button()
            # draw input box
            pygame.draw.rect(screen, (200, 200, 200), input_box)  # fill background
            pygame.draw.rect(screen, color, input_box, 2)  # border

            if player_name == "" and not active:
                # show placeholder when box is inactive and empty
                placeholder_surface = name_font.render("Enter your name", True, (150, 150, 150))
                screen.blit(placeholder_surface, (input_box.x + 5, input_box.y + 10))
            else:
                # show actual typed name
                text_surface = name_font.render(player_name, True, (0, 0, 0))
                screen.blit(text_surface, (input_box.x + 5, input_box.y + 10))

                # draw keyboard
            for k, rect in key_buttons:
                pygame.draw.rect(screen, (180, 180, 180), rect, border_radius=8)
                key_text = font_btn.render(k, True, (0, 0, 0))
                screen.blit(key_text, (rect.x + 10, rect.y + 10))

        clock.tick(60)  # change
        pygame.display.flip()
        await asyncio.sleep(0)

# This is the program entry point
asyncio.run(main())


