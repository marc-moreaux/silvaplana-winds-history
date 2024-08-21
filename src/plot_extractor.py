from datetime import datetime, timedelta
from typing import List
import re

import pandas as pd
import numpy as np
import pytesseract
import cv2


wind_plot_ys = (625, 775)


class PlotExtractor():

    def __init__(self, image_path: str,
                 plot_y0: int = 625,
                 plot_height: int = 150) -> None:
        '''Read the weather plot at <image_path>
        plot_y0 is 625 for wind and 780 for direction
        '''
        self.image = cv2.imread(image_path)
        y1 = plot_y0 + plot_height
        self.full_plot = self.image[plot_y0: y1]
        self.extract_plot_and_axis()

    def extract_plot_and_axis(self) -> None:
        '''Extract the image of the axis from the plot
        '''
        self.img_xs = self.full_plot[-21:]
        self.img_ys = self.full_plot[:-21, :22]
        self.plot = self.full_plot[8:-26, 24:-14]

    def _extract_plot_value_at_x(self, x: int) -> float:
        '''Get the value of a function at x on a <plot>
        '''
        value = np.where(self.plot[:, x, 0] == 204)[0].mean()
        normalized_value = value / self.plot.shape[0]
        normalized_value = 1 - normalized_value
        return normalized_value

    def _extract_plot_values(self) -> List[float]:
        '''Get the values of a plot on an <plot> scaled from 0 to 100
        '''
        return [self._extract_plot_value_at_x(x)
                for x in range(self.plot.shape[1])]

    def read_x_axis(self) -> List[str]:
        ''' Read values on on the x axis
        '''
        config = '--psm 13 --oem 3 -c tessedit_char_whitelist=0123456789:'
        xs_values = pytesseract.image_to_string(
            self.img_xs, lang='eng', config=config)
        xs_values = re.findall(r"(\d{1,2}:\d\d)", xs_values)
        return xs_values

    def read_y_axis(self) -> int:
        '''Read value on top of the y axis
        '''
        config = '--psm 13 --oem 3 -c tessedit_char_whitelist=0123456789:'
        y_value = pytesseract.image_to_string(
            self.img_ys[:20], lang='eng', config=config)
        y_value = re.findall(r"\d+", y_value)[0]
        y_value = int(y_value)
        return y_value

    def extract_plot_values(self,
                            current_date: datetime = datetime.now() - timedelta(days=1)
                            ) -> pd.DataFrame:
        '''Extract the values on the plot
        '''
        # Get values
        max_y = self.read_y_axis()
        values = self._extract_plot_values()
        values = np.array(values) * max_y

        # Create x axis as dt
        date_format = "%H:%M"
        x_value = self.read_x_axis()[0]
        dt = datetime.strptime(x_value, date_format)
        dt = dt.replace(year=current_date.year,
                        month=current_date.month,
                        day=current_date.day)
        x_axis = [str(dt + (x * timedelta(hours=24)/(len(values)-1)))
                  for x in range(len(values))]

        # Create a Dataframe out of the datas
        df = pd.DataFrame({'timestamp': x_axis,
                           'values': values})

        # Resample the data to 10 minutes data
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df = df.set_index('timestamp')
        df = df.resample('10min').mean()
        df = df.reset_index()
        df['timestamp'] = df['timestamp'].apply(lambda ts: str(ts))

        return df


'''
# Convert image to grayscale
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Use canny edge detection
edges = cv2.Canny(gray, 50, 150, apertureSize=3)

# Apply HoughLinesP method to
# to directly obtain line end points
lines_list = []
lines = cv2.HoughLinesP(
    edges,  # Input edge image
    1,  # Distance resolution in pixels
    np.pi/180,  # Angle resolution in radians
    threshold=100,  # Min number of votes for valid line
    minLineLength=5,  # Min allowed length of line
    maxLineGap=10  # Max allowed gap between line for joining them
)

# Iterate over points
for points in lines:
    # Extracted points nested in the list
    x1, y1, x2, y2 = points[0]
    # Draw the lines joing the points
    # On the original image
    cv2.line(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
    # Maintain a simples lookup list for points
    lines_list.append([(x1, y1), (x2, y2)])

# Save the result image
cv2.imwrite('detectedLines.png', image)
'''
