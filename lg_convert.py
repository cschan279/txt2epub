import os
from glob import glob

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

        
def convert_file(fn:str,nfn:str):
    content = list()
    with open(fn) as f:
        content.extend(f.read().splitlines())
    
    with open(nfn,'w') as nf:
        nf.write('<?xml version="1.0" encoding="utf-8"?>\n')
        nf.write('<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN"\n')
        nf.write('  "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">\n')
        nf.write('<html xmlns="http://www.w3.org/1999/xhtml">\n')
        nf.write('<head>\n')
        nf.write(f'  <title>{fn}</title>\n')
        nf.write('</head>\n')
        nf.write('<body>\n')
        for i,r in enumerate(content):
            if r[:2] == '# ':#subheader
                r_head = r.replace('# ','')
                print(r, r_head)
                nf.write(f"  <h2>{r_head}</h2>\n")
            elif len(r)==0:#blank line
                pass
            elif '（插圖' in r:
                img_fname=r.split(' ')[-1].replace('）','')
                nf.write(f"  <img alt='{img_fname}' src='../Images/{img_fname}'/>\n")
            else:#normal content
                row = r.replace("　　","")
                nf.write(f'  <p>{row}</p>\n')
        nf.write('</body>\n')
        nf.write('</html>\n')

if __name__ == "__main__":
    #for fn in sorted(glob('text/*.txt')):
    path_list = list()
    for txt_path in glob('lg_txt/*/ch/*.txt'):
        xml_path = txt_path.replace('/ch/','/xhtml/').replace('.txt','.xhtml')


        convert_file(txt_path,xml_path)
