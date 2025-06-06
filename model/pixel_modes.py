from enum import Enum, auto

class PixelationMode(Enum):
    SCHEMATIC_APPROXIMATION = auto()
    PYTHAGOREAN_COLOR_AVERAGE = auto()
    SIMPLE_AVERAGE = auto()
    MEDIAN_COLOR = auto()
    DOMINANT_COLOR = auto()