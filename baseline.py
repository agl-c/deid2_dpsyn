import csv
import json
import sys
from pathlib import Path

import numpy as np
import typer
from tqdm import trange


def simulate_row(parameters, epsilon=None, sim_individual_id=None):
    """Naively create a valid row by picking random but valid values using the parameters file.
    
    Note that this function specifically serves for the certain dataset structure,  
    refer to parameters.json to get a general understanding of the description,
    which includes all the coloums'names and the descriptions of the corresponding valid value,
    like possible values given in array, minimum and maximum valus, as well as value type

    Args:
        parameters: the json file describing the structure of a valid row 
        epsilon: usual dp def
    TODO: sim_individual_id: specifically for the sprint2 dataset
    """
    row = {}
    if epsilon is not None:
        row["epsilon"] = epsilon
    for col, d in parameters["schema"].items(): #d means the detailed description of the valid value
        value = 0
        if "values" in d:
            value = np.random.choice(d["values"])
        elif "min" in d:
            if "int" in d["dtype"]:
                value = np.random.randint(d["min"], d["max"])
            else:
                value = np.random.uniform(d["min"], d["max"])
        elif col in {"HHWT", "PERWT"}:
            value = np.round(np.random.exponential(100), 1)
        elif col in {"INCTOT", "INCWAGE", "INCEARN"}:
            value = int(np.random.exponential(30_000))
        row[col] = value
    if sim_individual_id is not None:
        row["sim_individual_id"] = sim_individual_id
    return row


def main(
        parameters_file: Path, per_epsilon: int = 20_000, seed: int = 42,
):
    """Create synthetic data naively for the Sprint 2 competition.
        
    Args:
        parameters_file: path of the json file
    TODO: per_epsilon: here is hard coded
          seed: here is har coded 
    """
    np.random.seed(seed)

    with parameters_file.open("r") as fp:
        parameters = json.load(fp)

    epsilons = [run["epsilon"] for run in parameters["runs"]]
    columns = list(parameters["schema"].keys())
    headers = ["epsilon"] + columns + ["sim_individual_id"]

    # start writing the CSV with headers
    output = csv.DictWriter(sys.stdout, fieldnames=headers, dialect="unix")
    output.writeheader()

    for epsilon in epsilons:
        for sim_individual_id in trange(per_epsilon):
            row = simulate_row(parameters, epsilon=epsilon, sim_individual_id=sim_individual_id)
            output.writerow(row)


if __name__ == "__main__":
    typer.run(main)
