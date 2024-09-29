import numpy as np
from typing import List, Tuple, Union
import plotly.graph_objects as go

def visualizeMapWithStartGoal(data: Union[List[Tuple[int, int, int]], np.ndarray],
                              startNode: Tuple[int, int, int] = None,
                              targetNode: Tuple[int, int, int] = None,
                              path: List[np.ndarray] = None):
    if isinstance(data, np.ndarray):
        occupied_voxel_coords = np.argwhere(data != 0)  
    elif isinstance(data, list):
        occupied_voxel_coords = np.array(data)  
    else:
        raise ValueError("Unsupported data type. Provide either a list of coordinates or a NumPy array.")

    x_coords = occupied_voxel_coords[:, 0]
    y_coords = occupied_voxel_coords[:, 1]
    z_coords = occupied_voxel_coords[:, 2]

    fig = go.Figure(data=[
        go.Scatter3d(
            x=x_coords,
            y=y_coords,
            z=z_coords,
            mode='markers',
            marker=dict(size=1, color='gray', symbol='circle'),
            name="Occupied Voxels"
        )
    ])

    if startNode:
        fig.add_trace(go.Scatter3d(
            x=[startNode[0]], y=[startNode[1]], z=[startNode[2]],
            mode='markers',
            marker=dict(size=10, color='yellow',  symbol='circle'),
            name="Start Node"
        ))

    if targetNode:
        fig.add_trace(go.Scatter3d(
            x=[targetNode[0]], y=[targetNode[1]], z=[targetNode[2]],
            mode='markers',
            marker=dict(size=10, color='red',symbol='circle'),
            name="Target Node"
        ))

    if path:
        path_coords = np.array(path)
        fig.add_trace(go.Scatter3d(
            x=path_coords[:, 0], y=path_coords[:, 1], z=path_coords[:, 2],
            mode='lines+markers',
            marker=dict(size=0, color='green'),
            line=dict(color='green', width=8),
            name="Path"
        ))

    fig.update_layout(
        title="3D Voxel Grid Map",
        scene=dict(
            xaxis_title="Grid X Index",
            yaxis_title="Grid Y Index",
            zaxis_title="Grid Z Index"
        )
    )

    fig.show()
