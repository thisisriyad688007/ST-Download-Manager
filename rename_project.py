import os
import re

# পরিবর্তনের তালিকা (যেগুলো খুঁজতে হবে এবং যার দ্বারা প্রতিস্থাপন করতে হবে)
replacements = {
    "ST Download Manager": "ST Download Manager",
    "ST Download Manager": "ST Download Manager",
    "ST Download Manager": "ST Download Manager"
}

exclude_dirs = {'.git', 'node_modules', 'venv', '__pycache__'}

for root, dirs, files in os.walk('.'):
    dirs[:] = [d for d in dirs if d not in exclude_dirs]
    for file in files:
        file_path = os.path.join(root, file)
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            modified = False
            for old, new in replacements.items():
                if old in content:
                    content = content.replace(old, new)
                    modified = True
            
            if modified:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"Updated: {file_path}")
        except Exception as e:
            pass

print("All names successfully changed to ST Download Manager!")
