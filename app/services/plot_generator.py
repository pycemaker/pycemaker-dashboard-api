import matplotlib as mpl
import matplotlib.dates
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
# import seaborn as sns
from dateutil.parser import parse
import io


def plot_line_chart(data):

    df = pd.DataFrame(data)
    df['time_series'] = pd.to_datetime(df['time_series']).dt.tz_convert(None)
    df['time_series'] = df['time_series'].dt.strftime("%d/%m %H:%M:%S")
    df['value'] = df['value'] * 100
    ax = df.plot(kind='line', x='time_series', y='value', fontsize=13)
    ax.set_alpha(0.8)
    # ax.set_title("Consumo", fontsize=22)
    ax.set_ylabel("Porcentagem", fontsize=15)
    ax.set_xlabel("Tempo", fontsize=15)
    plt.xticks(rotation=45)
    plt.tight_layout()

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)

    plt.close()

    return buf


def plot_barh_chart(data):

    df = pd.DataFrame(data)
    df = df.replace(np.nan, 0)
    df = df.groupby(['criticity'])['value'].sum()
    ax = df.plot(kind='barh', color=[
                 "indigo", "red", "green", "orange"], fontsize=13)
    ax.set_alpha(0.8)
    ax.set_title("Níveis de Consumo", fontsize=22)
    ax.set_ylabel("Criticidade", fontsize=15)
    ax.set_xlabel("Porcentagem de Tempo", fontsize=15)
    plt.tight_layout()

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)

    plt.close()

    return buf
