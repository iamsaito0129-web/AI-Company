
import sys

def generate_mapping(w, h, d):
    face_mapping = {}
    reverse_mapping = {}
    id_counter = 1
    for x in range(w):
        for y in range(h):
            for z in range(d):
                is_outer = (x == 0 or x == w - 1 or y == 0 or y == h - 1 or z == 0 or z == d - 1)
                if is_outer:
                    # 0:+x, 1:-x, 2:+y, 3:-y, 4:+z, 5:-z
                    for i in range(6):
                        is_out = (i==0 and x==w-1) or (i==1 and x==0) or (i==2 and y==h-1) or (i==3 and y==0) or (i==4 and z==d-1) or (i==5 and z==0)
                        if is_out:
                            face_mapping[id_counter] = (x, y, z, i)
                            reverse_mapping[(x, y, z, i)] = id_counter
                            id_counter += 1
    return face_mapping, reverse_mapping

W, H, D = 5, 5, 10
face_mapping, reverse_mapping = generate_mapping(W, H, D)

# Normal mapping
NORMALS = {0:(1,0,0), 1:(-1,0,0), 2:(0,1,0), 3:(0,-1,0), 4:(0,0,1), 5:(0,0,-1)}

def get_adj_v2():
    adj = {}
    # Internal move directions (on face plane)
    plane_dirs = {
        0: [(0,1,0), (0,-1,0), (0,0,1), (0,0,-1)],
        1: [(0,1,0), (0,-1,0), (0,0,1), (0,0,-1)],
        2: [(1,0,0), (-1,0,0), (0,0,1), (0,0,-1)],
        3: [(1,0,0), (-1,0,0), (0,0,1), (0,0,-1)],
        4: [(1,0,0), (-1,0,0), (0,1,0), (0,-1,0)],
        5: [(1,0,0), (-1,0,0), (0,1,0), (0,-1,0)],
    }
    
    for fid in face_mapping:
        x, y, z, f = face_mapping[fid]
        adj[fid] = []
        for dx, dy, dz in plane_dirs[f]:
            nx, ny, nz = x + dx, y + dy, z + dz
            # Same face?
            if (nx, ny, nz, f) in reverse_mapping:
                adj[fid].append((reverse_mapping[(nx, ny, nz, f)], (dx, dy, dz)))
            else:
                # Edge fold
                # The node (x, y, z, f) is at the edge. The direction we move is the NEW normal.
                nf = -1
                if dx == 1: nf = 0
                elif dx == -1: nf = 1
                elif dy == 1: nf = 2
                elif dy == -1: nf = 3
                elif dz == 1: nf = 4
                elif dz == -1: nf = 5
                
                if (x, y, z, nf) in reverse_mapping:
                    # Neighbor is the orthogonal face on the same cube.
                    # NEW direction on face nf is -OriginalNormal.
                    orig_n = NORMALS[f]
                    new_vec = (-orig_n[0], -orig_n[1], -orig_n[2])
                    adj[fid].append((reverse_mapping[(x, y, z, nf)], new_vec))
    return adj

# Simplified Hamiltonian Solver
adj_map = get_adj_v2()
START_ID = 233
GOAL_ID = 77
YELLOW_IDS = [63, 69, 235, 73, 48, 16, 33, 94, 202, 199, 196, 232, 17, 147, 154]
YELLOW_SET = set(YELLOW_IDS)
ALL_TARGETS = (1 << len(YELLOW_IDS)) - 1
Y_BIT = {tid: 1 << i for i, tid in enumerate(YELLOW_IDS)}
WALLS = set([243, 108, 79, 98, 128, 158, 226, 224, 221, 219, 214, 212, 209, 207, 231, 194, 49, 50, 51, 54, 56, 37, 38, 39, 42, 44, 2, 114])

def solve(curr, mask, visited, path, last_v):
    if curr == GOAL_ID:
        if mask == ALL_TARGETS: return path
        return None
    
    # Optional: Pruning
    # if (curr, mask, last_v) in memo: return ...
    
    for nxt, vec in adj_map[curr]:
        if nxt in visited or nxt in WALLS: continue
        
        # turn cond
        if last_v is not None and vec != last_v:
            if curr not in YELLOW_SET:
                continue
        
        new_mask = mask | Y_BIT.get(nxt, 0)
        visited.add(nxt)
        path.append(nxt)
        res = solve(nxt, new_mask, visited, path, vec)
        if res: return res
        path.pop()
        visited.remove(nxt)
    return None

sys.setrecursionlimit(5000)
print("Starting Geodesic Hamiltonian Solver...")
res = solve(START_ID, Y_BIT.get(START_ID, 0), {START_ID}, [START_ID], None)
if res:
    print("Found SOLUTION:", res)
else:
    print("No solution.")
