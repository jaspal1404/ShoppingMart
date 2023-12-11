from fastapi import APIRouter, Depends, HTTPException, Path
from pydantic import BaseModel, Field
from starlette import status
from models import Items, Cart
from typing import Annotated
from database import SessionLocal
from sqlalchemy.orm import Session

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class ItemRequest(BaseModel):
    name: str
    description: str
    brand: str
    category: str
    price: float
    quantity: int
    delivery_channel: str
    store_id: int


class CartRequest(BaseModel):
    name: str
    description: str
    brand: str
    category: str
    price: float
    quantity: int
    delivery_channel: str
    user_id: int
    item_id: int


db_dependency = Annotated[Session, Depends(get_db)]



@router.get("/get-item", status_code=status.HTTP_200_OK)
async def get_item_by_name(db: db_dependency, item_name: str, delivery_method: str, quantity: int):

    item = db.query(Items).filter(Items.name == item_name).first()
    if item is None:
        return {"response": False, "reason": "Item not found! Would you like to try again ?"}
    else:
        if item.quantity >= quantity:
            if item.delivery_method == delivery_method:
                return {"response": True, "reason": "Item available & added to cart. Would you like to add another item ?", "id": item.id}
            else:
                return {"response": False, "reason": "Item not available for " + delivery_method + ". Would you like to try a different delivery method ?"}
        else:
            if item.delivery_method == delivery_method:
                return {"response": False, "reason": "Only " + str(item.quantity) + " units of the item available. Would you like to proceed ?"}
            else:
                return {"response": False, "reason": "Only " + str(item.quantity) + " units of the item available, but not available for " + delivery_method + ". Would you like to try a different delivery method ?"}



@router.post("/add-item", status_code=status.HTTP_201_CREATED)
async def add_item(db: db_dependency, item: ItemRequest):

    item_model = db.query(Items).filter(Items.name == item.name).first()
    if item_model is None:
        item_model = Items(**item.model_dump())
        db.add(item_model)
        db.commit()
    else:
        raise HTTPException(status_code=404, detail="Item already exists")
