from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.framework.database import database
from src.framework.responses import ApiSuccessResponse
from src.framework.serializers import ApiModelSerializer
from src.products.schemas import ProductCreateSchema
from src.products.services import ProductService

router = APIRouter(prefix="/products", tags=["products"])


@router.get("/")
def get_all_products(db: Session = Depends(database.get_db)) -> ApiSuccessResponse:
    products = ProductService(db_session=db).get_all_products()
    serializer = ApiModelSerializer(data_to_serialize=products)
    return ApiSuccessResponse(data=serializer)


@router.post("/")
def create_product(product: ProductCreateSchema, db: Session = Depends(database.get_db)) -> ApiSuccessResponse:
    product = ProductService(db_session=db).create_product(product)
    serializer = ApiModelSerializer(data_to_serialize=product)
    return ApiSuccessResponse(data=serializer)
