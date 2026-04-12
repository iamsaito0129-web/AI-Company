import json
import os
import re

def export_to_js():
    base_path = r'c:\Users\iamsa\ローカルプライベートフォルダー\私用(PC)\AI-company\.company\finance\data\master'
    input_file = os.path.join(base_path, 'notion_settlement_raw_v6.json')
    output_path = r'c:\Users\iamsa\ローカルプライベートフォルダー\私用(PC)\AI-company\.company\finance\dashboard\js\data.js'
    
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    try:
        with open(input_file, 'r', encoding='utf-8', errors='replace') as f:
            settlement_data = json.load(f)
            
        formatted_data = []
        for row in settlement_data.get('results', []):
            props = row.get('properties', {})
            
            date_val = 'Unknown'
            for k, v in props.items():
                if v.get('type') == 'date' and v.get('date'):
                    date_val = v['date']['start']
                    break
            
            item = {'date': date_val}
            
            for k, v in props.items():
                if v.get('type') == 'formula':
                    formula = v.get('formula', {})
                    val = 0
                    if formula.get('type') == 'string':
                        s = formula['string']
                        nums = re.findall(r'[0-9,]+', s)
                        if nums: val = int(nums[0].replace(',', ''))
                    elif formula.get('type') == 'number':
                        val = formula['number']
                    
                    item['total_str'] = f'¥ {val:,}'
                    item['total'] = val
                
                if v.get('type') == 'number':
                    num = v.get('number', 0)
                    pid = v.get('id', '')
                    
                    # More robust matching including ID heuristics (already helpful)
                    if 'pay' in k.lower() or pid == 'f%3B%3Co': item['paypay'] = num
                    if 'éè¡' in k or pid == 'S~%3CW': item['bank'] = num
                    if 'é' in k or pid == 'xLc%7B': item['wallet_blue'] = num
                    if 'é»' in k or pid == 'pX%3F%5C': item['wallet_black'] = num
                    if 'ã¸ããã' in k or pid == 'Pmv%3F': item['hesokuri'] = num
                    if 'suica' in k.lower() or pid == '%7Dns%3F': item['suica'] = num
                    
                    # Try to capture anything that looks like a bank or investment if bank is 0
                    if num > 100000 and 'total' not in k.lower():
                        if 'bank' not in item or item['bank'] == 0:
                            item['bank'] = num
            
            for field in ['paypay', 'bank', 'wallet_blue', 'wallet_black', 'hesokuri', 'suica']:
                if field not in item: item[field] = 0
                
            formatted_data.append(item)
            
        formatted_data.sort(key=lambda x: x['date'])
        
        js_content = f'const FINANCE_DATA = {json.dumps(formatted_data, indent=2, ensure_ascii=False)};'
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(js_content)
        print(f'Data exported to {output_path}')
        
    except Exception as e:
        print(f'Error: {e}')

if __name__ == "__main__":
    export_to_js()
