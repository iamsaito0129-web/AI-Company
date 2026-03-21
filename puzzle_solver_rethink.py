
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

def get_full_adj():
    # Returns (node, from_dir) -> list of (nxt_node, to_dir, is_turn_on_node)
    # A move is "surface-straight" if it continues in the same surface-direction.
    # We'll use global vectors to trace, but define "surface-straight" at edges.
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
                # Same face: Straight if vector matches
                adj[fid].append((rm[(nx,ny,nz,f)], v, False))
            else:
                # Crossing edge
                nf = -1
                if v==(1,0,0): nf=0
                elif v==(-1,0,0): nf=1
                elif v==(0,1,0): nf=2
                elif v==(0,-1,0): nf=3
                elif v==(0,0,1): nf=4
                elif v==(0,0,-1): nf=5
                if (x,y,z,nf) in rm:
                    on = NORMALS[f]
                    # This move (v) is a "Surface Straight" if we continue on the NEW face nf.
                    # The natural next direction ON face nf is -on.
                    nv = (-on[0], -on[1], -on[2])
                    # Crucially: From the perspective of the node fid, 
                    # moving into neighbor face nf is a SINGLE step.
                    # Is this step a "Turn" relative to the PREVIOUS step?
                    # If the previous step arrived with vector 'prev_v', 
                    # and our NEW step starts with vector 'v'.
                    # This step is straight if v == prev_v.
                    adj[fid].append((rm[(x,y,z,nf)], v, False)) # Wait, 'v' is the vector that gets us to nf
                    # But once we ARE at nf, we must move with 'nv'.
                    # This is complex. Let's simplify.
    return adj

# BETTER APPROACH: Adjacency as (curr_node, in_vector) -> (next_node, out_vector, is_turn)
def build_choice_graph():
    # A step moves from node A to node B.
    # If A and B are same face, vector is constant.
    # If A and B are different faces, vector changes from v1 to v2.
    # But it's ONE step.
    pass

# Redefining Straight:
# p_id -> c_id (vec1) -> n_id (vec2)
# is_straight = (vec1 == vec2) if same face.
# If crossing edge at c_id: vec1 matches the edge-direction v. 
# And vec2 must be the natural continuation (-normal_of_prev_face).

def is_surf_straight(p_id, c_id, n_id):
    px, py, pz, pf = fm[p_id]
    cx, cy, cz, cf = fm[c_id]
    nx, ny, nz, nf = fm[n_id]
    
    v1 = (cx-px, cy-py, cz-pz)
    v2 = (nx-cx, ny-cy, nz-cz)
    
    if pf == cf:
        # Arrived at c_id via v1.
        if cf == nf:
            return v1 == v2
        else:
            # Crossing edge at c_id.
            # v1 was local on face cf. v2 is local on face nf.
            # This is straight if v2 == -NORMAL[cf].
            # AND v1 must be the direction that points to face nf.
            # (e.g. if nf is +x face, v1 must be (1,0,0)).
            return v2 == (-NORMALS[cf][0], -NORMALS[cf][1], -NORMALS[cf][2])
    else:
        # Cross happened p_id -> c_id. 
        # So we are now on face cf.
        # The vector that got us to c_id was actually unique.
        # This is getting messy. Let's use the 4 directions "Up, Down, Left, Right" per face.
        pass

# I'll use local 2D coordinates for each face to define "Straight".
# Face 0 (+x): (y, z). 1 (-x): (y, z). 2 (+y): (x, z). 3 (-y): (x, z). 4 (+z): (x, y). 5 (-z): (x, y).
# ... This is exactly what the "v2 == -Normal[cf]" logic does!
