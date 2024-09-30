import importlib.util

def check_library_installed():
    with open('libraries.txt', 'r') as file:
        content = file.readlines()
        print(content)
    ''' spec = importlib.util.find_spec(library_name)
    if spec is not None:
        print(f"'{library_name}' is installed.")
    else:
        print(f"'{library_name}' is not installed.")
        '''


if __name__ == "__main__":
    check_library_installed()