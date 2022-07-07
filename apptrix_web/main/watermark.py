from PIL import Image

from apptrix_web.settings import MEDIA_ROOT


def paste_watermark(image_path):
    with Image.open(image_path) as im:
        width, height = im.size

        with Image.open(MEDIA_ROOT + '/watermarks/watermark.jpg') as watermark:
            wm_width, wm_height = watermark.size
            ratio = wm_width / width
            new_size = width, int(wm_height / ratio)

            watermark = watermark.resize(new_size, Image.ANTIALIAS)
            watermark.putalpha(70)

            pos = 0, (height - watermark.height) // 2
            im.paste(watermark, box=pos, mask=watermark)
            im.save(image_path)
