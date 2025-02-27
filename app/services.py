# @cursor start
import json
import tempfile
from pathlib import Path
import os
import sys
import numpy as np
from typing import Any, Dict, List, Union

from AsiteNwells.IO.solu2json import solu2json
from AsiteNwells.IO.solu2json import soluList2json

# 添加项目根目录到系统路径
current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(current_dir)

# 添加PYD文件所在目录到Python路径
pyd_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'build', 'lib.win-amd64-cpython-311'))
sys.path.append(pyd_path)

from .models import FieldOptInput
from CLS_OptField import OptField, NumpyEncoder

def safe_convert(obj: Any) -> Any:
    """安全地转换各种类型的数据为JSON可序列化的格式"""
    if isinstance(obj, (np.integer, np.int64, np.int32)):
        return int(obj)
    elif isinstance(obj, (np.float, np.float64, np.float32)):
        if np.isnan(obj) or np.isinf(obj):
            return None
        return float(obj)
    elif isinstance(obj, np.ndarray):
        if obj.ndim > 2:  # 如果是3维或更高维数组
            # 只返回非空值的索引和对应的值
            non_null_indices = np.argwhere(~np.isnan(obj) & ~np.isinf(obj))
            values = obj[tuple(non_null_indices.T)]
            return {
                "indices": non_null_indices.tolist(),
                "values": values.tolist()
            }
        return [safe_convert(x) for x in obj.tolist()]
    elif isinstance(obj, (list, tuple)):
        return [safe_convert(x) for x in obj]
    elif isinstance(obj, dict):
        return {k: safe_convert(v) for k, v in obj.items()}
    elif isinstance(obj, (str, int, float, bool, type(None))):
        return obj
    else:
        try:
            return str(obj)
        except:
            return None

def compress_grid_data(x: np.ndarray, y: np.ndarray) -> Dict:
    """压缩网格数据"""
    if x.ndim == 2 and y.ndim == 2:
        # 提取唯一的x和y值
        x_unique = np.unique(x[0, :])
        y_unique = np.unique(y[:, 0])
        return {
            "x_range": [float(x_unique[0]), float(x_unique[-1])],
            "y_range": [float(y_unique[0]), float(y_unique[-1])],
            "x_step": float(x_unique[1] - x_unique[0]),
            "y_step": float(y_unique[1] - y_unique[0]),
            "nx": len(x_unique),
            "ny": len(y_unique)
        }
    return {"x": safe_convert(x), "y": safe_convert(y)}

def process_field_optimization(input_data: dict):
    """处理优化计算请求"""
    try:
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
            
            # 执行优化计算
            myfield.get_contours()
            
            # 获取等值线数据
            grid_info = compress_grid_data(myfield.X, myfield.Y)
            contours_data = {
                "grid": grid_info,
                "values": safe_convert(myfield.Contour_ValM),
                "indices": safe_convert(myfield.Contour_IndM)
            }
            
            # 获取单站点优化结果
            myfield.get_1site()

            soluListJson = soluList2json(myfield.soluList_1site, myfield.WellNo[myfield.indices_1site], "heiss_traj_.json")
            soluListJson_obj = [json.loads(x) for x in soluListJson]

            # print("soluList_1site:", myfield.soluList_1site)
            
            
            # 收集所有需要的数据
            result_data = {
                "status": "success",
                "data": {
                    "contours": contours_data,
                    "site_optimization": {
                        "indices_1site": myfield.indices_1site,
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
