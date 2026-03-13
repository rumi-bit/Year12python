import sys
import os
import ctypes

# Arch Linker Fix
os.environ["PYSDL2_DLL_PATH"] = "/usr/lib"

from sdl2 import * # noqa: F403, F405
from sdl2.sdlgfx import * # noqa: F403, F405
import sdl2.ext  # noqa: F401



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
logic_ref = OrderSystem

class AppWindow:
    def __init__(self, logic_ref):
        self.logic = logic_ref

        SDL_Init(SDL_INIT_VIDEO)
        self.window = SDL_CreateWindow(b"Freddy's Fast Fish", SDL_WINDOWPOS_CENTERED, SDL_WINDOWPOS_CENTERED, 800, 600, SDL_WINDOW_SHOWN)
        self.renderer = SDL_CreateRenderer(self.window, -1, SDL_RENDERER_ACCELERATED)
        self.running = True
        self.state = 0



        self.shark_button = SDL_Rect(50, 100, 200, 50)
        self.pickupbutton = SDL_Rect(425, 500, 350, 50 )
        self.deliverybutton = SDL_Rect(25, 500, 350, 50)

    def draw_menu(self):
      roundedBoxRGBA(self.renderer, self.deliverybutton.x, self.deliverybutton.y, self.deliverybutton.x + self.deliverybutton.w, self.deliverybutton.y + self.deliverybutton.h, 12, 255, 0, 0, 255)
      roundedBoxRGBA(self.renderer, self.pickupbutton.x, self.pickupbutton.y, self.pickupbutton.x + self.pickupbutton.w, self.pickupbutton.y + self.pickupbutton.h, 12, 255, 0, 0, 255)


    def draw_shop(self):
      roundedBoxRGBA(self.renderer, self.shark_button.x, self.shark_button.y, self.shark_button.x + self.shark_button.w, self.shark_button.y + self.shark_button.h, 12, 255, 0, 0, 255)



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


                            self.state = 1
                        if SDL_PointInRect(point, self.pickupbutton):
                            print("pickup pushed")
                    elif self.state == 1:
                        if SDL_PointInRect(point, self.shark_button):
                            print("shark pushed")
                    elif self.state == 2:
                        if SDL_PointInRect(point, self.deliverybutton):
                            print("delivery pushed")



            SDL_SetRenderDrawColor(self.renderer, 30, 30, 40, 255)
            SDL_RenderClear(self.renderer)

            if self.state == 0:
                self.draw_menu()

            elif self.state == 1:
                self.draw_shop()

            elif self.state == 2:
                self.draw_checkout()


            SDL_RenderPresent(self.renderer)


        SDL_DestroyRenderer(self.renderer)
        SDL_DestroyWindow(self.window)
        SDL_Quit()

if __name__ == "__main__":
    system = OrderSystem()


    app = AppWindow(system)
    app.run_gui()
