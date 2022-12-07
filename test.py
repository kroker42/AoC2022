import unittest
import elftasks
from io import StringIO


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
