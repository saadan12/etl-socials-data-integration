import json
import csv
import os
import requests
from datetime import datetime
import time

from .email.gateway import *

# Django Imports
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.db.utils import IntegrityError
from django.contrib.auth import authenticate, login, logout
from django.middleware import csrf
from django.conf import settings
from django.db.models import Q

# Formatters
from django.http import HttpResponse, JsonResponse, HttpRequest, QueryDict, HttpResponseRedirect
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.http import require_POST
from django.db.models.functions import Trunc, TruncDay, TruncHour, TruncMinute, TruncMonth

# Rest Framework Imports
from rest_framework.views import APIView
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import action

# Serializers:
from .serializer.register import RegisterSerializer
from .serializer.account import AccountSerializer
from .serializer.settings.userType import UserTypeSerializer
from .serializer.settings.sector import SectorSerializer
from api.serializer.profile.userProfile import UserSerializer, UpdateUserSerializer, ChangePasswordSerializer
from .serializer.company import CompanySerializer
from .serializer.project import ProjectSerializer
from .serializer.userProject import UserProjectSerializer
from .serializer.socialLinks import SocialLinksSerializer
from .serializer.user import LoginSerializer
from .serializer.globalv import GlobalSerializer
from .serializer.performance import PerformanceSerializer


from abc import abstractmethod, ABC

from .models import *
from .responses.responses import *

from .endpoints.functions.general import *
from .endpoints.functions.validate import *
from .endpoints.functions.searchData import *
from .endpoints.functions.login import *
from .endpoints.functions.builders import *

# Generic GetData function


class GetData(ABC):
    @abstractmethod
    def getData(self, request, *args, **kwargs):
        pass
