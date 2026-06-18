from sympy import symbols, sqrt, limit

n = symbols('n')
term_n = (2 * n ** 2 - n) / sqrt(n ** 5 + 5)
term_n_plus_1 = (2 * (n + 1) ** 2 - (n + 1)) / sqrt((n + 1) ** 5 + 5)
ratio = term_n_plus_1 / term_n
ratio_limit = limit(ratio, n, float('inf'))
print(ratio_limit)
