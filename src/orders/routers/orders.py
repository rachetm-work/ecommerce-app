from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.framework.database import database
from src.framework.responses import ApiSuccessResponse
from src.framework.serializers import ApiModelSerializer
from src.orders.schemas import OrderSchema, OrderCreateSchema
from src.orders.services import OrderService

router = APIRouter(prefix="/orders", tags=["orders"])


@router.post("/", response_model=OrderSchema)
def create_order(order: OrderCreateSchema, db: Session = Depends(database.get_db)):
    """Create an order ensuring products exist and stock is available."""
    order = OrderService(db_session=db).create_order(order)
    serializer = ApiModelSerializer(data_to_serialize=order)
    return ApiSuccessResponse(data=serializer)
