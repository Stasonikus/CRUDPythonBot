from sqlmodel import Session, select
from typing import List, Optional
from .models import Product
from .schemas import ProductCreate, ProductUpdate

def create_product(session: Session, data: ProductCreate) -> Product:
    product = Product(**data.dict())
    session.add(product)
    session.commit()
    session.refresh(product)
    return product

def get_product(session: Session, product_id: int) -> Optional[Product]:
    return session.get(Product, product_id)

def get_products(session: Session) -> List[Product]:
    return session.exec(select(Product)).all()

def update_product(session: Session, product_id: int, data: ProductUpdate) -> Optional[Product]:
    product = session.get(Product, product_id)
    if not product:
        return None
    for key, value in data.dict(exclude_unset=True).items():
        setattr(product, key, value)
    session.add(product)
    session.commit()
    session.refresh(product)
    return product

def delete_product(session: Session, product_id: int) -> bool:
    product = session.get(Product, product_id)
    if not product:
        return False
    session.delete(product)
    session.commit()
    return True
