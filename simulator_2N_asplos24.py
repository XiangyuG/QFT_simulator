from util import *
import pdb
import sys

def reverse_LNN(pos, I, r1, N, swap_total):
    for i in range(2 * N - 3):
        if i % 2 == 0:
            for j in range(N - 1, -1, -2):
                if j - 1 < 0:
                    break
                cnode = pos[r1][j]
                tnode = pos[r1][j - 1]
                if cnode < tnode and I[cnode][tnode] == 0 and OK_to_do_control(cnode, I):
                    I[cnode][tnode] = 1
                    pos[r1][j], pos[r1][j - 1] = pos[r1][j - 1], pos[r1][j] 
                    swap_total += 1
                else:
                    break
        else:
            for j in range(N - 2, -1, -2):
                if j - 1 >= N:
                    break
                cnode = pos[r1][j]
                tnode = pos[r1][j - 1]
                if cnode < tnode and I[cnode][tnode] == 0 and OK_to_do_control(cnode, I):
                    I[cnode][tnode] = 1
                    pos[r1][j], pos[r1][j - 1] = pos[r1][j - 1], pos[r1][j] 
                    swap_total += 1
                else:
                    break
    return pos, I, swap_total

def LNN(pos, I, r1, N, swap_total):
    for i in range(2 * N - 3):
        if i % 2 == 0:
            for j in range(0, N, 2):
                if j + 1 >= N:
                    break
                cnode = pos[r1][j]
                tnode = pos[r1][j + 1]
                if cnode < tnode and I[cnode][tnode] == 0 and OK_to_do_control(cnode, I):
                    I[cnode][tnode] = 1
                    pos[r1][j], pos[r1][j + 1] = pos[r1][j + 1], pos[r1][j] 
                    swap_total += 1
                else:
                    break
        else:
            for j in range(1, N, 2):
                if j + 1 >= N:
                    break
                cnode = pos[r1][j]
                tnode = pos[r1][j + 1]
                if cnode < tnode and I[cnode][tnode] == 0 and OK_to_do_control(cnode, I):
                    I[cnode][tnode] = 1
                    pos[r1][j], pos[r1][j + 1] = pos[r1][j + 1], pos[r1][j] 
                    swap_total += 1
                else:
                    break
    return pos, I, swap_total

def consecutive_swap(pos, start_pos, r1, swap_total):
    size = len(pos[0])
    for i in range(start_pos, size, 2):
        if i + 1 >= size:
            break
        pos[r1][i], pos[r1][i + 1] = pos[r1][i + 1], pos[r1][i]
        swap_total += 1
    return pos, swap_total

def INTER_U(pos, I, r1, swap_total):
    size = len(pos[0])
    for i in range(size):
        # CPHASE
        for j in range(size):
            cnode = pos[r1][j]
            tnode = pos[r1 + 1][j]
            if cnode < tnode and I[cnode][tnode] == 0 and OK_to_do_control(cnode, I):
                I[cnode][tnode] = 1
        # SWAP
        if i % 2 == 0:
            pos, swap_total = consecutive_swap(pos, 0, r1, swap_total)
            pos, swap_total = consecutive_swap(pos, 1, r1 + 1, swap_total)
        else:
            pos, swap_total = consecutive_swap(pos, 1, r1, swap_total)
            pos, swap_total = consecutive_swap(pos, 0, r1 + 1, swap_total)
    return pos, I, swap_total

def main(argv):
    if len(argv) != 2:
        print("Usage: python3", argv[0], "<the value of m for 2*m grid>")
        sys.exit(1)
    N = int(argv[1])

    pos = [[],[]]
    for i in range(N):
        pos[0].append(i)
    for i in range(N):
        pos[1].append(i + N)
    up_pos = pos

    # Dependency 2D arrary
    I = []
    for i in range(N * 2):
        l = []
        for j in range(N * 2):
            l.append(0)
        I.append(l)

    swap_total = 0
    total_depth = 0

    total_depth += 4 * N - 6
    up_pos, up_I, swap_total = LNN(up_pos, I, 0, N, swap_total)
    print("up_pos =", up_pos)

    total_depth += N * 2
    up_pos, up_I, swap_total = INTER_U(up_pos, I, 0, swap_total) 
    print("up_pos =", up_pos)

    total_depth += 4 * N - 6
    up_pos, up_I, swap_total = reverse_LNN(up_pos, I, 1, N, swap_total)

    if check_qft_gates(I):
        final_print(up_pos, swap_total, total_depth)

if __name__ == '__main__':
    main(sys.argv)