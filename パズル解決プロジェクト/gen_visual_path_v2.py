
from puzzle_solver_final_task import ADJ, fm, rm, YELLOWS, START, GOAL, WALLS

def bfs(s, e, visited):
    if s == e: return []
    q = [ (s, []) ]
    v = set(visited)
    while q:
        curr, path = q.pop(0)
        for n, _, _ in ADJ[curr]:
            if n == e: return path + [n]
            if n not in v and n not in WALLS:
                v.add(n)
                q.append((n, path + [n]))
    return None

# Sequential path
order = [233, 235, 241, 232, 202, 199, 196, 154, 94, 33, 16, 17, 48, 147, 63, 69, 73, 77]
# I'll just join them
full = [233]
for i in range(len(order)-1):
    seg = bfs(order[i], order[i+1], set(full))
    if seg:
        full.extend(seg)
    else:
        # Try without visited constraint for visual
        seg2 = bfs(order[i], order[i+1], {order[i]})
        if seg2:
            full.extend(seg2)

print(full)
