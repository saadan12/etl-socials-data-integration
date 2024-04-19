from ...views import http_ok, Users, action, bad_request, \
                    UpdateUserSerializer, \
                    ChangePasswordSerializer, Response, \
                    get_object_or_404, IsAuthenticated, \
                    UserSerializer, APIView, viewsets


class UserProfileViewSet(viewsets.ViewSet, APIView):
    model = Users
    serializer_class = UserSerializer
    queryset = UserSerializer.Meta.model.objects.filter(id=1)
    permission_classes = (IsAuthenticated,)

    # GET: abstract function to get User and if not, throw an error
    def get_object(self, id):
        return get_object_or_404(self.model, id=id)

    # GET: fecth authenticated user
    @action(methods=["GET"], detail=False, url_path="profile")
    def get_user_profile(self, request):
        """
        Get Data of User Profile.
        """
        user = self.get_object(request.user.id)
        user_serializer = self.serializer_class(user)
        return Response({"data": user_serializer.data})

    # PUT: Update user information
    @action(methods=["PUT"], detail=False, url_path="edit-profile")
    def edit_user_profile(self, request):
        """
        Change Password.
        """
        user = self.get_object(request.user.id)
        password_data = request.data['password']
        user_details = request.data['data']

        if password_data['old_password'] == '':
            user_serializer = UpdateUserSerializer(user, data=user_details)

            if user_serializer.is_valid():
                user_serializer.save()
                return http_ok(user_serializer.data)
        else:
            password_serializer = ChangePasswordSerializer(
                data=password_data, context={'user': user})
            if password_serializer.is_valid():
                user.set_password(password_data['new_password'])
                user_serializer = UpdateUserSerializer(user, data=user_details)

                if user_serializer.is_valid():
                    user_serializer.save()
                    return http_ok(user_serializer.data)

                return bad_request(
                    'An error happened when updating the user',
                    'An error happened when updating the user',
                    user_serializer.errors)
            else:

                # No user serializer if old password is incorrect
                return bad_request(
                    'An error happened when updating the user',
                    'An error happened when updating the user',
                    password_serializer.errors)

    # DELETE: change state of is_active.
    @action(methods=["DELETE"], detail=False, url_path="delete-profile")
    def delete_user_profile(self, request):
        """
        Change is_active=0 for a User. Disable account.
        """
        user = Users.objects.filter(id=request.user.id)
        user.update(is_active=False)
        return http_ok('User status changed to inactive')

    # GET: fectch all Users
    @action(methods=["GET"], detail=False, url_path="users-account")
    def get_all_users(self, request):
        """
        Get a List of ALL Users.
        """
        user_account = Users.objects.filter(
            id=request.user.id).values_list('account', flat=True).first()
        users = Users.objects.all().filter(account=user_account)
        users_serializer = self.serializer_class(users, many=True)
        return http_ok(users_serializer.data)
