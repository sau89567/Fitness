from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse
from aws_services.s3 import upload_to_s3

def upload_file(request):
    if request.method == "POST" and request.FILES.get("file"):
        file = request.FILES["file"]
        s3_url = upload_to_s3(file, "your-bucket-name", file.name)
        return JsonResponse({"url": s3_url})

    return JsonResponse({"error": "No file uploaded"}, status=400)
