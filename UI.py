import bpy
import json
from bpy.types import Operator
from bpy.props import StringProperty, IntProperty, FloatProperty
import os
import sys

# Get the directory of this script
#script_dir = os.path.dirname(os.path.abspath(__file__))
script_dir = r'D:\Projects\Dev\Python\ETL02_blender'

# Add to Python path
if script_dir not in sys.path:
    sys.path.insert(0, script_dir)

# Function to load config defaults
def load_config_defaults():
    """Load default values from config.json"""
    config_path = os.path.join(script_dir, "config.json")
    with open(config_path, 'r', encoding='utf-8') as f:
        config = json.load(f)
    return config

# Load config defaults
config_loaded = load_config_defaults()

# Global variable to store current report content
current_report_content = "Click 'Run Validation' to generate report..."

class ETL_OT_ValidationWindow(Operator): # Inherits from bpy.types.Operator
    bl_idname = "etl.validation_window" # Unique ID to call this operator
    bl_label = "Validation Tool by Fang Yu"
    bl_description = "by Fang Yu"
    bl_options = {'REGISTER'} # Register for undo/redo support
    
    # Input parameters
    max_faces: IntProperty(
        name="Max Faces",
        description="Maximum allowed face count per mesh",
        default=config_loaded['max_faces'],
        min=1
    )
    
    min_vertex_distance: FloatProperty(
        name="Min Vertex Distance", 
        description="Minimum distance between vertices",
        default=config_loaded['min_vertex_distance'],
        min=0.0001,
        precision=6
    )
    
    # Individual suffix properties (dynamic)
    suffix_count: IntProperty(
        name="Number of Suffixes",
        description="Number of allowed suffixes",
        default=len(config_loaded['allowed_name_suffixes']),
        min=1,
        max=10
    )
    
    suffix_1: StringProperty(name="Suffix 1", default="") # Placeholder for suffixes
    suffix_2: StringProperty(name="Suffix 2", default="") 
    suffix_3: StringProperty(name="Suffix 3", default="")
    suffix_4: StringProperty(name="Suffix 4", default="") 
    suffix_5: StringProperty(name="Suffix 5", default="")
    suffix_6: StringProperty(name="Suffix 6", default="")
    suffix_7: StringProperty(name="Suffix 7", default="")
    suffix_8: StringProperty(name="Suffix 8", default="")
    suffix_9: StringProperty(name="Suffix 9", default="")
    suffix_10: StringProperty(name="Suffix 10", default="")
    
    # Report content
    def get_report_content(self):
        return current_report_content
        
    def set_report_content(self, value):
        global current_report_content
        current_report_content = value
    
    report_content: StringProperty(
        name="Report",
        description="Validation report content",
        default="Click 'Run Validation' to generate report...",
        get=get_report_content, # Always returns current value
        set=set_report_content # Updates can come from anywhere
    )
    
    status_message: StringProperty(
        name="Status",
        description="Current status",
        default="Ready"
    )
    
    def get_scene_stats(self):
        try:
            # Count mesh objects only (exclude cameras, lights, etc.)
            mesh_objects = [obj for obj in bpy.context.scene.objects if obj.type == 'MESH']
            object_count = len(mesh_objects)
            
            # Count total faces across all mesh objects
            total_faces = 0
            for obj in mesh_objects:
                if obj.data and hasattr(obj.data, 'polygons'):
                    total_faces += len(obj.data.polygons)
            
            return f"Scene: {object_count} mesh objects, {total_faces} total faces"
        except Exception as e:
            return f"Error getting scene stats: {str(e)}"
    
    def execute(self, context):
        return {'FINISHED'} # This operator does nothing by itself
    
    def invoke(self, context, event):
        # Initialize individual suffix fields from the config defaults
        suffixes = config_loaded['allowed_name_suffixes']
        self.suffix_count = len(suffixes)
        
        # Set individual suffix fields
        for i, suffix in enumerate(suffixes[:10], 1):
            setattr(self, f"suffix_{i}", suffix) # Initialize suffix properties with config values
        
        # Clear any remaining suffix fields
        for i in range(len(suffixes) + 1, 11):
            setattr(self, f"suffix_{i}", "") # Clear unused suffixes properties
            
        return context.window_manager.invoke_props_dialog(self, width=600)
    
    def draw(self, context):
        layout = self.layout
        
        # Title
        row = layout.row()
        row.label(text="Validation Tool", icon='MESH_DATA')
        
        layout.separator()
        
        # Parameters section
        box = layout.box() # Box of parameters
        box.label(text="Validation Parameters:", icon='SETTINGS')
        
        col = box.column()
        col.prop(self, "max_faces") # Expose properties to the UI
        col.prop(self, "min_vertex_distance")
        
        # Suffixes section
        suffix_box = box.box() # Box in a box, particularly for suffixes
        suffix_box.label(text="Allowed Name Suffixes:", icon='OUTLINER_OB_FONT')
        
        # Number of suffixes
        row = suffix_box.row()
        row.prop(self, "suffix_count")
        
        # Individual suffix inputs
        suffix_col = suffix_box.column()
        for i in range(1, self.suffix_count + 1):
            row = suffix_col.row() # Add a row for each suffix count
            row.prop(self, f"suffix_{i}", text=f"Allowed Suffix {i}") # Expose individual suffix properties to the UI
        
        layout.separator()
        
        # Execute button
        row = layout.row()
        row.scale_y = 2
        op = row.operator("etl.run_validation", text="Run Validation", icon='PLAY') # Button to run validation
        op.max_faces = self.max_faces # Pass parameters to the operator
        op.min_vertex_distance = self.min_vertex_distance
        for i in range(1, self.suffix_count + 1):
            suffix_value = getattr(self, f"suffix_{i}", "").strip() # Remove leading/trailing spaces, if any
            if suffix_value:
                setattr(op, f"suffix_{i}", suffix_value) # Pass individual suffix values to the operator
        op.suffix_count = self.suffix_count # Pass the count of suffixes to the operator
        
        layout.separator()
        
        # Status
        box = layout.box()
        box.label(text="Scene Status:", icon='INFO')
        
        # Get current scene statistics
        scene_stats = self.get_scene_stats()
        box.label(text=scene_stats)
        
        layout.separator()

        # Report section
        box = layout.box()
        box.label(text="Validation Report:", icon='TEXT')
        col = box.column()
        lines = self.report_content.split('\n') # Split each line into a list
        for line in lines[:20]:  # Show first 20 lines
            if line.strip(): # Only show non-empty lines
                col.label(text=line) # Display each line as a label
        
        if len(lines) > 20:
            col.label(text=f"... and {len(lines) - 20} more lines")




class ETL_OT_RunValidation(Operator):
    bl_idname = "etl.run_validation"
    bl_label = "Run Validation"
    bl_description = "Execute validation"
    
    # Parameters passed from the dialog
    max_faces: IntProperty(default=100)
    min_vertex_distance: FloatProperty(default=0.001)
    suffix_count: IntProperty(default=3)
    suffix_1: StringProperty(default="")
    suffix_2: StringProperty(default="")
    suffix_3: StringProperty(default="")
    suffix_4: StringProperty(default="")
    suffix_5: StringProperty(default="")
    suffix_6: StringProperty(default="")
    suffix_7: StringProperty(default="")
    suffix_8: StringProperty(default="")
    suffix_9: StringProperty(default="")
    suffix_10: StringProperty(default="")
    
    def execute(self, context):
        try:
            # Collect suffixes in a list
            suffixes = []
            for i in range(1, self.suffix_count + 1):
                suffix_value = getattr(self, f"suffix_{i}", "").strip() # Read individual suffix properties
                if suffix_value: # If exists
                    suffixes.append(suffix_value) # Add to suffixes list
            
            self.update_config(suffixes) # Update config.json with current parameters
            self.run_main_script() # Run main.py
            self.update_report_in_ui(context) # Update the report content in the UI
            
            # Force UI refresh to show updated report
            for window in context.window_manager.windows:
                for area in window.screen.areas:
                    area.tag_redraw()  # Refresh all areas to ensure dialog updates
            
            # System message
            self.report({'INFO'}, "Validation completed! Report updated below.")
            
        except Exception as e:
            print(f"ERROR: {str(e)}")
            print("=" * 60)
            self.report({'ERROR'}, f"Error running validation: {str(e)}")
        
        return {'FINISHED'}
    
    def update_config(self, suffixes):
        config_path = os.path.join(script_dir, "config.json")
        
        config = {
            "max_faces": self.max_faces,
            "allowed_name_suffixes": suffixes,
            "min_vertex_distance": self.min_vertex_distance
        }
        
        try:
            with open(config_path, "w", encoding="utf-8") as f:
                json.dump(config, f, indent=4) # Write config with indentation
        except Exception as e:
            print(f"Error updating config: {e}")
    
    def run_main_script(self):
        """Execute the main.py script"""
        main_script = os.path.join(script_dir, "main.py")
        
        if not os.path.exists(main_script):
            raise Exception(f"main.py not found at {main_script}")
        
        # Change to script directory to ensure proper module loading
        original_cwd = os.getcwd() # Save original working directory
        
        try:
            os.chdir(script_dir) # Change to the script directory
            print(f"Changed working directory to: {os.getcwd()}")
            
            # Read and execute the main script
            with open(main_script, 'r', encoding='utf-8') as f:
                script_content = f.read()
            
            # Create a globals dict with the correct __file__ path
            script_globals = {
                '__file__': main_script,
                '__name__': '__main__'
            }
            
            # Execute the script
            exec(compile(script_content, main_script, 'exec'), script_globals)
            
        except Exception as e:
            print(f"Error executing main.py: {e}")
            raise
        finally:
            # Always restore original working directory
            os.chdir(original_cwd)
            print(f"Restored working directory to: {os.getcwd()}")
    
    def update_report_in_ui(self, context):
        """Update the report content in the UI window"""
        global current_report_content
        report_path = os.path.join(script_dir, "report.txt")
        
        try:
            if os.path.exists(report_path):
                with open(report_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Update the global report content
                current_report_content = content if content.strip() else "Report generated but is empty."
                
                # Force UI redraw to show updated report
                for window in context.window_manager.windows:
                    for area in window.screen.areas:
                        area.tag_redraw()
                
                print("Report loaded into UI successfully!")
                print("Report content preview:")
                print(content[:200] + "..." if len(content) > 200 else content)
                
            else:
                current_report_content = f"Report file not found at: {report_path}"
                print(f"Report file not found at: {report_path}")
                
        except Exception as e:
            current_report_content = f"Error loading report: {str(e)}"
            print(f"Error updating report in UI: {e}")

class ETL_OT_AddSuffix(Operator):
    bl_idname = "etl.add_suffix"
    bl_label = "Add Suffix"
    bl_description = "Add a new suffix field"
    
    def execute(self, context):
        # This is a validation tool button - the actual logic is handled by the suffix_count property
        return {'FINISHED'}

class ETL_OT_RemoveSuffix(Operator):
    bl_idname = "etl.remove_suffix"
    bl_label = "Remove Suffix"
    bl_description = "Remove the last suffix field"
    
    def execute(self, context):
        # This is a validation tool button - the actual logic is handled by the suffix_count property
        return {'FINISHED'}

# Validation Tool registration
def register_validation_tool():
    try:
        bpy.utils.register_class(ETL_OT_ValidationWindow)
        bpy.utils.register_class(ETL_OT_RunValidation)
        print("Validation Tool registered!")
        return True
    except Exception as e:
        print(f"Registration error: {e}")
        return False

def unregister_validation_tool():
    try:
        bpy.utils.unregister_class(ETL_OT_RunValidation)
        bpy.utils.unregister_class(ETL_OT_ValidationWindow)
        print("Validation Tool unregistered!")
    except Exception as e:
        print(f"Unregistration error: {e}")

# Main execution
if __name__ == "__main__":
    # Clean up
    unregister_validation_tool()
    
    # Register and open window
    if register_validation_tool():
        # Open the validation window
        bpy.ops.etl.validation_window('INVOKE_DEFAULT')
        print("\nValidation Tool is ready!")
        print("The configuration window should be open.")