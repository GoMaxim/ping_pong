import pygame
import random
import math

pygame.init()
scr = pygame.display.set_mode((500, 500))
clock = pygame.time.Clock()


def rare_high_rgb(power=1):
    r = int((random.random() ** power) * 255)
    g = int((random.random() ** power) * 255)
    b = int((random.random() ** power) * 255)
    return r, g, b

def brightness_to_rarity_percent(rgb):
    r, g, b = rgb
    brightness = 0.299 * r + 0.587 * g + 0.114 * b
    percent = (brightness / 255.0) * 100.0
    return percent


class Area:
    def __init__(self, x, y, width, height, color=(255, 255, 255)):
        self.rect = pygame.Rect(x, y, width, height)
        self.fill_color = color

    def draw(self):
        pygame.draw.rect(scr, self.fill_color, self.rect)

    def change_color(self, x_color):
        self.fill_color = x_color

class Label(Area):
    def settext(self, fsize, text, text_color):
        self.font_size = int(fsize)
        self.text = text
        self.text_color = text_color
        try:
            font = pygame.font.SysFont('Verdana', int(fsize))
        except:
            font = pygame.font.Font(None, int(fsize))
        self.image = font.render(self.text, True, self.text_color)

    def drawn(self, shift_x, shift_y):
        self.draw()
        scr.blit(self.image, (self.rect.x + shift_x, self.rect.y + shift_y))


current_rgb = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))


is_rolling = False
roll_total_frames = 0          
roll_step_frames = 5           
roll_max_frames = 180           
final_rgb = None
final_rare_text = ""


hold_final_color = False
hold_frames_left = 0

timer = 0
gradient_timer = 0.0
times = 0.0
random_color_thingy = random.randint(1, 8)
random_color_thingy1 = random.randint(1, 4)
random_color_thingy2 = random.randint(1, 2)
y_mover = True
atts = 1
colors = []
colors_rarity = []

speed_x = 3
speed_y = 3
move_speed_y = 0.5

show_latest = True
show = False

gen_button = Label(162, 300, 265, 75, (0, 0, 0))
gen_button.settext(17, 'Нажми чтобы получить цвет!', (0, 0, 0))

rarity_text = Label(135, 25, 0, 0, (0, 0, 0))
rarity_text.settext(25, 'Редкость:', (0, 0, 0))

rgb_vl_text = Label(0, 175, 0, 0, (0, 0, 0))
rgb_vl_text.settext(25, 'Последний цвет:', (0, 0, 0))
viewing_rect = Area(150, 175, 300, 20, (0, 0, 0))

lucky_countdown = Label(150, 450, 0, 0, (0, 0, 0))
lucky_countdown.settext(15, f'До следующей удачи ещё {10 - atts} попыток', (0, 0, 0))

bouncy_logo = Label(random.randint(0, 350), random.randint(0, 350), 200, 25, (0, 0, 0))
bouncy_logo.settext(20, 'Поставь три лайка!', (255, 255, 255))

FPS = 60
HOLD_FRAMES = 90  

while True:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if is_rolling:
                break

            x, y = event.pos
            if gen_button.rect.collidepoint(x, y):
                atts += 1

                if atts % 10 == 0:
                    lucky_countdown.settext(20, 'УУУУУДАЧА!! (10x шанс)', (255, 0, 0))
                    final_rgb = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
                    atts = 0
                else:
                    power = 1
                    final_rgb = rare_high_rgb(power=power)
                    remaining = 10 - (atts % 10)
                    lucky_countdown.settext(15, f'До следующей удачи ещё {remaining} попыток', (0, 0, 0))

                rare_pct = brightness_to_rarity_percent(final_rgb)
                inverted_rare = 100 - rare_pct
                final_rare_text = f'Редкость: {inverted_rare:.1f}%'

                is_rolling = True
                roll_total_frames = 0
                roll_step_frames = 5
                current_rgb = (0, 0, 0)

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_l:
                show_latest = True
            elif event.key == pygame.K_r:
                show_latest = False

    mx, my = pygame.mouse.get_pos()
    show = viewing_rect.rect.collidepoint(mx, my)
    if show:
        if show_latest:
            showed_color = Area(mx, my, 135, 135, last_rgb)
        else:
            showed_color = Area(mx, my, 135, 135, rarest_rgb)
        show = True
    else:
        show = False

    if is_rolling:
        roll_total_frames += 1

        if roll_total_frames % roll_step_frames == 0 or roll_total_frames == 1:
            current_rgb = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
            roll_step_frames = min(roll_step_frames * 1.5, roll_max_frames)


        if roll_total_frames >= roll_max_frames:
            is_rolling = False
            hold_final_color = True
            hold_frames_left = HOLD_FRAMES
            current_rgb = final_rgb
            rarity_text.settext(22, final_rare_text, (0, 0, 0))
            rgb_vl_text.settext(25, f'Тебе выпал цвет: {final_rgb}', (0, 0, 0))

            colors.append(final_rgb)
            colors_rarity.append(100 - brightness_to_rarity_percent(final_rgb))


    elif hold_final_color:
        hold_frames_left -= 1
        if hold_frames_left <= 0:
            hold_final_color = False

    if not is_rolling and not hold_final_color:
        timer += 1
        if timer >= 60:
            current_rgb = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
            timer = 0

    times += 1.666667
    if times >= 240:
        random_color_thingy = random.randint(1, 2)
        random_color_thingy1 = random.randint(1, 4)
        random_color_thingy2 = random.randint(1, 2)
        times = 0


    bouncy_logo.rect.x += speed_x
    bouncy_logo.rect.y += speed_y
    if bouncy_logo.rect.y < 0 or bouncy_logo.rect.y >= 425:
        speed_y *= -1
    if bouncy_logo.rect.x <= 0 or bouncy_logo.rect.x >= 375:
        speed_x *= -1


    next_y = gen_button.rect.y

    if y_mover:  
        next_y -= move_speed_y
        if next_y <= 250:
            gen_button.rect.y = 250
            y_mover = False
        else:
            gen_button.rect.y = next_y
    else:  
        next_y += move_speed_y
        if next_y >= 350:
            gen_button.rect.y = 350  
            y_mover = True
        else:
            gen_button.rect.y = next_y

    gradient_timer += 0.1
    s = math.sin(gradient_timer)
    r_val = int((s + random_color_thingy) * 127.5)
    g_val = int((s + random_color_thingy1) * 127.5 + 127.5)
    b_val = int((s + random_color_thingy2) * 127.5 + 127.5)
    r_val = max(0, min(255, r_val))
    g_val = max(0, min(255, g_val))
    b_val = max(0, min(255, b_val))
    gen_button.change_color((r_val, g_val, b_val))


    if show_latest:
        if colors:
            last_rgb = colors[-1]
            last_rare = colors_rarity[-1]
            rgb_vl_text.settext(25, f'Твой Последний цвет: {last_rgb}', (0, 0, 0))
            rarity_text.settext(22, f'Редкость: {last_rare:.1f}%', (0, 0, 0))
        else:
            last_rgb = (0, 0, 0)
            rgb_vl_text.settext(25, 'Нет цветов', (0, 0, 0))
            rarity_text.settext(22, 'Редкость: 100%', (0, 0, 0))
    else:
        if colors_rarity:
            best_index = colors_rarity.index(min(colors_rarity))
            rarest_rgb = colors[best_index]
            rarest_rarity = colors_rarity[best_index]
            rgb_vl_text.settext(25, f'Твой лучший цвет: {rarest_rgb}', (0, 0, 0))
            rarity_text.settext(22, f'Самый редкий %: {rarest_rarity:.1f}%', (0, 0, 0))
        else:
            rarest_rgb = (0, 0, 0)
            rgb_vl_text.settext(25, 'Нет цветов', (0, 0, 0))
            rarity_text.settext(22, 'Редкость: 100%', (0, 0, 0))

    scr.fill(current_rgb)

    bouncy_logo.drawn(0, 0)
    rarity_text.drawn(0, 0)
    lucky_countdown.drawn(0, 0)
    rgb_vl_text.drawn(0, 0)

    if not is_rolling:
        gen_button.drawn(3.75, 30)
    if show:
        showed_color.draw()    

    pygame.display.update()