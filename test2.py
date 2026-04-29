import os
import codecs

filepath = r'c:\Users\iamsa\ローカルプライベートフォルダー\私用(PC)\AI-company\company\hr\members\line_logs\[LINE]こにたん.txt'
with codecs.open(filepath, 'r', encoding='utf-8-sig') as f:
    for i in range(10):
        print(repr(f.readline()))
