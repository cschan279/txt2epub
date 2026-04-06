#!/usr/bin/env python3
import re
import os
import glob




REPLACEMENTS = [
    (r'。(?![」\n])', r'。\n', 0),
    (r'！(?![」\n])', r'！\n', 0),
    (r'？(?![」\n])', r'？\n', 0),
    (r'」(?!\n)', lambda m: m.group(0) + '\n', 0),
    (r'」[ \t\u3000]+「', r'」\n「', 0),
    (r'(?<!\n)「', r'\n「', 0),
    (r'book18.org\n','\n',0),
    (r'\n　　','\n',0),
    (r'　　','\n',0)
]

def apply_replacements(text):
    for pat, repl, flags in REPLACEMENTS:
        #print("Pattern: ", pat)
        regex = re.compile(pat, flags)
        while True:
            new_text, n = regex.subn(repl, text)
            if n == 0:
                break
            text = new_text
    return text

def process_all(src_dir, dst_dir):
    pattern = os.path.join(src_dir, '*.txt')
    for src_path in sorted(glob.glob(pattern)):
        print("File: ", src_path)
        with open(src_path, 'r', encoding='utf-8') as f:
            text = f.read()
        new_text = apply_replacements(text)
        dst_path = os.path.join(dst_dir, os.path.basename(src_path))
        with open(dst_path, 'w', encoding='utf-8') as f:
            f.write(new_text)
        print('Wrote:', dst_path)

if __name__ == '__main__':
    SRC_DIR = 'preprocess'   # source folder
    DST_DIR = 'txt'   # destination folder
    process_all(SRC_DIR, DST_DIR)
