from ...views import viewsets, APIView, action, \
    UserTypeSerializer, bad_request, \
    http_ok, IntegrityError, HttpResponse


class UserTypeRegister(viewsets.ViewSet, APIView):
    # permission_classes = (IsAuthenticated,)

    @action(methods=["POST"], detail=False, url_path="user-type")
    def postUserType(self, request):
        """
        Insert a new User Type on DB.
        """
        request.data["name"] = request.data["name"].lower()
        request.data["description"] = request.data["description"].lower()

        user_type = UserTypeSerializer(data=request.data)

        if not user_type.is_valid(raise_exception=True):
            return bad_request('Inputs are invalid', 'Inputs are invalid', '')
        try:
            user_type.save()
            return http_ok('User Type registered successfully')
        except IntegrityError as e:
            return HttpResponse(e)
