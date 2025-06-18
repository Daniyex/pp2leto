def gramstoounces(gramm):
    ounces = gramm/28.3495231
    return ounces


gramm = int(input("input gramm: "))
ounces = gramstoounces(gramm)
print(ounces)
