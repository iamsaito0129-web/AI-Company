
def generate_mapping(w, h, d):
    face_mapping = {}
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
                            id_counter += 1
    return face_mapping

fm = generate_mapping(5, 5, 10)
path = [233, 161, 131, 101, 63, 65, 67, 69, 71, 73, 75, 77]
for i in path:
    print(f"{i}: {fm[i]}")
