# built-in imports
# standard library imports
import pickle
from collections import defaultdict

import requests

# external imports
from flask import current_app

# internal imports
from codeapp import db
from codeapp.models import Jobs


def get_data_list() -> list[Jobs]:
    """
    Function responsible for downloading the dataset from the source, translating it
    into a list of Python objects, and saving it to a Redis list.
    """

    ##### check if dataset already exists, and if so, return the existing dataset  #####
    if db.exists("dataset_list") > 0:  # checks if the `dataset` key already exists
        current_app.logger.info("Dataset already downloaded.")
        dataset_stored: list[Jobs] = []  # empty list to be returned
        raw_dataset: list[bytes] = db.lrange("dataset_list", 0, -1)  # get list from DB
        for item in raw_dataset:
            dataset_stored.append(pickle.loads(item))  # load item from DB
        return dataset_stored

    ################# dataset has not been downloaded, downloading now #################
    current_app.logger.info("Downloading dataset.")
    respons = requests.get(
        "https://onu1.s2.chalmers.se/datasets/AI_ML_jobs.json", timeout=5
    )
    data_dict: list[dict[str, int]] = respons.json()
    current_app.logger.info(respons)
    ########################## saving dataset to the database ##########################
    dataset_base: list[Jobs] = []  # list to store the items
    # for each item in the dataset...
    for row in data_dict:
        # create a new object
        ai_jobs = Jobs(
            title=str(["Title"]),  
            company=str(row["Company"]),
            location=str(row["Location"]),
            position_type=str(row["Type of Positions"]),
            job_description=str(row["Job Description"]),
            salary=row["Salary"],
            identified_skills=["Identified_Skills"],
        )
        # push object to the database list
        db.rpush("dataset_list", pickle.dumps(ai_jobs))
        dataset_base.append(ai_jobs)  # append to the list

    return dataset_base


def calculate_statistics(dataset: list[Jobs]) -> dict[int, int]:
    counter: dict[int, int] = defaultdict(int)
    for item in dataset:
            counter[item.salary] += 1
    return counter


def prepare_figure(input_figure: str) -> str:
    """
    Method that removes limits to the width and height of the figure. This method must
    not be changed by the students.
    """
    output_figure = input_figure.replace('height="345.6pt"', "").replace(
        'width="460.8pt"', 'width="100%"'
    )
    return output_figure