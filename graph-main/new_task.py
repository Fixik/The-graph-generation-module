from new_main import get_graph, DataGraph
import json
from io import BytesIO
import PIL.Image as Image


def clish(key):
    with open("json/other_stats.json", "r+") as file:
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

            def adding_the_list(name, box):
                general_box.append(DataGraph(name=name, box_x=box_uptime, box_y=box))

            match key:
                # добавление uptime и contracts
                case 0:
                    adding_the_list(f"{name} contracts", box_contracts)

                # добавление uptime и descriptors
                case 1:
                    adding_the_list(f"{name} descriptors", box_descriptors)

                # добавление uptime и total_memory
                case 2:
                    adding_the_list(f"{name} total_memory", box_total_memory)

                # добавление uptime и используемой памяти
                case 3:
                    adding_the_list(f"{name} used_memory", box_used_memory)

                # добавление в список всех параметров
                case 4:
                    general_box = [
                        name,
                        box_contracts,
                        box_descriptors,
                        box_total_memory,
                        box_uptime,
                        box_used_memory,
                    ]

        return general_box


def snmp():
    DataCore = []

    with open(f"json/cpu.json", "r") as file:
        file = json.load(file)

        for name, nested_dictionary in file.items():
            entry = 0
            block_data = [name, [], []]

            for block in nested_dictionary:
                for block_key, data in block.items():
                    match block_key:
                        case "cores":
                            if entry == 0:
                                for g in range(0, len(data)):
                                    block_data[2].append([])

                                entry += 1

                            for core in range(0, len(data)):
                                block_data[2][core].append(data[core])

                        case "uptime":
                            block_data[1].append(data)

            for g in range(0, len(block_data[2])):
                DataCore.append(
                    DataGraph(
                        name=(f"{block_data[0]}, core: {g}"),
                        box_x=block_data[1],
                        box_y=block_data[2][g],
                    )
                )

    return DataCore


# utilization parameter
def parameter_utilization(basketA, basketB):
    max_value = max(basketB[0].box_y)
    basketA[0].box_y = list(map(lambda element: ((element / max_value) * 100), basketA[0].box_y))
    return basketA


def filter(data, device):
    sorted_list = []
    for block in data:
        if device in block.name:
            sorted_list.append(block)

    return sorted_list



a1 = filter(clish(3), "pep1")
b1 = filter(clish(2), "pep1")

a2 = filter(clish(3), "pep2")
b2 = filter(clish(2), "pep2")

box1 = parameter_utilization(a1,b1) + filter(snmp(), "pep1")
box2 = parameter_utilization(a2,b2) + filter(snmp(), "pep2")

(Image.open(BytesIO(get_graph(box1, 0, 1)))).save(f"data{1}.png")
(Image.open(BytesIO(get_graph(box2, 0, 1)))).save(f"data{2}.png")