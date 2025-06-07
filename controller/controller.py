import math
from typing import Callable
from PySide6.QtWidgets import QFileDialog
from PIL import Image
import colorsys
import numpy as np

from model.pixel_modes import PixelationMode

class AppController:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.load_image("assets/default.png")
        self._connect_signals()

    def _connect_signals(self):
        # Sliders
        sliders = self.view.sliders
        sliders.pixelAmountChanged.connect(lambda val: self._slider_changed("pixel_amount", val))
        sliders.brightnessChanged.connect(lambda val: self._slider_changed("brightness", val))
        sliders.saturationChanged.connect(lambda val: self._slider_changed("saturation", val))
        sliders.contrastChanged.connect(lambda val: self._slider_changed("contrast", val))

        # File‐open / save
        self.view.options.open_button.clicked.connect(self.open_image)
        self.view.options.save_as_button.clicked.connect(self.save_image)

        # Color mode and scheme
        self.view.colors.combo_mode.currentIndexChanged.connect(self._on_mode_changed)
        self.view.colors.combo_scheme.currentIndexChanged.connect(self._on_scheme_changed)

    def _on_slider(self, name: str, val: int):
        self.model.update_slider(name, val)
        self.render_image()

    def _on_mode_changed(self, idx: int):
        mode = self.view.colors.combo_mode.itemData(idx)
        # now mode is never None
        self.model.pixel_mode = mode
        self.view.colors.combo_scheme.setEnabled(mode == PixelationMode.SCHEMATIC_APPROXIMATION)
        self.render_image()

    def _on_scheme_changed(self, idx: int):
        if self.view.colors.combo_scheme.isEnabled():
            scheme = self.view.colors.combo_scheme.itemData(idx)
            self.model.color_scheme = scheme
            self.render_image()

    def reset_parameters(self):
        self.model.pixel_amount = 0
        self.model.brightness = 50
        self.model.saturation = 50
        self.model.contrast = 50

        sliders = self.view.sliders
        sliders.pixelAmountSlider.setValue(0)
        sliders.brightnessSlider.setValue(50)
        sliders.saturationSlider.setValue(50)
        sliders.contrastSlider.setValue(50)

    def open_image(self):
        path, _ = QFileDialog.getOpenFileName(
            self.view, "Open Image", "", "Image Files (*.png *.jpg *.jpeg *.bmp)"
        )
        if not path:
            return
        self.load_image(path)

    def load_image(self, path):
        image = Image.open(path).convert("RGB")
        resized = self.resize_to_fit(image, 400, 400)
        self.reset_parameters()
        self.view.options.save_as_button.setEnabled(True)
        self.model.load_image(resized)
        self.view.preview.set_image(resized)

    def save_image(self):
        image = self.model.image_edited
        if image is None:
            return

        path, _ = QFileDialog.getSaveFileName(
            self.view, "Save Image As", "", "JPEG (*.jpg);;PNG (*.png);;All Files (*)"
        )
        if not path:
            return

        ext = path.split('.')[-1].upper()
        fmt = "JPEG" if ext.lower() == "jpg" else ext
        try:
            image.save(path, fmt)
        except Exception as e:
            print(f"Failed to save image: {e}")

    def resize_to_fit(self, img: Image.Image, max_w=400, max_h=400) -> Image.Image:
        img.thumbnail((max_w, max_h), Image.LANCZOS)
        return img

    def _slider_changed(self, name, value):
        self.model.update_slider(name, value)
        self.render_image()

    def render_image(self):
        img = self.model.image.copy()
        if img is None:
            return

        # Pass in mode + scheme to edit_pixelation
        pixelated = self.edit_pixelation(img)
        bright = self.edit_brightness(pixelated)
        sat = self.edit_saturation(bright)
        contr = self.edit_contrast(sat)

        self.model.image_edited = contr
        self.view.preview.set_image(contr)

    def calculate_factor(self, raw_value):
        if raw_value < 50:
            return raw_value / 50
        else:
            return 1 + 4 * ((raw_value - 50) / 50) ** 2

    def edit_pixelation(self, image: Image.Image) -> Image.Image:
        mode = self.model.pixel_mode
        amount = self.model.pixel_amount or 0

        if amount == 0:
            return image

        match mode:
            case PixelationMode.PYTHAGOREAN_COLOR_AVERAGE:
                return self.pythagorean_color_average(amount, image)
            case PixelationMode.SCHEMATIC_APPROXIMATION:
                return self.schematic_approximation(amount, image)
            case PixelationMode.MEDIAN_COLOR:
                return self.median_color_average(amount, image)
            case _:
                return image

    def map_amount_to_pixel_size(self, amount, max_dim=400):
            min_blocks = 1
            max_blocks = 400
            normalized = amount / 100
            num_blocks = int(min_blocks + (max_blocks - min_blocks) * (1 - normalized) ** 2)
            return max(1, max_dim // num_blocks)

    def process_blocks(self, arr: np.ndarray, ps: int,
                   init_fn: Callable[[np.ndarray], np.ndarray],
                   select_fn: Callable[[np.ndarray, np.ndarray], np.ndarray]
                  ) -> Image.Image:
        """
        arr: H×W×3 float32
        ps: block size
        init_fn: e.g. lambda blk: blk       # identity for mean/median
                or lambda blk: blk**2     # square for RMS
        select_fn: (flattened_pixels, block_mean) -> RGB(3,)
        """
        h, w, _ = arr.shape
        by, bx = math.ceil(h/ps), math.ceil(w/ps)
        pad_h, pad_w = by*ps - h, bx*ps - w

        # edge‐pad
        a = np.pad(arr, ((0,pad_h),(0,pad_w),(0,0)), mode='edge')
        blocks = (a
                .reshape(by, ps, bx, ps, 3)
                .transpose(0,2,1,3,4))      # [by, bx, ps, ps, 3]

        flat = blocks.reshape(by, bx, ps*ps, 3)     # [by, bx, P, 3]
        proc = init_fn(flat)                        # same shape
        means = proc.mean(axis=2, keepdims=True)    # [by, bx, 1, 3]

        # select one RGB per block:
        # vectorize over by,bx:
        rep = np.zeros((by, bx, 3), dtype=np.float32)
        for i in range(by):
            for j in range(bx):
                rep[i,j] = select_fn(proc[i,j], means[i,j,0])

        # expand back to full image:
        expanded = rep.repeat(ps, axis=0).repeat(ps, axis=1)
        out = np.clip(expanded[:h, :w], 0, 255).astype(np.uint8)
        return Image.fromarray(out)

    def pythagorean_color_average(self, amount, image):
        arr = np.asarray(image, np.float32)
        ps = self.map_amount_to_pixel_size(amount, max(*arr.shape[:2]))
        if ps<=1: return image

        # init: square; select: take sqrt(mean)
        return self.process_blocks(
            arr, ps,
            init_fn=lambda blk: blk**2,
            select_fn=lambda blk, m: np.sqrt(m)   # m is already mean of squares
        )

    def median_color_average(self, amount, image):
        arr = np.asarray(image, np.float32)
        ps = self.map_amount_to_pixel_size(amount, max(*arr.shape[:2]))
        if ps<=1: return image

        # init: identity; select: pick real pixel closest to block mean
        def pick_median(blk, m):
            # blk: P×3, m: 3-vector
            d = ((blk - m)**2).sum(axis=1)
            return blk[d.argmin()]
        return self.process_blocks(arr, ps,
                                init_fn=lambda blk: blk,
                                select_fn=pick_median)

    def schematic_approximation(self, amount, image):
        arr = np.asarray(image, np.float32)
        ps = self.map_amount_to_pixel_size(amount, max(*arr.shape[:2]))
        if ps<=1: return image

        palette = self.model.color_scheme.palette()
        # init: identity; select: pick nearest palette color
        def pick_palette(blk, m):
            d = ((palette - m)**2).sum(axis=1)
            return palette[d.argmin()]

        return self.process_blocks(arr, ps,
                                init_fn=lambda blk: blk,
                                select_fn=pick_palette)

    def edit_brightness(self, image: Image.Image) -> Image.Image:
        factor = self.calculate_factor(self.model.brightness)
        arr = np.array(image, dtype=np.float32)
        arr *= factor
        arr = np.clip(arr, 0, 255).astype(np.uint8)
        return Image.fromarray(arr)

    def edit_saturation(self, image: Image.Image) -> Image.Image:
        factor = self.calculate_factor(self.model.saturation)
        arr = np.array(image, dtype=np.float32) / 255.0
        r, g, b = arr[..., 0], arr[..., 1], arr[..., 2]

        hls = np.vectorize(colorsys.rgb_to_hls)(r, g, b)
        h, l, s = hls
        s = np.clip(s * factor, 0, 1)

        rgb = np.vectorize(colorsys.hls_to_rgb)(h, l, s)
        r2, g2, b2 = rgb
        out = np.stack([r2, g2, b2], axis=-1) * 255
        return Image.fromarray(out.astype(np.uint8))

    def edit_contrast(self, image: Image.Image) -> Image.Image:
        factor = self.calculate_factor(self.model.contrast)
        arr = np.array(image, dtype=np.float32)
        arr = 128 + (arr - 128) * factor
        arr = np.clip(arr, 0, 255).astype(np.uint8)
        return Image.fromarray(arr)