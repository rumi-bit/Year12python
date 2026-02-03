import ctypes
import os
import time

os.environ["PYSDL2_DLL_PATH"] = "/usr/lib"

import sdl2.ext  # noqa: F401
from sdl2 import *  # noqa: F403, F405
from sdl2.sdlgfx import *  # noqa: F403, F405
from sdl2.sdlttf import *  # noqa: F403, F405


class OrderSystem:
    def __init__(self):
        self.frozen_fee = 1.05
        self.fishmenu = [
            {"name": "Shark", "price": "4.10", "type": "Normal"},
            {"name": "Flounder", "price": "4.10", "type": "Normal"},
            {"name": "Cod", "price": "4.10", "type": "Normal"},
            {"name": "Gurnet", "price": "4.10", "type": "Normal"},
            {"name": "Hoki", "price": "4.10", "type": "Normal"},
            {"name": "Tarakihi", "price": "4.10", "type": "Normal"},
            {"name": "Snapper", "price": "7.20", "type": "Deluxe"},
            {"name": "Pink Salmon", "price": "7.20", "type": "Deluxe"},
            {"name": "Tuna", "price": "7.20", "type": "Deluxe"},
            {"name": "Smoked Marlin", "price":"7.20", "type": "Deluxe"},
            {"name": "John Dory", "price": "7.20", "type": "Deluxe"},
            {"name": "Swordfish", "price": "7.20", "type": "Deluxe"},
        ]
        self.order = {
            "type": "",
            "fee": 0.0,
            "fish": [],
            "items": [],
            "price": 0.0,
            "name": "",
            "phonenumber": "",
            "address": "",
        }


class AppWindow:
    def __init__(self, logic_ref):
        self.logic = logic_ref
        SDL_Init(SDL_INIT_VIDEO)
        self.window = SDL_CreateWindow(b"Freddy's Fast Fish", SDL_WINDOWPOS_CENTERED, SDL_WINDOWPOS_CENTERED, 800, 600, SDL_WINDOW_SHOWN,)
        self.renderer = SDL_CreateRenderer(self.window, -1, SDL_RENDERER_ACCELERATED)
        self.running = True
        self.state = 0

        if TTF_Init() == -1:
            print(f"TTF Init Error: {TTF_GetError()}")
        script_dir = os.path.dirname(os.path.abspath(__file__))
        font_path = os.path.join(script_dir, "sdlfont.ttf").encode("utf-8")
        self.font_main = TTF_OpenFont(font_path, 24)
        self.font_title = TTF_OpenFont(font_path, 60)
        if not self.font_main or not self.font_title:
            print(f"Font Error: {SDL_GetError()}")

        self.inputs = {
            "name": {
                "rect": SDL_Rect(250, 150, 300, 40),
                "text": "",
                "label": "Full Name",
                "warning": "Invalid name",
            },
            "phone": {
                "rect": SDL_Rect(250, 250, 300, 40),
                "text": "",
                "label": "Phone Number",
            },
            "address": {
                "rect": SDL_Rect(250, 350, 300, 40),
                "text": "",
                "label": "Address",
            },
        }
        self.activefield = None

        self.buttons = {
            "menu": {
                "pickup": {"rect": SDL_Rect(425, 500, 350, 50), "text": "Pickup"},
                "delivery": {"rect": SDL_Rect(25, 500, 350, 50), "text": "Delivery"},
            },
            "details": {"next": {"rect": SDL_Rect(200, 500, 400, 50), "text": "Next"}},
        }

    def validator (self, input, x, y, w, h, checktype = (), length = (), size = (), message = None, colour = (255, 0, 0), active = None ):

        if self.activefield == active:
            for check in checktype:
                if check == "alpha":
                    if len(input) > 0 and not input.replace(" ", "").isalpha():
                        self.drawtext(message, x, y + h + 5, self.font_main, (colour[0], colour[1], colour[2], 255))
                    else:
                        print("valid alpha")

                elif check == "digit":
                    if len(input) > 0 and not input.replace(" ", "").isdigit():
                        self.drawtext(message, x, y + h + 5, self.font_main, (colour[0], colour[1], colour[2], 255))
                    else:
                        print("valid digit")
            if length:
                if len(input) > 0 and not length[0] < len(input.replace(" ", "")) < length[1]:
                    self.drawtext(message, x, y + h + 5, self.font_main, (colour[0], colour[1], colour[2], 255))
                else:
                    print("valid")

            if size:
                try:
                    if len(input) > 0 and not size[0] < int(input) < size[1]:
                        self.drawtext(message, x + w, y + h, self.font_main, (colour[0], colour[1], colour[2], 255))
                except ValueError:
                    print("Value error not sure how you achieved this?")









    def drawtext(self, text, x, y, font_ref, color=(255, 255, 255)):
        if not text or not font_ref:
            return
        sdl_color = SDL_Color(color[0], color[1], color[2], 255)
        surface = TTF_RenderText_Blended(font_ref, text.encode("utf-8"), sdl_color)
        if not surface:
            return

        texture = SDL_CreateTextureFromSurface(self.renderer, surface)
        w, h = surface.contents.w, surface.contents.h
        dest_rect = SDL_Rect(x, y, w, h)

        SDL_RenderCopy(self.renderer, texture, None, dest_rect)
        SDL_FreeSurface(surface)
        SDL_DestroyTexture(texture)

    def draw_menu(self):
        self.drawtext("Freddy's Fast Fish", 130, 30, self.font_title)
        for key, btn in self.buttons["menu"].items():
            r = btn["rect"]
            roundedBoxRGBA(self.renderer, r.x, r.y, r.x + r.w, r.y + r.h, 12, 200, 200, 200, 200)
            self.drawtext(btn["text"], r.x + 125, r.y + 10, self.font_main)

    def shop(self):
        column = 1
        counter = 0
        self.drawtext("Menu", 315, 25, self.font_title)
        for counter, items in enumerate(self.logic.fishmenu):
            column = counter % 2
            row = counter // 2
            x = 25 + (column * 400)
            y = 100 + (row * 60)
            self.drawtext(items["name"], x, y, self.font_main)
            self.drawtext(items["price"], x + 300, y, self.font_main)
            outline = SDL_Rect(x- 15, y, 375, 60)
            SDL_SetRenderDrawColor(self.renderer, 0, 0, 0, 0)
            SDL_RenderDrawRect(self.renderer, outline)

    def details(self):
        self.drawtext("Details", 300, 40, self.font_title)
        for key, btn in self.buttons["details"].items():
            r = btn["rect"]
            roundedBoxRGBA(self.renderer, r.x, r.y, r.x + r.w, r.y + r.h, 12, 200, 200, 200, 200)
            self.drawtext(btn["text"], r.x + 170, r.y + 10, self.font_main)

        for key, data in self.inputs.items():
            r = data["rect"]
            self.drawtext(data["label"], r.x, r.y - 25, self.font_main)
            box_color = (0, 255, 255) if self.activefield == key else (200, 200, 200)
            roundedBoxRGBA(self.renderer, r.x, r.y, r.x + r.w, r.y + r.h, 5, *box_color, 255)
            self.drawtext(data["text"], r.x + 5, r.y + 5, self.font_main)

        if self.activefield == "name":
            if len(self.inputs["name"]["text"]) > 0 and not self.inputs["name"]["text"].replace(" ", "").isalpha():
                r = self.inputs["name"]["rect"]
                self.drawtext(self.inputs["name"]["warning"], r.x + 30, r.y + 40, self.font_main)
                print("warning drawn")

            else:
                print("not drawn")

    def rungui(self):
        event = SDL_Event()
        while self.running:
            while SDL_PollEvent(ctypes.byref(event)) != 0:
                if event.type == SDL_QUIT:
                    self.running = False

                if event.type == SDL_MOUSEBUTTONDOWN:
                    point = SDL_Point(event.button.x, event.button.y)

                    if self.state == 0:
                        if SDL_PointInRect(
                            point, self.buttons["menu"]["delivery"]["rect"]):
                            self.logic.order["type"] = "delivery"
                            self.logic.order["fee"] = 5.0
                            self.state = 2
                        elif SDL_PointInRect(
                            point, self.buttons["menu"]["pickup"]["rect"]):
                            self.logic.order["type"] = "pickup"
                            self.state = 2

                    elif self.state == 2:
                        box_selected = False
                        for key, data in self.inputs.items():
                            if SDL_PointInRect(point, data["rect"]):
                                self.activefield = key
                                SDL_StartTextInput()
                                box_selected = True
                                break

                        if SDL_PointInRect(
                            point, self.buttons["details"]["next"]["rect"]):
                            self.state = 1

                        if not box_selected:
                            self.activefield = None
                            SDL_StopTextInput()


                if event.type == SDL_TEXTINPUT and self.activefield:
                    char = event.text.text.decode("utf-8")
                    self.inputs[self.activefield]["text"] += char


                if event.type == SDL_KEYDOWN and self.activefield:
                    if event.key.keysym.sym == SDLK_BACKSPACE:
                        self.inputs[self.activefield]["text"] = self.inputs[self.activefield]["text"][:-1]

            SDL_SetRenderDrawColor(self.renderer, 30, 30, 40, 255)
            SDL_RenderClear(self.renderer)

            if self.state == 0:
                self.draw_menu()
            elif self.state == 1:
                self.shop()
            elif self.state == 2:
                self.details()

            SDL_RenderPresent(self.renderer)

        SDL_Quit()


if __name__ == "__main__":
    system = OrderSystem()
    app = AppWindow(system)
    app.rungui()
