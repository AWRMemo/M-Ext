import trimesh
import xatlas
import numpy as np
import os

class MVAdapterNode:
    def process(self, image, mesh):
        print(f"Loading chunky mesh from {mesh}...")
        
        scene = trimesh.load(mesh, force='mesh')
        
        if isinstance(scene, trimesh.Scene):
            if not scene.geometry:
                raise ValueError("No geometry found in the input mesh.")
            geometry = trimesh.util.concatenate(
                tuple(trimesh.Trimesh(vertices=g.vertices, faces=g.faces)
                    for g in scene.geometry.values())
            )
        else:
            geometry = scene

        vertices = geometry.vertices
        faces = geometry.faces

        print("Calculating optimal UV islands via Xatlas...")
        vmapping, indices, uvs = xatlas.parametrize(vertices, faces)

        new_vertices = vertices[vmapping]
        new_faces = indices

        unwrapped_mesh = trimesh.Trimesh(vertices=new_vertices, faces=new_faces)
        unwrapped_mesh.visual = trimesh.visual.TextureVisuals(uv=uvs)

        output_mesh_path = "output_unwrapped_mesh.glb"
        print("Exporting UV-unwrapped mesh...")
        unwrapped_mesh.export(output_mesh_path)
        
        return output_mesh_path
