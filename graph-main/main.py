import io
import matplotlib.pyplot as plt
from dataclasses import dataclass


@dataclass
class DataGraph:
    name: str
    box_x: list[float]
    box_y: list[float]


def get_graph(data, max_y=0):

    for index_list_block in data:
        data_X_for_normalization = list(
            map(
                lambda uptime: (uptime - index_list_block.box_x[0]),
                index_list_block.box_x,
            )
        )

        plt.plot(
            data_X_for_normalization,
            index_list_block.box_y,
            label=index_list_block.name,
            drawstyle="steps-mid",
        )

    if max_y != 0:
        plt.ylim(0, max_y)

    buf = io.BytesIO()
    buf.seek(0)
    plt.xlabel("uptime")
    plt.legend()
    plt.grid()
    plt.savefig(buf, format="png")
    plt.close("all")
    return buf.getvalue()
