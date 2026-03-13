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
    price: float
    catagory: str = "normal"
    
    
@dataclass
class Ui:
    state: str
    buttons: List[Element] = field(default_factory=list)
    text: List[Element] = field(default_factory=list)
