# This function is not intended to be invoked directly. Instead it will be
# triggered by an orchestrator function.
# Before running this sample, please:
# - create a Durable orchestration function
# - create a Durable HTTP starter function
# - add azure-functions-durable to requirements.txt
# - run pip install -r requirements.txt

import logging
import azure.functions as func
import json


def main(req: func.HttpRequest) -> func.HttpResponse:
    input_config = req.get_json()

    tasks_list = []

    last_item = input_config["site_list"][-1]
    list_size = len(input_config["site_list"]) - 1

    for index, value in enumerate(input_config["site_list"]):
        logging.info(
            f"DEBUG HERE {index} and value {value}  last item {last_item} list size {list_size}"
        )
        input_dict_copy = input_config.copy()
        input_dict_copy["site_list"] = [value]

        if index == list_size:
            input_dict_copy["last_call"] = True
        else:
            input_dict_copy["last_call"] = False

        input_dict_copy["n_sites"] = len(input_config["site_list"])
        logging.info(f"Dict to add to tasks list {input_dict_copy}")
        tasks_list.append(input_dict_copy)

    logging.info(f"Tasks for pagespeed: {tasks_list}")
    return func.HttpResponse(json.dumps(tasks_list))
