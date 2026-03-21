
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

def get_adj_v3():
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
            if (nx, ny, nz, f) in rm:
                # Neighbor on same face
                adj[fid].append((rm[(nx,ny,nz,f)], v, v)) # (node, move_vector, next_expected_vector)
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
                    # Cross to nf: current move is 'v'. Next step must be 'nv' to be straight.
                    adj[fid].append((rm[(x,y,z,nf)], v, nv))
    return adj

ADJ = get_adj_v3()
START = 233
GOAL = 77
YELLOW_IDS = [63, 69, 235, 73, 16, 17, 33, 48, 94, 202, 199, 196, 232, 147, 154]
YELLOWS = set(YELLOW_IDS)
Y_BIT = {tid: 1 << i for i, tid in enumerate(YELLOW_IDS)}
ALL_MASK = (1 << len(YELLOW_IDS)) - 1
WALLS = set([243, 108, 79, 98, 128, 158, 226, 224, 221, 219, 214, 212, 209, 207, 231, 194, 49, 50, 51, 54, 56, 37, 38, 39, 42, 44, 2, 114])

def solve():
    memo = {}
    
    def dfs(curr, mask, visited_all, expected_v, turns):
        if turns > 30: return None # Increased limit
        if curr == GOAL and mask == ALL_MASK:
            return [GOAL]
        
        for nxt, move_v, next_exp_v in ADJ[curr]:
            if nxt in visited_all or nxt in WALLS: continue
            
            is_turn = (expected_v is not None and move_v != expected_v)
            if is_turn:
                if curr not in YELLOWS: continue
                new_turns = turns + 1
            else:
                new_turns = turns
            
            new_mask = mask | Y_BIT.get(nxt, 0)
            visited_all.add(nxt)
            res = dfs(nxt, new_mask, visited_all, next_exp_v, new_turns)
            if res: return [curr] + res
            visited_all.remove(nxt)
        return None

    return dfs(START, Y_BIT.get(START, 0), {START}, None, 0)

sys.setrecursionlimit(5000)
print("Running Surface-Straight Hamiltonian Solver...")
res = solve()
if res: print("Found Solution:", res)
else: print("No solution.")
