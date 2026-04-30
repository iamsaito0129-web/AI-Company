import os
import re
import yaml
import sys

# Ensure stdout handles UTF-8
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

# Path configuration
BASE_DIR = r"C:\Users\iamsa\ローカルプライベートフォルダー\私用(PC)\AI-company"
REGEX_FILE = os.path.join(BASE_DIR, "company", "hr", "members", "line_name_regex.md")
LOGS_DIR = os.path.join(BASE_DIR, "company", "hr", "members", "line_logs")

def parse_mapping(file_path):
    mapping = {}
    ignore_names = set()
    rescue_mapping = {} # For "名前が不足 " prefix rescue
    simple_mapping = {} # For stripped names rescue (e.g. "かりん" -> "実委 かりん")
    
    prefixes = ["実委 ", "学校教育 ", "PA ", "実委② ", "実委③ ", "多文化 "]
    
    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()
    
    # Find table start
    table_started = False
    for line in lines:
        line = line.strip()
        if "|" in line and "A列" in line:
            table_started = True
            continue
        if table_started and line.startswith("| :---"):
            continue
        if table_started and line.startswith("|"):
            parts = [p.strip() for p in line.split("|")]
            if len(parts) >= 4:
                raw_name = parts[1]
                target = parts[3]
                
                # Check if it's strictly an ignore pattern
                if target == "^名前が不足$" or target == "名前が不足":
                    ignore_names.add(raw_name)
                else:
                    canonical = target.strip("^$").replace("\\ ", " ")
                    mapping[raw_name] = canonical
                    
                    # Build simple name (stripped of common prefixes)
                    simple_name = raw_name
                    has_prefix = False
                    for pref in prefixes:
                        if raw_name.startswith(pref):
                            simple_name = raw_name[len(pref):]
                            has_prefix = True
                            break
                    
                    if has_prefix:
                        # Map "名前が不足 かりん" -> "実委 かりん"
                        rescue_key = "名前が不足 " + simple_name
                        rescue_mapping[rescue_key] = canonical
                        
                        # Map "かりん" -> "実委 かりん" (if unambiguous)
                        if simple_name not in simple_mapping:
                            simple_mapping[simple_name] = canonical
                        elif simple_mapping[simple_name] != canonical:
                            # Ambiguous!
                            simple_mapping[simple_name] = None

    return mapping, ignore_names, rescue_mapping, simple_mapping

def process_logs(mapping, ignore_names, rescue_mapping, simple_mapping):
    if not os.path.exists(LOGS_DIR):
        print(f"Directory not found: {LOGS_DIR}")
        return

    files = [f for f in os.listdir(LOGS_DIR) if f.endswith(".md")]
    
    for filename in files:
        filepath = os.path.join(LOGS_DIR, filename)
        
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
        
        # Split YAML and Body
        parts = re.split(r"^---$", content, flags=re.MULTILINE)
        if len(parts) < 3:
            continue
        
        yaml_content = parts[1]
        body_content = "---".join(parts[2:])
        
        try:
            metadata = yaml.safe_load(yaml_content)
        except Exception as e:
            print(f"Error parsing YAML in {filename}: {e}")
            continue
        
        if metadata is None:
            metadata = {}

        seen_speakers = set()
        
        def replace_label(match):
            time_part = match.group(1)
            original_speaker = match.group(2)
            
            # Normalize logic:
            # 1. Direct match in mapping (A column)
            if original_speaker in mapping:
                norm_name = mapping[original_speaker]
                seen_speakers.add(norm_name)
                return f"- **{time_part} {norm_name}**:"
            
            # 2. Rescue from "名前が不足 " corruption
            if original_speaker in rescue_mapping:
                norm_name = rescue_mapping[original_speaker]
                seen_speakers.add(norm_name)
                return f"- **{time_part} {norm_name}**:"
            
            # 3. Rescue from already-stripped names (e.g. "かりん" -> "実委 かりん")
            if original_speaker in simple_mapping and simple_mapping[original_speaker] is not None:
                norm_name = simple_mapping[original_speaker]
                seen_speakers.add(norm_name)
                return f"- **{time_part} {norm_name}**:"

            # 4. If it is already a canonical name (VALUE in mapping)
            if original_speaker in mapping.values():
                seen_speakers.add(original_speaker)
                return f"- **{time_part} {original_speaker}**:"

            # 5. Check if it's an ignore pattern
            if original_speaker in ignore_names:
                return match.group(0)
            
            # 6. Fallback
            seen_speakers.add(original_speaker)
            return f"- **{time_part} {original_speaker}**:"

        new_body = re.sub(r"- \*\*(\d{1,2}:\d{2}) (.+?)\*\*:", replace_label, body_content)
        
        # Update Metadata
        metadata['speakers'] = sorted(list(seen_speakers))
        
        # Keep original property if it existed (e.g. "登場人物")
        if '登場人物' in metadata:
            metadata['登場人物'] = sorted(list(seen_speakers))
        
        new_yaml = yaml.dump(metadata, allow_unicode=True, sort_keys=False)
        new_content = f"---\n{new_yaml}---\n{new_body}"
        
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(new_content)

    print(f"Processed {len(files)} files.")

if __name__ == "__main__":
    # 1. Parse regex table
    mapping, ignore_names, rescue_mapping, simple_mapping = parse_mapping(REGEX_FILE)
    print(f"Loaded {len(mapping)} mappings, {len(ignore_names)} ignore patterns, {len(rescue_mapping)} rescue patterns, and {len(simple_mapping)} simple patterns.")
    
    # 2. Process logs
    process_logs(mapping, ignore_names, rescue_mapping, simple_mapping)
    print("Normalization complete.")
