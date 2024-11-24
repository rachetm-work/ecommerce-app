from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.framework.database import database
from app.framework.responses import ApiSuccessResponse
from app.framework.serializers import ApiModelSerializer
from app.products.schemas import ProductCreateSchema
from app.products.services import ProductService

router = APIRouter(prefix="/products", tags=["products"])


@router.get("/")
def get_all_products(db: Session = Depends(database.get_db)):
    products = ProductService(db_session=db).get_all_products()
    serializer = ApiModelSerializer(data_to_serialize=products)
    return ApiSuccessResponse(data=serializer)


@router.post("/")
def create_product(product: ProductCreateSchema, db: Session = Depends(database.get_db)):
    product = ProductService(db_session=db).create_product(product)
    serializer = ApiModelSerializer(data_to_serialize=product)
    return ApiSuccessResponse(data=serializer)
