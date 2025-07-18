import os

def export_invalid_objects_report(invalid_objects, filepath="invalid_objects_report.txt"):
    """
    Export a text report of invalid objects and their reasons.
    Each object will list its name and the specific reasons for failure.
    Creates the directory structure if it doesn't exist.
    """
    try:
        # Ensure the directory exists
        directory = os.path.dirname(filepath)
        if directory and not os.path.exists(directory):
            os.makedirs(directory, exist_ok=True)
            print(f"Created directory: {directory}")
        
        lines = []
        lines.append("Invalid Objects Report")
        lines.append("=====================")
        lines.append("")
        
        if not invalid_objects:
            lines.append("All objects passed the checks.")
        else:
            lines.append(f"Total invalid objects: {len(invalid_objects)}")
            lines.append("")
            
            for item in invalid_objects:
                lines.append(f"- {item['object']}:")
                for reason in item['reasons']:
                    lines.append(f"    Reason: {reason}")
                lines.append("")  # Blank line for separation
        
        # Write the file
        with open(filepath, "w", encoding="utf-8") as f:
            for line in lines:
                f.write(line + "\n")
        
        print(f"Invalid objects report exported to: {os.path.abspath(filepath)}")
        return True
        
    except Exception as e:
        print(f"Error creating report file: {e}")
        return False