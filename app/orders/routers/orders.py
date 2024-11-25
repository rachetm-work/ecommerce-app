from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.framework.database import database
from app.framework.responses import ApiSuccessResponse
from app.framework.serializers import ApiModelSerializer
from app.orders.schemas import OrderSchema, OrderCreateSchema
from app.orders.services import OrderService

router = APIRouter(prefix="/orders", tags=["orders"])


@router.post("/", response_model=OrderSchema)
def create_order(order: OrderCreateSchema, db: Session = Depends(database.get_db)):
    """Create an order ensuring products exist and stock is available."""
    order = OrderService(db_session=db).create_order(order)
    serializer = ApiModelSerializer(data_to_serialize=order)
    return ApiSuccessResponse(data=serializer)
