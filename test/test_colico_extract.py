from src.colico_extract import Weather_Plot
import matplotlib.pyplot as plt


def init_example() -> Weather_Plot:
    test_plot = 'db/colico/20240805-2112.png'
    wp = Weather_Plot(test_plot)
    return wp


def test_plot_extract():
    '''Test extracting of wind values in plot
    '''
    wp = init_example()
    values = wp._extract_plot_values()
    assert values[0] == 1 - (67 / wp.plot.shape[0])
    return wp


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
    winds_dt = wp.extract_plot_values()

    plt.plot(winds_dt['datetime'], winds_dt['values'])
    plt.show()
