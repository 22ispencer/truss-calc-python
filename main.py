import matplotlib.pyplot as plt
import numpy as np
import os
import json
from tkinter import Tk
import tkinter.filedialog as fd


class Node:
    def __init__(self, x: float, y: float, x_support: bool = False, y_support: bool = False):
        self.x = x
        self.y = y
        self.x_support = x_support
        self.y_support = y_support
        self.ext_force = np.zeros(2)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def set_supports(self, x_support: bool = False, y_support: bool = False):
        self.x_support = x_support
        self.y_support = y_support

    def add_force(self, force_x: float, force_y: float):
        self.ext_force = [force_x, force_y]

    def print(self):
        return f"x: {self.x}, y: {self.y}, x_support: {self.x_support}, y_support: {self.y_support}"


nodes = []
members = []
member_count = 0


def prompt(cmd_str) -> str:
    return input(f"\n{cmd_str}\n> ")


def clear_lines():
    for i in range(os.get_terminal_size().columns // 2):
        os.system('cls' if os.name == 'nt' else 'clear')


def bold(input: str) -> str:
    return f"{str}"


def italic(input: str, add_quote: bool = False) -> str:
    return f"\x1B[3m\"{str}\"\x1B[0m" if add_quote else f"\x1B[3m{str}\x1B[0m"


def try_add_member(node_1_in, node_2_in) -> str | None:
    try:
        node_1 = int(node_1_in)
        node_2 = int(node_2_in)
        node_ids = range(len(nodes))
        if ({node_1, node_2} in members):
            statement = "Cannot add duplicate members"
        elif not (node_1 in node_ids and node_2 in node_ids):
            statement = "Node out of range"
        else:
            members.append({node_1, node_2})
            nodes[node_1].add_connection(node_2)
            nodes[node_2].add_connection(node_1)
    except Exception as e:
        return "Invalid parameter type"


def try_add_node(x_in, y_in, x_support_in=None, y_support_in=None) -> str | None:
    try:
        x = float(x_in)
        y = float(y_in)

        x_support = False
        if x_support_in:
            if not (x_support_in.lower() in yes_list + no_list):
                raise Exception("Invalid Parameter")
            x_support = x_support_in.lower() in yes_list

        y_support = False
        if y_support_in:
            if not (y_support_in.lower() in yes_list + no_list):
                raise Exception("Invalid Parameter")
            y_support = y_support_in.lower() in yes_list

        node = Node(x, y, x_support, y_support)
        if not (node in nodes):
            nodes.append(node)
        else:
            return "Node already exists."
    except Exception as e:
        return "Invalid parameter type"


def try_add_force(node_in, param_1, param_2, option=None) -> str | None:
    try:
        node = int(node_in)
        if option in ["-d", "--degrees"]:
            force = float(param_1)
            angle = float(param_2) * np.pi/180
            force_x = float(force * np.cos(angle))
            force_y = float(force * np.sin(angle))
        elif option in ["-r", "--radians"]:
            force = float(param_1)
            angle = float(param_2)
            force_x = float(force * np.cos(angle))
            force_y = float(force * np.sin(angle))
        elif option == None:
            force_x = float(param_1)
            force_y = float(param_2)
        else:
            return "Invalid option type"
        if node in range(len(nodes)):
            nodes[node].add_force(force_x, force_y)
        else:
            return "Node out of bounds"
    except Exception as e:
        return "Invalid parameter type"


def try_solve():
    supports = []
    for i in enumerate(nodes):
        node_id = i[0]
        node = i[1]
        if (node.x_support is True):
            supports.append((node_id, "x"))
        if (node.y_support is True):
            supports.append((node_id, "y"))

    if not (len(members) + len(supports) == 2 * len(nodes)):
        return "Truss is statically indeterminate, try adding or removing a support"

    dim = 2 * len(nodes)
    left = np.zeros((dim, dim))
    right = np.zeros(dim)

    for i in enumerate(nodes):
        node = i[1]
        node_id = i[0]

        connections = filter(lambda m: node_id in m, members)

        for mem in connections:
            mem_list = list(mem)
            mem_list.remove(node_id)
            node_2 = mem_list[0]
            d_x = nodes[node_2].x - node.x
            d_y = nodes[node_2].y - node.y
            d = np.sqrt(d_x ** 2 + d_y ** 2)
            left[2*node_id, members.index(mem)] = d_x/d
            left[2*node_id+1, members.index(mem)] = d_y/d

        if (node_id, "x") in supports:
            left[2*node_id, len(members)+supports.index((node_id, "x"))] = 1
        if (node_id, "y") in supports:
            left[2*node_id+1, len(members)+supports.index((node_id, "y"))] = 1

        if not (node.ext_force[0] == 0 and node.ext_force[1] == 0):
            right[2*node_id] = -1*node.ext_force[0]
            right[2*node_id+1] = -1*node.ext_force[1]

    solutions = np.linalg.solve(left, right)

    return_string = ""

    for i in enumerate(solutions):
        solu_num = i[0]
        solu = i[1]

        if (solu_num < len(members)):
            if solu_num == 0:
                return_string += "Member Forces (positive assumes tension): "
            return_string += "\n" + str(members[solu_num]) + ": " + str(solu)
        else:
            index = solu_num - len(members)
            if index == 0:
                return_string += "\n\nSupport Reactions:"
            return_string += "\n" + \
                str(supports[index][0]) + "-" + \
                supports[index][1] + ": " + str(solu)

    return return_string


def try_load(filepath=""):
    if not filepath:
        root = Tk()
        root.withdraw()
        root.lift()
        filepath = fd.askopenfilename()
    try:
        data = json.load(open(filepath))
    except Exception as e:
        return "Invalid filepath"

    try:
        for node in data["nodes"]:
            node_obj = Node(float(node["x"]), float(node["y"]),
                            node["x_support"], node["y_support"])
            node_obj.add_force(
                float(node["ext_force"][0]), float(node["ext_force"][1]))
            nodes.append(node_obj)

        for mem in data["members"]:
            members.append({mem[0], mem[1]})

        return "Successfully loaded data"
    except Exception as e:
        return "Invalid data"


def save(directory="", filename="", overwrite=False):
    if not directory:
        root = Tk()
        root.withdraw()
        root.lift()
        directory = fd.askdirectory()

    if not directory:
        return "Must choose a save folder"

    nodes_dicts = []
    members = []

    for n in enumerate(nodes):
        node_id = n[0]
        node = n[1]
        node_dict = {
            "x": node.x,
            "y": node.y,
            "x_support": node.x_support,
            "y_support": node.y_support,
            "ext_force": node.ext_force
        }
        nodes_dicts.append(node_dict)

        for conn in node.connections:
            if not {node_id, conn} in members:
                members.append({node_id, conn})

    members_json = list(map(lambda m: [min(m), max(m)], members))

    data_dict = {
        "nodes": nodes_dicts,
        "members": members_json
    }

    json_obj = json.dumps(data_dict, separators=(',', ':'))

    filename = filename if not filename == "" else "truss_data"

    filename_split = filename.split(".")

    if len(filename_split) > 1:
        filename = ".".join(filename_split[:-1])
        file_ext = filename_split[-1]
    else:
        file_ext = ".json"

    file = directory + "/" + filename + file_ext

    loop = not overwrite
    while loop:
        if os.path.isfile(file):
            file_split = filename.split("_")
            if (len(file_split) >= 2):
                filenames = file_split[:-1]
                try:
                    file_count = int(file_split[-1])
                except:
                    filenames = file_split
                    file_count = int(0)
                filename = "_".join(filenames) + "_" + str(file_count+1)
            else:
                filename = file_split[0] + "_1"
            file = directory + "/" + filename + file_ext
        else:
            loop = False

    with open(file, "w") as f:
        f.write(json_obj)

    return "File successfully saved"


def plot():

    fig, ax = plt.subplots()

    for member in members:
        member_data = list(member)
        node_1 = nodes[member_data[0]]
        node_2 = nodes[member_data[1]]
        x = np.array([node_1.x, node_2.x])
        y = np.array([node_1.y, node_2.y])
        ax.plot(x, y, "g-", linewidth=2)

    x = np.array(list(map(lambda n: n.x, nodes)))
    y = np.array(list(map(lambda n: n.y, nodes)))

    ax.scatter(x, y)

    for i in enumerate(zip(x, y)):
        point_id = i[0]
        xy = i[1]
        ax.annotate(str(point_id), xy=xy, textcoords='data')

    x_range = max(x) - min(x)
    y_range = max(y) - min(y)
    xlim = (min(x) - x_range/8, max(x) + x_range/8)
    ylim = (min(y) - y_range/8, max(y) + y_range/8)

    ax.set(xlim=xlim, ylim=ylim)

    ax.set_aspect("equal", adjustable="box")

    plt.show()


yes_list = ["yes", "y", "1", "true"]
no_list = ["no", "n", "0", "false"]

clear_lines()
print("\nWelcome to Isaac's Truss Force Calculator.")
while True:
    cmd = prompt("What would you like to do?")
    cmd = cmd.strip()
    sub_cmds = cmd.split(" ")
    params = len(sub_cmds)

    statement = None

    if (sub_cmds[0] == "new"):
        if (sub_cmds[1] == "node"):
            if (params == 6):
                statement = try_add_node(sub_cmds[2], sub_cmds[3],
                                         sub_cmds[4], sub_cmds[5])
            elif (params == 4):
                statement = try_add_node(sub_cmds[2], sub_cmds[3])
            elif (params == 2):
                x = prompt("What is the x coordinate?")
                y = prompt("What is the y coordinate?")
                x_support = prompt("Does it have support in the x plane?")
                y_support = prompt("Does it have support in the y plane?")
                statement = try_add_node(x, y, x_support, y_support)
            else:
                statement = "Invalid number of arguments."
        elif (sub_cmds[1] == "member"):
            if (params == 4):
                statement = try_add_member(sub_cmds[2], sub_cmds[3])
            elif (params == 2):
                node_1 = int(prompt("What is the first node id?"))
                node_2 = int(prompt("What is the second node id?"))
                statement = try_add_member(node_1, node_2)
            else:
                statement = "Invalid number of arguments"
        elif (sub_cmds[1] == "force"):
            if (params == 5):
                statement = try_add_force(
                    sub_cmds[2], sub_cmds[3], sub_cmds[4])
            elif (params == 6):
                statement = try_add_force(
                    sub_cmds[2], sub_cmds[3], sub_cmds[4])
            else:
                statement = "Invalid number of arguments"
        else:
            statement = "\nPlease specify a new type, for help type " + \
                italic("help new", True)
    elif (sub_cmds[0] == "print"):
        if (sub_cmds[1] == "nodes"):
            print(bold("Nodes:"))
            for i in enumerate(nodes):
                node_id = i[0]
                node = i[1]
                print(f"node_{node_id}: \n  x: {node.x} \n  y: {node.y} \n  x_support: "
                      f"{node.x_support} \n  y_support: {node.y_support}\n")
    elif sub_cmds[0] == "solve":
        statement = try_solve()
    elif sub_cmds[0] == "plot":
        if (len(nodes) > 0):
            plot()
        else:
            statement = "Cannot plot without data"
    elif sub_cmds[0] == "load":
        if (params == 2):
            statement = try_load(sub_cmds[1])
        elif (params == 1):
            statement = try_load()
        else:
            statement = "Invalid number of arguments"
    elif sub_cmds[0] == "save":
        if (params == 3):
            statement = save(sub_cmds[1], sub_cmds[3])
        elif (params == 2):
            statement = save(sub_cmds[1])
        elif (params == 1):
            statement = save()
        else:
            statement = "Invalid number of arguments"

    if statement:
        print(f"\n{statement}")

    if cmd == "exit":
        exit()
