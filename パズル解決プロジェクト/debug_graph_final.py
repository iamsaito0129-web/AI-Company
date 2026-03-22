
from puzzle_solver_final import ADJ, WALLS, START, YELLOWS, GOAL, Y_BIT, fm

segments = []
mandatory = set([START, GOAL] | YELLOWS)

for start_node in mandatory:
    for nxt, move_v, next_exp_v in ADJ[start_node]:
        if nxt in WALLS: continue
        path = [nxt]
        curr = nxt
        curr_mask = Y_BIT.get(curr, 0)
        curr_exp = next_exp_v
        while True:
            if curr in mandatory:
                segments.append((start_node, move_v, curr, curr_exp, list(path), curr_mask))
            poss = [ (n, mv, ev) for n, mv, ev in ADJ[curr] if mv == curr_exp ]
            if not poss or poss[0][0] in WALLS or poss[0][0] in path: break
            curr, curr_v, curr_exp = poss[0]
            path.append(curr)
            curr_mask |= Y_BIT.get(curr, 0)

reach = {START}
q = [START]
while q:
    c = q.pop(0)
    for sn, sd, en, ed, sp, sm in segments:
        if sn == c and en not in reach:
            reach.add(en)
            q.append(en)

lost = [m for m in mandatory if m not in reach]
print(f"Nodes unreachable in Segment Graph (with 241): {lost}")
