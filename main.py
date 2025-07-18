import bpy
import json
import sys
import os
import importlib

# Get the absolute path of the script directory
script_dir = r'D:\Projects\Dev\Python\ETL02_blender'

# Add the script directory to Python path if not already there
if script_dir not in sys.path:
    sys.path.insert(0, script_dir)

print(f"Script directory: {script_dir}")
print(f"Current First Python path: {sys.path[:1]}...")

# Force reload modules to pick up changes during development
# This is to avoid error of "Module ... has no attribute ..."
def reload_modules():
    """Force reload all custom modules to pick up changes."""
    modules = ['checker.name_check', 'checker.mesh_check', 'checker.pivot_check', 
               'checker.lod_check', 'checker.bone_check', 'exporter.report_export']
    for module in modules:
        if module in sys.modules: # If the module is already loaded
            importlib.reload(sys.modules[module]) # Reload the module
            print(f"{module} reloaded")

reload_modules()

# After script_dir is specified, and modules are reloaded
from checker import name_check, mesh_check, pivot_check, lod_check, bone_check
from exporter import report_export

#######################################################################################################################
# This script is an ETL (Extract, Transform, Load) tool for Blender.
#######################################################################################################################

# Load configuration from config.json
def load_config(config):
    config_path = os.path.join(script_dir, config)
    with open(config_path, "r", encoding="utf-8") as f:
        return json.load(f)

def check_all_objects(config):
    invalid_objects = [] # A list of dictionaries, objcet name as key, and a list of reasons as values

    for obj in bpy.data.objects:  # Iterate through all objects in the scene and do all checks
        reasons = [] # Collect reasons for invalid objects

        # Mesh face check
        ok_faces, msg_faces = mesh_check.check_mesh_faces(obj, config["max_faces"])
        if not ok_faces:
            reasons.append(msg_faces)

        # Name check (using allowed suffixes)
        allowed_suffixes = config["allowed_name_suffixes"]
        ok_name, msg_name = name_check.check_object_name(obj, allowed_suffixes)
        if not ok_name:
            reasons.append(msg_name)

        # Close vertices check (only for mesh objects)
        if obj.type == 'MESH':
            min_distance = config["min_vertex_distance"]
            ok_vertices, msg_vertices, close_pairs = mesh_check.check_close_vertices(obj, min_distance) # close_pairs left for future use
            if not ok_vertices:
                reasons.append(msg_vertices)

        if reasons:
            invalid_objects.append({
                "object": obj.name, # Name of the object
                "reasons": reasons # List reasons
            })

    return invalid_objects

def main():
    config = load_config("config.json")
    invalid_objects = check_all_objects(config)

    # Export txt report for invalid objects only
    report_path = os.path.join(script_dir, "report.txt")
    report_export.export_invalid_objects_report(invalid_objects, report_path)
    '''
    for res in results:
        # Read from the dictionary
        print(f"[{res['type']}] {res['object']}: {'PASS' if res['result'] else 'FAIL'} - {res['message']}") #
    print("\nSummary of invalid objects (failed naming, face count, or close vertices check):")
    if invalid_objects:
        for item in invalid_objects:
            print(f"- {item['object']}:")
            for reason in item['reasons']:
                print(f"    Reason: {reason}")
    else:
        print("All objects passed the checks.")
    '''

if __name__ == "__main__":
    main()