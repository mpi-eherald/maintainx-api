import os
import httpx
from dotenv import load_dotenv
from fastapi import FastAPI

load_dotenv()

token = os.getenv('MAINTAINX_TOKEN')
baseUrl = 'https://api.getmaintainx.com/v1/assets?expand=status'
headers = {
  'Authorization': f'Bearer {token}' 
}

r = httpx.get(baseUrl, headers=headers)

assets = r.json()["assets"]

assetStatus = []
for asset in assets:
  assetStatus.append({asset["name"]: asset["status"]["status"]})

app = FastAPI()

@app.get("/")
def read_root():
  return assetStatus