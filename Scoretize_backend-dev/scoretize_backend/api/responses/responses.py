# BAD REQUEST
from rest_framework.response import Response
from rest_framework import status


def bad_request(error, message, data):
    return Response({
        'error': error,
        'message': message,
        'data': data,
    }, status=status.HTTP_400_BAD_REQUEST, content_type='application/json')


def not_found(error, data):
    return Response({
        'error': error,
        'data': data,
    }, status=status.HTTP_404_NOT_FOUND, content_type='application/json')


def http_ok(data):
    return Response({
        'error': '',
        'message': 'Successful request',
        'data': data
    }, status=status.HTTP_200_OK)


def br_project_not_user():
    return Response({
        'error': 'URLs are invalid',
        'message': 'This project does not belong to this user',
        'data': '',
    }, status=status.HTTP_400_BAD_REQUEST, content_type='application/json')
