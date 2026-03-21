
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

# Config
START_ID = 233
GOAL_ID = 77
YELLOW_IDS = [63, 69, 235, 73, 48, 16, 33, 94, 202, 199, 196, 232, 17, 147, 154]
YELLOW_SET = set(YELLOW_IDS)
WALL_IDS = set([243, 108, 79, 98, 128, 158, 226, 224, 221, 219, 214, 212, 209, 207, 231, 194, 49, 50, 51, 54, 56, 37, 38, 39, 42, 44, 2, 114])

def get_adj():
    adj = {}
    move_dirs = {
        0: [(0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)],
        1: [(0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)],
        2: [(1, 0, 0), (-1, 0, 0), (0, 0, 1), (0, 0, -1)],
        3: [(1, 0, 0), (-1, 0, 0), (0, 0, 1), (0, 0, -1)],
        4: [(1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0)],
        5: [(1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0)],
    }
    for fid in face_mapping:
        x, y, z, f = face_mapping[fid]
        adj[fid] = []
        for dx, dy, dz in move_dirs[f]:
            nx, ny, nz = x + dx, y + dy, z + dz
            if (nx, ny, nz, f) in reverse_mapping:
                adj[fid].append((reverse_mapping[(nx, ny, nz, f)], (dx, dy, dz)))
            else:
                nf = -1
                if dx == 1: nf = 0
                elif dx == -1: nf = 1
                elif dy == 1: nf = 2
                elif dy == -1: nf = 3
                elif dz == 1: nf = 4
                elif dz == -1: nf = 5
                if (x, y, z, nf) in reverse_mapping:
                    adj[fid].append((reverse_mapping[(x, y, z, nf)], (dx, dy, dz)))
    return adj

adj_map = get_adj()
mandatory = set([START_ID, GOAL_ID] + YELLOW_IDS)

# Precompute segments
segments = [] # (from_id, to_id, list_of_tiles)
for start_node in mandatory:
    for nxt, vec in adj_map[start_node]:
        if nxt in WALL_IDS: continue
        path = [nxt]
        curr = nxt
        curr_v = vec
        while True:
            if curr in mandatory:
                segments.append((start_node, curr, path))
                break
            # Continue straight
            poss = [n for n, v in adj_map[curr] if v == curr_v]
            if not poss or poss[0] in WALL_IDS:
                break
            curr = poss[0]
            path.append(curr)

# DFS on segments
y_mask = {tid: 1 << i for i, tid in enumerate(YELLOW_IDS)}
ALL_TARGETS = (1 << len(YELLOW_IDS)) - 1

def solve_dfs(curr, mask, visited_all, full_path):
    if mask == ALL_TARGETS and curr == GOAL_ID:
        return full_path
    
    for start_node, end_node, path_tiles in segments:
        if start_node != curr: continue
        
        # Check overlaps
        overlap = False
        for t in path_tiles:
            if t in visited_all:
                overlap = True
                break
        if overlap: continue
        
        # New State
        new_mask = mask
        if end_node in y_mask:
            new_mask |= y_mask[end_node]
            
        # Recurse
        for t in path_tiles: visited_all.add(t)
        full_path.extend(path_tiles)
        
        res = solve_dfs(end_node, new_mask, visited_all, full_path)
        if res: return res
        
        # Backtrack
        full_path[len(full_path)-len(path_tiles):] = []
        for t in path_tiles: visited_all.remove(t)
        
    return None

sys.setrecursionlimit(2000)
print("Starting Segment Solver...")
init_mask = y_mask[START_ID] if START_ID in y_mask else 0
sol = solve_dfs(START_ID, init_mask, {START_ID}, [START_ID])

if sol:
    print("Found SOLUTION:")
    print(sol)
else:
    print("No solution found.")
