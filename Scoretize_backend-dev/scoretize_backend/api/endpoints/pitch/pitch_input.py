from ...views import viewsets, APIView, action,\
                    Response, status,\
                    IsAuthenticated, Project, Users,\
                    IntegrityError
from ...serializer.pitchInputs import PitchInputsSerializer
from ...models import PitchInputs
from django.utils import timezone

class PitchInput(viewsets.ViewSet, APIView):
    permission_classes = (IsAuthenticated,)

    @action(methods=["POST"], detail=False,
            url_path="pitch-inputs")
    def createPitchInputs(self, request):

        # Get project Id from request
        project_id = int(request.data["project_id"])

        # Initialise pitch input dictionary to place values in to api_pitchinputs table
        pitch_input_dict = {}

        # Required
        pitch_input_dict["project_id"] = project_id
        pitch_input_dict["agency_name"] = request.data["agency_name"].lower()
        pitch_input_dict["agency_domain"] = request.data["agency_domain"].lower()
        pitch_input_dict["brief"] = request.data["brief"].lower()
        pitch_input_dict["timestamp"] = timezone.now()
        pitch_input_dict["template"] = request.data["template"]

        current_pitch_data = PitchInputs.objects.filter(project_id=project_id).values().last()

        if not current_pitch_data:
            pitch_input_dict["status"] = 0
            pitchInputsSerializer = PitchInputsSerializer(data=pitch_input_dict)
            pitchInputsSerializer.is_valid(raise_exception=False)

            try:
                PitchInputs.objects.update_or_create(project_id=project_id, defaults=pitch_input_dict)
            except IntegrityError as e:
                print(e)

            return Response({
                'error': '',
                'message': 'Successful request',
                'data': '',
                'response_ETL': 'OK'
            }, status=status.HTTP_200_OK)
        
        else:
            dict_check = {
                "agency_name": False,
                "agency_domain": False,
                "brief": False,
                "timestamp": False,
                "template": False
            }

            if current_pitch_data["agency_name"] == pitch_input_dict["agency_name"]:
                dict_check["agency_name"] = True
            if current_pitch_data["agency_domain"] == pitch_input_dict["agency_domain"]:
                dict_check["agency_domain"] = True
            if current_pitch_data["brief"] == pitch_input_dict["brief"]:
                dict_check["brief"] = True
            if current_pitch_data["template"] == pitch_input_dict["template"]:
                dict_check["template"] = True
            if current_pitch_data["timestamp"].strftime("%Y-%m") == pitch_input_dict["timestamp"].strftime("%Y-%m"):
                dict_check["timestamp"] = True
            
            if all(dict_check.values()):
                return Response({
                    'error': '',
                    'message': 'Successful request',
                    'data': '',
                    'response_ETL': 'OK'
                }, status=status.HTTP_200_OK)

            else:
                pitch_input_dict["status"] = 0
                pitchInputsSerializer = PitchInputsSerializer(data=pitch_input_dict)
                pitchInputsSerializer.is_valid(raise_exception=False)

                try:
                    PitchInputs.objects.update_or_create(project_id=project_id, defaults=pitch_input_dict)
                except IntegrityError as e:
                    print(e)

                return Response({
                    'error': '',
                    'message': 'Successful request',
                    'data': '',
                    'response_ETL': 'OK'
                }, status=status.HTTP_200_OK)
    
    @action(methods=["GET"], detail=False,
            url_path="pitch-info/(?P<pk>\\d+)")
    def getPitchInputs(self, request, pk):

        # Fetched data from api_pitchinput table for a given project Id
        inputs = PitchInputs.objects.filter(project_id=pk).values().last()

        # If pitch input data does not exist for project with given project Id,
        # return inputs dictionary with relevant fields set to empty strings
        if not inputs:
            #Initialise inputs dictionary to store fetched data 
            # from api_pitchinput table for a given project Id
            inputs = {}

            # Required
            inputs["project_id"] = pk
            inputs["agency_name"] = ""
            inputs["agency_domain"] = ""
            inputs["brief"] = ""
            inputs["timestamp"] = (timezone.now()).strftime("%Y-%m-%d %H:%M:%S.%f")
            inputs["status"] = None
            inputs["template"] = 1
        
        return Response({
            'error': '',
            'message': 'Successful request',
            'data': inputs,
            'response_ETL': 'OK'
        }, status=status.HTTP_200_OK)