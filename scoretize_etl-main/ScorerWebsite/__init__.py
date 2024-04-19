# This function is not intended to be invoked directly. Instead it will be
# triggered by an orchestrator function.
# Before running this sample, please:
# - create a Durable orchestration function
# - create a Durable HTTP starter function
# - add azure-functions-durable to requirements.txt
# - run pip install -r requirements.txt

import logging
from ScorerWebsite.website_scorer import website_scorer
import azure.functions as func


def main(req: func.HttpRequest) -> func.HttpResponse:
    input_config = req.get_json()

    logging.debug(
        f"Scorer called with input {input_config} of type {type(input_config)}"
    )
    website_scorer(input_config)

    return func.HttpResponse("Score created")
