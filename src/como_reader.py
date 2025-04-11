from datetime import datetime
import logging
import urllib
import os

import pandas as pd

from .wind_reader import WindReader
from .plot_extractor import PlotExtractor

bbox_conf1 = {
    'wind_speed': {'bbox_plot': (24, 633, 274, 749),
                   'bbox_y_label': (3, 625, 20, 640),
                   'bbox_x_label':  (7, 755, -1, 770),
                   'x_format': r"(\d{1,2}:\d\d)",
                   'date_format': r"%H:%M"},
    'wind_dir': {'bbox_plot': (24, 788, 274, 904),
                 'bbox_y_label': (0, 780, 20, 800),
                 'bbox_x_label':  (7, 910, -1, 925),
                 'x_format': r"(\d{1,2}:\d\d)",
                 'date_format': r"%H:%M"},
}
bbox_conf2 = {
    'wind_speed': {'bbox_plot': (39, 622, 278, 749),
                   'bbox_y_label': (3, 616, 35, 630),
                   'bbox_x_label': (7, 757, -1, 775),
                   'x_format': r"(\d{2})",
                   'date_format': r"%H"},
    'wind_dir': {'bbox_plot': (39, 778, 279, 906),
                 'bbox_y_label': (0, 772, 35, 784),
                 'bbox_x_label':  (7, 915, -1, 927),
                 'x_format': r"(\d{2})",
                 'date_format': r"%H"},
}
parameters = {
    'Gera_Lario': {
        'url': 'http://rete.centrometeolombardo.com/Como/geralario/immagini/g.png',  # 2
        'bbox_conf': bbox_conf2
    },
    'Pian_di_Spagna': {
        'url': 'http://rete.centrometeolombardo.com/Como/piandispagna/immagini/g.png',  # 2
        'bbox_conf': bbox_conf2
    },
    'Gravedona': {
        'url': 'http://rete.centrometeolombardo.com/Como/gravedona/immagini/g.png',  # 2
        'bbox_conf': bbox_conf2
    },
    'Dongo': {
        'url': 'http://rete.centrometeolombardo.com/Como/dongo/immagini/g.png',  # 2
        'bbox_conf': bbox_conf2
    },
    'Dervio': {
        'url': 'http://rete.centrometeolombardo.com/Lecco/dervio/immagini/g.png',  # 1
        'bbox_conf': bbox_conf1
    },
    'Perledo_Cantone': {
        'url': 'http://rete.centrometeolombardo.com/Lecco/perledo_cantone/immagini/g.png',  # 1
        'bbox_conf': bbox_conf1
    },
    'Ossuccio': {
        'url': 'http://rete.centrometeolombardo.com/Como/ossuccio/immagini/g.png',  # 2
        'bbox_conf': bbox_conf2
    },
    'Oliveto_Lario': {
        'url': 'http://rete.centrometeolombardo.com/Lecco/olivetolario/immagini/g.png',  # 1
        'bbox_conf': bbox_conf1
    },
    'Mandello': {
        'url': 'http://rete.centrometeolombardo.com/Lecco/mandello/immagini/g.png',  # 2
        'bbox_conf': bbox_conf2
    },
    'Lecco': {
        'url': 'http://rete.centrometeolombardo.com/Lecco/lecco/immagini/g.png',  # 2
        'bbox_conf': bbox_conf2
    },
    'Garlate': {
        'url': 'http://rete.centrometeolombardo.com/Lecco/garlate/immagini/g.png',  # 2
        'bbox_conf': bbox_conf2
    }
}


class ComoReader(WindReader):
    def __init__(self, wind_station):
        url = parameters[wind_station]['url']
        self.bbox_conf = parameters[wind_station]['bbox_conf']
        super().__init__(wind_station=wind_station, url=url)

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
        logging.info(f'Downloading image from : {self.url}')
        with urllib.request.urlopen(self.url) as f:
            img = f.read()

        # Save image
        logging.info(f'Saving image at {img_path}')
        with open(img_path, 'wb+') as fp:
            fp.write(img)

        # Extract wind speed and direction from image
        logging.info(f'Extract wind speed and direction from image')
        wp = PlotExtractor(
            img_path,
            **self.bbox_conf['wind_speed']
        )
        winds_df = wp.extract_plot_values()
        wind_speed = (winds_df['values'] * 100).astype(int).astype(float) / 100

        dp = PlotExtractor(
            img_path,
            **self.bbox_conf['wind_dir']
        )
        direction_df = dp.extract_plot_values()
        wind_dir = direction_df['values'].astype(int)

        df = pd.DataFrame({'timestamp': winds_df['timestamp'],
                           'wind_speed': wind_speed,
                           'wind_dir': wind_dir}).set_index('timestamp')

        # Delete image
        logging.info(f'Deleting image at: {img_path}')
        os.remove(img_path)

        return df
