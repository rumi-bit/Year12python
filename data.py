from dataclasses import dataclass, field
from typing import List, Optional, Callable, Tuple, Any
from sdl2 import SDL_Rect
from main3 import RenderUi
import ctypes

@dataclass
class Element:
    state: str
    id: str
    text: str
    rect: SDL_Rect
    font_size: int = 24
    texture: ctypes.c_void_p = None
    dirty: bool = True
    
    on_click: Optional[Callable] = None
    font: Optional[ctypes.c_void_p] = None
    txt_colour: Optional[Tuple[int, int, int]] = (0, 0, 0)
    txt_field: Optional[bool] = False
    bg_colour: Optional[Tuple[int, int, int]] = (255, 255, 255)

    
    
    
    
    
    

@dataclass
class Fish:
    fish: str
    price: float = 4.10
    catagory: str = "normal"
    
    




FISHMENU = [
    Fish("Shark"),
    Fish("Flounder"),
    Fish("Cod"),
    Fish("Gurnet"),
    Fish("Hoki"),
    Fish("Tarakihi"),
    Fish("Snapper", 7.20, "Deluxe"),
    Fish("Pink Salmon", 7.20, "Deluxe"),
    Fish("Tuna", 7.20, "Deluxe"),
    Fish("Smoked Marlin", 7.20, "Deluxe"),
    Fish("John Dory", 7.20, "Deluxe"),
    Fish("Swordfish", 7.20, "Deluxe"),
]


ELEMENTS = [
    Element("home","pickup_btn", "Pickup", SDL_Rect(500, 500, 300, 50), 24, None, dirty = True, on_click=lambda app: setattr(app.ui, "state", "details") , font = None),
    Element("home","delivery_btn", "Delivery", SDL_Rect(100, 500, 300, 50), 24, None, dirty = True, on_click=lambda app: setattr(app.ui, "state", "details") , font = None),
    Element("home","header", "Freddy's Fish Shop", SDL_Rect(130, 30, 0, 0), 60, None, dirty = True,on_click=None ,font = None, txt_colour=(255, 255, 255)),
    Element("details", "details", "Details", SDL_Rect(300, 40, 0, 0), 24, None, dirty = True, on_click=None, font = None),
    Element("details", "name", "Full Name", SDL_Rect(250, 150, 300, 40), 24, None, dirty = True, on_click=lambda app: setattr(app.events, "active_field", "name"), font = None, txt_field=True),
    

    
    
  
    
]
    
print(W_HEIGHT, W_WIDTH)

    
    

