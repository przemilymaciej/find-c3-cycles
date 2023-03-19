import networkx as nx
import numpy as np
import time

def get_matrix():
    print("Wprowadz macierz sasiedztwa")

    matrix = []

    while True:
        try:
            line = input()
        except EOFError:
            break
        matrix.append(line)

    return matrix


def format_matrix(mat_1):
    m1 = []
    for i in mat_1:
        part = []
        for j in i.split(' '):
            part.append(int(j))
        m1.append(part)

    return m1


def get_c3_cycles(cycles):
    c3_cycles = []

    for i in cycles:
        if len(i) == 3:
            c3_cycles.append(i)

    return c3_cycles


def naive_method(matrix):
    start = time.time()

    M = np.matrix(matrix)

    G = nx.convert_matrix.from_numpy_array(M)

    all_cycles = nx.cycle_basis(G)

    c3_cycles = get_c3_cycles(all_cycles)

    end = time.time()

    if c3_cycles:
        print(f"Wszystkie cykle c3 w grafie : {c3_cycles}")
    else:
        print("Graf nie ma cykli c3!")

    print(f"Metoda naiwna zajela: {end-start}s")


def to_dict(matrix):
    adj_dict = {}
    k = -1

    for line in matrix:
        k += 1
        n_bor = -1
        for v in line:
            n_bor += 1
            if v > 0:
                if k in adj_dict.keys():
                    adj_dict[k].append(n_bor)
                else:
                    adj_dict[k] = [n_bor]

    return adj_dict


def dfs(u, color, adj_list):
    color[u] = 'G'
    for v in adj_list[u]:
        if color[v]=='W':
            cycle = dfs(v, color, adj_list)
            if cycle:
                return True
        elif color[v]=='G': # cycle is present
            return True
    color[u] = 'B'
    return False


def dfs_method(matrix):
    start = time.time()
    dictionary = to_dict(matrix)
    color = {}
    cycles = []

    for i in dictionary.keys():
        for u in dictionary.keys():
            color[u] = 'W'

        dfs_res = dfs(i, color, dictionary)

        new_cycle = []
        if dfs_res:
            for k in color:
                if color[k] == 'G':
                    new_cycle.append(k)
            cycles.append(new_cycle)

    unique_c3s = set(tuple(cycle) for cycle in cycles if len(cycle) == 3)

    end = time.time()

    if unique_c3s:
        print(f"Wszystkie cykle c3 w grafie : {unique_c3s}")
    else:
        print("Graf nie ma cykli c3!")

    print(f"Metoda DFS zajela: {end-start}s")



def get_c3_matrix_m(matrix):
    n = len(matrix)
    c3 = []

    for i in range(n):
        for j in range(i + 1, n):
            for k in range(j + 1, n):
                if (matrix[i][j] and matrix[j][k] and matrix[k][i]):
                    c3.append([i, j, k])

    return c3


def matrix_method(matrix):
    start = time.time()

    multiplied = np.matmul(matrix,matrix)

    c3_cycles = get_c3_matrix_m(multiplied)

    end = time.time()

    if c3_cycles:
        print(f"Wszystkie cykle c3 w grafie : {c3_cycles}")
    else:
        print("Graf nie ma cykli c3!")

    print(f"Metoda mnozenia macierzy zajela: {end-start}s")


def choose_method(method, matrix):
    if method != "A" and method != "B" and method != "C":
        print("Taka metoda nie istnieje")
        new_m = input("Ktora metode wybierasz? A - Naiwna, B - DFS, C = Macierzowa \n")
        choose_method(new_m)
    else:
        if method == "A":
            print("Wybrales metode naiwna")
            naive_method(matrix)
        elif method == "B":
            print("Wybrales metode DFS")
            dfs_method(matrix)
        elif method == "C":
            print("Wybrales metode macierzowa")
            matrix_method(matrix)

        return method


def main():
    matrix = format_matrix(get_matrix())

    method = input("Ktora metode wybierasz? A - Naiwna, B - DFS, C = Macierzowa \n")
    choose_method(method, matrix)


main()