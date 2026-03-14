import ctypes
import os
import sys
import sdl2.ext  


from sdl2 import *  
from sdl2.sdlgfx import *  
from sdl2.sdlttf import *  
from dataclasses import dataclass
from data import Element, Fish, ELEMENTS, FISHMENU




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
        for _, element in self.app.el.items():
            if element.font_size:
                element.font = TTF_OpenFont(font_path, element.font_size)
                if not element.font: print(f"Font Error: {SDL_GetError()}")
        
        






    def texturing(self, ostate, nstate):
        
        
        for item in self.app.get_state_elements(ostate):
            if item.texture != None: SDL_DestroyTexture(item.texture)
            item.texture = None
            item.dirty = True
            
        
            
        for item in self.app.get_state_elements(nstate):
            if item.dirty:
                sdl_color = SDL_Color(item.txt_colour[0], item.txt_colour[1], item.txt_colour[2], 255)
                surface = TTF_RenderText_Blended(item.font, item.text.encode("utf-8"), sdl_color)
                if surface:
                    texture = SDL_CreateTextureFromSurface(self.app.ui.renderer, surface)
                    item.texture = texture
                    item.rect.w, item.rect.h = surface.contents.w, surface.contents.h
                    SDL_FreeSurface(surface)
                item.dirty = False
                
                
    def element_texturing(self, element):
        if element.dirty:
            if element.texture != None: SDl_DestroyTexture(element.texture)
            element.texture = None
            sdl_color = SDL_Color(element.txt_colour[0], element.txt_colour[1], element.txt_colour[2], 255)
            surface = TTF_RenderText_Blended(element.font, element.text.encode("utf-8"), sdl_color)
            if surface:
                texture = SDL_CreateTextureFromSurface(self.app.ui.renderer, surface)
                element.texture = texture
                element.rect.w, element.rect.h = surface.contents.w, surface.contents.h
                SDL_FreeSurface(surface)
                return element.dirty == False
            else: return element.dirty == True
            
            




    def valiator(self): print("valid")
    
    
    
    
    def texture_destroy(self): print("hello")
    
    
    
    
    

class RenderUi:
    def __init__(self, app):
        self.app = app
        SDL_Init(SDL_INIT_VIDEO)
        W_HEIGHT = 600
        W_WIDTH = 800
        self.window = SDL_CreateWindow(b"Freddy's Fast Fish", SDL_WINDOWPOS_CENTERED, SDL_WINDOWPOS_CENTERED, W_WIDTH, W_HEIGHT, SDL_WINDOW_SHOWN)
        self.renderer = SDL_CreateRenderer(self.window, -1, SDL_RENDERER_ACCELERATED)
        self.running = True
        self._state = "home"
        
        
        

        
        
        
        

    @property
    def state(self): return self._state
    
    
    
    

    @state.setter
    def state(self, new_state):
        if self._state != new_state:
            self.app.utils.texturing(self._state, new_state)
            self._state = new_state
            
            
            
            
            

    def elementrender(self): 
        for render in self.app.get_state_elements(self.state):
            if not render.dirty and render.texture != None:
                roundedBoxRGBA(self.app.ui.renderer, render.rect.x, render.rect.y, render.rect.x + render.rect.w, render.rect.y + render.rect.h, 12, 255, 0, 0, 255)
                SDL_RenderCopy(self.app.ui.renderer, render.texture, None, render.rect)
                
            elif render.dirty:
                self.app.utils.element_texturing(render)
                render.dirty = False
                if render.texture: 
                    SDL_RenderCopy(self.app.ui.renderer, render.texture, None, render.rect)

                
                
                
                   

    def rungui(self): 
        self.app.events.events()
        self.app.utils.texturing("home", "home")
        
        
        
        
        
        
        
        
        
    
    
    
    
    

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
                    for key, button in self.app.el.items():
                        if SDL_PointInRect(point, button.rect) and button.on_click != None and button.state == self.app.ui.state:
                            print(button.id)
                            if button.txt_field:
                                print(button.id)
                                
                                SDL_StartTextInput()
                            else:
                                button.on_click(self.app)
                            
                            
                            
                            

                            
                            

            SDL_SetRenderDrawColor(self.app.ui.renderer, 30, 30, 40, 255)
            SDL_RenderClear(self.app.ui.renderer)
            self.app.ui.elementrender()
            SDL_RenderPresent(self.app.ui.renderer)
            
            
            
            
        SDL_Quit()
        
        
        
        
        


class App:
    def __init__(self):
        self.ele = ELEMENTS
        self.el = {e.id: e for e in self.ele}
        self.utils = Utilities(self)
        self.logic = Logic(self)
        self.ordersystem = OrderSystem(self)
        self.ui = RenderUi(self)
        self.events = Events(self)
        self.elitem = self.el.items()
        
    def get_state_elements(self, state):
        return [el for el in self.el.values() if el.state == state]
                    
        
        
        
        
        
        
        
        
        
        

if __name__ == "__main__":
    my_app = App()
    my_app.ui.rungui()
