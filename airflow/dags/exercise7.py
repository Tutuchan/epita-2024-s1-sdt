import json
from datetime import datetime

import requests

from airflow.decorators import dag, task


@dag(schedule=None, start_date=datetime(2024, 1, 1), catchup=False)
def exercise7():
    @task(multiple_outputs=True)
    def get_people():
        request = requests.get("https://swapi.dev/api/people")
        response = request.json()
        results = response["results"]

        while response["next"] is not None:
            print(f"Calling {response['next']}")
            request = requests.get(response["next"])
            response = request.json()
            results.extend(response["results"])
        return {"people": results}

    @task
    def write_users(path: str, data: dict):
        with open(path, "w") as f:
            json.dump(data["people"], f)

    people = get_people()
    write_users("./airflow/dags/data/exercise7.json", people)


exercise7()
