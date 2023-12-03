import pandas as pd
import pygame
from sklearn.linear_model import LinearRegression
import time

pygame.init()

WIDTH, HEIGHT = 1000, 750
BUTTON_WIDTH,  BUTTON_HEIGHT = 150, 50

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Prodigy_ML_01")
BG = pygame.transform.scale(pygame.image.load("imgs\\bg.png"), (WIDTH, HEIGHT))
BG_LAYER = pygame.transform.scale(pygame.image.load("imgs\\bg_layer.png"), (800, 700))
SUBMIT = pygame.image.load("imgs\\submit.png")

base_font = pygame.font.Font(None, 32)

input_LotArea = pygame.Rect(350, 300, 140, 32)
input_FullBath = pygame.Rect(350, 350, 140, 32)
input_BedroomAbvGr = pygame.Rect(425, 400, 140, 32)

def draw(LotArea, color_LotArea, FullBath, color_FullBath, BedroomAbvGr, color_BedroomAbvGr, visible_result, result):

    WIN.blit(BG, (0, 0))
    WIN.blit(BG_LAYER, (8, 25))
    WIN.blit(SUBMIT, (240, 125))

    pygame.draw.rect(WIN, color_LotArea, input_LotArea)
    pygame.draw.rect(WIN, color_FullBath, input_FullBath)
    pygame.draw.rect(WIN, color_BedroomAbvGr, input_BedroomAbvGr)

    text_surface = base_font.render(LotArea, True, (255, 255, 255))
    text_surface1 = base_font.render(FullBath, True, (255, 255, 255))
    text_surface2 = base_font.render(BedroomAbvGr, True, (255, 255, 255))

    WIN.blit(text_surface, (input_LotArea.x + 5, input_LotArea.y + 5))
    WIN.blit(text_surface1, (input_FullBath.x + 5, input_FullBath.y + 5))
    WIN.blit(text_surface2, (input_BedroomAbvGr.x + 5, input_BedroomAbvGr.y + 5))

    input_LotArea.w = max(100, text_surface.get_width() + 10)
    input_FullBath.w = max(100, text_surface1.get_width() + 10)
    input_BedroomAbvGr.w = max(100, text_surface2.get_width() + 10)

    text_LotArea = base_font.render("LotArea :", 1, (0, 0, 0))
    text_FullBath = base_font.render("FullBath :", 1, (0, 0, 0))
    text_BedroomAbvGr = base_font.render("BedroomAbvGr :", 1, (0, 0, 0))

    WIN.blit(text_LotArea, (245, 305))
    WIN.blit(text_FullBath, (245, 355))
    WIN.blit(text_BedroomAbvGr, (245, 405))

    if visible_result:
        text_result = base_font.render(f"$ {result}", 1, (0, 0, 0))
        WIN.blit(text_result, (245, 500))

    pygame.display.update()



def main():

    result = ""
    visible_result = False
    LotArea = ""
    FullBath = ""
    BedroomAbvGr = ""
    active_LotArea = False
    active_FullBath = False
    active_BedroomAbvGr = False
    back_LotArea = False
    back_FullBath = False
    back_BedroomAbvGr = False
    color_active = pygame.Color('lightskyblue3')
    color_passive = pygame.Color('azure4')
    color_LotArea = color_passive
    color_FullBath = color_passive
    color_BedroomAbvGr = color_passive

    df = pd.read_csv('train.csv')
    df2 = pd.read_csv('test.csv')

    X = df[['LotArea', 'FullBath', 'BedroomAbvGr']]
    y = df['SalePrice']
    X_test = df2[['LotArea', 'FullBath', 'BedroomAbvGr']]

    model = LinearRegression()
    model.fit(X, y)

    y_pred = model.predict(X_test)

    run = True

    while run:

        mouse_x, mouse_y = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.MOUSEBUTTONDOWN and input_LotArea.collidepoint(event.pos):
                active_LotArea = True
                active_FullBath = False
                active_BedroomAbvGr = False

            if event.type == pygame.MOUSEBUTTONDOWN and input_FullBath.collidepoint(event.pos):
                active_FullBath = True
                active_LotArea = False
                active_BedroomAbvGr = False

            if event.type == pygame.MOUSEBUTTONDOWN and input_BedroomAbvGr.collidepoint(event.pos):
                active_FullBath = False
                active_LotArea = False
                active_BedroomAbvGr = True

            if event.type == pygame.MOUSEBUTTONDOWN and 253 <= mouse_x <= 524 and 134 <= mouse_y <= 234:
                if 0 < len(LotArea) and 0 < len(FullBath) and 0 < len(BedroomAbvGr):
                    a = LotArea
                    b = FullBath
                    c = BedroomAbvGr

                    new_data_point = [[int(a), int(b), int(c)]]

                    predicted_sale_price = model.predict(new_data_point)

                    result = predicted_sale_price[0]

                    visible_result = True


            if event.type == pygame.KEYDOWN and active_LotArea:
                if event.key == pygame.K_BACKSPACE and event.key != pygame.K_RETURN:
                    back_LotArea = True

                elif event.key != pygame.K_RETURN:
                    if len(LotArea) <= 6:
                        LotArea += event.unicode

                else:
                    active_LotArea = False

            if event.type == pygame.KEYDOWN and active_FullBath:
                if event.key == pygame.K_BACKSPACE and event.key != pygame.K_RETURN:
                    back_FullBath = True

                elif event.key != pygame.K_RETURN:
                    if len(FullBath) <= 0:
                        FullBath += event.unicode

                else:
                    active_FullBath = False

            if event.type == pygame.KEYDOWN and active_BedroomAbvGr:
                if event.key == pygame.K_BACKSPACE and event.key != pygame.K_RETURN:
                    back_BedroomAbvGr = True

                elif event.key != pygame.K_RETURN:
                    if len(BedroomAbvGr) <= 0:
                        BedroomAbvGr += event.unicode

                else:
                    active_BedroomAbvGr = False

            if event.type == pygame.KEYUP and active_LotArea:
                if event.key == pygame.K_BACKSPACE:
                    back_LotArea = False

            if event.type == pygame.KEYUP and active_FullBath:
                if event.key == pygame.K_BACKSPACE:
                    back_FullBath = False

            if event.type == pygame.KEYUP and active_BedroomAbvGr:
                if event.key == pygame.K_BACKSPACE:
                    back_BedroomAbvGr = False

        if back_LotArea:
            time.sleep(0.125)
            LotArea = LotArea[:-1]

        if back_FullBath:
            time.sleep(0.125)
            FullBath = FullBath[:-1]

        if back_BedroomAbvGr:
            time.sleep(0.125)
            BedroomAbvGr = BedroomAbvGr[:-1]

        if active_LotArea:
            color_LotArea = color_active
        else:
            color_LotArea = color_passive

        if active_FullBath:
            color_FullBath = color_active
        else:
            color_FullBath = color_passive

        if active_BedroomAbvGr:
            color_BedroomAbvGr = color_active
        else:
            color_BedroomAbvGr = color_passive


        draw(LotArea, color_LotArea, FullBath, color_FullBath, BedroomAbvGr, color_BedroomAbvGr, visible_result, result)

if __name__ == "__main__":
    main()