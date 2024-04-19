from ...views import viewsets, APIView, action, \
    Users, bad_request, AccountSerializer, \
    Account, RegisterSerializer, Response, \
    IntegrityError, status, http_ok, requests, \
    os, HttpResponseRedirect, random_with_N_digits, \
    send_mail_for_registration_confirmation, \
    send_mail_for_email_verification


class UserRegister(viewsets.ViewSet, APIView):

    @action(methods=["POST"], detail=False, url_path="create-profile")
    def postRegister(self, request):
        """
        Register a new User.
        """
        request.data["email"] = request.data["email"].lower()
        request.data["name"] = request.data["name"].lower()
        request.data["surname"] = request.data["surname"].lower()

        request.data["account_name"] = request.data["account_name"].lower()

        email = Users.objects.filter(email=request.data["email"])

        if email:
            return bad_request(
                'Email already exists',
                'Email already exists',
                '')

        account_dict = {}
        account_dict["name"] = request.data["account_name"]
        account_dict["public_id"] = random_with_N_digits(5)

        account_check = Account.objects.filter(
            public_id=account_dict["public_id"])

        while account_check:
            if account_check:
                account_dict["public_id"] = random_with_N_digits(5)
            account_check = Account.objects.filter(
                public_id=account_dict["public_id"])

        account = AccountSerializer(data=account_dict)

        if not account.is_valid(raise_exception=True):
            return bad_request(
                'Account cannot be created',
                'Account cannot be created',
                '')
        else:
            account.save()

        account = Account.objects.filter(
            name=request.data["account_name"])

        account_id = account.values_list('id', flat=True).last()

        request.data["account"] = account_id
        request.data["is_active"] = False

        verify_number = random_with_N_digits(6)
        request.data["verify_number"] = verify_number

        serializer = RegisterSerializer(data=request.data)

        if not serializer.is_valid(raise_exception=True):
            return bad_request('Inputs are invalid', 'Inputs are invalid', '')

        try:
            serializer.save()
            send_mail_for_email_verification(
                to_emails=[request.data["email"]], name=request.data["name"],
                link=verify_number)
            return http_ok('Verify your email')
        except IntegrityError as e:
            return bad_request(e, e, '')

    @action(methods=["GET"], detail=False,
            url_path="active-profile")
    def activeUser(self, request):
        """
        Change is_active=1 for a User. Enable account.
        """
        email = self.request.GET.get('email')

        activation = Users.objects.filter(email=email)
        user_active = activation.values().first()["is_active"]

        if user_active:
            return Response({
                'error': '',
                'message': 'User already verified',
                'data': ''
            }, status=status.HTTP_200_OK)
        else:
            activation.update(is_active=True)
            user_name = activation.values().first()["name"]
            send_mail_for_registration_confirmation(
                to_emails=[email], name=user_name)

        return HttpResponseRedirect(
            redirect_to=os.environ["APP_URL"])

    @action(methods=["POST"], detail=False, url_path="test-profile")
    def testActiveUser(self, request):
        """
        Endpoint for testing Email Activation.
        """
        base_url = os.environ["BASE_URL"]
        url_user_activation = base_url + "/user/register/active-profile/"
        temp = {}
        email = "ruben.perez@thekeenfolks.com"
        temp["email"] = email
        requests.post(url_user_activation, json=temp)
        return Response({
            'error': '',
            'message': 'Successful request',
            'data': ''
        }, status=status.HTTP_200_OK)
