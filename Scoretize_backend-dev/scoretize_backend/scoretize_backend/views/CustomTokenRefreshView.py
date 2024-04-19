from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework.response import Response
from ..serializer.TokenRefreshSerializer import TokenRefreshSerializer


class CustomTokenRefreshView(TokenRefreshView):
    def post(self, request, *args, **kwargs):
        serializer = TokenRefreshSerializer(data={
            'data': super().post(request, *args, **kwargs).data
        })
        serializer.is_valid(raise_exception=True)
        return Response(serializer.validated_data)
