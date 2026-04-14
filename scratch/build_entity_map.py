import os
import re
import json
from collections import defaultdict

log_dir = r"c:\Users\iamsa\ローカルプライベートフォルダー\私用(PC)\AI-company\company\hr\members\line_logs"
output_file = r"c:\Users\iamsa\ローカルプライベートフォルダー\私用(PC)\AI-company\scratch\full_entity_map.json"

def analyze_all_entities():
    # person -> {display_names: set, chats: set, mentions: set, interactions: int}
    entities = defaultdict(lambda: {"chats": set(), "interaction_count": 0, "messages": []})
    
    # We'll use a rough grouping by "normalized name" (removing titles, schools etc)
    def normalize(name):
        n = re.sub(r'(学校教育|実委|馬渕|常翔|教職|PA|②|③|④|①|\d+回生|\d+回|先生|さん|くん|ちゃん|様|🦔|🍡|🐞|🔊|㊙️|☀️|⭐️|神霜|PA)', '', name)
        return n.strip()

    for filename in os.listdir(log_dir):
        if not filename.endswith('.txt'): continue
        path = os.path.join(log_dir, filename)
        chat_name = filename.replace('[LINE]', '').replace('.txt', '').strip()
        
        with open(path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            
        for line in lines:
            match = re.match(r'^(\d{2}:\d{2})\s+(.*?)\s+(.*)', line)
            if match:
                sender = match.group(2).strip()
                message = match.group(3)
                
                entities[sender]["chats"].add(chat_name)
                entities[sender]["interaction_count"] += 1
                
                # Check for mention patterns in message
                # "iroha(彩華)" or "@Name"
                # Mentions of names with honorifics
                # We'll collect candidates for identity resolution later
                
    # Prepare results
    result = {}
    for name, data in entities.items():
        result[name] = {
            "normalized": normalize(name),
            "chats": list(data["chats"]),
            "interactions": data["interaction_count"]
        }
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    print(f"Full entity map saved to {output_file}")

if __name__ == "__main__":
    analyze_all_entities()
