
import sys
from collections import deque

def generate_mapping(w, h, d):
    fm, rm = {}, {}
    id_counter = 1
    for x in range(w):
        for y in range(h):
            for z in range(d):
                if (x==0 or x==w-1 or y==0 or y==h-1 or z==0 or z==d-1):
                    for i in range(6):
                        if (i==0 and x==w-1) or (i==1 and x==0) or (i==2 and y==h-1) or (i==3 and y==0) or (i==4 and z==d-1) or (i==5 and z==0):
                            fm[id_counter] = (x, y, z, i)
                            rm[(x,y,z,i)] = id_counter
                            id_counter += 1
    return fm, rm

W, H, D = 5, 5, 10
fm, rm = generate_mapping(W, H, D)
NORMALS = {0:(1,0,0), 1:(-1,0,0), 2:(0,1,0), 3:(0,-1,0), 4:(0,0,1), 5:(0,0,-1)}

def get_adj():
    adj = {}
    pdirs = {
        0: [(0,1,0), (0,-1,0), (0,0,1), (0,0,-1)], 1: [(0,1,0), (0,-1,0), (0,0,1), (0,0,-1)],
        2: [(1,0,0), (-1,0,0), (0,0,1), (0,0,-1)], 3: [(1,0,0), (-1,0,0), (0,0,1), (0,0,-1)],
        4: [(1,0,0), (-1,0,0), (0,1,0), (0,-1,0)], 5: [(1,0,0), (-1,0,0), (0,1,0), (0,-1,0)],
    }
    for fid in fm:
        x, y, z, f = fm[fid]
        adj[fid] = []
        for v in pdirs[f]:
            nx, ny, nz = x+v[0], y+v[1], z+v[2]
            if (nx, ny, nz, f) in rm: adj[fid].append((rm[(nx,ny,nz,f)], v))
            else:
                nf = -1
                if v==(1,0,0): nf=0
                elif v==(-1,0,0): nf=1
                elif v==(0,1,0): nf=2
                elif v==(0,-1,0): nf=3
                elif v==(0,0,1): nf=4
                elif v==(0,0,-1): nf=5
                if (x,y,z,nf) in rm:
                    on = NORMALS[f]
                    nv = (-on[0], -on[1], -on[2])
                    adj[fid].append((rm[(x,y,z,nf)], nv))
    return adj

ADJ = get_adj()
START = 233
GOAL = 77
YELLOWS = [63, 69, 235, 73, 48, 16, 33, 94, 202, 199, 196, 232, 17, 147, 154]
WALLS = set([243, 108, 79, 98, 128, 158, 226, 224, 221, 219, 214, 212, 209, 207, 231, 194, 49, 50, 51, 54, 56, 37, 38, 39, 42, 44, 2, 114])

YBIT = {tid: 1 << i for i, tid in enumerate(YELLOWS)}
ALL_MASK = (1 << len(YELLOWS)) - 1
mandatory = set([START, GOAL] + YELLOWS)

# Brute force search state: (curr_node, mask, visited_set_as_tuple, last_v)
# 250 faces is small enough to keep full visited set.

def solve_bfs():
    # visited_states stores (curr_node, mask, last_v) -> max_visited_size? 
    # No, Hamiltonian path depends on the specific visited set.
    # But for a small graph, maybe DFS is better.
    
    memo = {}
    
    def dfs(curr, mask, visited_frozen, last_v):
        # Hamiltonian path on 250 nodes is hard, but turn constraints prune it.
        state = (curr, mask, last_v, visited_frozen)
        
        if curr == GOAL and mask == ALL_MASK:
            return [GOAL]
        
        # We can't use a simple memo because visited set is unique.
        
        for nxt, v in ADJ[curr]:
            if nxt in visited_frozen or nxt in WALLS: continue
            if last_v and v != last_v and curr not in YELLOWS:
                continue
            
            new_mask = mask | YBIT.get(nxt, 0)
            res = dfs(nxt, new_mask, visited_frozen | frozenset([nxt]), v)
            if res:
                return [curr] + res
        return None

    # Let's use Iterative Deepening or a restricted search?
    # Wait! The segment approach WAS correct. Let's fix it.
    pass

# Completing segment graph more robustly
segments = []
for node in mandatory:
    for nxt, vec in ADJ[node]:
        if nxt in WALLS: continue
        # Trace path
        curr = nxt
        path = [curr]
        mask = YBIT.get(curr, 0)
        
        # Stop at ANY mandatory node? No, if we pass through one, we keep going straight.
        # But we record EVERY mandatory node we hit as a possible "End Node" for a turn.
        while True:
            if curr in mandatory:
                segments.append((node, vec, curr, path[:], mask))
                # Note: We can CONTINUE straight past a yellow Tile.
            
            next_steps = [n for n, v in ADJ[curr] if v == vec]
            if not next_steps or next_steps[0] in WALLS or next_steps[0] in path:
                break
            curr = next_steps[0]
            path.append(curr)
            if curr in YBIT: mask |= YBIT[curr]

def solve_final():
    # DFS on segments
    def dfs_seg(curr, mask, visited_all, full_path, last_v):
        if curr == GOAL and mask == ALL_MASK:
            return full_path
        
        for snode, sdir, enode, spath, smask in segments:
            if snode != curr: continue
            if last_v and sdir != last_v and curr not in YELLOWS: continue
            
            # Check overlap
            if any(tid in visited_all for tid in spath): continue
            
            # Recurse
            for tid in spath: visited_all.add(tid)
            res = dfs_seg(enode, mask | smask, visited_all, full_path + spath, sdir)
            if res: return res
            for tid in spath: visited_all.remove(tid)
        return None

    return dfs_seg(START, YBIT.get(START, 0), {START}, [START], None)

print("Running refined Segment Solver...")
sol = solve_final()
if sol: print("Found Solution:", sol)
else: print("No solution.")
