from datetime import datetime
from bs4 import BeautifulSoup
import urllib.request
import pandas as pd
import logging
import re
import os


def date2datetime(str_date: str,
                  date_format: str = "%d.%m. %H:%M",
                  today: datetime = datetime.now()):
    '''convert a str date to datetime and 
    include the current year in the date
    '''
    dt = datetime.strptime(str_date, date_format)

    # Get year of tick (beware of january / december)
    if today.month < dt.month:
        current_year = today.year - 1
    else:
        current_year = today.year

    # Override year of tick
    dt = dt.replace(year=current_year)
    return dt


class WindReader():
    def __init__(self):
        self.url = 'https://www.kitesailing.ch/en/spot/webcam'
        self.db_dir = './db/'

    @property
    def db_file(self):
        return f'{self.db_dir}/winds.csv'

    def read_last_csv(self):
        '''Read the last CSV that was downloaded

        output:
            df (DataFrame): Last csv downloaded
        '''
        # Open csv
        df = pd.read_csv(self.dl_path, encoding='latin1',
                         on_bad_lines='skip', sep=';')

        return df

    def append_to_db(self, df):
        '''Append <df> to a csv database. The database has windSpeed and windDir columns indexed by date
        (eg: "       ,windSpeed ,windDir"
             "12/11 ,13         ,358")
        '''
        # Maybe create dir
        if not os.path.isdir(self.db_dir):
            os.mkdir(self.db_dir)

        # Maybe create db_file
        if not os.path.isfile(self.db_file):
            df.to_csv(self.db_file)

        # If DB already exists, merge df and db_file
        else:
            # Read DB
            db = pd.read_csv(self.db_file, index_col=False)
            db = db.set_index('timestamp')

            # Merge DB and the new df
            db = pd.concat([db, df], axis=0)

            # Save DB
            db.to_csv(self.db_file)

    def update_db(self):
        '''Download new readings and merge them into the DB
        '''
        df = self.read_new_winds()
        self.append_to_db(df)

    def read_new_winds(self):
        '''Read the HTML of kitesailing and get the winds informations of the past 6 hours
        '''
        # Html to soup
        logging.info(f"Reading Website {self.url}")
        html_content = urllib.request.urlopen(self.url).read()
        soup = BeautifulSoup(html_content, 'html.parser')
        html = str(soup)

        # Get wind speed, wind direction and timestamps
        logging.info(f"Extracting winds info")
        timestamps = eval(re.findall(r"labels: \[([^]]*)\]", html)[0])
        timestamps = list(map(date2datetime, timestamps))
        wind_speed, wind_dir = map(
            eval, re.findall(r"data: \[([^]]*)\]", html))
        logging.info(
            f"Found {len(timestamps)} timestamps / {len(wind_dir)} wind_dir / {len(wind_speed)} wind_speed")

        logging.info(f"Store new_winds in dataframe")
        df = pd.DataFrame({'timestamp': timestamps,
                           'wind_speed': wind_speed,
                           'wind_dir': wind_dir}).set_index('timestamp')
        return df
