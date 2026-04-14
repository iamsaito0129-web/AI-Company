import os
import re
import json
from collections import defaultdict

log_dir = r"c:\Users\iamsa\ローカルプライベートフォルダー\私用(PC)\AI-company\company\hr\members\line_logs"
output_file = r"c:\Users\iamsa\ローカルプライベートフォルダー\私用(PC)\AI-company\scratch\full_entity_map.json"

def analyze_all_entities_v3():
    entities = defaultdict(lambda: {"chats": set(), "interaction_count": 0})
    
    # Common prefixes that are followed by a space but are part of the sender name
    prefixes = ["学校教育", "実委", "常翔", "馬渕", "教職", "西淀", "常翔"]

    def normalize(name):
        n = re.sub(r'(学校教育|実委|馬渕|常翔|教職|PA|②|③|④|①|\d+回生|\d+回|先生|さん|くん|ちゃん|様|🦔|🍡|🐞|🔊|㊙️|☀️|⭐️|神霜|PA)', '', name)
        return n.strip()

    for filename in os.listdir(log_dir):
        if not filename.endswith('.txt'): continue
        path = os.path.join(log_dir, filename)
        chat_name = filename.replace('[LINE]', '').replace('.txt', '').strip()
        
        current_sender = None
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                # LINE format: HH:MM Sender Message
                # Example: 15:35 学校教育 いつき ありがとう
                match = re.match(r'^(\d{2}:\d{2})\s+(.*)', line)
                if match:
                    rest = match.group(2)
                    sender_candidate = ""
                    message = ""
                    
                    # Try to match prefixes first
                    found_prefix = False
                    for p in prefixes:
                        if rest.startswith(p):
                            # Usually "Prefix Name Message"
                            # We look for the next space after the prefix
                            parts = rest.split(' ', 2)
                            if len(parts) >= 2:
                                sender_candidate = f"{parts[0]} {parts[1]}".strip()
                                message = parts[2] if len(parts) > 2 else ""
                                found_prefix = True
                                break
                    
                    if not found_prefix:
                        # Case: "Name Message" (no prefix)
                        parts = rest.split(' ', 1)
                        sender_candidate = parts[0].strip()
                        message = parts[1] if len(parts) > 1 else ""
                    
                    current_sender = sender_candidate
                    entities[current_sender]["chats"].add(chat_name)
                    entities[current_sender]["interaction_count"] += 1
                elif current_sender and line.strip() and not re.match(r'^\d{4}\.\d{2}\.\d{2}', line):
                    entities[current_sender]["interaction_count"] += 1

    result = {}
    for name, data in entities.items():
        result[name] = {
            "normalized": normalize(name),
            "chats": list(data["chats"]),
            "interactions": data["interaction_count"]
        }
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    print(f"Full entity map (v3) saved to {output_file}")

if __name__ == "__main__":
    analyze_all_entities_v3()
