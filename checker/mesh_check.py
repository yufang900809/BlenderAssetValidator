import bpy
import bmesh
from mathutils import Vector

def check_mesh_faces(obj, max_faces=50000):
    """Check if the mesh object exceeds the maximum allowed face count."""
    if obj.type == 'MESH': # Check if the object is a mesh
        face_count = len(obj.data.polygons) # Get the number of faces in the mesh
        if face_count > max_faces: # If the face count exceeds the maximum allowed
            return False, f"Mesh '{obj.name}' exceeds max face count: {face_count} > {max_faces}"
        else: # If the face count is within the limit
            return True, f"Mesh '{obj.name}' face count OK: {face_count} <= {max_faces}"
    return True, f"Object '{obj.name}' is not a mesh, skipped face check." # Not a mesh object

def check_close_vertices(obj, min_distance=0.001):
    """
    Check if there are vertices that are too close to each other.
    
    Args:
        obj: Blender object to check
        min_distance: Minimum allowed distance between vertices
    
    Returns:
        tuple: (is_valid, message, close_pairs_list)
    """
    if obj.type != 'MESH': # Check if the object is a mesh
        return True, f"Object '{obj.name}' is not a mesh, skipped close vertices check.", []
    
    try:
        # Get mesh data
        mesh = obj.data
        vertices = mesh.vertices
        
        if len(vertices) < 2: # Check only object with more than 1 vertex
            return True, f"Mesh '{obj.name}' has less than 2 vertices, skipped close vertices check.", []
        
        # Transform vertices to world coordinates
        world_matrix = obj.matrix_world # Get the world transform of the object
        world_vertices = [world_matrix @ vertex.co for vertex in vertices] # World coordinates of vertices
        
        close_pairs = []
        
        # Check all pairs of vertices
        for i in range(len(world_vertices)): # Iterate through each vertex
            for j in range(i + 1, len(world_vertices)): # Compare with subsequent vertices
                distance = (world_vertices[i] - world_vertices[j]).length # Get the distance between two vertices
                
                if distance < min_distance:
                    close_pairs.append({
                        #'vertex_1': i,
                        #'vertex_2': j,
                        'vertex_1': vertices[i].index, # Use vertex index for better identification
                        'vertex_2': vertices[j].index,
                        'distance': distance,
                        'pos_1': world_vertices[i],
                        'pos_2': world_vertices[j]
                    })
        
        # Report close vertex pairs
        if len(close_pairs) > 0:
            if len(close_pairs) <= 5:
                # List all close pairs if 5 or fewer
                close_pairs_summary = []
                for pair in close_pairs:
                    close_pairs_summary.append(f"vertices {pair['vertex_1']}-{pair['vertex_2']}: {pair['distance']:.6f}")
                summary_msg = ", ".join(close_pairs_summary)
                return False, f"Mesh '{obj.name}' has {len(close_pairs)} vertex pairs closer than {min_distance}: {summary_msg}", close_pairs
            else:
                # Summarize if more than 5 pairs
                close_pairs_summary = []
                for pair in close_pairs[:5]:  # Show first 5 pairs
                    close_pairs_summary.append(f"vertices {pair['vertex_1']}-{pair['vertex_2']}: {pair['distance']:.6f}")
                
                summary_msg = ", ".join(close_pairs_summary)
                summary_msg += f" (and {len(close_pairs) - 5} more)" # If there are more than 5 pairs, summarize the rest
                
                return False, f"Mesh '{obj.name}' has {len(close_pairs)} vertex pairs closer than {min_distance}: {summary_msg}", close_pairs
        else:
            return True, f"Mesh '{obj.name}' has no vertices closer than {min_distance}", []
            
    except Exception as e: # Handle any exceptions that occur during the check
        return False, f"Error checking close vertices for '{obj.name}': {str(e)}", []


