# @cursor start
import json
import tempfile
from pathlib import Path
import os
import sys
import numpy as np
from typing import Any, Dict, List, Union
import math

# 添加项目根目录到系统路径
current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if current_dir not in sys.path:
    sys.path.append(current_dir)

# 添加PYD文件所在目录到Python路径
pyd_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'build', 'lib.win-amd64-cpython-311'))
if pyd_path not in sys.path:
    sys.path.insert(0, pyd_path)

from AsiteNwells.IO.solu2json import solu2json
from AsiteNwells.IO.solu2json import soluList2json

from .models import FieldOptInput
from CLS_OptField import OptField, NumpyEncoder

def safe_convert(obj: Any) -> Any:
    """安全地转换各种类型的数据为JSON可序列化的格式"""
    try:
        if isinstance(obj, (np.integer, np.int64, np.int32)):
            return int(obj)
        elif isinstance(obj, (np.float64, np.float32)):
            # 先转换为 Python float，再检查是否为 nan 或 inf
            float_val = float(obj)
            if math.isnan(float_val) or math.isinf(float_val):
                return None
            return float_val
        elif isinstance(obj, np.ndarray):
            # 先将数组转换为 Python 列表
            array_list = obj.tolist()
            if isinstance(array_list, list):
                return [safe_convert(item) for item in array_list]
            return array_list
        elif isinstance(obj, (list, tuple)):
            return [safe_convert(item) for item in obj]
        elif isinstance(obj, dict):
            return {str(k): safe_convert(v) for k, v in obj.items()}
        return obj
    except Exception as e:
        print(f"Warning: Error converting object {type(obj)}: {str(e)}")
        return None

def compress_grid_data(x: np.ndarray, y: np.ndarray) -> Dict:
    """压缩网格数据"""
    try:
        if x.ndim == 2 and y.ndim == 2:
            # 提取唯一的x和y值，并转换为Python列表
            x_unique = np.unique(x[0, :]).tolist()
            y_unique = np.unique(y[:, 0]).tolist()
            
            # 进行安全的浮点数转换
            x_start = float(x_unique[0])
            x_end = float(x_unique[-1])
            y_start = float(y_unique[0])
            y_end = float(y_unique[-1])
            x_step = float(x_unique[1] - x_unique[0])
            y_step = float(y_unique[1] - y_unique[0])
            
            return {
                "x_range": [x_start, x_end],
                "y_range": [y_start, y_end],
                "x_step": x_step,
                "y_step": y_step,
                "nx": len(x_unique),
                "ny": len(y_unique)
            }
        
        # 如果不是2D数组，转换为普通列表
        return {
            "x": x.tolist() if isinstance(x, np.ndarray) else x,
            "y": y.tolist() if isinstance(y, np.ndarray) else y
        }
    except Exception as e:
        print(f"Warning: Error in compress_grid_data: {str(e)}")
        # 返回原始数据的字符串表示
        return {
            "x": str(x),
            "y": str(y)
        }

def process_field_optimization(input_data: dict):
    """处理优化计算请求"""
    try:
        print("input_data:", input_data)
        # 构建输入数据格式
        json_data = {
            "FIELDOPT INPUT BLOCK": input_data
        }
        
        # 创建临时JSON文件
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as tmp:
            json.dump(json_data, tmp, indent=4)
            tmp_path = tmp.name
        
        try:
            # 初始化OptField实例
            myfield = OptField(tmp_path)
            
            # 获取单站点优化结果
            myfield.get_1site()
            # print("soluListJson:", soluListJson)
            # return soluListJson
            

            soluListJson = soluList2json(myfield.soluList_1site, myfield.WellNo[myfield.indices_1site], "heiss_traj_.json")
            soluListJson_obj = [json.loads(x) for x in soluListJson]
            
            # 收集所有需要的数据
            result_data = {
                "status": "success",
                "data": {
                    "site_optimization": {
                        "indices_1site": myfield.indices_1site.tolist() if isinstance(myfield.indices_1site, np.ndarray) else myfield.indices_1site,
                        "soluList_1site": myfield.soluList_1site,
                        "optimal_site": getattr(myfield, 'optimal_site', None),
                        "soluListJson": soluListJson,
                        "soluListJson_obj": soluListJson_obj
                    },
                },
                "message": "优化计算完成"
            }
            
            # 安全转换所有数据
            cleaned_result = safe_convert(result_data)
            
            return cleaned_result
            
        except Exception as e:
            return {
                "status": "error",
                "message": f"优化计算错误: {str(e)}"
            }
        finally:
            # 清理临时文件
            if os.path.exists(tmp_path):
                Path(tmp_path).unlink()
    except Exception as e:
        return {
            "status": "error",
            "message": f"服务器错误: {str(e)}"
        }
# @cursor end
