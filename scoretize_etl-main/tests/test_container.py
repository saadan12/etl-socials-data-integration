from container import main
import os


def test_container():
    os.environ['AZURE_STORAGE_CONNECTION_STRING'] = "DefaultEndpointsProtocol=https;AccountName=scoretizedev;AccountKey=Z4/xuieLf4ldeOnz1rVOZ8IbaN6rHeP3obFAN65nmewbtA1ml1LNpVo9k5tFVLvQfKdPR+DRext0gnETsPVAFA==;EndpointSuffix=core.windows.net"
    container_name = "config-files"
    result = main(container_name)
    assert result == "Container already exists"
