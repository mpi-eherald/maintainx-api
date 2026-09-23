from contextlib import asynccontextmanager
from datetime import datetime, timezone
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path as p
from sqlmodel import Session, col, select
from typing import Sequence
from .db import create_db_and_tables, engine
from .sync import *

import platform
import sys


@asynccontextmanager
async def lifespan(app: FastAPI):
  app_name = app.title
  startup_time = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S %Z")
  python_version = platform.python_version()
  
  path = p("database.db")

  if path.is_file():
    print("\n‼️   Your database already exists! Upserts are not supported yet.")
    # response = input("Delete database and try again? (yes/no)\n").lower()

    # if response != "yes":
    #   print("❎  Exiting program...")
    #   sys.exit()

    print("\n🗑️   Deleting database...\n")
    # path.unlink()
    path.unlink()

  create_db_and_tables()
  sync_tables_with_mx()

  print(
      "\n=========================================\n"
      "          Application Startup            \n"
      "=========================================\n"
      f"App Name        : {app_name}\n"
      f"Startup Time    : {startup_time}\n"
      f"Python Version  : {python_version}\n"
      "=========================================\n"
  )
  yield
  shutdown_time = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S %Z")
  print(
      "\n=========================================\n"
      "          Application Shutdown           \n"
      "=========================================\n"
      f"Shutdown Time   : {shutdown_time}\n"
      "=========================================\n"
  )

app = FastAPI(title="MX Asset API", lifespan=lifespan, root_path="/api/v1")

origins = [
  "http://localhost:5173",
  "localhost:5173"
]

app.add_middleware(
  CORSMiddleware,
  allow_origins=origins,
  allow_credentials=True,
  allow_methods=["*"],
  allow_headers=["*"]
)


@app.get("/", tags=["root"], include_in_schema=False)
def read_root():
  return {"message": "Welcome to MPi's MX Asset List API."}


@app.get("/assets", tags=["assets"])
def get_assets():
  with Session(engine) as session:
    statement = select(Asset, Location).join(Location)
    response = session.exec(statement).all()
    responseArray: list[object] = []
    for asset, location in response:
      responseArray.append({
        "id": asset.id,
        "name":asset.name,
        "description": asset.description,
        "updatedAt": asset.updatedAt,
        "status": asset.status,
        "downtimeType": asset.downtimeType,
        "assetState": asset.assetState,
        "location": location.name
      })

    return responseArray
