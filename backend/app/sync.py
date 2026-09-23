from benedict import benedict
from datetime import datetime
from dotenv import load_dotenv
from sqlmodel import Session, SQLModel, create_engine, col, select

from .models import Location, Asset

import httpx
import os


load_dotenv()


sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

engine = create_engine(sqlite_url)


def create_db_and_tables():
  print("✨  Creating database and generating tables ...")
  SQLModel.metadata.create_all(engine)
  print("✅  Tables generated!")
    

def sync_tables_with_mx():
  token = os.getenv('MAINTAINX_TOKEN')
  baseUrl = 'https://api.getmaintainx.com/v1/'
  headers = {
    'Authorization': f'Bearer {token}'
  }


  with httpx.Client(base_url=baseUrl, headers=headers) as client:
    print("ℹ️   Requesting asset and location data from MaintainX API.")
    r1 = client.get('/locations')
    r2 = client.get('/assets?expand=status')

    print("ℹ️   Asset and location data received ... processing now.")

    locations = r1.json()["locations"]
    assets = r2.json()["assets"]


  print("ℹ️   Opening database session to write new rows.")
  with Session(engine) as session:

    for location in locations:
      tmp_l = Location(
          id=location["id"],
          name=location["name"]
        )
    
      session.add(tmp_l)
      session.commit()

    print("✅  Shop locations added to database!")

    for asset in assets:
      a = benedict(asset)
      al = asset["locationId"]

      updatedAt = datetime.fromisoformat(asset["updatedAt"])
      status = str(a.get("status.status", default=None)) if str else ""
      downtimeType = str(a.get("status.downtimeType", default=None)) if str else ""
      assetState = str(a.get("status.customStatus.label", default=None)) if str else ""

      statement = select(Location).where(col(Location.id) == al)
      foreignLocation = session.exec(statement).first()

      statement = select(Location.id).where(col(Location.id) == al)
      fkLocationId = session.exec(statement).first()
      
      tmp_a = Asset(
          id=asset["id"],
          name=asset["name"],
          description=asset["description"],
          updatedAt=updatedAt,
          status=status,
          downtimeType=downtimeType,
          assetState=assetState,
          location=foreignLocation,
          fkLocationId=fkLocationId
        )

      session.add(tmp_a)
      session.commit()

    print("✅  Assets added to database!")
  print("🔥  MaintainX sync complete.")


if __name__ == '__main__':
    create_db_and_tables()
    sync_tables_with_mx()
