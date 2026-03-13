import ctypes
import os
import sys
import sdl2.ext  


from sdl2 import *  
from sdl2.sdlgfx import *  
from sdl2.sdlttf import *  
from dataclasses import dataclass
from data.py import Element, Fish, Ui



class OrderSystem:
    def __init__(self, app):
        self.app = app
        self.fishmenu = [
            Fish("Shark", 4.10),
            Fish("Flounder", 4.10),
            Fish("Cod", 4.10),
            Fish("Gurnet", 4.10),
            Fish("Hoki", 4.10),
            Fish("Tarakihi", 4.10),
            Fish("Snapper", 7.20, "Deluxe"),
            Fish("Pink Salmon", 7.20, "Deluxe"),
            Fish("Tuna", 7.20, "Deluxe"),
            Fish("Smoked Marlin", 7.20, "Deluxe"),
            Fish("John Dory", 7.20, "Deluxe"),
            Fish("Swordfish", 7.20, "Deluxe"),
        ]










class Logic:
    def __init__(self, app):
        self.app = app




















class Utilities:
    def __init__(self, app):
        self.app = app
        self.font()





    def font(self):
        if TTF_Init() == -1: print(f"TTF Init Error: {TTF_GetError()}")
        script_dir = os.path.dirname(os.path.abspath(__file__))
        font_path = os.path.join(script_dir, "sdlfont.ttf").encode("utf-8")
        self.font_main = TTF_OpenFont(font_path, 24)
        self.font_title = TTF_OpenFont(font_path, 60)
        if not self.font_main or not self.font_title: print(f"Font Error: {SDL_GetError()}")






    def texturing(self, tomake, color=(255, 255, 255)):
        for key, item in tomake.items():
            if item.get("dirty"):
                sdl_color = SDL_Color(color[0], color[1], color[2], 255)
                surface = TTF_RenderText_Blended(item["font"], item["text"].encode("utf-8"), sdl_color)
                if surface:
                    texture = SDL_CreateTextureFromSurface(self.app.ui.renderer, surface)
                    item["texture"] = texture
                    item["width"], item["height"] = surface.contents.w, surface.contents.h
                    SDL_FreeSurface(surface)
                item["dirty"] = False




    def valiator(self): print("valid")
    
    
    
    
    def texture_destroy(self): print("hello")
    
    
    
    
    

class RenderUi:
    def __init__(self, app):
        self.app = app
        SDL_Init(SDL_INIT_VIDEO)
        self.window = SDL_CreateWindow(b"Freddy's Fast Fish", SDL_WINDOWPOS_CENTERED, SDL_WINDOWPOS_CENTERED, 800, 600, SDL_WINDOW_SHOWN)
        self.renderer = SDL_CreateRenderer(self.window, -1, SDL_RENDERER_ACCELERATED)
        self.running = True
        self._state = "main"
        
        
        
        self.ui = {
            "main": {
                "text": {
                    "header": {"text": "Freddy's Fish Shop", "font": self.app.utils.font_main, "dirty": True, "texture": None, "rect": SDL_Rect(130, 30, 0, 0)}
                }
                "buttons": {
                    "pickup": {"text": "Pickup", "font": self.app.utils.font_main, "texture": None, "rect": SDL_Rect(425, 500, 350, 50)"state": ("details", "pickup")}
                    "delivery": {"text": "Delivery", "font": self.app.utils.font_main, "texture": None, "rect": SDL_Rect(25, 500, 350, 50)"state": ("details", "delivery")}
                }
            },
            "details": {
                "pickup": {
                    "state": "pickup",
                    "text": {
                        
                    },
                    "buttons": {
                        
                    }
                }
                    
                "delivery": {
                    "text": {
                        
                    },
                    "buttons": {
                        
                    }
                },
                
            }, 
            "shop": {},
            "checkout": {},
        }
        
        
        
        

    @property
    def state(self): return self._state
    
    
    
    

    @state.setter
    def state(self, new_state):
        if self._state != new_state:
            self._state = new_state
            self.app.utils.texturing(self.ui[self._state].get("text", {}))
            
            
            
            

    def elementrender(self): print("elementrender")
    def rungui(self): self.app.events.events()
    
    
    
    
    

class Events:
    def __init__(self, app):
        self.app = app
        
        
        
        
        
        

    def events(self):
        event = SDL_Event()
        while self.app.ui.running:
            while SDL_PollEvent(ctypes.byref(event)) != 0:
                if event.type == SDL_QUIT: 
                    self.app.ui.running = False
                    
                if event.type == SDL_MOUSEBUTTONDOWN:
                    point = SDL_Point(event.button.x, event.button.y)
                    for items, key in self.app.ui.ui[self.app.ui._state]["buttons"].items():
                        if SDL_PointInRect(point, key["rect"]):
                            self.app.ui.state = items["state"][0]
                            self.truestate = items["state"][1]

                            
                            

            SDL_SetRenderDrawColor(self.app.ui.renderer, 30, 30, 40, 255)
            SDL_RenderClear(self.app.ui.renderer)
            SDL_RenderPresent(self.app.ui.renderer)
            
            
            
            
        SDL_Quit()
        
        
        
        
        


class App:
    def __init__(self):
        self.utils = Utilities(self)
        self.logic = Logic(self)
        self.ordersystem = OrderSystem(self)
        self.ui = RenderUi(self)
        self.events = Events(self)
        
        
        
        
        

if __name__ == "__main__":
    my_app = App()
    my_app.ui.rungui()
