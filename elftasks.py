import string
import time
from collections import namedtuple


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


def parse_output(output):
    root = Dir("/")
    current_dir = root

    data = iter(output)
    try:
        d = next(data)
        while True:
            if d[0] == '$':
                if d[1] == "cd":
                    if d[2] == ".." and current_dir != root:
                        current_dir = current_dir.parent
                    elif d[2] == "/":
                        current_dir = root
                    else:
                        current_dir = current_dir.dirs[d[2]]
                    d = next(data)
                elif d[1] == "ls":
                    d = parse_ls(data, current_dir)
    except StopIteration:
        return root


def day7():
    data = [line.strip().split(" ") for line in open('input7.txt')]
    start_time = time.time()

    root = parse_output(data)
    dirs = root.flatten()
    task1 = sum([s for s in [d.size() for d in dirs] if s <= 100000])

    task2 = None

    return time.time() - start_time, task1, task2

