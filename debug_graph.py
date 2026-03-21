
import json
from puzzle_solver_choice import segments, START, GOAL, YELLOWS

print(f"Segments: {len(segments)}")
for s in segments[:3]:
    print(s[:3]) # snode, sdir, enode

reach = {START}
q = [START]
while True:
    new = False
    for sn, sd, en, sp, sm in segments:
        if sn in reach and en not in reach:
            reach.add(en)
            new = True
    if not new: break

all_m = set([START, GOAL] + YELLOWS)
lost = [m for m in all_m if m not in reach]
print(f"Unreachable in SegGraph: {lost}")
