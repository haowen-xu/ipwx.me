#!/usr/bin/env python

import os

from PIL import Image

IMAGE_EXTENSIONS = ('.jpg', '.jpeg')
SIZE_LIMIT = 3000
SIZE_PREFERENCES = {
    (6000, 4000): (3000, 2000),
}


def scale_image(path):
    name = os.path.split(path)[-1]
    im = Image.open(path)
    out = None
    try:
        h, w = None, None
        old_h, old_w = im.size
        # if (h, w) or (w, h) in SIZE_PREFERENCES, then use the preferenced new size
        if (old_h, old_w) in SIZE_PREFERENCES:
            h, w = SIZE_PREFERENCES[(old_h, old_w)]
        elif (old_w, old_h) in SIZE_PREFERENCES:
            w, h = SIZE_PREFERENCES[(old_w, old_h)]
        else:
            # otherwise determine the new size according to limit
            ratio = max(old_h / SIZE_LIMIT, old_w / SIZE_LIMIT, 1.)
            if ratio > 1. + 1e-3:
                h, w = int(round(old_h / ratio)), int(round(old_w / ratio))

        # scale the image if required
        if h is not None:
            print(f'{name}: {old_w}x{old_h} -> {w}x{h}')
            out = im.resize((h, w), resample=Image.ANTIALIAS)
    finally:
        im.close()
        if out is not None:
            try:
                out.save(path, quality=90, optimize=True, progressive=True)
            finally:
                out.close()


def process_dir(root_dir):
    for name in os.listdir(root_dir):
        path = os.path.join(root_dir, name)
        base, ext = os.path.splitext(name)
        if os.path.isdir(path):
            process_dir(path)
        elif ext.lower() in IMAGE_EXTENSIONS:
            scale_image(path)
        

def main():
    process_dir('.')


if __name__ == '__main__':
    main()
