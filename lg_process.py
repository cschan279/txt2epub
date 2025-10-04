#!/usr/bin/env python3
import os
from glob import glob
import re

def check_file(fn:str):
    with open(fn) as f:
        content = f.read().splitlines()
        for i,r in enumerate(content):
            if i==0:
                print(r)
            elif r[:1].isdigit():#subheader
                print(r)
            elif len(r)==0:#blank line
                pass
            else:#normal content
                pass

def new_file(fn:str,title:str):
    f = open(fn,'w')
    f.write('<?xml version="1.0" encoding="utf-8"?>\n')
    f.write('<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN"\n')
    f.write('  "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">\n')
    f.write('<html xmlns="http://www.w3.org/1999/xhtml">\n')
    f.write('<head>\n')
    f.write(f'  <title>{title}</title>\n')
    f.write('</head>\n')
    f.write('<body>\n')
    return f




        
def convert_file(book_dir:str):
    fn = os.path.join(book_dir,'ch','999.txt')
    if not os.path.exists(fn):
        print(f"No ch/999.txt found in {book_dir}, skip...")
        return
    out_dir = os.path.join(book_dir,'xhtml')
    os.makedirs(out_dir, exist_ok=True)
    content = list()
    with open(fn) as f:
        content.extend(f.read().splitlines())
    
    counter = 100
    out_fn = os.path.join(out_dir,'000.xhtml')
    writer = new_file(out_fn,'Summary')
    for i,r in enumerate(content):
        ln = r.strip('\t　 ')
        if len(ln) == 0:
            writer.write("<br/>\n")
        elif ln[0] == '#': # header
            writer.write('</body>\n</html>\n')
            writer.close()
            print(ln)
            out_fn = os.path.join(out_dir,f'{counter:03d}.xhtml')
            counter += 1
            writer = new_file(out_fn,ln[1:])
            writer.write(f"  <h2>{ln[1:]}</h2>\n")
        elif '（插圖' in ln:
            print(ln)
            img_index=ln.replace('（插圖','').replace('）','')
            img_fn = os.path.join('Images',f"{img_index}.jpg")
            writer.write(f"  <img alt='{img_index}' src='../{img_fn}'/>\n")
        else:
            writer.write(f"  <p>{ln}</p>\n")
    writer.write('</body>\n</html>\n')
    writer.close()
    return


if __name__ == "__main__":
    #for fn in sorted(glob('text/*.txt')):
    path_list = list()
    for ch_dir in glob('lg_txt/*/ch'):
        book_dir = os.path.dirname(ch_dir)
        convert_file(book_dir)
