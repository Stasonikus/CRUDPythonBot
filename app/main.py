from fastapi import FastAPI, HTTPException
from sqlmodel import Session
from .database import engine, init_db
from . import crud
from .models import Product
from .schemas import ProductCreate, ProductUpdate

app = FastAPI(title="Products API")

@app.on_event("startup")
def on_startup():
    init_db()

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/products", response_model=Product)
def create_product(product: ProductCreate):
    with Session(engine) as session:
        return crud.create_product(session, product)

@app.get("/products", response_model=list[Product])
def list_products():
    with Session(engine) as session:
        return crud.get_products(session)

@app.get("/products/{product_id}", response_model=Product)
def read_product(product_id: int):
    with Session(engine) as session:
        product = crud.get_product(session, product_id)
        if not product:
            raise HTTPException(status_code=404, detail="Not found")
        return product

@app.put("/products/{product_id}", response_model=Product)
def update_product(product_id: int, product: ProductUpdate):
    with Session(engine) as session:
        updated = crud.update_product(session, product_id, product)
        if not updated:
            raise HTTPException(status_code=404, detail="Not found")
        return updated

@app.delete("/products/{product_id}")
def delete_product(product_id: int):
    with Session(engine) as session:
        ok = crud.delete_product(session, product_id)
        if not ok:
            raise HTTPException(status_code=404, detail="Not found")
        return {"ok": True}
