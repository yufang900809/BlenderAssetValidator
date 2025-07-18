import bpy
from bpy.types import Operator
from bpy.props import StringProperty, IntProperty

class HelloNameOperator(Operator):
    bl_idname = "object.test_operator"
    bl_label = "Cube Manager"

    # Input properties
    name: StringProperty(
        name="Name",
        description="Name to greet",
        default="testCube"
    )
    repeat: IntProperty(
        name="Repeat",
        description="How many times to say hello",
        default=8,
        min=1,
        max=10
    )

    # Create a simple cube and return a list of created objects, and name them with the given name
    def create_cubes(self, name, repeat):
        created_objects = []
        for i in range(repeat):
            # Create the box with the give namd and index, and append the created object to the list
            bpy.ops.mesh.primitive_cube_add(size=1, location=(i * 2, 0, 2))
            obj = bpy.context.active_object
            obj.name = f"{name}_{i + 1}"
            created_objects.append(obj)
        return created_objects

    def remove_cubes(self, objects):
        for obj in objects:
            # Remove the object in the list from the scene
            bpy.data.objects.remove(obj, do_unlink=True)

    def execute(self, context): # Resembles the event graph in UE5
        return {'FINISHED'}

    def invoke(self, context, event): # Resembles the construction script in UE5
        # Initialize created cubes list if it doesn't exist
        if "created_cubes" not in context.scene:
            context.scene["created_cubes"] = []
        
        # Store parameters in scene for access by action operators
        context.scene["cube_manager_props"] = {
            "name": self.name,
            "repeat": self.repeat
        }
        return context.window_manager.invoke_props_dialog(self)

    def draw(self, context): # Resembles Widgets in UE5
        layout = self.layout
        layout.prop(self, "name")
        layout.prop(self, "repeat")
        
        # Custom action buttons
        row = layout.row()
        row.operator("object.create_cubes", text="Create Cubes")
        row.operator("object.remove_cubes", text="Remove Cubes")
        row.operator("object.select_cubes", text="Select Cubes")
        row = layout.row()
        row.label(text="testRow:")
        row.operator("object.select_cubes", text="Select Cubes")

class CreateCubesOperator(Operator):
    bl_idname = "object.create_cubes"
    bl_label = "Create Cubes"
    
    def execute(self, context):
        # Get parameters from the main operator
        main_op = context.scene.get("cube_manager_props", {})
        name = main_op.get("name", "testCube")
        repeat = main_op.get("repeat", 8)
        
        # Create cubes and add to tracking list
        created_cubes = list(context.scene.get("created_cubes", []))
        for i in range(repeat):
            bpy.ops.mesh.primitive_cube_add(size=1, location=(i * 2, 0, 2))
            obj = bpy.context.active_object
            obj.name = f"{name}_{i + 1}"
            created_cubes.append(obj.name)  # Store object name for tracking
        
        context.scene["created_cubes"] = created_cubes
        self.report({'INFO'}, f"Created {repeat} cubes")
        return {'FINISHED'}

class RemoveCubesOperator(Operator):
    bl_idname = "object.remove_cubes"
    bl_label = "Remove Cubes"
    
    def execute(self, context):
        # Get tracked cubes list
        created_cubes = list(context.scene.get("created_cubes", []))
        
        # Remove cubes from the tracked list
        removed_count = 0
        for cube_name in created_cubes:
            obj = bpy.data.objects.get(cube_name)
            if obj:
                bpy.data.objects.remove(obj, do_unlink=True)
                removed_count += 1
        
        # Clear the tracking list
        context.scene["created_cubes"] = []
        
        self.report({'INFO'}, f"Removed {removed_count} cubes")
        return {'FINISHED'}
    
class SelectCubesOperator(Operator):
    bl_idname = "object.select_cubes"
    bl_label = "Select Cubes"
    
    def execute(self, context):
        # Get tracked cubes list
        created_cubes = list(context.scene.get("created_cubes", []))
        
        # Deselect all objects first
        bpy.ops.object.select_all(action='DESELECT')
        
        # Select all created cubes
        for cube_name in created_cubes:
            obj = bpy.data.objects.get(cube_name)
            if obj:
                obj.select_set(True)
        
        self.report({'INFO'}, f"Selected {len(created_cubes)} cubes")
        return {'FINISHED'}

# Register
def register():
    bpy.utils.register_class(HelloNameOperator)
    bpy.utils.register_class(CreateCubesOperator)
    bpy.utils.register_class(RemoveCubesOperator)
    bpy.utils.register_class(SelectCubesOperator)

def unregister():
    bpy.utils.unregister_class(HelloNameOperator)
    bpy.utils.unregister_class(CreateCubesOperator)
    bpy.utils.unregister_class(RemoveCubesOperator)
    bpy.utils.unregister_class(SelectCubesOperator)

if __name__ == "__main__":
    register()
    # Test call
    bpy.ops.object.test_operator('INVOKE_DEFAULT')
