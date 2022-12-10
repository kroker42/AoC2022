import string
import time
from collections import namedtuple
from itertools import accumulate
from operator import mul
from operator import add
from operator import sub
from operator import abs
from numpy import sign


def cals_per_elf(data):
    cals = [0]

    for d in data:
        if d is not None:
            cals[-1] += d
        else:
            cals.append(0)

    return cals


def day1():
    data = [int(line.strip()) if line != '\n' else None for line in open('input01.txt')]
    start_time = time.time()

    cals = sorted(cals_per_elf(data))
    task1 = cals[-1]
    task2 = sum(cals[-3:])

    return time.time() - start_time, task1, task2


class RPSGame:
    winning_moves = {'A': 'B', 'B': 'C', 'C': 'A'}

    @staticmethod
    def is_winner_p1(p1, p2):
        return RPSGame.winning_moves[p2] == p1

    class RPSScorer:
        @staticmethod
        def score_p2(p1, p2):
            scores = {'A': 1, 'B': 2, 'C': 3}
            win_scores = {-1: 0, 0: 3, 1: 6}

            p2_won = RPSGame.is_winner_p1(p2, p1) - RPSGame.is_winner_p1(p1, p2)
            return win_scores[p2_won] + scores[p2]

    @staticmethod
    def score_task1(p1, p2):
        task1_p2_map = {'X': 'A', 'Y': 'B', 'Z': 'C'}
        return RPSGame.RPSScorer.score_p2(p1, task1_p2_map[p2])

    @staticmethod
    def choose_move(opponent, win):
        losing_moves = {v: k for k, v in RPSGame.winning_moves.items()}
        return RPSGame.winning_moves[opponent] if win else losing_moves[opponent]

    @staticmethod
    def score_task2(p1_move, is_winner_p2):
        task2_score_map = {'X': -1, 'Y': 0, 'Z': 1}

        if task2_score_map[is_winner_p2]:
            p2_move = RPSGame.choose_move(p1_move, task2_score_map[is_winner_p2] == 1)
        else:
            p2_move = p1_move

        return RPSGame.RPSScorer.score_p2(p1_move, p2_move)


def day2():
    data = [line.strip().split(' ') for line in open('input02.txt')]
    start_time = time.time()

    task1 = sum([RPSGame.score_task1(rnd[0], rnd[1]) for rnd in data])
    task2 = sum([RPSGame.score_task2(rnd[0], rnd[1]) for rnd in data])

    return time.time() - start_time, task1, task2


def backpack_intersect(backpacks):
    isect = set(next(backpacks))
    for b in backpacks:
        isect = isect.intersection(b)
    return next(iter(isect))


def divide_list(l, n):
    for i in range(0, len(l), n):
        yield iter(l[i:i + n])


def compartment_intersect(b):
    return backpack_intersect(divide_list(b, len(b) // 2))


def item_priority(i):
    if i in string.ascii_lowercase:
        return ord(i) - ord('a') + 1
    else:
        return ord(i) - ord('A') + 27


def day3():
    data = [line.strip() for line in open('input3.txt')]
    start_time = time.time()

    task1 = sum(map(item_priority, [compartment_intersect(b) for b in data]))
    task2 = sum(map(item_priority, [backpack_intersect(g) for g in divide_list(data, 3)]))

    return time.time() - start_time, task1, task2


def contains_p(l):
    return contains(l[0], l[1])


def contains(a, b):
    if a[0] < b[0]:
        return b[1] <= a[1]
    elif b[0] < a[0]:
        return a[1] <= b[1]

    # a.start == b.start, so one must contain the other
    return True


def overlap(l):
    a = range(l[0][0], l[0][1] + 1)
    b = range(l[1][0], l[1][1] + 1)
    return b.start in a or b.stop - 1 in a or a.start in b or a.stop - 1 in b


def day4():
    data = [line.strip().split(',') for line in open('input4.txt')]
    data = [[list(map(int, p.split('-'))) for p in pair] for pair in data]
    start_time = time.time()

    task1 = sum(map(contains_p, data))
    task2 = sum(map(overlap, data))

    return time.time() - start_time, task1, task2


def parse_towers(data):
    towers = []
    line = next(data)

    while not line[1].isdigit():
        towers.append(line[1::4])
        line = next(data)

    stacks = [[] for i in range(len(towers[0]))]

    for layer in reversed(towers):
        for i in range(len(layer)):
            if layer[i] != ' ':
                stacks[i].append(layer[i])

    return stacks


def move_crate(stacks, move):
    for i in range(move[0]):
        stacks[move[2] - 1].append(stacks[move[1] - 1].pop())


def move_crate_2(stacks, move):
    stacks[move[2] - 1] = stacks[move[2] - 1] + stacks[move[1] - 1][-move[0]:]
    stacks[move[1] - 1] = stacks[move[1] - 1][0:-move[0]]


def move_crates(move_fn, stacks, moves):
    crates = [x.copy() for x in stacks]
    for move in moves:
        move_fn(crates, move)
    top_crates = []
    for s in crates:
        top_crates.append(s.pop())

    return ''.join(top_crates)


def day5():
    data = (line for line in open('input5.txt'))
    start_time = time.time()

    stacks = parse_towers(data)
    next(data)  # empty line
    moves = [line.strip().split(' ')[1::2] for line in data]
    moves = [list(map(int, x)) for x in moves]

    task1 = move_crates(move_crate, stacks, moves)
    task2 = move_crates(move_crate_2, stacks, moves)

    return time.time() - start_time, task1, task2


def find_unique(sequence, n):
    for i in range(len(sequence) - n):
        if len(set(sequence[i:i + n])) == n:
            yield i + n


def day6():
    data = open('input6.txt').readline().strip()
    start_time = time.time()

    finder = find_unique(data, 4)
    task1 = next(finder)

    finder = find_unique(data, 14)
    task2 = next(finder)

    return time.time() - start_time, task1, task2


File = namedtuple("File", "name size")


class Dir:

    def __init__(self, name, parent=None):
        self.name = name
        self.parent = parent
        self.dirs = {}
        self.files = []

    def size(self):
        return sum(map(Dir.size, self.dirs.values())) + sum([f.size for f in self.files])

    def flatten(self):
        dirs = list(self.dirs.values())

        for d in self.dirs.values():
            dirs += d.flatten()

        return dirs

def parse_ls(data, current_dir):
    d = next(data)

    while d[0] != "$":
        if d[0] == "dir":
            current_dir.dirs[d[1]] = Dir(d[1], current_dir)
        else:
            current_dir.files.append(File(d[1], int(d[0])))
        d = next(data)

    return d


def change_dir(new_dir_name, current_dir, root):
    new_dir = None
    if new_dir_name == ".." and current_dir != root:
        new_dir = current_dir.parent
    elif new_dir_name == "/":
        new_dir = root
    else:
        new_dir = current_dir.dirs[new_dir_name]

    return new_dir

def parse_output(output):
    root = Dir("/")
    current_dir = root

    data = iter(output)
    try:
        d = next(data)
        while True:
            if d[0] == '$':
                if d[1] == "cd":
                    current_dir = change_dir(d[2], current_dir, root)
                    d = next(data)
                elif d[1] == "ls":
                    d = parse_ls(data, current_dir)
    except StopIteration:
        return root


def day7():
    data = [line.strip().split(" ") for line in open('input7.txt')]
    start_time = time.time()

    root = parse_output(data)
    dirs = [root] + root.flatten()
    dir_sizes = [d.size() for d in dirs]
    task1 = sum([s for s in dir_sizes if s <= 100000])

    free_memory = 70000000 - root.size()
    space_needed = 30000000 - free_memory
    large_dirs = [d for d in dir_sizes if d >= space_needed]
    task2 = min(large_dirs)

    return time.time() - start_time, task1, task2


def visible_trees(trees, r, c):
    height = trees[r][c]
    visible_trees = [0] * 4

    for tree in reversed(trees[r][:c]):
        visible_trees[0] += 1
        if tree >= height:
            break

    for tree in trees[r][c + 1:]:
        visible_trees[1] += 1
        if tree >= height:
            break

    for row in reversed(trees[:r]):
        visible_trees[2] += 1
        if row[c] >= height:
            break

    for row in trees[r + 1:]:
        visible_trees[3] += 1
        if row[c] >= height:
            break

    score = 1
    for i in visible_trees:
        score *= i
    return score


def map_visible_trees(trees):
    cols = len(trees[0])
    rows = len(trees)

    visible = [[0] * cols for row in trees]
    for r in range(rows):
        for c in range(cols):
            visible[r][c] = visible_trees(trees, r, c)

    return max([max(row) for row in visible])


def is_visible(trees, r, c):
    height = trees[r][c]
    visible = [1] * 4

    for tree in trees[r][:c]:
        if tree >= height:
            visible[0] = 0

    for tree in trees[r][c+1:]:
        if tree >= height:
            visible[1] = 0

    for row in trees[:r]:
        if row[c] >= height:
            visible[2] = 0

    for row in trees[r+1:]:
        if row[c] >= height:
            visible[3] = 0

    return sum(visible) > 0


def count_visible_trees(trees):
    cols = len(trees[0])
    rows = len(trees)

    visible = [[0] * cols for row in trees]
    visible[0] = [1] * cols
    visible[-1] = [1] * cols
    for row in visible:
        row[0] = 1
        row[-1] = 1

    for r in range(rows):
        for c in range(cols):
            if not visible[r][c]:
                visible[r][c] = is_visible(trees, r, c)

    return sum([sum(row) for row in visible])


def day8():
    trees = [list(map(int, line.strip())) for line in open('input8.txt')]
    start_time = time.time()

    task1 = count_visible_trees(trees)
    task2 = map_visible_trees(trees)

    return time.time() - start_time, task1, task2
    

def move_snake(snake, move):
    move_map = {'R': [0, 1], 'L': [0, -1], 'U': [1, 0], 'D': [-1, 0]}
    step = move_map[move[0]]

    head = snake[0]
    tail = snake[-1]

    visited = []

    for i in range(move[1]):
        head[0] += step[0]
        head[1] += step[1]

        for seg in range(0, len(snake) - 1):
            steps = list(map(sub, snake[seg], snake[seg + 1]))
            dist = list(map(abs, steps))
            if sum(dist) > 1:
                if not(dist[0] == dist[1] and dist[1] == 1):
                    t_step = sign(steps)
                    snake[seg+1][0] += t_step[0]
                    snake[seg+1][1] += t_step[1]
                    visited.append(tuple(tail))

    return visited


def slither_snake(snake, moves):
    visited = set([(0, 0)])

    for m in moves:
        visited.update(move_snake(snake, m))

    return len(visited)


def day9():
    moves = [line.strip().split(" ") for line in open('input9.txt')]
    moves = [(m[0], int(m[1])) for m in moves]
    start_time = time.time()

    snake = [[0, 0] for i in range(2)]
    task1 = slither_snake(snake, moves)

    snake = [[0, 0] for i in range(10)]
    task2 = slither_snake(snake, moves)

    return time.time() - start_time, task1, task2
    

def cycle_x(ops):
    values = [1]
    for op in ops:
        values.append(values[-1])
        if op[0] == "addx":
            values.append(values[-1] + int(op[1]))

    return values

def day10():
    data = [line.strip().split(" ") for line in open('input10.txt')]
    start_time = time.time()

    values = cycle_x(data)
    signals = [c * values[c-1] for c in [20, 60, 100, 140, 180, 220]]
    task1 = sum(signals)

    task2 = None

    return time.time() - start_time, task1, task2
    