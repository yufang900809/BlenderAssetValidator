# Blender ETL Validation Tool

## Professional 3D Asset Quality Control Pipeline for Blender

A comprehensive Python-based validation system for Blender that automates mesh quality checks, enforces naming conventions, and generates detailed reports for production pipelines.

## 🚀 Features

### Core Validation Modules
- **Mesh Face Count Validation** - Automatically detects meshes exceeding polygon limits for performance optimization
- **Close Vertex Detection** - Identifies problematic vertices that are too close together with precise distance measurements
- **Naming Convention Enforcement** - Validates object names follow studio standards (customizable suffixes: `_geo`, `_jnt`, `_grp`)

### Production-Ready Architecture
- **JSON Configuration System** - Flexible parameter storage for different project requirements
- **Automated TXT Report Export** - Comprehensive validation reports with detailed error locations and statistics
- **Modular Design** - Extensible checker system with separate modules for different validation types
- **Custom Blender UI** - Professional dialog interface with real-time scene statistics and configuration

### Technical Highlights
- **World Space Calculations** - Accurate vertex distance measurements in world coordinates
- **Batch Processing** - Validates entire scenes in one operation
- **Error Handling** - Robust exception management with detailed error reporting
- **Performance Optimized** - Efficient algorithms for large scene validation

## 🛠️ Installation & Usage

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/blender-etl-validation-tool.git
   ```

2. **Run in Blender:**
   - Open Blender
   - Load and execute `UI.py` in the Scripting workspace
   - Update the `script_dir` variable in both `main.py` and `UI.py` to match your project folder path
   - Use the validation dialog to configure parameters and run checks

3. **Configure validation parameters:**
   - Edit `config.json` or use the UI to set:
     - Maximum face count per mesh
     - Minimum vertex distance threshold
     - Allowed naming suffixes

## 📊 Example Output

```
Invalid Objects Report
=====================

Total invalid objects: 2

- Icosphere_geo:
    Reason: Mesh 'Icosphere_geo' exceeds max face count: 320 > 300
    Reason: Mesh 'Icosphere_geo' has 487 vertex pairs closer than 1.0: 
            vertices 0-42: 0.606683, vertices 0-47: 0.606689 (and 482 more)

- Camera_cam:
    Reason: Object 'Camera_cam' does not end with ['_geo', '_jnt', '_grp'].
```

## 🔧 Configuration

Edit `config.json` to customize validation parameters:

```json
{
    "max_faces": 300,
    "allowed_name_suffixes": ["_geo", "_jnt", "_grp"],
    "min_vertex_distance": 1.0
}
```