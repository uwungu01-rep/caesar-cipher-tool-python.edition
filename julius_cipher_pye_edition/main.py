import string
from os import system, path
from sys import platform
import tkinter
import tkinter.filedialog

root = tkinter.Tk()
root.withdraw()

COMMAND = [*"12"]

def check(arg1: str, arg2: str) -> bool:
    """
    Check if any of arg1's element exist in arg2, use to determine if a file name is illegal or not
    """
    for k in arg1:
        if k in arg2:
            return True
    return False

def Caesar(user_input: str, shift: int) -> str:
    """
    Process texts. By default, this only encipher texts, input minus shift if you want to decipher texts
    """
    output = ""
    ALPHABET, ALPHABET_UPPER = [*string.ascii_lowercase], [*string.ascii_uppercase]
    shifted =  ALPHABET[shift % 26:] + ALPHABET[:shift % 26]
    shifted_upper = ALPHABET_UPPER[shift % 26:] + ALPHABET_UPPER[:shift % 26]
    for k in user_input:
        if k in ALPHABET:
            output += shifted[ALPHABET.index(k)]
        elif k in ALPHABET_UPPER:
            output += shifted_upper[ALPHABET_UPPER.index(k)]
        else:
            output += k
    return output

def fileProcessor(file_name: str, output_file: str, shift: int) -> None:
    """
    Process the file_name file and put it in output_file
    """
    with open(file_name, encoding = "latin-1") as data:
        with open(output_file, "w", encoding = "latin-1") as out:
            out.write(Caesar(data.read(), shift))

def clear():
    """
    Clear the terminal
    """
    if platform == "win32":
        system("cls")
    else:
        system("clear")

def IsInt(inp: str) -> bool:
    """
    Check if inp is an integer or not. Return True if yes, return False if not 
    """
    try:
        int(inp)
        return True
    except ValueError:
        return False

def main() -> None:
    """
    The main function
    """
    clear()
    while True:
        run = False
        count = 0
        cmd = input("1. Enciphering. \n2. Deciphering. \n3. Exit. \nYour input: ").strip()
        clear()
        if cmd == "3":
            root.destroy()
            clear()
            exit(0)
        elif not cmd:
            print("Invalid input: Empty input. \n")
            continue
        elif cmd not in COMMAND:
            print("Invalid input: Command does not exist. \n")
            continue
        
        while True:
            mode = input("1. Input from keyboard. \n2. Input from file. \n3. Cancel. \nYour input: ").strip()
            clear()
            if mode == "2":
                input_file = tkinter.filedialog.askopenfilename(title="Choose your input file (cancel to go back to menu)", 
                                                                filetypes=[("All files", "*.*")])
                if not input_file:
                    break
            elif mode not in COMMAND:
                print("Invalid input: Mode does not exist. \n")
                continue

            break

        while mode == "2" and input_file:
            output_file = input("""Type the name of your output file, leave empty for the default name (output.txt)
(If the name does not contain an extension then the program will automatically add a .txt extension): """).strip()
            clear()
            if check(output_file, [*'\\/:*?"<>|']) and not output_file:
                print("Invalid input: Illegal file name (file name cannot contains \"\\/:*?\"<>|\"). \n")
            elif output_file == input_file:
                print("Invalid input: Output file cannot be the same name as input file. \n")
            elif not output_file:
                output_file = "output.txt"
                run = True
                break
            elif output_file[len(output_file) - 1] != "." or "." not in output_file:
                output_file += ".txt"
                run = True
                break
        
        while mode == "2" and input_file:
            output_folder = tkinter.filedialog.askdirectory(title="Choose your output folder")
            if output_folder:
                output_dir = path.join(output_folder, output_file)
                break

        while mode == "1":
            user_input = [*input("Your input: ").strip()]
            clear()
            if not user_input:
                print("Invalid input: Empty input. \n")
            else:
                run = True
                break

        while mode != "3" and run:
            print(f"Input: {"".join(user_input)}")
            shift = input("Shift (type / to cancel): ").strip()
            clear()
            if IsInt(shift) and mode == "1":
                if cmd == "1": print(f"Output: {Caesar(user_input, int(shift))}")
                elif cmd == "2": print(f"Output: {Caesar(user_input, -int(shift))}")
            elif IsInt(shift) and mode == "2":
                if cmd == "1": fileProcessor(input_file, output_dir, int(shift))
                elif cmd == "2": fileProcessor(input_file, output_dir, -int(shift))
            elif shift == "/":
                break
            elif not shift:
                print("Invalid input: Empty input. \n")
            else:
                print("Invalid input: Not an integer. \n")
        
if __name__ == "__main__":
    main()
