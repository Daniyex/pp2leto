def squares(a, b):
    for i in range(a, b + 1):
        yield i ** 2

start = int(input())
end = int(input())

print(f"Squares from {start} to {end}:")
for square in squares(start, end):
    print(square)
