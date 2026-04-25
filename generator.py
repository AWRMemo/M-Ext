import trimesh
import xatlas
import numpy as np
import os

def auto_unwrap_mesh(input_mesh_path, output_mesh_path, uv_padding=2):
    print(f"Loading chunky mesh from {input_mesh_path}...")
    
    scene = trimesh.load(input_mesh_path, force='mesh')
    
    if isinstance(scene, trimesh.Scene):
        if not scene.geometry:
            raise ValueError("No geometry found in the input mesh.")
        mesh = trimesh.util.concatenate(
            tuple(trimesh.Trimesh(vertices=g.vertices, faces=g.faces)
                for g in scene.geometry.values())
        )
    else:
        mesh = scene

    vertices = mesh.vertices
    faces = mesh.faces

    print("Calculating optimal UV islands via Xatlas...")
    vmapping, indices, uvs = xatlas.parametrize(vertices, faces)

    new_vertices = vertices[vmapping]
    new_faces = indices

    unwrapped_mesh = trimesh.Trimesh(vertices=new_vertices, faces=new_faces)
    unwrapped_mesh.visual = trimesh.visual.TextureVisuals(uv=uvs)

    print("Exporting UV-unwrapped mesh...")
    unwrapped_mesh.export(output_mesh_path)
    
    return output_mesh_path
