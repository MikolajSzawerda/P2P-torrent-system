import pandas as pd
import os
import matplotlib.pyplot as plt
current_directory = os.getcwd()
dfs = []
for filename in os.listdir(current_directory):
    if filename.startswith('log') and not filename.endswith(".png"):
        dfs.append((filename, pd.read_csv(filename)))

min_size = min([len(df) for (fn, df) in dfs])
for filename, df in dfs:
    df = df.head(min_size)
    print(filename)
    print(df.describe())
    fig = df.plot(xlabel="# pakiety", ylabel="Czas wykonania send", title="Wykres czasu wysłania od zdarzeń wysłania").get_figure()
    fig.set_size_inches(18.5, 10.5)
    fig.savefig(filename+"-plot.png")
