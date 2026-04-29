import os
import re
import glob
import codecs

base_dir = r'c:\Users\iamsa\ローカルプライベートフォルダー\私用(PC)\AI-company\company\hr\members\line_logs'
files = glob.glob(os.path.join(base_dir, '**', '[LINE]*.txt'), recursive=True)

def process_file(filepath):
    try:
        with codecs.open(filepath, 'r', encoding='utf-8-sig') as f:
            lines = f.readlines()
    except UnicodeDecodeError:
        try:
            with codecs.open(filepath, 'r', encoding='shift_jis') as f:
                lines = f.readlines()
        except Exception as e:
            print(f'Error reading {filepath}: {e}')
            return
            
    print(f'Read {len(lines)} lines from {os.path.basename(filepath)}')

process_file(os.path.join(base_dir, '[LINE]こにたん.txt'))
