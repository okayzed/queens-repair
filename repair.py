# trying out iterative repair...
# for every piece on the board, evaluate how many conflicts it currently has
# the, go through all other squares for the max conflict piece on its row (or col) and move it to the best one
import random
from board import Board

class RepairingBoard(Board):
    def __init__(self, size=8):
        self._placed = []

        vals = range(size)
        random.shuffle(vals)
        for i in xrange(size):
            self._placed.append((i, vals[i]))

        
        self.__size = size

        Board.__init__(self, size)


    def repair_board(self):
        conflict_counts = self.get_conflict_counts()
        keys = conflict_counts.keys()
        made_movement = False

        for piece in keys:
            if conflict_counts[piece] == 0:
                continue


            self._placed.remove(piece)
            repair_conflicts = self.get_repair_conflicts(piece)

            repair_keys = repair_conflicts.keys()
            random.shuffle(repair_keys)
            repair_keys.sort(key=lambda x: repair_conflicts[x])

            val = repair_keys[0]


            intended = repair_conflicts[val]
            if intended > conflict_counts[piece]:
                self._placed.append(piece)
                continue

            print "MOVING", piece, "TO", val
            made_movement = True

            self._placed.append(val)
            conflict_counts = self.get_conflict_counts()

        return made_movement



    def get_repair_conflicts(self, max_piece):

        dangers = {}
        for i in xrange(self.__size):
            danger = 0
            this_piece = (max_piece[0], i)
            if this_piece in self._placed:
                continue

            if this_piece == max_piece:
                continue

            dangers[this_piece] = 0
            for other_piece in self._placed:
                if self.check_pieces_in_danger(this_piece, other_piece):
                    danger += 1

            dangers[this_piece] = danger

        return dangers

    def solve(self):
        for i in xrange(1000):
            print "ITERATING", i
            if not self.repair_board():
                print "NO MOVEMENTS LEFT"
                break

        
if __name__ == "__main__":
    import sys
    size = 11
    if len(sys.argv) > 1:
        size = int(sys.argv[1])

    b = RepairingBoard(size)
    b.solve()
