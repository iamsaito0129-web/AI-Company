
from puzzle_solver_final_task import ADJ, fm, rm, YELLOWS, Y_BIT, START, GOAL, WALLS

# Check intermediate IDs for segments
def get_path(s, e, expected_v):
    path = []
    curr = s
    curr_v = expected_v
    while curr != e:
        # Move one step
        poss = [ (n, mv, ev) for n, mv, ev in ADJ[curr] if mv == curr_v ]
        if not poss: return None
        curr, curr_v, curr_exp = poss[0]
        path.append(curr)
        curr_v = curr_exp
    return path

# Target checkpoints
# 241 is (4,4,5,2)
checkpoints = [
    (233, 241, (0,0,1)), # S to 241
    (241, 154, None),    # 241 to 154? 
]

# Wait, I need a valid Hamiltonian path.
# Let's use a small script to find it with 241 added.
YELLOWS_EXT = list(YELLOWS)
if 241 not in YELLOWS_EXT: YELLOWS_EXT.append(241)
YBIT = {tid: 1 << i for i, tid in enumerate(YELLOWS_EXT)}
ALL_M = (1 << len(YELLOWS_EXT)) - 1

def solve():
    segments = []
    mandatory = set([START, GOAL] + YELLOWS_EXT)
    for node in mandatory:
        for nxt, start_v, start_ev in ADJ[node]:
            if nxt in WALLS: continue
            path = [nxt]
            curr = nxt
            curr_v = start_ev
            curr_mask = YBIT.get(curr, 0)
            while True:
                if curr in mandatory:
                    segments.append((node, start_v, curr, curr_v, list(path), curr_mask))
                poss = [ (no, mv, ev) for no, mv, ev in ADJ[curr] if mv == curr_v ]
                if not poss or poss[0][0] in WALLS: break
                new_node, _, next_exp = poss[0]
                if new_node in path: break
                curr = new_node
                path.append(curr)
                curr_mask |= YBIT.get(curr, 0)
                curr_v = next_exp

    def dfs(curr, mask, visited_all, full_path, last_v):
        if mask == ALL_M and curr == GOAL: return full_path
        for snode, sdir, enode, edir, spath, smask in segments:
            if snode != curr: continue
            if last_v and sdir != last_v and curr not in YELLOWS_EXT: continue
            if any(t in visited_all for t in spath): continue
            for t in spath: visited_all.add(t)
            res = dfs(enode, mask | smask, visited_all, full_path + spath, edir)
            if res: return res
            for t in spath: visited_all.remove(t)
        return None

    return dfs(START, YBIT.get(START,0), {START}, [START], None)

sol = solve()
if sol:
    print(sol)
else:
    print("NO_PATH")
