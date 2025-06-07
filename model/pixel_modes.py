from enum import Enum, auto
import numpy as np

class PixelationMode(Enum):
    SCHEMATIC_APPROXIMATION = auto()
    PYTHAGOREAN_COLOR_AVERAGE = auto()
    MEDIAN_COLOR = auto()

class ColorScheme(Enum):
    WARM_BEIGE   = "warm beige"
    COOL_GRAY    = "cool gray"
    VIBRANT_SUNSET = "vibrant sunset"
    PASTEL_MINT  = "pastel mint"
    HOT_N_COLD   = "hot n cold"
    ICE_CREAM     = "ice cream"
    WARM_CLAY = "warm clay"
    FROSTED_LAVENDER = "frost lavender"
    DEEP_OCEAN = "deep ocean"
    SAGE_FOREST = "sage forest"
    INFRARED = "infrared"

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
                (240, 240, 240),
                (200, 200, 200),
                (160, 160, 160),
                (120, 120, 120),
                (80, 80, 80),
            ],
            ColorScheme.VIBRANT_SUNSET: [
                (255, 94, 77),
                (255, 149, 128),
                (255, 205, 178),
                (255, 188, 160),
                (255, 223, 200),
            ],
            ColorScheme.HOT_N_COLD: [
                (227, 23, 10),
                (225, 96, 54),
                (214, 169, 154),
                (214, 203, 193),
                (205, 214, 208),
            ],
            ColorScheme.ICE_CREAM: [
                (255, 166, 158),
                (255, 126, 107),
                (140, 94, 88),
                (169, 240, 209),
                (255, 247, 248),
            ],
            ColorScheme.WARM_CLAY: [
                (237, 201, 175),
                (210, 161, 131),
                (176, 122, 99),
                (139, 91, 70),
                (104, 67, 49),
            ],
            ColorScheme.FROSTED_LAVENDER: [
                (242, 235, 255),
                (215, 200, 255),
                (180, 160, 225),
                (140, 120, 190),
                (100, 85, 150),
            ],
            ColorScheme.DEEP_OCEAN: [
                (20, 40, 80),
                (30, 60, 120),
                (40, 90, 150),
                (60, 120, 170),
                (90, 150, 190),
            ],
            ColorScheme.SAGE_FOREST: [
                (220, 235, 220),
                (180, 210, 180),
                (140, 180, 140),
                (100, 150, 100),
                (60, 100, 60),
            ],
            ColorScheme.INFRARED: [
                (255, 228, 225),
                (255, 200, 195),
                (255, 170, 165),
                (240, 130, 130),
                (220, 90, 100),
            ]
        }
        return np.array(schemes[self], dtype=np.float32)