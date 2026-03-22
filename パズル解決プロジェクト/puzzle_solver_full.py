
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
YELLOW_LIST = [63, 69, 235, 73, 48, 16, 33, 94, 202, 199, 196, 232, 17, 147, 154]
YELLOWS = set(YELLOW_LIST)
Y_BIT = {tid: 1 << i for i, tid in enumerate(YELLOW_LIST)}
ALL_MASK = (1 << len(YELLOW_LIST)) - 1
WALLS = set([243, 108, 79, 98, 128, 158, 226, 224, 221, 219, 214, 212, 209, 207, 231, 194, 49, 50, 51, 54, 56, 37, 38, 39, 42, 44, 2, 114])

segments = []
mandatory = set([START, GOAL]).union(YELLOWS)

for node in mandatory:
    for nxt, start_v, start_ev in ADJ[node]:
        if nxt in WALLS: continue
        path = [nxt]
        curr = nxt
        curr_v = start_ev
        curr_mask = Y_BIT.get(curr, 0)
        while True:
            if curr in mandatory:
                segments.append((node, start_v, curr, curr_v, list(path), curr_mask))
            poss = [n for n, mv, ev in ADJ[curr] if mv == curr_v]
            if not poss or poss[0] in WALLS: break
            # Next step in path
            new_node = poss[0]
            if new_node in path: break
            curr = new_node
            path.append(curr)
            curr_mask |= Y_BIT.get(curr, 0)
            # Find the new curr_v for the next step (could have crossed edge)
            # Actually, my ADJ returns (node, move_v, next_exp_v).
            # If I'm AT curr, moving in curr_v takes me to next_node.
            # I need the next_exp_v from the adj call.
            _, _, next_v = [ (n, mv, ev) for n, mv, ev in ADJ[path[-2]] if n == curr ][0]
            curr_v = next_v

# BFS solver for Hamiltonian
def solve_tsp():
    # State: (curr_node, mask, last_v)
    # Using DFS with pruning
    memo = {}
    
    def dfs(curr, mask, visited_all, last_v, full_path):
        state = (curr, mask, last_v)
        # Using a subset of visited_all (only mandatory) for memo? No, one-stroke rule.
        # But maybe we can ignore minor tiles?
        
        if mask == ALL_MASK and curr == GOAL:
            return full_path
        
        valid_segments = []
        for snode, sdir, enode, edir, spath, smask in segments:
            if snode != curr: continue
            if last_v and sdir != last_v and curr not in YELLOWS: continue
            if any(t in visited_all for t in spath): continue
            valid_segments.append((snode, sdir, enode, edir, spath, smask))
            
        # Priority: segments that gain more mask bits
        valid_segments.sort(key=lambda x: bin(x[5]).count('1'), reverse=True)
            
        for snode, sdir, enode, edir, spath, smask in valid_segments:
            for t in spath: visited_all.add(t)
            res = dfs(enode, mask | smask, visited_all, edir, full_path + spath)
            if res: return res
            for t in spath: visited_all.remove(t)
        return None

    return dfs(START, Y_BIT.get(START, 0), {START}, None, [START])

sys.setrecursionlimit(2000)
print("Solving Hamiltonian for All Yellows...")
res = solve_tsp()
if res: print("Found Solution:", res)
else: print("No solution.")
