#!/bin/bash
set -x

app_name=$1

capitalized_app="$(tr '[:lower:]' '[:upper:]' <<< "${app_name:0:1}")${app_name:1}"


django-admin startapp $app_name

rm $app_name/admin.py $app_name/models.py $app_name/tests.py $app_name/views.py



mkdir $app_name/admin
touch $app_name/admin/__init__.py
touch $app_name/admin/${app_name}_admin.py
echo "from django.contrib import admin" > $app_name/admin/${app_name}_admin.py

mkdir $app_name/models
touch $app_name/models/__init__.py
touch $app_name/models/${app_name}_models.py
echo "from django.db import models" > $app_name/models/${app_name}_models.py

mkdir $app_name/views
touch $app_name/views/__init__.py
touch $app_name/views/${app_name}_views.py
echo "from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated" > $app_name/views/${app_name}_views.py

mkdir $app_name/querysets
touch $app_name/querysets/__init__.py
touch $app_name/querysets/${app_name}_queryset.py
echo "class ${capitalized_app}Queryset:
  pass" > $app_name/querysets/${app_name}_queryset.py

mkdir $app_name/utilities
touch $app_name/utilities/__init__.py

mkdir $app_name/caches
touch $app_name/caches/__init__.py
touch  $app_name/caches/${app_name}_cache.py
echo "from django.core.cache import cache" > $app_name/caches/${app_name}_cache.py

mkdir $app_name/tests
touch $app_name/tests/__init__.py

mkdir $app_name/serializers
touch $app_name/serializers/__init__.py
touch $app_name/serializers/${app_name}_serializers.py
echo "from rest_framework import serializers" > $app_name/serializers/${app_name}_serializers.py


