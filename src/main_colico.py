from datetime import datetime
import urllib.request
import logging
import os

from src.colico_extract import Weather_Plot


urls = {
    'Gera_Lario': 'http://rete.centrometeolombardo.com/Como/geralario/immagini/g.png',
    'Pian_di_Spagna': 'http://rete.centrometeolombardo.com/Como/piandispagna/immagini/g.png',
    'Gravedona': 'http://rete.centrometeolombardo.com/Como/gravedona/immagini/g.png',
    'Dongo': 'http://rete.centrometeolombardo.com/Como/dongo/immagini/g.png',
    'Dervio': 'http://rete.centrometeolombardo.com/Lecco/dervio/immagini/g.png',
    'Perledo_Cantone': 'http://rete.centrometeolombardo.com/Lecco/perledo_cantone/immagini/g.png',
    'Ossuccio': 'http://rete.centrometeolombardo.com/Como/ossuccio/immagini/g.png',
    'Oliveto_Lario': 'http://rete.centrometeolombardo.com/Lecco/olivetolario/immagini/g.png',
    'Mandello': 'http://rete.centrometeolombardo.com/Lecco/mandello/immagini/g.png',
    'Lecco': 'http://rete.centrometeolombardo.com/Lecco/lecco/immagini/g.png',
    'Garlate': 'http://rete.centrometeolombardo.com/Lecco/garlate/immagini/g.png',
}


def get_images():
    for city, url in urls.items():

        # Create image path
        img_dir = os.path.join('db/Como', city)
        img_name = datetime.now().strftime('%Y%m%d-%H%M.png')
        img_path = os.path.join(img_dir, img_name)
        os.makedirs(img_dir, exist_ok=True)

        try:
            # Read image
            with urllib.request.urlopen(url) as f:
                img = f.read()

            # Save image
            with open(img_path, 'wb+') as fp:
                fp.write(img)

            # Extract wind from image
            wp = Weather_Plot(img_path)
            winds_dt = wp.extract_plot_values()

            # Delete image
            os.remove(img_path)

        except Exception as e:
            logging.error(
                f"Could not read and save image from {city}. Error: {e}")


if __name__ == '__main__':
    get_images()
