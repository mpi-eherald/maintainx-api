from datetime import datetime
from sqlmodel import Field, Relationship, SQLModel

class Location(SQLModel, table=True):
  id: int | None = Field(default=None, primary_key=True)
  name: str

  assets: list["Asset"] = Relationship(back_populates="location")


class Asset(SQLModel, table=True):
  id: int | None = Field(default=None, primary_key=True)
  name: str
  description: str | None
  updatedAt: datetime
  status: str | None # status/status
  downtimeType: str | None # status/downtimeType
  assetState: str | None # status/customStatus/label

  fkLocationId: int | None = Field(default=None, foreign_key="location.id")
  location: Location | None = Relationship(back_populates="assets")