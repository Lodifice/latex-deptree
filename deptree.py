import re
import sys

def run(graph_stream):
    nodes = {}
    edges = {}
    for line in graph_stream:
        match = re.match("^N (\S+) (\S+)$", line)
        if match:
            label, environment = match.groups()
            nodes[label] = environment
            continue
        match = re.match("^E (\S+) (\S+)$", line)
        if match:
            start, end = match.groups()
            edges.setdefault(start, set()).add(end)
            continue
        sys.stderr.write("warning: ignoring unrecognized line: " + line)
    print("digraph dependencies {")
    nodes = { label: environment
              for label, environment in nodes.items()
              if label in edges.keys() or any(label in v for v in edges.values()) }
    edges = { start: set(end for end in ends if end in nodes and end != start)
              for start, ends in edges.items()
              if start in nodes }
    for label, environment in nodes.items():
        print(graphviz_node(label, environment))
    for start, ends in edges.items():
        for end in ends:
            print(graphviz_edge(start, end))
    print("}")

def graphviz_node(key, description):
    return "{pkey} [label=\"{description} {key}\"]".format(
            pkey=printable(key),
            description=description,
            key=key)

def graphviz_edge(start, end):
    return "{start} -> {end} [];".format(
            start=printable(start),
            end=printable(end))

def printable(identifier):
    return re.sub("\W", "_", identifier, flags=re.ASCII)

if __name__ == "__main__":
    run(sys.stdin)
