from ...views import viewsets, APIView, action, \
    HttpResponse, get_company_id, \
    get_company_url_by_id, \
    Response, \
    IntegrityError, \
    PitchInputs, datetime, get_company_id

from azure.mgmt.datafactory import DataFactoryManagementClient
from azure.identity import ClientSecretCredential
from azure.storage.blob import BlobServiceClient


from ...models import Seo, PitchInputs

from ..website.website import website_direct_competitors_dict
from ..seo import seo_direct_competitors_dict
from ..searchAds import paid_media_direct_competitors_dict
from ..socialMedia import social_media_direct_competitors_dict
from ..globalv import global_direct_competitors_dict
from datetime import datetime
import pandas as pd
from io import BytesIO
import os 
from django.utils import timezone
from dotenv import load_dotenv, find_dotenv
from dateutil.relativedelta import relativedelta
import re
from zipfile import ZipFile
from django.utils import timezone
from dotenv import load_dotenv, find_dotenv
from dateutil.relativedelta import relativedelta
from zipfile import ZipFile

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

_ = load_dotenv(find_dotenv()) # read local .env file
slidepack_api  = os.getenv('SLIDEPACK_API_KEY') # Read SLIDEPACK_API_KEY

class PitchDeck(viewsets.ViewSet, APIView):

    @action(methods=["GET"], detail=False,
            url_path="pitch-download/(?P<pk>\\w+)")
    def pitchDownload(self, request, pk):
        """
        Not used endpoint
        """
        container_name = 'tkf-' + str(pk)
        storage_name = os.environ["STORAGE_NAME"]
        # Create a connection to the Azure Storage Account
        blob_service_client = BlobServiceClient(
        account_url=f"https://{storage_name}.blob.core.windows.net/",
        credential=os.environ["STORAGE_KEY"],
        )

        end_date = datetime.now()
        start_date = end_date - relativedelta(months=1)

        # Get the container
        container_client = blob_service_client.get_container_client(container_name)

        blob_list = list(container_client.list_blobs())

        # Filter the blobs based on the creation time within the range
        filtered_blobs = [
            blob
            for blob in blob_list
            if re.search(r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d+Z', blob.name) and
            start_date <= datetime.strptime(re.search(r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d+Z', blob.name).group(), '%Y-%m-%dT%H:%M:%S.%fZ') <= end_date and
            blob.name.endswith("/output/presentation/presentation.pptx")
        ]
        # Sort the blobs by creation time (descending order)
        sorted_blobs = sorted(filtered_blobs, key=lambda x: x.name, reverse=True)
        if sorted_blobs:
            # Get the last (most recent) blob
            blob = sorted_blobs[0]
            # Download the blob content
            blob_data = container_client.get_blob_client(blob).download_blob().readall()
            # Create the HTTP response with the blob content
            response = HttpResponse(blob_data, content_type='application/vnd.openxmlformats-officedocument.presentationml.presentation')
            # Set the appropriate content disposition header for auto-download
            response['Content-Disposition'] = 'attachment; filename="presentation.pptx"'

            return response

        # No blobs found
        return Response({'error': 'No files found'}, status=404)
    
    @action(methods=["GET"], detail=False,
            url_path="generate-pitch-etl/(?P<pk>\\d+)")
    def generate_pitch_etl(self, request, pk):
        pitchUpdate = PitchInputs.objects.filter(project_id=pk)
        pitchUpdate.update(status=2)
        pitchInputs = PitchInputs.objects.filter(
            project_id=pk).values().last()
        company_id = get_company_id(pk)
        company_url = get_company_url_by_id(company_id)
        container_name = 'tkf-' + str(pk)
        ETL_dict = {}
        ETL_dict["brief"] = pitchInputs["brief"]
        ETL_dict["project_id"] = pitchInputs["project_id"]
        ETL_dict["client_id"] = company_id
        ETL_dict["container_name"] = container_name
        ETL_dict["template_idx"] = pitchInputs["template"]
        ETL_dict["timestamp"] = pitchInputs["timestamp"]
        ETL_dict["agency_url"] = pitchInputs["agency_domain"]
        ETL_dict["client_url"] = company_url

        try:
            credentials = ClientSecretCredential(
                client_id='6abdc6fb-f717-45d3-a1e0-84e804be58ec',
                client_secret='HW68Q~.VgLY4G4UP8L4ND_Vu60cI~0YOUz_IdddV',
                tenant_id='0382225c-93b8-4c82-b547-47fd564d990c')
            adf_client = DataFactoryManagementClient(
                credentials,
                os.environ['DF_MANAGEMENT_CLIENT'])
            run_response = adf_client.pipelines.create_run(
                os.environ['RESOURCE_GROUP'],
                os.environ['PITCH_PIPELINE'],
                "Control",
                parameters={'function_dictionary': ETL_dict})
            return Response({
                'SUCCESS': 'SUCCESS'
            })
        except IntegrityError as e:
            return Response({
                e
            })
