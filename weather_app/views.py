from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView


class WeeklyDataView(APIView):
    def post(self, request):
        return Response("Data", status=status.HTTP_200_OK)


class WeeklySummaryView(APIView):
    def post(self, request):
        return Response("Summary", status=status.HTTP_200_OK)
