
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
                        is_out = False
                        if i == 0 and x == w - 1: is_out = True
                        if i == 1 and x == 0: is_out = True
                        if i == 2 and y == h - 1: is_out = True
                        if i == 3 and y == 0: is_out = True
                        if i == 4 and z == d - 1: is_out = True
                        if i == 5 and z == 0: is_out = True
                        if is_out:
                            face_mapping[id_counter] = (x, y, z, i)
                            reverse_mapping[(x, y, z, i)] = id_counter
                            id_counter += 1
    return face_mapping, reverse_mapping

W, H, D = 5, 5, 10
fm, rm = generate_mapping(W, H, D)

for i in [63, 65, 67, 69, 71, 73, 75, 77]:
    print(f"ID {i}: {fm[i]}")
