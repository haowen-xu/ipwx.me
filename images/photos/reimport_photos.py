#!/usr/bin/env python

import os
import re
import shutil

ORIGINAL_DIR = '/Users/ipwx/Library/Mobile Documents/com~apple~CloudDocs/照片'
IMAGE_EXTENSIONS = ('.jpg', '.jpeg')


def scan_dir(root_dir, db):
    for name in os.listdir(root_dir):
        path = os.path.join(root_dir, name)
        base, ext = os.path.splitext(name)
        if os.path.isdir(path):
            scan_dir(path, db)
        elif ext.lower() in IMAGE_EXTENSIONS:
            m = re.match(r'(DSC\d+)[.-]?', base)
            if m:
                key = base
                db[key] = path

    return db


def main():
    origin_db = scan_dir(ORIGINAL_DIR, {})
    current_db = scan_dir('.', {})
    for key in current_db:
        if key not in origin_db:
            print(f'Source not found: {current_db[key]}')
        else:
            if os.stat(origin_db[key]).st_size != os.stat(current_db[key]).st_size:
                print(f'Import: {origin_db[key]} -> {current_db[key]}')
                shutil.copy(origin_db[key], current_db[key])


if __name__ == '__main__':
    main()

