import sys
import os
import ctypes

# Arch Linker Fix
os.environ["PYSDL2_DLL_PATH"] = "/usr/lib"

from sdl2 import * # noqa: F403, F405
from sdl2.sdlgfx import * # noqa: F403, F405
import sdl2.ext  # noqa: F401
from sdl2.sdlttf import * # noqa: F403, F405



class OrderSystem:
    def __init__(self):
        # Configuration and Data
        self.frozen_fee = 1.05
        self.fish_menu = [
            {"name": "Shark", "price": 4.10, "type": "Normal"},
            {"name": "Flounder", "price": 4.10, "type": "Normal"},
            {"name": "Cod", "price": 4.10, "type": "Normal"},
            {"name": "Gurnet", "price": 4.10, "type": "Normal"},
            {"name": "Hoki", "price": 4.10, "type": "Normal"},
            {"name": "Tarakihi", "price": 4.10, "type": "Normal"},
            {"name": "Snapper", "price": 7.20, "type": "Deluxe"},
            {"name": "Pink Salmon", "price": 7.20, "type": "Deluxe"},
            {"name": "Tuna", "price": 7.20, "type": "Deluxe"},
            {"name": "Smoked Marlin", "price": 7.20, "type": "Deluxe"},
            {"name": "John Dory", "price": 7.20, "type": "Deluxe"},
            {"name": "Swordfish", "price": 7.20, "type": "Deluxe"},
        ]

        self.order_configs = {
            "pickup": {"fee": 0},
            "delivery": {"fee": 5},
        }

        self.order = {
            "type": "",
            "fee": 0.0,
            "fish": [],
            "items": [],
            "price": 0.0,
            "name": "",
            "phonenumber": 0,
            "address": "",
        }

    def validateinput(self, prompt, validoptions=None, checktypes=None, exitchar='`', length=(), size=0):
        while True:
            userinput = input(f"{prompt}(Press {exitchar} to exit): ").strip().lower()

            if userinput == exitchar:
                print("Exiting")
                sys.exit()

            if validoptions and userinput not in validoptions:
                print(f"Invalid input. Please enter one of the following: {', '.join(validoptions)}")
                continue

            if checktypes == 'alpha':
                if not userinput.replace(" ", "").isalpha():
                    print("Invalid input. Please enter letters only.")
                    continue
            if checktypes == 'digit':
                if not userinput.isdigit():
                    print("Invalid input. Please use numbers only")
                    continue
            if size:
                try:
                    if not int(userinput) < size:
                        print("Too many options selected")
                        continue
                except ValueError:
                    print("Invalid input. Please enter a number.")
                    continue
            if length:
                if not (length[0] <= len(userinput) <= length[1]):
                    print(f"Input must be between {length[0]} and {length[1]} characters.")
                    continue
            return userinput

    def run_order_logic(self):
        print("Welcome to Freddy's Fast Fish!")
        ordertype = self.validateinput("Would you like to order pickup or delivery", validoptions=('pickup', 'delivery'))
        name = self.validateinput("What is your name", checktypes='alpha')
        phone = self.validateinput("What is your phone number", checktypes='digit', length=(8, 11))

        if ordertype == "delivery":
            address = self.validateinput("What is your address")
            self.order["fee"] += 5
            self.order["address"] = address

        self.order["type"] = ordertype
        self.order["name"] = name
        self.order["phonenumber"] = phone

        for i in range(len(self.fish_menu)):
            print(f"{i + 1}. {self.fish_menu[i]['name']} (${self.fish_menu[i]['price']:.2f})")


class AppWindow:
    def __init__(self, logic_ref):
        self.logic = logic_ref

        SDL_Init(SDL_INIT_VIDEO)
        self.window = SDL_CreateWindow(b"Freddy's Fast Fish", SDL_WINDOWPOS_CENTERED, SDL_WINDOWPOS_CENTERED, 800, 600, SDL_WINDOW_SHOWN)
        self.renderer = SDL_CreateRenderer(self.window, -1, SDL_RENDERER_ACCELERATED)
        self.running = True
        self.state = 0
        if TTF_Init() == -1:
            print(f"TTF Init Error: {TTF_GetError()}")
        self.font_main = TTF_OpenFont(b"font.ttf", 24)
        self.font_title = TTF_OpenFont(b"font.ttf", 60)
        self.font_small = TTF_OpenFont(b"font.ttf", 16)


        self.inputs = {
            "name": {"rect": SDL_Rect(250, 150, 300, 40), "text": "", "label": "Full Name"},
            "phone": {"rect": SDL_Rect(250, 250, 300, 40), "text": "", "label": "Phone Number"},
            "address": {"rect": SDL_Rect(250, 350, 300, 40), "text": "", "label": "Address"}
        }
        self.active_field = None







        self.shark_button = SDL_Rect(50, 100, 200, 50)
        self.pickupbutton = SDL_Rect(425, 500, 350, 50 )
        self.deliverybutton = SDL_Rect(25, 500, 350, 50)
        self.nextbutton = SDL_Rect(250,)


    def drawtext(self, text, x, y, font_ref, color=(255, 255, 255,)):


        if not text:
            return


        sdl_color = SDL_Color(color[0], color[1], color[2], 255)
        surface = TTF_RenderText_Blended(font_ref, text.encode('utf-8'), sdl_color)


        texture = SDL_CreateTextureFromSurface(self.renderer, surface)


        w, h = surface.contents.w, surface.contents.h
        dest_rect = SDL_Rect(x, y, w, h)


        SDL_RenderCopy(self.renderer, texture, None, dest_rect)


        SDL_FreeSurface(surface)
        SDL_DestroyTexture(texture)


    def draw_menu(self):
      self.drawtext("Freddy's Fast Fish", 130, 30, self.font_title)



      roundedBoxRGBA(self.renderer, self.deliverybutton.x, self.deliverybutton.y, self.deliverybutton.x + self.deliverybutton.w, self.deliverybutton.y + self.deliverybutton.h, 12, 255, 0, 0, 255)
      roundedBoxRGBA(self.renderer, self.pickupbutton.x, self.pickupbutton.y, self.pickupbutton.x + self.pickupbutton.w, self.pickupbutton.y + self.pickupbutton.h, 12, 255, 0, 0, 255)
      self.drawtext("Delivery", self.deliverybutton.x + 125, self.deliverybutton.y + 10, self.font_main)
      self.drawtext("Pickup", self.pickupbutton.x + 125, self.pickupbutton.y + 10, self.font_main)


    def draw_shop(self):
      roundedBoxRGBA(self.renderer, self.shark_button.x, self.shark_button.y, self.shark_button.x + self.shark_button.w, self.shark_button.y + self.shark_button.h, 12, 255, 0, 0, 255)




    def details(self):
        self.drawtext("Details", 300, 40, self.font_title)
        roundedBoxRGBA(self.renderer, self.shark_button.x, self.shark_button.y, self.shark_button.x + self.shark_button.w, self.shark_button.y + self.shark_button.h, 12, 255, 0, 0, 255)


        for key, data in self.inputs.items():
            r = data["rect"]
            self.drawtext(data["label"], r.x, r.y - 25, self.font_main)
            color = (0, 255, 255) if self.active_field == key else (200, 200, 200)
            roundedBoxRGBA(self.renderer, r.x, r.y, r.x+r.w, r.y+r.h, 5, *color, 255)
            self.drawtext(data["text"], r.x + 5, r.y + 5, self.font_main)

    def draw_checkout(self):
         print("checkout drew")



    def run_gui(self):
        event = SDL_Event()
        while self.running:
            while SDL_PollEvent(ctypes.byref(event)) != 0:
                if event.type == SDL_QUIT:
                    self.running = False


                if event.type == SDL_MOUSEBUTTONDOWN:
                    mx = event.button.x
                    my = event.button.y
                    point = SDL_Point(mx, my)
                    print(f"Mouse: {mx}, {my} | Button: {self.shark_button.x}, {self.shark_button.y}")

                    if self.state == 0:
                        if SDL_PointInRect(point, self.deliverybutton):
                            self.logic.order["type"] = "delivery"  # Set the type string
                            self.logic.order["fee"] = 5.0
                            self.state = 2
                        if SDL_PointInRect(point, self.pickupbutton):
                            self.logic.order["type"] = "pickup"

                            self.state = 1
                    elif self.state == 1:
                        if SDL_PointInRect(point, self.shark_button):
                            print("shark pushed")
                    elif self.state == 2:
                        boxselect = False
                        for key, data in self.inputs.items():
                            if SDL_PointInRect(point, data["rect"]):
                                self.active_field = key
                                SDL_StartTextInput()
                                boxselect = True
                                print(f"Selected: {key}")
                                break


                        if not boxselect:
                            self.active_field = None
                            SDL_StopTextInput()

                if event.type == SDL_TEXTINPUT and self.active_field:
                    char = event.text.text.decode('utf-8')
                    self.inputs[self.active_field]["text"] += char

                if event.type == SDL_KEYDOWN and self.active_field:
                    if event.key.keysym.sym == SDLK_BACKSPACE:
                        self.inputs[self.active_field]["text"] = self.inputs[self.active_field]["text"][:-1]



            SDL_SetRenderDrawColor(self.renderer, 30, 30, 40, 255)
            SDL_RenderClear(self.renderer)

            if self.state == 0:
                self.draw_menu()

            elif self.state == 1:
                self.draw_shop()

            elif self.state == 2:
                self.details()
            elif self.state == 3:
                self.draw_checkout()

            SDL_RenderPresent(self.renderer)


        SDL_DestroyRenderer(self.renderer)
        SDL_DestroyWindow(self.window)
        SDL_Quit()

if __name__ == "__main__":
    system = OrderSystem()


    app = AppWindow(system)
    app.run_gui()
