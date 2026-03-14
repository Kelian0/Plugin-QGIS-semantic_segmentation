def toggle_strikethrough(is_checked, checkbox):
    font = checkbox.font()
    
    if is_checked:
        font.setStrikeOut(True)
    else:
        font.setStrikeOut(False)
        
    checkbox.setFont(font)

def get_color(class_name, file_path):
    with open(file_path, 'r') as file:
        for line in file:
            parts = line.strip().split()
            current_class = parts[5]
            if current_class == class_name:
                r = int(parts[1])
                g = int(parts[2])
                b = int(parts[3])
                return f"#{r:02x}{g:02x}{b:02x}"
    
def toggle_exclusive_groupboxes(is_checked, other_groupbox):
    other_groupbox.blockSignals(True)
    
    if is_checked:
        other_groupbox.setChecked(False)
    else:
        other_groupbox.setChecked(True)
        
    other_groupbox.blockSignals(False)