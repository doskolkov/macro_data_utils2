import matplotlib.pyplot as plt

def format_date(date, lang):
    month_names = {
        'rus': {1: 'янв', 2: 'фев', 3: 'мар', 4: 'апр', 5: 'май', 6: 'июн',
                7: 'июл', 8: 'авг', 9: 'сен', 10: 'окт', 11: 'ноя', 12: 'дек'},
        'eng': {1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May', 6: 'Jun',
                7: 'Jul', 8: 'Aug', 9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dec'}
    }
    year = str(date.year)[-2:]
    month = month_names[lang][date.month]
    return f"{month} '{year}"

#OLD format - need refactoring
def format_date_2(date, lang):
    rus_month = {1: 'янв', 2: 'фев', 3: 'мар', 4: 'апр', 5: 'май', 6: 'июн',
                 7: 'июл', 8: 'авг', 9: 'сен', 10: 'окт', 11: 'ноя', 12: 'дек'}
    eng_month = {1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May', 6: 'Jun',
                 7: 'Jul', 8: 'Aug', 9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dec'}
    day = str(date.day)
    if lang == 'rus':
        month = rus_month[date.month]
    if lang == 'eng':
        month = eng_month[date.month]
    return month + ' ' + day

def get_cib_color(n):
    blue_chill = [0, 118, 108, 26, 132, 123, 51, 145, 137, 77, 159, 152, 102, 173, 167, 127, 186, 181, 153, 200, 196, 178, 214, 211, 204, 228, 226, 229, 241, 240]
    graphite = [63, 72, 81, 78, 83, 92, 92, 96, 104, 107, 109, 117, 123, 124, 131, 140, 140, 147, 159, 158, 164, 178, 177, 182, 199, 199, 202, 223, 222, 223]
    vivid_violet = [97, 29, 108, 114, 61, 123, 130, 70, 140, 145, 104, 152, 160, 125, 167, 176, 146, 180, 192, 169, 197, 207, 189, 210, 224, 212, 226, 239, 233, 240]
    color_groups = [blue_chill, graphite, vivid_violet]
    ord_colors = [color_group[i:i+3] for i in range(0, 30, 3) for color_group in color_groups]

    for i in range(n):
        rgb_color = tuple(c / 255 for c in ord_colors[i])
        yield rgb_color

def set_chart_style():
    """

    """
    plt.rc('font', size=18)
    plt.rc('axes', titlesize=18)
    plt.rc('axes', labelsize=18)
    plt.rc('xtick', labelsize=18)
    plt.rc('ytick', labelsize=18)
    plt.rc('legend', fontsize=18)
    plt.rc('figure', titlesize=18)


import numpy as np
import pandas as pd


def plot_graph(dates, var1, var2, lang, label1, label2, single_axis=False, x_tick_interval='quarterly'):
    colors = list(get_cib_color(2))

    interval_map = {
        'daily': 1,
        'monthly_3': 3,
        'monthly_6': 6,
        'weekly': 7,
        'monthly': 30,
        'quarterly': 90,
        'annual': 365
    }

    tick_interval = interval_map[x_tick_interval]
    tick_indexes = np.arange(0, len(dates), tick_interval)
    formatted_dates = [format_date(dates[i], lang) for i in tick_indexes]

    plt.figure(figsize=(11, 5))
    set_chart_style()

    ax1 = plt.axes()
    if single_axis:
        ax2 = ax1
    else:
        ax2 = ax1.twinx()

    leg_one = ax1.plot(dates, var1, label=label1, color=colors[0], linewidth=3)
    leg_two = ax2.plot(dates, var2, label=label2, color=colors[1], linewidth=3)
    lns = leg_one + leg_two
    labs = [l.get_label() for l in lns]
    ax1.legend(lns, labs, loc='upper left', bbox_to_anchor=(-0.05, -0.18, 1.1, 0.1), ncol=2, framealpha=0)
    plt.xticks(ticks=[dates[i] for i in tick_indexes], labels=formatted_dates)
    plt.grid()
    plt.xlim(dates[0], dates[-1])

    for spine in ax1.spines:
        ax1.spines[spine].set_visible(False)
    for spine in ax2.spines:
        ax2.spines[spine].set_visible(False)

    plt.show()

