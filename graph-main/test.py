import main
import json
from io import BytesIO
import PIL.Image as Image
from dataclasses import astuple


def open_file():
    with open("test.json", "r+") as file:
        file = json.load(file)
        general_box = []

        for name, nested_dictionary in file.items():

            (
                box_contracts,
                box_descriptors,
                box_total_memory,
                box_uptime,
                box_used_memory,
            ) = ([], [], [], [], [])

            for block in nested_dictionary:
                box_contracts.append(block["contracts"])
                box_descriptors.append(block["descriptors"])
                box_total_memory.append(block["total_memory"])
                box_uptime.append(block["uptime"])
                box_used_memory.append(block["used_memory"])

            general_box.append(
                [
                    name,
                    box_contracts,
                    box_descriptors,
                    box_total_memory,
                    box_uptime,
                    box_used_memory,
                ]
            )

        return general_box


spisok = open_file()

# преобразование времени (мс -> с)

for index in range(0, len(spisok)):
    spisok[index][4] = list(map(lambda g: (g / 1000), spisok[index][4]))


# отвечает за ограничение вертикальной оси графика
limit_y = 4000


graph_2 = [
    [spisok[0][0] + " used_memory ", spisok[0][4], spisok[0][5]],
    [spisok[1][0] + " used_memory ", spisok[1][4], spisok[1][5]],
]


graph_1 = [
    astuple(main.DataGraph(spisok[0][0] + " contracts ", spisok[0][4], spisok[0][1])),
    astuple(main.DataGraph(spisok[0][0] + " descriptors ", spisok[0][4], spisok[0][2])),
    astuple(main.DataGraph(spisok[1][0] + " contracts ", spisok[1][4], spisok[1][1])),
    astuple(main.DataGraph(spisok[1][0] + " descriptors ", spisok[1][4], spisok[1][2])),
]


graph_2 = [
    astuple(main.DataGraph(spisok[0][0] + " used_memory ", spisok[0][4], spisok[0][5])),
    astuple(main.DataGraph(spisok[1][0] + " used_memory ", spisok[1][4], spisok[1][5])),
]


(Image.open(BytesIO(main.get_graph(graph_1, limit_y)))).save(f"data{1}.png")
(Image.open(BytesIO(main.get_graph(graph_2, limit_y)))).save(f"data{2}.png")
