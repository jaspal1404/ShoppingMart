from fastapi import APIRouter, Depends, HTTPException, Path
from pydantic import BaseModel, Field
from starlette import status
from models import Items, Cart, Users
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
    delivery_method: str
    store_id: int


class CartRequest(BaseModel):
    name: str
    description: str
    brand: str
    category: str
    price: float
    quantity: int
    delivery_method: str
    user_id: int
    item_id: int


db_dependency = Annotated[Session, Depends(get_db)]


@router.get("/get-all-items", status_code=status.HTTP_200_OK)
async def get_all_items(db: db_dependency):

    return db.query(Items).all()



@router.get("/get-item", status_code=status.HTTP_200_OK)
async def get_item_by_name(db: db_dependency, item_name: str, delivery_method: str, quantity: int):

    item = db.query(Items).filter(Items.name == item_name).first()
    if item is None:
        return {"response": False, "reason": "Item not found! Would you like to try again ?"}
    else:
        if item.quantity >= quantity:
            if item.delivery_method == delivery_method:
                return {"response": True, "reason": "Item available & added to cart. Would you like to add another item ?"}
            else:
                return {"response": False, "reason": "Item not available for " + delivery_method + ". Would you like to try a different delivery method ?"}
        else:
            if item.delivery_method == delivery_method:
                return {"response": False, "reason": "Only " + str(item.quantity) + " units of the item available. Would you like to proceed ?"}
            else:
                return {"response": False, "reason": "Only " + str(item.quantity) + " units of the item available, but not available for " + delivery_method + ". Would you like to try a different delivery method ?"}



@router.post("/add-item", status_code=status.HTTP_201_CREATED)
async def add_item(db: db_dependency, item: ItemRequest):

    item_model = db.query(Items).filter(Items.name == item.name).filter(Items.brand == item.brand).filter(Items.delivery_method == item.delivery_method).first()
    if item_model is None:
        item_model = Items(**item.model_dump())
        db.add(item_model)
        db.commit()
    else:
        raise HTTPException(status_code=404, detail="Item already exists")



@router.post("/add-to-cart", status_code=status.HTTP_201_CREATED)
async def add_to_cart(db: db_dependency, item_name: str, delivery_method: str, quantity: int, brand: str = ""):

    if brand != "":
        item = db.query(Items).filter(Items.name == item_name).filter(Items.delivery_method == delivery_method)\
            .filter(Items.brand == brand).first()
    else:
        item = db.query(Items).filter(Items.name == item_name).filter(Items.delivery_method == delivery_method).first()

    cart_item = Cart()
    cart_item.name = item.name
    cart_item.description = item.description
    cart_item.brand = item.brand
    cart_item.category = item.category
    cart_item.quantity = quantity
    cart_item.price = item.price
    cart_item.item_id = item.id
    cart_item.user_id = 1

    db.add(cart_item)
    db.commit()



@router.get("/get-cart-items", status_code=status.HTTP_200_OK)
async def get_cart_items(db: db_dependency):

    return db.query(Cart).all()
