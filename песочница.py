
import numpy as np


def get_mark(matrix, function, basis):
    c_basis = []
    for i in basis:
        c_basis.append(function[i - 1])
    mark = np.dot(c_basis, matrix) - (np.append([0], function))
    return mark


def countinue(mark_in):
    return any(mark_in[1:] > 0)


def get_basis(matrix):
    basis = []
    for i in range(len(matrix)):
        basis.append(matrix.shape[1] - len(matrix) + i)
    return basis


def add_variables(matrix, function):
    num_new_variables = matrix.shape[0]

    identity_matrix = np.eye(num_new_variables)
    augmented_matrix = np.concatenate((matrix, identity_matrix), axis=1)

    num_existing_variables = len(function)
    new_function = np.append(function, np.zeros(num_new_variables))

    return augmented_matrix, new_function


def recount(matrix_in, index_input, index_output):
    matrix = np.copy(matrix_in)

    pivot_element = matrix[index_output, index_input]
    matrix[index_output] /= pivot_element

    num_rows = matrix.shape[0]
    for i in range(num_rows):
        if i != index_output:
            multiplier = matrix[i, index_input]
            matrix[i] -= multiplier * matrix[index_output]

    return matrix


def index_input(mark):
    return np.argmax(mark)


def index_output(index_input, matrix_in):
    matrix = np.copy(matrix_in)
    p_i = matrix[:, index_input].copy()
    p_i[p_i == 0] = -1

    p_0 = matrix[:, 0]
    teta = p_0 / p_i

    teta[teta <= 0] = np.inf
    index_output = np.argmin(teta)

    if teta[index_output] == np.inf:
        raise Exception("Нет решений")
    else:
        return index_output


def solve(matrix, function, basis):
    mark = get_mark(matrix, function, basis)
    flag = countinue(mark)

    while flag:
        indexInput = index_input(mark)
        indexOutput = index_output(indexInput, matrix)
        matrix = recount(matrix, indexInput, indexOutput)
        basis[indexOutput] = indexInput
        mark = get_mark(matrix, function, basis)
        flag = countinue(mark)

    return matrix, function, basis


def to_canon(a, b, c, constraints):
    matrix = np.copy(a)
    vector = np.copy(b)
    function = np.copy(c)

    matrix = np.concatenate((vector.T, matrix), axis=1)
    matrix, function = add_variables(matrix, function)
    basis = get_basis(matrix)

    for i, constraint in enumerate(constraints):
        if constraint == '=':
            pass
        elif constraint == '<':
            matrix[i, -1] = 1
        elif constraint == '>':
            matrix[i, -1] = -1
            function *= -1

    return matrix, function, basis


def simplex(matrix, function, basis):
    matrix, function, basis = solve(matrix, function, basis)
    mark = get_mark(matrix, function, basis)

    p_0 = matrix[:, 0]
    x = np.zeros(len(function))

    original_variable_indices = [b - 1 for b in basis if (b - 1) < len(function)]

    for i, idx in enumerate(original_variable_indices):
        x[idx] = p_0[i]

    x_values = [f"x[{i + 1}] = {x[i]:.0f}" for i in range(len(function))]

    print(", ".join(x_values))

    print(f"f(x) = {mark[0] * -1:.0f}")


def read_data(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()
        constraints = [line.split()[-1] for line in lines[:-2]]
        a = np.array([list(map(float, line.split()[:-1])) for line in lines[:-2]])
        b = np.array([list(map(float, lines[-2].split()))])
        c = np.array(list(map(float, lines[-1].split()))) * -1
    return a, b, c, constraints


def print_simplex_table(matrix, basis):
    num_constraints, num_variables = matrix.shape

    print("Basis\tP0\t", end="")
    for j in range(1, num_variables):
        print(f"P{j}\t", end="")
    print()

    for i in range(num_constraints):
        basis_idx = basis[i] - 1
        constraint_b = matrix[i, 0]

        p_values = matrix[i, 1:num_variables]

        basis_var = f"x[{basis_idx + 1}]"
        constraint_b_str = f"{constraint_b:.2f}"
        p_values_str = "\t".join(f"{p:.2f}" for p in p_values)

        print(f"{basis_var}\t{constraint_b_str}\t{p_values_str}")




def extract_simplex_table_matrix(matrix, basis):
    num_constraints = len(basis)
    num_variables = matrix.shape[1] - 1

    simplex_table_matrix = np.zeros((num_constraints, num_variables + 1), dtype=float)

    for i in range(num_constraints):
        basis_idx = basis[i] - 1
        simplex_table_matrix[i, 0] = float(matrix[i, 0])
        simplex_table_matrix[i, 1:] = matrix[i, 1:num_variables + 1].astype(float)

    return simplex_table_matrix


def extract_added_variables_matrix(matrix, basis, original_variable_count):
    num_constraints = len(basis)
    num_variables = matrix.shape[1] - 1

    added_variables_indices = [i for i in range(original_variable_count, num_variables)]

    added_variables_matrix = np.zeros((num_constraints, len(added_variables_indices)), dtype=float)

    for i in range(num_constraints):
        for j, idx in enumerate(added_variables_indices):
            added_variables_matrix[i, j] = matrix[i, idx + 1]

    return added_variables_matrix


def matrix_with_new_p0(final_matrix_added_variables, final_matrix, vector_range):
    for v in vector_range:
        new_p0 = np.dot(final_matrix_added_variables, v)
        final_matrix[:, 0] = new_p0

    return final_matrix


if __name__== "main":
    np.set_printoptions(suppress=True)
    filename = "C:\\Users\\aayza\\PycharmProjects\\Учебные проекты на пайтон\\data.txt"
    a, b, c, constraints = read_data(filename)
    matrix, function, basis = to_canon(a, b, c, constraints)

    matrix, function, basis = solve(matrix, function, basis)
    simplex(matrix, function, basis)

    final_matrix = extract_simplex_table_matrix(matrix, basis)

    print_simplex_table(matrix, basis)

    print()
    print("-----------Анализ на чувствительность-----------")
    print()

    original_variable_count = len(c)
    final_matrix_added_variables = extract_added_variables_matrix(matrix, basis, original_variable_count)

    vector_range = [
        np.array([500, 500, 10])
    ]

    last_matrix = matrix_with_new_p0(final_matrix_added_variables, final_matrix, vector_range)
    print_simplex_table(last_matrix, basis)