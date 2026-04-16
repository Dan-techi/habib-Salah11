import re
from pathlib import Path
base = Path('.')
home = base / 'guma-smart.html'
text = home.read_text(encoding='utf-8')
css_start = text.index('.cart-fab{')
css_end = text.index('.receipt-or::after{right:0}') + len('.receipt-or::after{right:0}')
css_block = text[css_start:css_end]
pattern = re.compile(r'\.cart-fab\{.*?\.receipt-cancel\{.*?\}', re.S)
pages = ['iphone.html','samsung.html','infinix.html','tecno.html','itel.html']
for p in pages:
    path = base / p
    content = path.read_text(encoding='utf-8')
    found = bool(pattern.search(content))
    print(p, 'match_found=', found)
    if found:
        new_content = pattern.sub(css_block, content, count=1)
        path.write_text(new_content, encoding='utf-8')
        print(p, 'replaced')
    else:
        print(p, 'no match')
