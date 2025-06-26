import os

file_path = input("Enter the full path of the file to delete: ")

if os.path.exists(file_path):
    if os.access(file_path, os.W_OK):
        try:
            os.remove(file_path)
            print(f"File '{file_path}' has been deleted.")
        except Exception as e:
            print(f"An error occurred while deleting the file: {e}")
    else:
        print(f"No permission to delete the file '{file_path}'.")
else:
    print(f"The file '{file_path}' does not exist.")
 