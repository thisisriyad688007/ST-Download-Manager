import os

# এখানে আপনার আগের ডেভেলপার ক্রেডিট বা নামগুলো লিখবেন, যেগুলো পরিবর্তন করতে চান
old_credits = ["Swap Tech", "Swap Tech", "Swap Tech"] 
new_credit = "Swap Tech"  # আপনার ব্র্যান্ডের নাম

exclude_dirs = {'.git', 'node_modules', 'venv', '__pycache__'}

for root, dirs, files in os.walk('.'):
    dirs[:] = [d for d in dirs if d not in exclude_dirs]
    for file in files:
        file_path = os.path.join(root, file)
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            modified = False
            for old in old_credits:
                if old in content:
                    content = content.replace(old, new_credit)
                    modified = True
            
            if modified:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"Updated credits in: {file_path}")
        except Exception as e:
            pass

print("Developer credits successfully updated to Swap Tech!")
