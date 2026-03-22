
from puzzle_solver_final_task import ADJ, fm, rm, YELLOWS, START, GOAL, WALLS

# Pathfinding between pairs
def bfs_path(s, e, visited):
    q = [ (s, [s]) ]
    v = set(visited)
    v.add(s)
    local_visited = {s}
    while q:
        curr, path = q.pop(0)
        if curr == e: return path[1:]
        for n, _, _ in ADJ[curr]:
            if n not in v and n not in local_visited and n not in WALLS:
                local_visited.add(n)
                q.append((n, path + [n]))
    return None

checkpoints = [233, 235, 241, 232, 202, 199, 196, 154, 94, 33, 16, 17, 48, 147, 63, 69, 73, 77]
# Wait, I'll check if these are all connected
full_path = [233]
visited = {233}
for i in range(len(checkpoints)-1):
    segment = bfs_path(checkpoints[i], checkpoints[i+1], visited)
    if segment:
        full_path.extend(segment)
        for t in segment: visited.add(t)
    else:
        print(f"FAILED AT {checkpoints[i]} to {checkpoints[i+1]}")
        break

print(full_path)
