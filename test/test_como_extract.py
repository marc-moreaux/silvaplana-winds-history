from src.plot_extractor import PlotExtractor
import matplotlib.pyplot as plt
from datetime import datetime, timedelta


def init_example() -> PlotExtractor:
    test_plot = 'db/colico/20240805-2112.png'
    wp = PlotExtractor(test_plot)
    return wp


def test_plot_extract():
    '''Test extracting of wind values in plot
    '''
    wp = init_example()
    values = wp._extract_plot_values()
    assert values[0] == 1 - (67 / wp.plot.shape[0])


def test_read_xs():
    '''Test read x values'''
    wp = init_example()
    xs = wp.read_x_axis()
    assert '23:10' in xs


def test_read_ys():
    '''Test read y values'''
    wp = init_example()
    y = wp.read_y_axis()
    assert y == 25


def test_extract_plot_real_values():
    '''test the real extraction of values
    '''
    wp = init_example()
    df = wp.extract_plot_values()
    dt = datetime.now() - timedelta(days=1)
    dt = dt.replace(hour=23, minute=10, second=0, microsecond=0)
    assert df['timestamp'][0] == str(dt)

    plt.plot(df['timestamp'], df['values'])
    plt.show()


def test_image_show_all():
    '''Show the images extracted
    '''
    wp = init_example()
    plt.imshow(wp.image)
    plt.show()


def test_image_extraction_speed():
    '''Show the images extracted
    '''
    wp = init_example()
    fig, ax = plt.subplots(2, 2)
    ax[0, 0].imshow(wp.image)
    ax[0, 1].imshow(wp.plot)
    ax[1, 0].imshow(wp.img_xs)
    ax[1, 1].imshow(wp.img_ys)
    plt.show()


def test_image_extraction_dir():
    '''Show the images extracted
    '''
    test_plot = 'db/colico/20240805-2112.png'
    wp = PlotExtractor(
        test_plot,
        bbox_plot=(24, 788, 274, 904),
        bbox_y_label=(0, 780, 20, 800),
        bbox_x_label=(7, 910, -1, 925))

    fig, ax = plt.subplots(2, 2)
    ax[0, 0].imshow(wp.image)
    ax[0, 1].imshow(wp.plot)
    ax[1, 0].imshow(wp.img_xs)
    ax[1, 1].imshow(wp.img_ys)
    plt.show()
