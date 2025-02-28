# @cursor start
from fastapi import APIRouter, HTTPException
from .models import FieldOptInput
from .services import process_field_optimization

router = APIRouter()

@router.post("/optimize")
async def optimize_field_layout(input_data: FieldOptInput):
    """
    接收优化参数并执行优化计算
    """
    try:
        # 将Pydantic模型转换为字典
        input_dict = input_data.FIELDOPT_INPUT_BLOCK
        # 执行优化计算
        result = process_field_optimization(input_dict)
        return result
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail={
                "status": "error",
                "message": f"error: {str(e)}",
                "error_type": type(e).__name__
            }
        )

@router.get("/")
async def root():
    """
    API root
    """
    return {"message": "welcome to OptLayout API"}
# @cursor end
