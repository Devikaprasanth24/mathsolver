from math_api.sympy_solver import solve_expression_step_by_step
import json

problems = [
    "2x + 4 = 10",
    "3x - 5 = 7",
    "x/2 + 3 = 8",
    "5 = 2x - 1"
]

for p in problems:
    print(f"\n--- Problem: {p} ---")
    steps = solve_expression_step_by_step(p)
    for s in steps:
        print(s)
