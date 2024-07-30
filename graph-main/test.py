import main as main
import json
from io import BytesIO
import PIL.Image as Image
from dataclasses import astuple


def open_file():
    with open("json/test.json", "r+") as file:
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


graph_1 = [
    (
        main.DataGraph(
            name=spisok[0][0] + " contracts ", box_x=spisok[0][4], box_y=spisok[0][1]
        )
    ),
    (
        main.DataGraph(
            name=spisok[0][0] + " descriptors ", box_x=spisok[0][4], box_y=spisok[0][2]
        )
    ),
    (
        main.DataGraph(
            name=spisok[1][0] + " contracts ", box_x=spisok[1][4], box_y=spisok[1][1]
        )
    ),
    (
        main.DataGraph(
            name=spisok[1][0] + " descriptors ", box_x=spisok[1][4], box_y=spisok[1][2]
        )
    ),
]


graph_2 = [
    (
        main.DataGraph(
            name=spisok[0][0] + " used_memory ", box_x=spisok[0][4], box_y=spisok[0][5]
        )
    ),
    (
        main.DataGraph(
            name=spisok[1][0] + " used_memory ", box_x=spisok[1][4], box_y=spisok[1][5]
        )
    ),
]


(Image.open(BytesIO(main.get_graph(graph_1, limit_y)))).save(f"data{1}.png")
(Image.open(BytesIO(main.get_graph(graph_2, limit_y)))).save(f"data{2}.png")
