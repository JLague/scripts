#!/usr/bin/python3

from os.path import dirname
from pathlib import Path
import argparse
import os
import pygraphviz as pgv

def get_args():
    parser = argparse.ArgumentParser(description='Generate a graph of directories.')
    parser.add_argument('dir', nargs='?', default=os.getcwd(), type=str, help='The directory for which to generate the graph (default: "%(default)s)"')
    parser.add_argument('-c', '--color', default='#03A9F4', nargs='?', type=str, help='The color of the nodes in the graph (default: "%(default)s)"')
    parser.add_argument('-n', '--name', default="", nargs='?', type=str, help='The name of the graph (default: "%(default)s")')
    parser.add_argument('-i', '--include-files', action='store_true', help='Include files in the generated graph (default: False)')
    parser.add_argument('-o', '--output', default='graph.png', nargs='?', type=str, help='The name of the generated file (default: "%(default)s")')
    parser.add_argument('-s', '--separation', default='1.0', nargs='?', type=str, help='The separation between the layers of the graph (default: "%(default)s")')
    return parser.parse_args()

def populate_graph(root, graph, incl_files):
    for child in root.children:
        if child.type == 'file' and incl_files:
            graph.add_node(child, shape='note', label=child.name)
            graph.add_edge(root, child)
        elif child.type == 'dir':
            graph.add_node(child, label=child.name)
            graph.add_edge(root, child)
            populate_graph(child, graph, incl_files)

def save_graph(graph, color, name, filename):
    if name:
        graph.graph_attr['label'] = name
    graph.node_attr['style'] = 'filled'
    graph.node_attr['color'] = color

    graph.draw(filename, prog='dot')

def main():
    args = get_args()
    dir = Path(args.dir)
    root = File(None, dir.parent.absolute(), dir.name, 'dir')
    graph = pgv.AGraph(ranksep=args.separation, directed=True, rankdir='LR')
    graph.node_attr['shape'] = 'folder'

    graph.add_node(root, label=root.name)
    populate_graph(root, graph, args.include_files)
    save_graph(graph, args.color, args.name, args.output)

class File:
    def __init__(self, parent, path, name, type):
        self.children = []
        self.parent = parent
        self.name = name
        self.path = path
        self.type = type
        
        if self.type == 'dir':
            subpath = f'{self.path}/{self.name}'
            for file in os.scandir(subpath):
                self.children.append(File(self, subpath, file.name, 'dir' if file.is_dir() else 'file'))

if __name__=="__main__": main()
