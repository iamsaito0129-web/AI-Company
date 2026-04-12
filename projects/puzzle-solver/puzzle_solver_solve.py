import sys
import json
import os

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

NORMALS = {0:(1,0,0), 1:(-1,0,0), 2:(0,1,0), 3:(0,-1,0), 4:(0,0,1), 5:(0,0,-1)}

def get_adj_v3(fm, rm):
    adj = {}
    # NORMALS definitions: 0:+x, 1:-x, 2:+y, 3:-y, 4:+z, 5:-z
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
            # 1. 同じ面内で隣接している場合
            if (nx, ny, nz, f) in rm:
                adj[fid].append((rm[(nx,ny,nz,f)], v, v))
            else:
                # 2. 面を跨ぐ移動 (nx, ny, nz は変わるが f も変わる)
                for nf in range(6):
                    if nf == f: continue
                    if (nx, ny, nz, nf) in rm:
                        # 法線が直交している場合に限り、境界をまたぐ
                        ni, nj = NORMALS[f], NORMALS[nf]
                        if ni[0]*nj[0] + ni[1]*nj[1] + ni[2]*nj[2] == 0:
                            on = NORMALS[f]
                            nv = (-on[0], -on[1], -on[2])
                            adj[fid].append((rm[(nx,ny,nz,nf)], v, nv))
        
        # 3. カドでの移動 (x, y, z は同じだが f だけ変わる)
        for nf in range(6):
            if nf == f: continue
            if (x, y, z, nf) in rm:
                ni, nj = NORMALS[f], NORMALS[nf]
                if ni[0]*nj[0] + ni[1]*nj[1] + ni[2]*nj[2] == 0:
                    # これはカドを曲がる動作。move_v と next_exp_v を nj (新しい面の法線方向) 等で設定し、
                    # 確実に方向転換として検知させる
                    # 便宜上、現在の面 f の法線の逆方向から、新しい面 nf の法線の順方向へ曲がると定義
                    adj[fid].append((rm[(x,y,z,nf)], nj, nj))
    return adj

import time

def solve_puzzle(config):
    start_time = time.time()
    TIMEOUT = 300 # 探索時間をさらに延長
    dim = config['dimensions']
    fm, rm = generate_mapping(dim['w'], dim['h'], dim['d'])
    adj = get_adj_v3(fm, rm)
    
    start_id = config['start'][0]
    goal_id = config['goal'][0]
    yellow_ids = config['yellow']
    walls = set(config['lightblue'])
    
    yellows = set(yellow_ids)
    y_bit = {tid: 1 << i for i, tid in enumerate(yellow_ids)}
    all_mask = (1 << len(yellow_ids)) - 1
    
    memo = {}
    TARGET_TURNS = 16

    # 17番が「曲がり」としてカウントされることを保証する
    # ユーザー指示: 17番が渦巻き(カド/境界)であり、そこを通るときに曲がる
    # 現在の get_adj_v3 で同一座標の別面に移動する際は move_v != next_exp_v となり
    # is_turn が True になる

    def get_dist_to_next_target(node, mask):
        x1, y1, z1, _ = fm[node]
        remaining_y = [tid for tid in yellow_ids if not (mask & y_bit[tid])]
        if not remaining_y:
            x2, y2, z2, _ = fm[goal_id]
        else:
            # 最小マンハッタン距離
            dists = []
            for tid in remaining_y:
                x2, y2, z2, _ = fm[tid]
                dists.append(abs(x1-x2) + abs(y1-y2) + abs(z1-z2))
            return min(dists)
        return abs(x1-x2) + abs(y1-y2) + abs(z1-z2)

    def dfs(curr, mask, visited_mask, last_move_v, turns):
        if time.time() - start_time > TIMEOUT: return None
        if turns > TARGET_TURNS: return None
        
        # 状態圧縮: turns を含める
        state = (curr, mask, last_move_v, turns)
        if state in memo: return memo[state]
        
        if curr == goal_id:
            if mask == all_mask and turns == TARGET_TURNS:
                return [goal_id]

        options = adj[curr][:]
        # ヒューリスティック: 目標に近い、かつ曲がらない方向を優先
        options.sort(key=lambda x: (get_dist_to_next_target(x[0], mask), x[1] != last_move_v if last_move_v else False))
        
        for nxt, move_v, next_exp_v in options:
            if (visited_mask & (1 << nxt)) or nxt in walls: continue
            
            # ターン判定の厳密化
            # 1. 面内での転換 (move_v != last_move_v)
            # 2. 面境界での転換 (move_v != next_exp_v)
            # これを合わせると 17番(境界)での移動が 1回としてカウントされる
            is_turn = (last_move_v is not None and move_v != last_move_v) or (move_v != next_exp_v)
            new_turns = turns + 1 if is_turn else turns
            
            if new_turns > TARGET_TURNS: continue
            
            new_mask = mask | y_bit.get(nxt, 0)
            res = dfs(nxt, new_mask, visited_mask | (1 << nxt), next_exp_v, new_turns)
            if res: 
                memo[state] = [curr] + res
                return memo[state]
            
        memo[state] = None
        return None

    sys.setrecursionlimit(50000)
    start_v_mask = 1 << start_id
    initial_mask = y_bit.get(start_id, 0)
    return dfs(start_id, initial_mask, start_v_mask, None, 0)

if __name__ == "__main__":
    config_path = "puzzle_config.json"
    if not os.path.exists(config_path):
        print(f"Error: {config_path} not found.")
        sys.exit(1)
        
    with open(config_path, "r", encoding="utf-8") as f:
        config = json.load(f)
        
    print("Running Optimized Puzzle Solver...")
    result_path = solve_puzzle(config)
    
    if result_path:
        print("Found Solution!")
        config['solved_route'] = result_path
        with open(config_path, "w", encoding="utf-8") as f:
            json.dump(config, f, indent=4, ensure_ascii=False)
        print(f"Result saved to {config_path}")
    else:
        print("No solution found within constraints.")
