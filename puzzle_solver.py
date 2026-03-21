
# 3D Route Puzzle Solver v4 - Hamiltonian Path Case
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
                    for i in range(6):
                        is_out = (i == 0 and x == w - 1) or (i == 1 and x == 0) or (i == 2 and y == h - 1) or (i == 3 and y == 0) or (i == 4 and z == d - 1) or (i == 5 and z == 0)
                        if is_out:
                            face_mapping[id_counter] = (x, y, z, i)
                            reverse_mapping[(x, y, z, i)] = id_counter
                            id_counter += 1
    return face_mapping, reverse_mapping

W, H, D = 5, 5, 10
face_mapping, reverse_mapping = generate_mapping(W, H, D)

# Puzzle Constraints
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
            # Same face
            if (nx, ny, nz, f) in reverse_mapping:
                adj[fid].append((reverse_mapping[(nx, ny, nz, f)], (dx, dy, dz)))
            else:
                # Edge fold
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

adj = get_adj()

# Optimization: Precompute target mapping
target_mask = {tid: 1 << i for i, tid in enumerate(YELLOW_IDS)}
ALL_TARGETS_MASK = (1 << len(YELLOW_IDS)) - 1

sol_path = []

def solve_hamiltonian(curr, visited_all, mask, last_vec, path):
    # Success condition
    if curr == GOAL_ID:
        if mask == ALL_TARGETS_MASK:
            return path
        return None
    
    # Pruning: If path exists to goal but too short? 
    # With 15 targets, we just DFS.
    
    # Sort neighbors: prioritize moving towards targets or keeping straight?
    # Actually, the turn constraint is the main pruner.
    for nxt, vec in adj[curr]:
        if nxt in visited_all or nxt in WALL_IDS: continue
        
        # Turn Constraint: White must continue last_vec
        if last_vec is not None:
            if vec != last_vec:
                if curr not in YELLOW_SET:
                    continue # Must be straight
        
        # Update state
        new_mask = mask
        if nxt in target_mask:
            new_mask |= target_mask[nxt]
        
        visited_all.add(nxt)
        path.append(nxt)
        res = solve_hamiltonian(nxt, visited_all, new_mask, vec, path)
        if res: return res
        path.pop()
        visited_all.remove(nxt)
    
    return None

sys.setrecursionlimit(10000)
print("Starting Hamiltonian Solver...")
start_mask = target_mask[START_ID] if START_ID in target_mask else 0
init_path = [START_ID]
result = solve_hamiltonian(START_ID, {START_ID}, start_mask, None, init_path)

if result:
    print("Found solution:")
    print(result)
else:
    print("No solution found.")
