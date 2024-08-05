from datetime import datetime
import urllib.request
import os

url = 'http://rete.centrometeolombardo.com/Lecco/dervio/immagini/g.png'
img_dir = './db/colico/'
img_name = datetime.now().strftime('%Y%m%d-%H%M.png')
img_path = os.path.join(img_dir, img_name)

with urllib.request.urlopen(url) as f:
    img = f.read()

with open(img_path, 'wb+') as fp:
    fp.write(img)
