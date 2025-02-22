import os
import sys
from os import path

if __name__ == '__main__':
    """
    This script generates the KB of events that give form to the set of pathways (in pathways.txt), inferred
    with prolog, from the general KB of events. The idea about this other reduced KB, is to offer
    a way to get the graph that represents the pathways in pathways.txt.
    """

    print("\n" + f'Printing the pathways\'s knowledge base  ...' + "\n")

    # Setting the main folders

    for arg in sys.argv:
        print(f'{arg}')

    root = sys.argv[1]
    ruta = "minery/networks/COVID-19/COVID-19-IMMUNOLOGY-DRUGS"
    cwd = os.getcwd()

    print(f'root: {root}')

    pathways_path = root + "/" + ruta + '/pathways.txt'
    kb_events_path = root + "/" + ruta + '/kb_pathways.pl'

    if not path.exists(pathways_path):
        print(f'Not "pathways.txt" file available. Please check.')
        exit()

    with open(pathways_path, 'r', encoding="utf8") as pp:
        pathways_lines = [line.strip() for line in pp.readlines()]

    # Getting the regulatory events from the "pathways.txt" file.
    pathways_events = []
    for line in pathways_lines:
        if line.startswith("'"):
            events = line.split(";")
            for event in events:
                if event not in pathways_events:
                    pathways_events.append(event)

    with open(kb_events_path, 'w', encoding="utf8") as kb_p:
        kb_p.write("base([" + "\n")
        for event in pathways_events[:-1]:
            new_event = "event(" + event + ")"
            kb_p.write(new_event + "," + "\n")
        else:
            new_event = "event(" + pathways_events[-1] + ")"
            kb_p.write(new_event + "\n")
            kb_p.write("]).")