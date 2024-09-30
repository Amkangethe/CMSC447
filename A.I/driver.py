import importlib.util
import ai

def check_library_installed():
    # open the file containing library names
    with open('A.I/libraries.txt', 'r') as file:
        # Iterate over each line (library name) in the file
        for library in file:
            library = library.strip()  # Remove newline and extra spaces

            if not library:  # Skip empty lines
                continue

            try:
                # Check if the library is installed
                spec = importlib.util.find_spec(library)
                if spec is not None:
                    print(f"'{library}' is installed.")
                else:
                    print(f"'{library}' is not installed. Try \"pip install {library}\" to install")
                    exit()
            except Exception as e:
                print(f"An error occurred while checking '{library}': {e}")


        


if __name__ == "__main__":
    check_library_installed()
    dog = ai.ai_assistant()

    while(True):
        userInput = input("What do you want to tell me: ")
        dog.get_response(userInput, True)