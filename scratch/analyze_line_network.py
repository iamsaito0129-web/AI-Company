import os
import re
import json
from collections import defaultdict

log_dir = r"c:\Users\iamsa\ローカルプライベートフォルダー\私用(PC)\AI-company\company\hr\members\line_logs"
output_file = r"c:\Users\iamsa\ローカルプライベートフォルダー\私用(PC)\AI-company\scratch\line_analysis_result.json"

# People names to look for (from filenames and common patterns)
def analyze_logs():
    network = defaultdict(lambda: {"chats": set(), "interactions": 0, "mentioned_by": defaultdict(int)})
    
    for filename in os.listdir(log_dir):
        if not filename.endswith('.txt'): continue
        path = os.path.join(log_dir, filename)
        
        chat_name = filename.replace('[LINE]', '').replace('.txt', '').strip()
        
        with open(path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            
        for line in lines:
            # Match LINE format: "Time Name Message" or "Date Day"
            # Typical: 11:41 学校教育 いつき 画像
            match = re.match(r'^\d{2}:\d{2}\s+(.*?)\s+(.*)', line)
            if match:
                sender = match.group(1).strip()
                message = match.group(2)
                
                network[sender]["chats"].add(chat_name)
                network[sender]["interactions"] += 1
                
                # Look for mentions @Name or Nameちゃん/さん
                mentions = re.findall(r'[@\s]([^\s@　]{1,10})(?:さん|くん|ちゃん)', message)
                for m in mentions:
                    network[sender]["mentioned_by"][m] += 1

    # Convert sets to lists for JSON
    serializable_network = {}
    for person, data in network.items():
        serializable_network[person] = {
            "chats": list(data["chats"]),
            "interactions": data["interactions"],
            "mentions": dict(data["mentioned_by"])
        }
        
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(serializable_network, f, ensure_ascii=False, indent=2)
    print(f"Analysis complete. Results saved to {output_file}")

if __name__ == "__main__":
    analyze_logs()
