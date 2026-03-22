
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
                            id_cnt += 1
    return fm, rm

fm, _ = generate_mapping(5, 5, 10)
print(f"ID 241: {fm[241]}")
