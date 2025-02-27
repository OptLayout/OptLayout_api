# @cursor start
from pydantic import BaseModel, Field
from typing import List, Optional, Union, Dict, Any

class WellParameter(BaseModel):
    DESCRIPTION: str
    UNIT: str
    VALUE: Union[float, List[float], List[List[float]], List[int], List[str], str]

class FieldOptInputBlock(BaseModel):
    n: WellParameter
    WellNo: WellParameter
    PCM: WellParameter
    VCM: WellParameter
    PKzM: WellParameter
    VKM: WellParameter
    DLSM: WellParameter
    rM: WellParameter
    MD_intervalM: WellParameter
    XRange: WellParameter
    YRange: WellParameter
    resolution: WellParameter
    cst_radiusM: WellParameter

class FieldOptInput(BaseModel):
    FIELDOPT_INPUT_BLOCK: Dict[str, Any] = Field(..., alias="FIELDOPT INPUT BLOCK")

    class Config:
        populate_by_name = True
        json_encoders = {
            # 自定义编码器，处理特殊类型
            'numpy.ndarray': lambda x: x.tolist()
        }
# @cursor end
