import unittest
import elftasks
import numpy
from io import StringIO
from collections import deque
from operator import add
from operator import mul



class TestDay1(unittest.TestCase):
    def test_cals(self):
        data = [1000, 2000, 3000, None, 4000, None, 5000, 6000, None, 7000, 8000, 9000, None, 10000]
        cals = elftasks.cals_per_elf(data)
        self.assertEqual(5, len(cals))
        self.assertEqual(24000, max(cals))
        cals.sort()
        self.assertEqual(45000, sum(cals[-3:]))


class TestDay2(unittest.TestCase):
    def test_task1(self):
        self.assertEqual(8, elftasks.RPSGame.score_task1('A', 'Y'))
        self.assertEqual(1, elftasks.RPSGame.score_task1('B', 'X'))
        self.assertEqual(6, elftasks.RPSGame.score_task1('C', 'Z'))

    def test_task2(self):
        self.assertEqual(4, elftasks.RPSGame.score_task2('A', 'Y'))
        self.assertEqual(1, elftasks.RPSGame.score_task2('B', 'X'))
        self.assertEqual(7, elftasks.RPSGame.score_task2('C', 'Z'))


class TestDay3(unittest.TestCase):
    data = """vJrwpWtwJgWrhcsFMMfFFhFp
jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL
PmmdzqPrVvPwwTWBwg
wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn
ttgJtRGJQctTZtZT
CrZsJsPPZsGzwwsLwLmpwMDw"""
    def test_backpack(self):
        self.assertEqual('p', elftasks.compartment_intersect("vJrwpWtwJgWrhcsFMMfFFhFp"))

    def test_priority(self):
        self.assertEqual(1, elftasks.item_priority('a'))
        self.assertEqual(2, elftasks.item_priority('b'))
        self.assertEqual(27, elftasks.item_priority('A'))
        self.assertEqual(52, elftasks.item_priority('Z'))


class TestDay4(unittest.TestCase):
    def test_contains(self):
        self.assertEqual(True, elftasks.contains([1, 7], [1, 4]))
        self.assertEqual(True, elftasks.contains([1, 3], [1, 4]))
        self.assertEqual(True, elftasks.contains([2, 7], [1, 8]))
        self.assertEqual(True, elftasks.contains([2, 7], [1, 7]))
        self.assertEqual(False, elftasks.contains([1, 7], [3, 8]))
        self.assertEqual(False, elftasks.contains([1, 2], [2, 4]))
        self.assertEqual(False, elftasks.contains([1, 2], [3, 4]))

    def test_overlap(self):
        self.assertEqual(True, elftasks.overlap([[1, 7], [1, 4]]))
        self.assertEqual(True, elftasks.overlap([[1, 3], [1, 4]]))
        self.assertEqual(True, elftasks.overlap([[2, 7], [1, 8]]))
        self.assertEqual(True, elftasks.overlap([[2, 7], [1, 7]]))
        self.assertEqual(True, elftasks.overlap([[1, 7], [3, 8]]))
        self.assertEqual(True, elftasks.overlap([[0, 7], [1, 8]]))
        self.assertEqual(True, elftasks.overlap([[1, 2], [2, 4]]))
        self.assertEqual(True, elftasks.overlap([[2, 2], [2, 4]]))
        self.assertEqual(True, elftasks.overlap([[4, 4], [2, 4]]))
        self.assertEqual(False, elftasks.overlap([[1, 2], [3, 4]]))


if __name__ == '__main__':
    unittest.main()


class TestDay5(unittest.TestCase):
    data = """[D]        
[N] [C]    
[Z] [M] [P]
 1   2   3 
 
"""

    moves = """move 1 from 2 to 1
move 3 from 1 to 3
move 2 from 2 to 1
move 1 from 1 to 2"""
    def test_task1(self):
        towers = (line for line in StringIO(self.data))
        stacks = elftasks.parse_towers(towers)
        self.assertEqual([['Z', 'N', 'D'], ['M', 'C'], ['P']], stacks)

        moves = [line.strip().split(' ')[1::2] for line in StringIO(self.moves)]
        moves = [list(map(int, x)) for x in moves]
        elftasks.move_crate(stacks, moves[0])
        self.assertEqual([['Z', 'N', 'D', 'C'], ['M'], ['P']], stacks)
        elftasks.move_crate(stacks, moves[1])
        self.assertEqual([['Z'], ['M'], ['P', 'C', 'D', 'N']], stacks)

    def test_task2(self):
        towers = (line for line in StringIO(self.data))
        stacks = elftasks.parse_towers(towers)

        moves = [line.strip().split(' ')[1::2] for line in StringIO(self.moves)]
        moves = [list(map(int, x)) for x in moves]
        elftasks.move_crate_2(stacks, moves[0])
        self.assertEqual([['Z', 'N', 'D', 'C'], ['M'], ['P']], stacks)
        elftasks.move_crate_2(stacks, moves[1])
        self.assertEqual([['Z'], ['M'], ['P', 'N', 'D', 'C']], stacks)


class TestDay6(unittest.TestCase):
    def test_task1(self):
        data = "bvwbjplbgvbhsrlpgdmjqwftvncz"
        finder = elftasks.find_unique(data, 4)
        self.assertEqual(5, next(finder))


class TestDay7(unittest.TestCase):
    data = """$ cd /
$ ls
dir a
14848514 b.txt
8504156 c.dat
dir d
$ cd a
$ ls
dir e
29116 f
2557 g
62596 h.lst
$ cd e
$ ls
584 i
$ cd ..
$ cd ..
$ cd d
$ ls
4060174 j
8033020 d.log
5626152 d.ext
7214296 k"""

    def test_dir_size(self):
        root = elftasks.Dir("root")
        root.files.append(elftasks.File("", 234))
        root.files.append(elftasks.File("", 45))
        d = elftasks.Dir("d")
        d.files.append(elftasks.File("", 37))
        root.dirs["d"] = d
        self.assertEqual(316, root.size())

    def test_parse(self):
        output = [line.strip().split(" ") for line in StringIO(self.data)]
        self.assertEqual("/", elftasks.parse_output([output[0]]).name)

        root = elftasks.parse_output(output[:7])
        self.assertEqual(2, len(root.dirs))
        self.assertEqual(True, 'a' in root.dirs)
        self.assertEqual(True, 'd' in root.dirs)

        root = elftasks.parse_output(output)
        self.assertEqual(48381165, root.size())


class TestDay8(unittest.TestCase):
    data = """30373
25512
65332
33549
35390"""

    def test_task1(self):
        trees = [list(map(int, line.strip())) for line in StringIO(self.data)]
        self.assertEqual(21, elftasks.count_visible_trees(trees))

    def test_task2(self):
        trees = [list(map(int, line.strip())) for line in StringIO(self.data)]
        self.assertEqual(8, elftasks.visible_trees(trees, 3, 2))
        self.assertEqual(8, elftasks.map_visible_trees(trees))



class TestDay9(unittest.TestCase):
    data = """R 4
U 4
L 3
D 1
R 4
D 1
L 5
R 2"""

    def slither(self, moves, expected):
        snake = [[0, 0], [0, 0]]
        self.assertEqual(expected, elftasks.slither_snake(snake, moves))


    def test_task1(self):
        moves = [line.strip().split(" ") for line in StringIO(self.data)]
        moves = [(m[0], int(m[1])) for m in moves]

        self.assertEqual(13, elftasks.slither_snake([[0, 0], [0, 0]], moves))


class TestDay10(unittest.TestCase):
    def parse(self, data):
        return [line.strip().split(" ") for line in StringIO(data)]
    def test_cycle_x(self):
        data = """noop
addx 3
addx -5"""
        self.assertEqual([1, 1, 1, 4, 4, -1], elftasks.cycle_x(self.parse(data)))

        data = """addx 15
addx -11
addx 6
addx -3
addx 5
addx -1
addx -8
addx 13
addx 4
noop
addx -1"""
        exp = [1, 1] + [x + 1 for x in [15, 15, 4, 4, 10, 10, 7, 7, 12, 12, 11, 11, 3, 3, 16, 16, 20, 20, 20, 19]]
        values = elftasks.cycle_x(self.parse(data))
        self.assertEqual(exp, values)
        self.assertEqual(21, values[20])

        data = """addx 1
addx 5
noop
addx -1
noop
addx 3
addx 29
addx -1
addx -21
addx 5
noop
addx -20"""
        values = elftasks.cycle_x(self.parse(data))
        self.assertEqual([1, 1, 2, 2, 7, 7, 7, 6, 6, 6, 9, 9, 38, 38, 37, 37, 16, 16, 21, 21, 21, 1], values)
        self.assertEqual(21, values[20])

        signals = [c * values[c] for c in [2, 6, 10]]
        self.assertEqual([4, 6 * 7, 10 * 9], signals)

    data = """addx 15
addx -11
addx 6
addx -3
addx 5
addx -1
addx -8
addx 13
addx 4
noop
addx -1
addx 5
addx -1
addx 5
addx -1
addx 5
addx -1
addx 5
addx -1
addx -35
addx 1
addx 24
addx -19
addx 1
addx 16
addx -11
noop
noop
addx 21
addx -15
noop
noop
addx -3
addx 9
addx 1
addx -3
addx 8
addx 1
addx 5
noop
noop
noop
noop
noop
addx -36
noop
addx 1
addx 7
noop
noop
noop
addx 2
addx 6
noop
noop
noop
noop
noop
addx 1
noop
noop
addx 7
addx 1
noop
addx -13
addx 13
addx 7
noop
addx 1
addx -33
noop
noop
noop
addx 2
noop
noop
noop
addx 8
noop
addx -1
addx 2
addx 1
noop
addx 17
addx -9
addx 1
addx 1
addx -3
addx 11
noop
noop
addx 1
noop
addx 1
noop
noop
addx -13
addx -19
addx 1
addx 3
addx 26
addx -30
addx 12
addx -1
addx 3
addx 1
noop
noop
noop
addx -9
addx 18
addx 1
addx 2
noop
noop
addx 9
noop
noop
noop
addx -1
addx 2
addx -37
addx 1
addx 3
noop
addx 15
addx -21
addx 22
addx -6
addx 1
noop
addx 2
addx 1
noop
addx -10
noop
noop
addx 20
addx 1
addx 2
addx 2
addx -6
addx -11
noop
noop
noop"""

    def test_signal(self):
        values = elftasks.cycle_x(self.parse(self.data))
        signals = [c * values[c-1] for c in [20, 60, 100, 140, 180, 220]]
        self.assertEqual([420, 1140, 1800, 2940, 2880, 3960], signals)

    def test_task2(self):
        exp = """##..##..##..##..##..##..##..##..##..##..
###...###...###...###...###...###...###.
####....####....####....####....####....
#####.....#####.....#####.....#####.....
######......######......######......####
#######.......#######.......#######....."""
        values = elftasks.cycle_x(self.parse(self.data))
        image = elftasks.render(values)
        self.assertEqual("##..##..##..##..##..##..##..##..##..##.." , image[0].strip())
        self.assertEqual("#######.......#######.......#######....." , image[-1].strip())


class TestDay11(unittest.TestCase):
    data = """Monkey 0:
  Starting items: 79, 98
  Operation: new = old * 19
  Test: divisible by 23
    If true: throw to monkey 2
    If false: throw to monkey 3

Monkey 1:
  Starting items: 54, 65, 75, 74
  Operation: new = old + 6
  Test: divisible by 19
    If true: throw to monkey 2
    If false: throw to monkey 0

Monkey 2:
  Starting items: 79, 60, 97
  Operation: new = old * old
  Test: divisible by 13
    If true: throw to monkey 1
    If false: throw to monkey 3

Monkey 3:
  Starting items: 74
  Operation: new = old + 3
  Test: divisible by 17
    If true: throw to monkey 0
    If false: throw to monkey 1"""

    def test_monkey_equality(self):
        exp = elftasks.Monkey(0, deque([79, 98]), lambda x: x * 19, 23, 2, 3)
        got = elftasks.monkey_parser([line for line in StringIO(self.data)][:6])[0]
        self.assertEqual(exp.id, got.id)
        self.assertEqual(exp.items, got.items)
        self.assertEqual(exp.op(7), got.op(7))
        self.assertEqual(exp.predicate, got.predicate)
        self.assertEqual(exp.actions, got.actions)
        self.assertEqual(exp, got)

    def test_monkey_add_op(self):
        got = elftasks.monkey_parser([line for line in StringIO(self.data)][14:20])[0]
        self.assertEqual(9, got.op(3))

    def test_monkey_parser(self):
        exp = [elftasks.Monkey(0, deque([79, 98]), lambda a: a * 19, 23, 2, 3),
               elftasks.Monkey(1, deque([54, 65, 75, 74]), lambda a: a + 6, 19, 2, 0),
               elftasks.Monkey(2, deque([79, 60, 97]), lambda a: a * a, 13, 1, 3),
               elftasks.Monkey(3, deque([74]), lambda a: a + 3, 17, 0, 1)]
        self.assertEqual(exp, elftasks.monkey_parser([line for line in StringIO(self.data)]))

    def test_monkey_in_the_middle(self):
        monkeys = elftasks.monkey_parser([line for line in StringIO(self.data)])
        elftasks.play_monkey_in_the_middle(monkeys, lambda a: a // 3)
        items = [m.items for m in monkeys]
        self.assertEqual([deque([20, 23, 27, 26]), deque([2080, 25, 167, 207, 401, 1046]), deque(), deque()], items)

    def test_inspection_count(self):
        monkeys = elftasks.monkey_parser([line for line in StringIO(self.data)])
        for i in range(20):
            elftasks.play_monkey_in_the_middle(monkeys, lambda a: a // 3)
        inspection_count = [m.inspection_count for m in monkeys]
        self.assertEqual([101, 95, 7, 105], inspection_count)

    def test_monkey_in_the_middle_calmer_fn(self):
        monkeys = elftasks.monkey_parser([line for line in StringIO(self.data)])
        multipliers = numpy.prod([m.predicate for m in monkeys])
        for i in range(20):
            elftasks.play_monkey_in_the_middle(monkeys, lambda a: a % multipliers)
        inspection_count = [m.inspection_count for m in monkeys]
        self.assertEqual([99, 97, 8, 103], inspection_count)

