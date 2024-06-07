from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from celery.result import AsyncResult
from .tasks import scrape_coin_data
import uuid

class StartScraping(APIView):
    def post(self, request):
        coins = request.data.get("coins", [])
        job_id = str(uuid.uuid4())
        for coin in coins:
            scrape_coin_data.apply_async((coin,), task_id=f"{job_id}_{coin}")
        return Response({"job_id": job_id}, status=status.HTTP_202_ACCEPTED)

class ScrapingStatus(APIView):
    def get(self, request, job_id):
        tasks = []
        for coin in ["DUKO", "NOT", "GORILLA"]:  # This should be dynamic based on actual coins
            result = AsyncResult(f"{job_id}_{coin}")
            if result.ready():
                tasks.append({"coin": coin, "output": result.result})
            else:
                tasks.append({"coin": coin, "output": "Processing"})
        return Response({"job_id": job_id, "tasks": tasks}, status=status.HTTP_200_OK)
