import tkinter

import pygame
import sys
import graph
import interface
from tkinter import messagebox as mb

is_orient = False
nodes = []
buttons = []
selected = None
curr = None

pygame.init()

WINDOW_SIZE = 1200, 700

screen = pygame.display.set_mode(WINDOW_SIZE)
screen.fill((255, 255, 255))


def draw_graph():
    for node in nodes:
        for neigh, count in node.neigh.items():
            if node == neigh:
                interface.draw_self_lines(screen, node.x, node.y, count=count)
            else:
                interface.draw_lines(screen, (node.x, node.y), (neigh.x, neigh.y), count, is_orient)

    for node in nodes:
        interface.draw_node(screen, node.x, node.y, str(node.num), node == selected)


def init_buttons():
    # Orientation button
    def switch_orient(btn):
        global is_orient
        is_orient = not is_orient

        btn.text = "Orient" if btn.text == "Unorient" else "Unorient"

    b1 = interface.Button("Orient", lambda: switch_orient(btn), 50, WINDOW_SIZE[1] - 70, 167, 55)
    buttons.append(b1)

    # Get edges list button
    def copy_edge_lst():
        lst = graph.make_edges_set(nodes, is_orient)
        root = tkinter.Tk()
        root.withdraw()
        data = "\n".join(map(lambda x: f"{x[0]} {x[1]}", lst))
        mb.showinfo(title=f"Список рёбер ({len(lst)}) – скопировано", message=data)
        root.clipboard_clear()
        root.clipboard_append(data)
        root.destroy()

    b2 = interface.Button("Get edges list", copy_edge_lst, WINDOW_SIZE[0] - 600, WINDOW_SIZE[1] - 70, 290, 55)
    buttons.append(b2)

    # Get adjacency matrix
    def copy_matrix():
        root = tkinter.Tk()
        root.withdraw()
        if len(nodes):
            mtx = graph.make_matrix(nodes, is_orient)
            data = "\n".join(map(lambda x: " ".join(map(str, x)), mtx))
            root.clipboard_clear()
            root.clipboard_append(data)
        else:
            data = ""
        mb.showinfo(title=f"Матрица смежности – скопировано", message=data)
        root.destroy()

    b3 = interface.Button("Get matrix", copy_matrix, WINDOW_SIZE[0] - 260, WINDOW_SIZE[1] - 70, 210, 55)
    buttons.append(b3)

    # Clear
    def clear():
        nodes.clear()
        global node_num
        node_num = 1

    b4 = interface.Button("Clear", clear, 250, WINDOW_SIZE[1] - 70, 150, 55)
    buttons.append(b4)

    # Nodes count
    def nodes_count(btn):
        btn.text = "Nodes count: " + str(max(map(lambda x: x.num, nodes))) + "(" + str(len(nodes)) + ")"

    b5 = interface.Button("Nodes count: 0", lambda: nodes_count(b5), 20, 20, 375, 55)
    buttons.append(b5)


def node_num():
    nums = set(map(lambda x: x.num, nodes))
    for i in range(1, len(nodes) + 2):
        if i not in nums:
            return i


init_buttons()

while True:
    screen.fill((255, 255, 255))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            do = False

            for btn in buttons:
                if pos in btn:
                    btn.activate()
                    do = True

            if do: continue

            for i, node in enumerate(nodes):
                if interface.is_in_node(pos, (node.x, node.y)):
                    do = True
                    if event.button == 1:
                        if selected is None:
                            selected = node
                        else:
                            selected.link(node)
                            selected = None
                    elif event.button == 3:
                        if selected == node:
                            selected = None
                        node.__del__()
                        del nodes[i]
                    break

            if do: continue

            if event.button == 3:
                selected = None
            elif event.button == 1:
                nodes.append(graph.Node(node_num(), *pos))

    draw_graph()
    for btn in buttons:
        btn.draw(screen)
    pygame.display.flip()
