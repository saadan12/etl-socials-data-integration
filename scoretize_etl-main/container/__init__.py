# This function is not intended to be invoked directly. Instead it will be
# triggered by an orchestrator function.
# Before running this sample, please:
# - create a Durable orchestration function
# - create a Durable HTTP starter function
# - add azure-functions-durable to requirements.txt
# - run pip install -r requirements.txt

from shared_code.storage_functions import AzureStorage
import logging
import azure.functions as func


def main(req: func.HttpRequest) -> func.HttpResponse:
    """Check if container name passed as argument exists on the corresponding Azure Storage account

    Input:
    ------
    name = string
    """
    input_config = req.get_json()
    azs = AzureStorage(input_config["container_name"])
    exist = azs.container_exists()

    if exist:
        logging.info("Container already exists")
        return func.HttpResponse("Container already exists")
    else:
        azs.create_container()

    logging.info("Container created")
    return func.HttpResponse("Container created")
