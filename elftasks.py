import time


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

    cals = cals_per_elf(data)
    cals.sort()
    task1 = cals[-1]
    task2 = sum(cals[-3:])

    return time.time() - start_time, task1, task2


class RPSGame:

    winning_moves = {'A': 'B', 'B': 'C', 'C': 'A'}

    @staticmethod
    def is_winner_p1(p1, p2):
        return RPSGame.winning_moves[p2] == p1

    class RPSScorer:

        scores = {'A': 1, 'B': 2, 'C': 3}
        win_scores = {-1: 0, 0: 3, 1: 6}

        @staticmethod
        def score_p2(p1, p2):
            p2_won = RPSGame.is_winner_p1(p2, p1) - RPSGame.is_winner_p1(p1, p2)
            return RPSGame.RPSScorer.win_scores[p2_won] + RPSGame.RPSScorer.scores[p2]

    task1_p2_map = {'X': 'A', 'Y': 'B', 'Z': 'C'}

    @staticmethod
    def score_task1(p1, p2):
        return RPSGame.RPSScorer.score_p2(p1, RPSGame.task1_p2_map[p2])

    losing_moves = {v: k for k, v in winning_moves.items()}

    @staticmethod
    def choose_move(opponent, win):
        if win:
            return RPSGame.winning_moves[opponent]
        else:
            return RPSGame.losing_moves[opponent]

    task2_score_map = {'X': -1, 'Y': 0, 'Z': 1}

    @staticmethod
    def score_task2(p1_move, is_winner_p2):
        if RPSGame.task2_score_map[is_winner_p2]:
            p2_move = RPSGame.choose_move(p1_move, RPSGame.task2_score_map[is_winner_p2] == 1)
        else:
            p2_move = p1_move

        return RPSGame.RPSScorer.score_p2(p1_move, p2_move)


def day2():
    data = [line.strip().split(' ') for line in open('input02.txt')]
    start_time = time.time()

    task1 = sum([RPSGame.score_task1(rnd[0], rnd[1]) for rnd in data])
    task2 = sum([RPSGame.score_task2(rnd[0], rnd[1]) for rnd in data])

    return time.time() - start_time, task1, task2
    