import matplotlib as mpl
import matplotlib.dates
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from dateutil.parser import parse

# Import as Dataframe
df = pd.read_csv(r'pycedata.csv', parse_dates=['date'], infer_datetime_format=True)
df['cpu_usage'] = df['cpu_usage'].astype('float')/100.0

# Draw Plot
def plot_df(df, x, y, title="", xlabel='Date', ylabel='Value', dpi=100):
    plt.figure(figsize=(16,5), dpi=dpi)
    plt.plot(x, y, color='tab:red')
    plt.gca().set(title=title, xlabel=xlabel, ylabel=ylabel)
    plt.show()
    
    

plot_df(df, x=df.time, y=df.cpu_usage, title='CPU Process Usage')
