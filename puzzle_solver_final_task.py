
import sys

def generate_mapping(w, h, d):
    fm, rm = {}, {}
    id_cnt = 1
    for x in range(w):
        for y in range(h):
            for z in range(d):
                if (x==0 or x==w-1 or y==0 or y==h-1 or z==0 or z==d-1):
                    for i in range(6):
                        if (i==0 and x==w-1) or (i==1 and x==0) or (i==2 and y==h-1) or (i==3 and y==0) or (i==4 and z==d-1) or (i==5 and z==0):
                            fm[id_cnt] = (x, y, z, i)
                            rm[(x,y,z,i)] = id_cnt
                            id_cnt += 1
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
            if (nx, ny, nz, f) in rm: adj[fid].append((rm[(nx,ny,nz,f)], v, v))
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
                    adj[fid].append((rm[(x,y,z,nf)], v, nv))
    return adj

ADJ = get_adj()
START = 233
GOAL = 77
YELLOW_LIST = [63, 69, 235, 73, 48, 16, 33, 94, 202, 199, 196, 232, 17, 147, 154, 241]
YELLOWS = set(YELLOW_LIST)
Y_BIT = {tid: 1 << i for i, tid in enumerate(YELLOW_LIST)}
ALL_MASK = (1 << len(YELLOW_LIST)) - 1
WALLS = set([243, 108, 79, 98, 128, 158, 226, 224, 221, 219, 214, 212, 209, 207, 231, 194, 49, 50, 51, 54, 56, 37, 38, 39, 42, 44, 2, 114])

def solve_final():
    # Build complete segment graph
    mandatory = set([START, GOAL]).union(YELLOWS)
    segments = []
    for node in mandatory:
        for nxt, start_v, start_ev in ADJ[node]:
            if nxt in WALLS: continue
            path = [nxt]
            curr = nxt
            curr_mask = Y_BIT.get(curr, 0)
            curr_v = start_ev
            while True:
                if curr in mandatory:
                    segments.append((node, start_v, curr, curr_v, list(path), curr_mask))
                
                # Check for straight neighbor in ADJ[curr]
                poss = [ (no, mv, ev) for no, mv, ev in ADJ[curr] if mv == curr_v ]
                if not poss or poss[0][0] in WALLS: break
                
                new_node, _, next_exp = poss[0]
                if new_node in path: break # No loops in one segment
                
                curr = new_node
                path.append(curr)
                curr_mask |= Y_BIT.get(curr, 0)
                curr_v = next_exp

    # Search with state: (curr_node, mask, in_v) and visited_tiles_set
    # Using BFS for shortest or any path
    from collections import deque
    # queue: (curr_node, mask, in_v, full_path, visited_tiles_set)
    # But full_path and visited_tiles_set are too large.
    # Let's use DFS with bitmask.
    
    def dfs(curr, mask, visited_tiles, current_full_path, last_v):
        if mask == ALL_MASK and curr == GOAL:
            return current_full_path
        
        # Try segments
        for snode, sdir, enode, edir, spath, smask in segments:
            if snode != curr: continue
            if last_v and sdir != last_v and curr not in YELLOWS: continue
            
            # Check for tile repeat (One-stroke)
            overlap = False
            for t in spath:
                if t in visited_tiles:
                    overlap = True; break
            if overlap: continue
            
            # Recurse
            for t in spath: visited_tiles.add(t)
            res = dfs(enode, mask | smask, visited_tiles, current_full_path + spath, edir)
            if res: return res
            for t in spath: visited_tiles.remove(t)
        
        return None

    return dfs(START, Y_BIT.get(START,0), {START}, [START], None)

sys.setrecursionlimit(5000)
print("Searching for Hamiltonian...")
path = solve_final()
if path:
    print("SUCCESS:")
    print(path)
else:
    print("FAILED.")
