import os
import codecs

base_dir = r'c:\Users\iamsa\ローカルプライベートフォルダー\私用(PC)\AI-company\company\hr\members\line_logs'
files = []
for filename in os.listdir(base_dir):
    if filename.startswith('[整理済み]') and filename.endswith('.txt'):
        files.append(os.path.join(base_dir, filename))

files.sort(key=os.path.getsize)
smallest = files[0]

with codecs.open(smallest, 'r', encoding='utf-8') as f:
    print(f.read())
