from src.wind_reader import WindReader
from src.colico_extract import Weather_Plot
import logging
import pandas as pd
import urllib
from datetime import datetime
import os

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

wind_sation = 'Dervio'
url = 'http://rete.centrometeolombardo.com/Lecco/dervio/immagini/g.png'


class ComoReader(WindReader):
    def __init__(self):
        super().__init__(wind_station=wind_sation,
                         url=url)

    def read_new_winds(self):
        '''Download image of new winds from rete.centrometeolombardo,
        Save it in a temporary file. Extract wind info from the day. Delete file
        '''
        # Create image path
        img_dir = os.path.join(self.db_dir, self.wind_station)
        img_name = datetime.now().strftime('%Y%m%d-%H%M.png')
        img_path = os.path.join(img_dir, img_name)
        os.makedirs(img_dir, exist_ok=True)

        # Read image
        logging.info(f'Downloading image from : {url}')
        with urllib.request.urlopen(url) as f:
            img = f.read()

        # Save image
        logging.info(f'Saving image at {img_path}')
        with open(img_path, 'wb+') as fp:
            fp.write(img)

        # Extract wind speed and direction from image
        logging.info(f'Extract wind speed and direction from image')
        wp = Weather_Plot(img_path)
        winds_df = wp.extract_plot_values()
        wind_speed = (winds_df['values'] * 100).astype(int).astype(float) / 100

        dp = Weather_Plot(img_path, plot_y0=780)
        direction_df = dp.extract_plot_values()
        wind_dir = direction_df['values'].astype(int)

        df = pd.DataFrame({'timestamp': winds_df['timestamp'],
                           'wind_speed': wind_speed,
                           'wind_dir': wind_dir}).set_index('timestamp')

        # Delete image
        logging.info(f'Deleting image at: {img_path}')
        os.remove(img_path)

        return df
