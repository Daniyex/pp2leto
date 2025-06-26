import string 

for letter in string.ascii_uppercase:
    filename = f"{letter}.txt"
    with open(filename,'w') as file:
        file.write(f"this is file {filename}\n")

print("26 files created")