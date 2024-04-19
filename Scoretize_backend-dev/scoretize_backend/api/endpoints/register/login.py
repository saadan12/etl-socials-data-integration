from ...views import viewsets, APIView, AllowAny, Response, \
    authenticate, not_found, get_tokens_for_user, \
    settings, action, datetime, Users, \
    LoginSerializer


class Login(viewsets.ViewSet, APIView):
    serializer_class = LoginSerializer
    permission_classes = (AllowAny,)

    @action(methods=["POST"], detail=False, url_path="login")
    def postLogin(self, request):
        """
        Login with email and password.
        """
        data = request.data
        response = Response()
        email = data.get('email', None)
        password = data.get('password', None)
        user = authenticate(email=email, password=password)

        if user is None:
            return not_found(
                "Invalid username or password. Please, try again.", '')

        if user.is_active:
            data = get_tokens_for_user(user)

            access_token = data["access"]
            refresh_token = data["refresh"]

            response.data = {
                "message": "Successful login",
                "data": {
                    "access": access_token,
                    "refresh": refresh_token
                }
            }
            # Set refresh token as an HTTP-only cookie
            response.set_cookie(
                key="refresh_token",
                value=str(refresh_token),
                expires=settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME'],
                secure=settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
                httponly=True,
                samesite=settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE']
            )

            user = Users.objects.filter(email=email)
            user.update(last_login=datetime.datetime.now())
            return response

        else:
            return not_found(
                "Account not active. Please, try with another one.", '')
