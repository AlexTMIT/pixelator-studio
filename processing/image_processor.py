import math
from typing import Callable
from PIL import Image
import numpy as np
import colorsys
from model.pixel_modes import ColorScheme, PixelationMode

class ImageProcessor:
    def map_amount_to_pixel_size(self, amount: int, max_dim: int = 400) -> int:
        norm = amount / 100
        num_blocks = int(1 + (400 - 1) * (1 - norm) ** 2)
        return max(1, max_dim // num_blocks)

    def process_blocks(
        self, arr: np.ndarray, ps: int,
        init_fn: Callable[[np.ndarray], np.ndarray],
        select_fn: Callable[[np.ndarray, np.ndarray], np.ndarray]
    ) -> Image.Image:
        h, w, _ = arr.shape
        by = math.ceil(h/ps); bx = math.ceil(w/ps)
        pad_h = by*ps - h; pad_w = bx*ps - w
        a = np.pad(arr, ((0,pad_h),(0,pad_w),(0,0)), mode='edge')
        blocks = a.reshape(by, ps, bx, ps, 3).transpose(0,2,1,3,4)
        flat = blocks.reshape(by, bx, ps*ps, 3)
        proc = init_fn(flat)
        means = proc.mean(axis=2, keepdims=True)
        rep = np.zeros((by, bx, 3), dtype=np.float32)
        for i in range(by):
            for j in range(bx):
                rep[i,j] = select_fn(proc[i,j], means[i,j,0])
        expanded = rep.repeat(ps, axis=0).repeat(ps, axis=1)
        out = np.clip(expanded[:h, :w], 0, 255).astype(np.uint8)
        return Image.fromarray(out)

    def pixelate(self, mode: PixelationMode, amount: int, image: Image.Image, color_scheme: ColorScheme) -> Image.Image:
        amount = int((amount+42)*0.70) # ugly offset fix
        
        if mode == PixelationMode.PYTHAGOREAN_COLOR_AVERAGE:
            img = self.pythagorean_color_average(amount, image)
        elif mode == PixelationMode.MEDIAN_COLOR:
            img = self.median_color_average(amount, image)
        else:
            img = self.schematic_approximation(amount, image, color_scheme)
        return img

    def pythagorean_color_average(self, amount: int, image: Image.Image) -> Image.Image:
        arr = np.asarray(image, np.float32)
        ps = self.map_amount_to_pixel_size(amount, max(*arr.shape[:2]))
        if ps <= 1: return image
        return self.process_blocks(
            arr, ps,
            init_fn=lambda blk: blk**2,
            select_fn=lambda blk, m: np.sqrt(m)
        )

    def median_color_average(self, amount: int, image: Image.Image) -> Image.Image:
        arr = np.asarray(image, np.float32)
        ps = self.map_amount_to_pixel_size(amount, max(*arr.shape[:2]))
        if ps <= 1: return image
        def pick_median(blk, m):
            d = ((blk - m)**2).sum(axis=1)
            return blk[d.argmin()]
        return self.process_blocks(arr, ps, init_fn=lambda blk: blk, select_fn=pick_median)

    def schematic_approximation(self, amount: int, image: Image.Image, color_scheme: ColorScheme) -> Image.Image:
        arr = np.asarray(image, np.float32)
        ps = self.map_amount_to_pixel_size(amount, max(*arr.shape[:2]))
        if ps <= 1: return image
        palette = color_scheme.palette()
        def pick_palette(blk, m):
            d = ((palette - m)**2).sum(axis=1)
            return palette[d.argmin()]
        return self.process_blocks(arr, ps, init_fn=lambda blk: blk, select_fn=pick_palette)

    def edit_brightness(self, image: Image.Image, raw: int) -> Image.Image:
        factor = raw/50 if raw<50 else 1+4*((raw-50)/50)**2
        arr = np.clip(np.array(image, np.float32)*factor, 0,255).astype(np.uint8)
        return Image.fromarray(arr)

    def edit_saturation(self, image: Image.Image, raw: int) -> Image.Image:
        arr = np.array(image, np.float32)/255.0
        hls = np.vectorize(colorsys.rgb_to_hls)(arr[...,0], arr[...,1], arr[...,2])
        h,l,s = hls
        s = np.clip(s*(raw/50 if raw<50 else 1+4*((raw-50)/50)**2), 0,1)
        rgb = np.vectorize(colorsys.hls_to_rgb)(h,l,s)
        out = np.clip(np.stack(rgb,axis=-1)*255,0,255).astype(np.uint8)
        return Image.fromarray(out)

    def edit_contrast(self, image: Image.Image, raw: int) -> Image.Image:
        factor = raw/50 if raw<50 else 1+4*((raw-50)/50)**2
        arr = np.clip(128 + (np.array(image, np.float32)-128)*factor,0,255).astype(np.uint8)
        return Image.fromarray(arr)

    def process_image(self, img, b_amt, s_amt, c_amt, p_amt, pm, scheme):
        img = self.edit_brightness(img, b_amt)
        img = self.edit_saturation(img, s_amt)
        img = self.edit_contrast(img, c_amt)
        img = self.pixelate(pm, p_amt, img, scheme)
        return img