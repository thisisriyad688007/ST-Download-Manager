import sys
import re
import json

if len(sys.argv) < 2:
    print("ব্যবহারের নিয়ম: python3 update_version.py <নতুন_ভার্সন>")
    print("উদাহরণ: python3 update_version.py 0.1.5")
    sys.exit(1)

new_ver_raw = sys.argv[1].strip()
# 'v' থাকলে তা সরিয়ে ক্লিন ভার্সন নেওয়া
clean_ver = new_ver_raw.lstrip('v')
tag_ver = f"v{clean_ver}"

print(f"[*] Updating ST Download Manager version to: {tag_ver} ({clean_ver})")

# ১. package.json আপডেট
try:
    with open("package.json", "r", encoding="utf-8") as f:
        pkg = json.load(f)
    pkg["version"] = clean_ver
    with open("package.json", "w", encoding="utf-8") as f:
        json.dump(pkg, f, indent=2)
        f.write("\n")
    print("  [✓] Updated package.json")
except Exception as e:
    print(f"  [!] package.json update error: {e}")

# ২. desktop/main.cjs আপডেট
try:
    with open("desktop/main.cjs", "r", encoding="utf-8") as f:
        main_cjs = f.read()
    
    # currentVersion ভ্যারিয়েবল আপডেট
    main_cjs = re.sub(r"const currentVersion = ['\"]v?[0-9.]+['\"];", f"const currentVersion = '{tag_ver}';", main_cjs)
    main_cjs = re.sub(r"current:\s*['\"]v?[0-9.]+['\"]", f"current: '{tag_ver}'", main_cjs)
    
    with open("desktop/main.cjs", "w", encoding="utf-8") as f:
        f.write(main_cjs)
    print("  [✓] Updated desktop/main.cjs")
except Exception as e:
    print(f"  [!] desktop/main.cjs update error: {e}")

# ৩. renderer/index.html আপডেট (About & Update Dialogs)
try:
    with open("renderer/index.html", "r", encoding="utf-8") as f:
        html = f.read()
    
    # v0.1.x ব্যাজ ও টেক্সট আপডেট
    html = re.sub(r"v[0-9]+\.[0-9]+\.[0-9]+", tag_ver, html)
    
    with open("renderer/index.html", "w", encoding="utf-8") as f:
        f.write(html)
    print("  [✓] Updated renderer/index.html")
except Exception as e:
    print(f"  [!] renderer/index.html update error: {e}")

# ৪. renderer/app.js আপডেট
try:
    with open("renderer/app.js", "r", encoding="utf-8") as f:
        app_js = f.read()
    
    app_js = re.sub(r"CURRENT_VERSION = ['\"]v?[0-9.]+['\"];", f"CURRENT_VERSION = '{tag_ver}';", app_js)
    app_js = re.sub(r"v[0-9]+\.[0-9]+\.[0-9]+", tag_ver, app_js)
    
    with open("renderer/app.js", "w", encoding="utf-8") as f:
        f.write(app_js)
    print("  [✓] Updated renderer/app.js")
except Exception as e:
    print(f"  [!] renderer/app.js update error: {e}")


# ৫. manifest.json ফাইলগুলো আপডেট
import glob
for mf in glob.glob("**/manifest*.json", recursive=True):
    if "node_modules" in mf:
        continue
    try:
        with open(mf, "r", encoding="utf-8") as f:
            mdata = json.load(f)
        if "version" in mdata:
            mdata["version"] = clean_ver
            with open(mf, "w", encoding="utf-8") as f:
                json.dump(mdata, f, indent=2)
                f.write("\n")
            print(f"  [✓] Updated {mf}")
    except Exception:
        pass

print(f"\n[SUCCESS] Successfully bumped all project files to {tag_ver}!")
