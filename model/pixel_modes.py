from enum import Enum, auto
import numpy as np

class PixelationMode(Enum):
    SCHEMATIC_APPROXIMATION = auto()
    PYTHAGOREAN_COLOR_AVERAGE = auto()
    MEDIAN_COLOR = auto()
    #DOMINANT_COLOR = auto()

class ColorScheme(Enum):
    WARM_BEIGE = "warm_beige"
    COOL_PASTEL = "cool_pastel"

    def palette(self) -> np.ndarray:
        schemes = {
            ColorScheme.WARM_BEIGE: [
                (245, 233, 207),
                (216, 195, 165),
                (189, 161, 139),
                (131, 105,  83),
                (224, 214, 195),
            ],
            ColorScheme.COOL_PASTEL: [
                (200, 225, 255),
                (180, 210, 230),
                (160, 195, 205),
            ],
        }
        return np.array(schemes[self], dtype=np.float32)
    
    @classmethod
    def names(cls) -> list[str]:
        return [member.value.lower().replace("_", " ") for member in cls]