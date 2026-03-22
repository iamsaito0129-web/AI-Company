
from puzzle_solver_choice import ADJ, WALLS, START, YELLOWS, GOAL

visited = {START}
q = [START]
while q:
    c = q.pop(0)
    for n, v in ADJ[c]:
        if n not in visited and n not in WALLS:
            visited.add(n)
            q.append(n)

m = [y for y in YELLOWS if y not in visited]
print('Unreachable YELLOWS:', m)
print('Goal reachable:', GOAL in visited)
