from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
import requests
import json


def index(request):
    return render(request, "index.html")


class NLPView(GenericAPIView):
    """Rasa Chatbot POST API view"""
    def post(self, request):
        data = request.data
        r = requests.post('http://localhost:5005/webhooks/rest/webhook', json=data)
        res = json.loads(r.text)
        print(res)
        return Response(res)
