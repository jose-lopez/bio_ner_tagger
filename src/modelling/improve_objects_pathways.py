import os
import sys
from os import path

if __name__ == '__main__':
    """

    """

    print("\n" + f'Improving pathwaysObjects.pl ...' + "\n")

    # Setting the main folders

    for arg in sys.argv:
        print(f'{arg}')

    root = sys.argv[1]
    ruta = "minery/networks/COVID-19/COVID-19-IMMUNOLOGY"
    cwd = os.getcwd()
    on_process = root.split("/")[-2] + "/" + ruta.split("/")[-1]

    print(f'root: {root}')

    pathways_objects_path = root + '/pathwaysObjects.pl'
    biotypes_objects_path = root + '/biotypes.pl'
    expert_objects_path = "data/" + on_process + "/expert_objects.txt"
    kb_objects_path = root + '/kb_objects.txt'

    if not path.exists(pathways_objects_path):
        print(f'Not "pathwaysObjects.pl" file available. Please check.')
        exit()
    ending_facts = ["%las siguientes lineas son para evitar errores en el proceso no deben ser modificadas",
                    "enzyme('').", "protein('').", "transcription_factor('').", "receptor('').", "ligand('').",
                    "disease('')."]

    with open(pathways_objects_path, 'r', encoding="utf8") as path_objects:
        pathways_objects = [line.strip() for line in path_objects.readlines()]

    with open(biotypes_objects_path, 'r', encoding="utf8") as biotypes:
        biotypes = [line.strip() for line in biotypes.readlines()]

# Improving the pathwaysObjects.pl file.

    for biotype in biotypes:
        if biotype not in pathways_objects and biotype.startswith("ligand"):
            pathways_objects.append(biotype)

    with open(pathways_objects_path, 'w', encoding="utf8") as path_objects:

        for object_ in pathways_objects:
            if object_ not in ending_facts:
                path_objects.write(object_ + "\n")

        path_objects.write("\n")

        for fact in ending_facts:
            path_objects.write(fact + "\n")
        

# Improving the expert_objects.txt file.

    with open(expert_objects_path, 'r', encoding="utf8") as expert_objs:
        expert_objects = [line.strip() for line in expert_objs.readlines()]

    with open(kb_objects_path, 'r', encoding="utf8") as kb_objs:
        kb_objects = [line.strip() for line in kb_objs.readlines()]

    for kb_object in kb_objects:
        if kb_object not in expert_objects:
            expert_objects.append(kb_object)

    with open(expert_objects_path, 'w', encoding="utf8") as expert_objs:

        for object_ in expert_objects:
            expert_objs.write(object_ + "\n")



