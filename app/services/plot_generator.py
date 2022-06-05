import matplotlib as mpl
import matplotlib.dates
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
# import seaborn as sns
from dateutil.parser import parse
import io


def plot_line_chart(data, isPercentage):

    df = pd.DataFrame(data)
    # df['time_series'] = pd.to_datetime(df['time_series'])
    # df['time_series'] = pd.to_datetime(df['time_series']).dt.tz_convert(None)
    # df['time_series'] = df['time_series'].dt.strftime("%d/%m %H:%M:%S")
    if isPercentage:
        # df['value'] = df['value'] / 100
        df['value'] = df['value']
    else:
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
    df = (df.groupby(['criticity'])['value'].count() / len(df)) * 100
    ax = df.plot(kind='barh', color=[
                 "indigo", "red", "green", "orange"], fontsize=13, width=0.3)
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


def plot_health_chart(data, data2, isPercentage):

    df = pd.DataFrame(data)
    df2 = pd.DataFrame(data2)
    df2.rename(columns={'index': 'time_series',
               'predicted_mean': 'health'}, inplace=True)
    # df['time_series'] = pd.to_datetime(df['time_series'])
    # df['time_series'] = pd.to_datetime(df['time_series']).dt.tz_convert(None)
    # df['time_series'] = df['time_series'].dt.strftime("%d/%m %H:%M:%S")
    if isPercentage:
        # df['value'] = df['value'] / 100
        df['health'] = df['health']
        df2['health'] = df2['health']
    else:
        df['health'] = df['health'] * 100
        df2['health'] = df2['health'] * 100
    df['time_series'] = pd.to_datetime(df['time_series'])
    df2['time_series'] = pd.to_datetime(df2['time_series'])
    df = df.set_index("time_series")
    df2 = df2.set_index("time_series")
    ax = df.plot(label='Saúde do Período', fontsize=13)
    df2.plot(ax=ax,  label='Saúde Prevista')
    ax.set_alpha(0.8)
    # ax.set_title("Consumo", fontsize=22)
    ax.set_ylabel("Porcentagem", fontsize=15)
    ax.set_xlabel("Tempo", fontsize=15)
    L = plt.legend()
    L.get_texts()[0].set_text('Saúde do Período')
    L.get_texts()[1].set_text('Saúde Prevista')
    plt.tight_layout()

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)

    plt.close()

    return buf
