from dataclasses import dataclass, field
from typing import List, Optional, Callable, Tuple, Any
from sdl2 import SDL_Rect
import ctypes

@dataclass
class Element:
    id: str
    text: str
    rect: SDL_Rect
    font_size: int = 24
    texture: ctypes.c_void_p = None
    dirty: bool = True
    
    on_click: Optional[Callable] = None
    on_hover: Optional[Callable] = None
    bg_color: Optional[Tuple[int, int, int]] = (255, 255, 255)
    txt_color: Optional[Tuple[int, int, int]] = (0, 0, 0)
    
    
    
    
    

@dataclass
class Fish:
    fish: str
    price: float = 4.10
    catagory: str = "normal"
    
    
@dataclass
class Ui:
    state: str
    buttons: List[Element] = field(default_factory=list)
    text: List[Element] = field(default_factory=list)



fishmenu = [
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
    Element("pickup_btn", "Pickup", SDL_Rect(425, 500, 350, 50), 24, None, True, on_click=lambda app: setattr(app.ui, "state", "Pickup")),
    Element("delivery_btn", "Delivery", SDL_Rect(25, 500, 350, 50), 24, None, True, on_click=lambda app: setattr(app.ui, "state", "Delivery"))
    Element("header", "Freddy's Fish Shop", SDL_Rect(130, 30, 0, 0), 60, None, True, txt_colour=(255, 255, 255)),
    
    
    
    
    
]
    
    

    
    

