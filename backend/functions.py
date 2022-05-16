import json

from fastapi import HTTPException
from fastapi import status


def read_data(file):
    with open(f"{file}.json", "r+", encoding="utf-8") as f:
        return json.loads(f.read())  # Convert a file to a json


def overwrite_data(file, result):
    with open(f"{file}.json", "w", encoding="utf-8") as f:
        f.seek(0)  # move to the beginning of the file
        f.write(json.dumps(result))  # converting a json to a list


def show_data(file, id, info):
    results = read_data(file)
    id = str(id)
    for data in results:
        if data[f"{info}_id"] == id:
            return data
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"¡This {info} doesn't exist!"
        )


def delete_data(file, id, info):
    results = read_data(file)
    id = str(id)
    for data in results:
        if data[f"{info}_id"] == id:
            results.remove(data)
            overwrite_data(file, results)
            return data
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"¡This {info} doesn't exist!"
        )
