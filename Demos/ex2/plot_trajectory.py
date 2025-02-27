# @cursor start
import json
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def load_trajectory_data(file_path):
    """加载井眼轨迹数据"""
    with open(file_path, 'r') as f:
        data = json.load(f)
    return data['CURVES']

def plot_3d_trajectory(data):
    """绘制3D井眼轨迹图"""
    fig = plt.figure(figsize=(12, 8))
    ax = fig.add_subplot(111, projection='3d')
    
    # 绘制3D轨迹
    ax.plot(data['EAST'], data['NORTH'], -np.array(data['TVD']), 
            label='Well Trajectory', linewidth=2)
    
    # 设置轴标签
    ax.set_xlabel('East (m)')
    ax.set_ylabel('North (m)')
    ax.set_zlabel('TVD (m)')
    
    # 设置标题
    ax.set_title('3D Well Trajectory')
    
    # 添加图例
    ax.legend()
    
    # 调整视角
    ax.view_init(elev=20, azim=45)
    
    # 设置坐标轴比例相等
    ax.set_box_aspect([1,1,1])
    
    plt.show()

def plot_2d_projections(data):
    """绘制2D投影图"""
    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(15, 5))
    
    # 垂直剖面图 (TVD vs EAST)
    ax1.plot(data['EAST'], -np.array(data['TVD']))
    ax1.set_xlabel('East (m)')
    ax1.set_ylabel('TVD (m)')
    ax1.set_title('Vertical Section (E-W)')
    ax1.grid(True)
    
    # 垂直剖面图 (TVD vs NORTH)
    ax2.plot(data['NORTH'], -np.array(data['TVD']))
    ax2.set_xlabel('North (m)')
    ax2.set_ylabel('TVD (m)')
    ax2.set_title('Vertical Section (N-S)')
    ax2.grid(True)
    
    # 平面图 (EAST vs NORTH)
    ax3.plot(data['EAST'], data['NORTH'])
    ax3.set_xlabel('East (m)')
    ax3.set_ylabel('North (m)')
    ax3.set_title('Plan View')
    ax3.grid(True)
    
    plt.tight_layout()
    plt.show()

if __name__ == '__main__':
    # 加载数据
    file_path = 'heiss_traj_1.0.json'
    data = load_trajectory_data(file_path)
    
    # 绘制3D轨迹图
    plot_3d_trajectory(data)
    
    # 绘制2D投影图
    plot_2d_projections(data)
# @cursor end
