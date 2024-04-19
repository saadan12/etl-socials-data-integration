import requests
import logging
from shared_code.settings import ENDPOINT
import azure.functions as func


def main(req: func.HttpRequest) -> func.HttpResponse:
    input_config = req.get_json()
    print(input_config)
    if input_config[1] == "fail":
        url = (
            str(ENDPOINT)
            + f"/project/project/failed-social-project-update/{input_config[0]['project_id']}/"
        )
    else:
        url = (
            str(ENDPOINT)
            + f"/project/project/success-social-project-update/{input_config[0]['project_id']}/"
        )
    logging.info(url)
    response = requests.put(url)
    logging.info(response)

    return func.HttpResponse("ok")
