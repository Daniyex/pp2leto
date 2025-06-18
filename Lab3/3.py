def solve(heads, legs):
    for chickens in range(heads + 1):
        rabbits = heads - chickens
        if 2 * chickens + 4 * rabbits == legs:
            print(f"Chickens: {chickens}, Rabbits: {rabbits}")
            return
    print("No solution found.")

heads = int(input())
legs = int(input())
solve(heads,legs)
