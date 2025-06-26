
source_file = 'source.txt'
destination_file = 'destination.txt'

try:
    with open(source_file, 'r') as src, open(destination_file, 'w') as dest:
        for line in src:
            dest.write(line)
    print(f"Contents copied from '{source_file}' to '{destination_file}'.")
except FileNotFoundError:
    print(f"Error: The source file '{source_file}' does not exist.")
except IOError as e:
    print(f"An I/O error occurred: {e}")
