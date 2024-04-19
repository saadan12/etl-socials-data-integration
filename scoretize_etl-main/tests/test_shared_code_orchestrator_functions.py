import azure.durable_functions as df
import datetime
from azure.durable_functions.models.history import HistoryEventType
import json

from shared_code.orchestrator_functions import configure_dictionary


def test_configure_dictionary():
    """
    Test the function that configures the dictionary
    Creates a fake input dictionary, a fake durable functions context and checks if the output dictionary is correct
    """

    x = datetime.datetime.now()
    input_dict = {
        "client_id": 78,
        "project_id": 34,
        "sector_id": 33,
        "site_list": [
            "https://www.walmart.com",
            "https://www.ebay.com",
            "https://www.mangakakalot.com",
            "https://www.etsy.com",
            "https://www.aliexpress.com",
            "https://www.amazon.de",
        ],
        "company_id": [75, 76, 77, 78, 79, 80],
    }

    # Creates a Durable Functions context with the current timestamp and inserts the fake input dictionary into that context
    context = df.DurableOrchestrationContext(
        history=[
            {
                "EventType": HistoryEventType.ORCHESTRATOR_STARTED,
                "EventId": "Any",
                "IsPlayed": "Any",
                "Timestamp": str(x),
            }
        ],
        instanceId="1",
        isReplaying=False,
        parentInstanceId=None,
        input=input_dict,
    )
    context._input = json.dumps(input_dict)

    # Calls the function that configures the dictionary
    configured_dict = configure_dictionary(context)
    assert configured_dict["client_id"] == 78
    assert configured_dict["project_id"] == 34
    assert configured_dict["sector_id"] == 33
    assert configured_dict["site_list"] == [
        "https://www.walmart.com",
        "https://www.ebay.com",
        "https://www.mangakakalot.com",
        "https://www.etsy.com",
        "https://www.aliexpress.com",
        "https://www.amazon.de",
    ]
    assert configured_dict["company_id"] == [75, 76, 77, 78, 79, 80]
    assert configured_dict["connection_name"] == "tkf-78"
    assert configured_dict["timestamp"] == context.current_utc_datetime.strftime(
        "%Y-%m-%d"
    )
    assert configured_dict["uuid"] == str(context.new_guid)
