from enum import Enum, auto
import numpy as np

class PixelationMode(Enum):
    SCHEMATIC_APPROXIMATION = auto()
    PYTHAGOREAN_COLOR_AVERAGE = auto()
    MEDIAN_COLOR = auto()
    #DOMINANT_COLOR = auto()

class ColorScheme(Enum):
    WARM_BEIGE   = "warm beige"
    COOL_GRAY    = "cool gray"
    VIBRANT_SUNSET = "vibrant sunset"
    PASTEL_MINT  = "pastel mint"

    @classmethod
    def names(cls) -> list[str]:
        return [member.value for member in cls]

    @classmethod
    def first(cls) -> "ColorScheme":
        return next(iter(cls))

    def palette(self) -> np.ndarray:
        schemes = {
            ColorScheme.WARM_BEIGE: [
                (245, 233, 207),
                (216, 195, 165),
                (189, 161, 139),
                (131, 105,  83),
                (224, 214, 195),
            ],
            ColorScheme.COOL_GRAY: [
                (200, 200, 200),
                (160, 160, 160),
                (120, 120, 120),
            ],
            ColorScheme.VIBRANT_SUNSET: [
                (255, 94, 77),
                (255, 149, 128),
                (255, 205, 178),
            ],
            ColorScheme.PASTEL_MINT: [
                (189, 252, 201),
                (152, 232, 197),
                (109, 230, 181),
            ],
        }
        return np.array(schemes[self], dtype=np.float32)