import numpy as np
from matplotlib import pyplot as plt


def vertial_bar_nps_mean(dataframe, xaxis):
    media_por_setor = dataframe.groupby(f"{xaxis}").mean(numeric_only=True)["NPS interno"]

    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    ax.bar(media_por_setor.index, media_por_setor.values)
    ax.set_ylabel("NPS Médio por setores")
    ax.set_yticks(np.arange(0, 11, 1))
    ax.set_title(f"NPS médio mensal por {xaxis}")
    fig.savefig("graph_last_fig.png")
    return plt.close(fig)


def hist_nps(dataframe):
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    ax.hist(dataframe["NPS interno"])
    ax.set_title("Distribuição do NPS mensal")
    ax.set_xlabel("NPS")
    fig.savefig("graph_last_fig.png")
    return plt.close(fig)
