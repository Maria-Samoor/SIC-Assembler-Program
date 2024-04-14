# Pass One
# pass_one: Performs pass one assembler functionality. It creates SYMTAB (Symbol Table), LITTAB (Literal Table), and Intermediate file.
from tkinter import *

def pass_one(input_file_path="sic_input.asm", intermediate_file_path="intermediate_file.mdt", symtab_file_path="symbol_table.txt", littab_file_path="literal_table.txt"):
    """Assembles the SIC assembly code and generates output files.

    Args:
        input_file_path (str): Path to the input assembly file.
        intermediate_file_path (str): Path to the output intermediate file.
        symbol_table_path (str): Path to the output symbol table file.
        literal_table_path (str): Path to the output literal table file.

    Returns:
        tuple: A tuple containing (PRGNAME, PRGLTH, LOCCTR)
    """
    with open(input_file_path, "r") as input_file, \
         open(intermediate_file_path, "w") as intermediate_file, \
         open(symtab_file_path, "w") as symtab, \
         open(littab_file_path, "w") as littab_out:
        SYMTAB = {} # Dictionary to store symbols and check their existence before adding new symbol to symtab file
        error = []  # List to store any errors encountered during assembly # Dictionary to store literals and check their existence before adding new literal to littab_out file
        littab = {} # Dictionary containing operation codes for different instructions
        optab = {
            "ADD": "18", "AND": "40", "COMP": "28", "DIV": "24",
            "J": "3C", "JEQ": "30", "JGT": "34", "JLT": "38",
            "JSUB": "48", "LDA": "00", "LDCH": "50", "LDL": "08",
            "LDX": "04", "MUL": "20", "OR": "44", "RD": "D8",
            "RSUB": "4C", "STA": "0C", "STCH": "54", "STL": "14",
            "STSW": "E8", "STX": "10", "SUB": "1C", "TD": "E0",
            "TIX": "2C", "WD": "DC"
        }
        first = input_file.readline()
        if first[11:20].strip() == "START":
            LOCCTR = first[21:38].strip() # Location conunter start
            start1 = LOCCTR # Stast address as a string to be passed to pass two 
            start = int(LOCCTR, 16) # Start address 
            PRGNAME = first[0:10].strip() # Program name
            intermediate_file.write(LOCCTR + " " * 6 + first[0:38])
        else:
            LOCCTR = 0
        for i in input_file.readlines():
            n = i
            string = n[40:70]  
            if (n[11:20].strip() != 'END'):  # Check if this is the end of the program
                LOCCTR = LOCCTR.upper()  # Convert LOCCTR to uppercase
                if n[0] != '.':
                    if len(string) == 0:
                        if (n[11:20].strip() == "LTORG"):
                            intermediate_file.write(" " * 10 + n)
                        else:
                            intermediate_file.write(LOCCTR + " " * 6 + n)
                    else:
                        if (n[11:20].strip() == "LTORG"):
                            intermediate_file.write(" " * 10 + n)
                        else:
                            intermediate_file.write(LOCCTR + " " * 6 + n[0:38] + "\n")

                    if n[0:10].strip() != "":
                        if n[0:10].strip() in SYMTAB:
                            print("error:duplicate symbol : " + n[0:10].strip())
                            error.append("error:duplicate symbol : " + n[0:10].strip())
                        else:
                            space = 18 - len(n[0:10].strip())
                            symtab.write(n[0:10].strip() + " " * space + LOCCTR + "\n")
                            SYMTAB[n[0:10].strip()] = LOCCTR
                    if n[11:19].strip() in optab.keys() or n[11:19].strip() == "WORD":
                        LOCCTR = str(hex(int(LOCCTR, 16) + (3)))[2:]
                    elif n[11:19].strip() == "RESW":
                        temp = int(n[21:38].strip())
                        LOCCTR = str(hex(int(LOCCTR, 16) + (temp) * 3))[2:]
                    elif n[11:19].strip() == "RESB":
                        LOCCTR = str(hex(int(LOCCTR, 16) + int(n[21:38].strip())))[2:]
                    elif n[11:19].strip() == "BYTE":
                        if n[21:38].strip()[0] == "X":
                            LOCCTR = str(hex(int(LOCCTR, 16) + int((len(n[21:38].strip()) - 3) / 2)))[2:]
                        elif n[21:38].strip()[0] == "C":
                            LOCCTR = str(hex(int(LOCCTR, 16) + int((len(n[21:38].strip()) - 3))))[2:]
                    elif n[11:19].strip() == "LTORG":
                        for i in littab:
                            space = 18 - len(i)
                            intermediate_file.write(LOCCTR + " " * 6 + "*" + " " * 10 + i + "\n")
                            littab_out.write(i + " " * space + LOCCTR + "\n")  # Write to LiteralTab.txt
                            SYMTAB[i] = LOCCTR
                            LOCCTR = str(hex(int(LOCCTR, 16) + int(littab[i][0])))[2:]
                        littab = {}
                    if n[21:22] == '=':
                        literal = n[21:38].strip()
                        if literal[1] == 'X':
                            hexco = literal[3:-1]

                            if literal not in littab:
                                littab[literal] = [len(hexco) / 2]
                        elif literal[1] == 'C':
                            hexco = literal[3:-1]

                            if literal not in littab:
                                littab[literal] = [len(hexco)]
                        else:
                            print("ُERROR: NOT Valid Literal : " + literal)
                            error.append("ُERROR: NOT Valid Literal : " + literal)
            else:
                LOCCTR = LOCCTR.upper()  # Convert LOCCTR to uppercase
                intermediate_file.write(" " * 10 + n + '\n')
                if littab:
                    for i in littab:
                        space = 18 - len(i)
                        intermediate_file.write(LOCCTR + " " * 6 + "*" + " " * 10 + i + "\n")
                        littab_out.write(i + " " * space + LOCCTR + "\n")  # Write to LiteralTab.txt
                        SYMTAB[i] = LOCCTR

                        LOCCTR = str(hex(int(LOCCTR, 16) + int(littab[i][0])))[2:]
                else:
                    print("error: invalid opcdce" + n[11:19].strip())
                    error.append("error: invalid opcdce : " + n[11:19].strip())
                    break

        input_file.close()         # Close sic_input.asm
        intermediate_file.close()         # Close intermediate_file.mdt
        symtab.close()      # Close symbol_table.txt
        littab_out.close()  # Close literal_table.txt
        lastaddress = LOCCTR
        programLength = int(lastaddress, 16) - start
        PRGLTH = (hex(int(programLength))[2:]).upper()
        return PRGNAME, PRGLTH, LOCCTR.upper(),SYMTAB,start1, optab, error
    
""" 
 display_gui: Displays the results from pass_one_assembler as a graphical user interface (GUI) at which i used three screens: 
 one for displaying general information about the program,
 one for the symbol table, and one for the literals table.
"""
def display_gui(PRGNAME, PRGLTH, LOCCTR,symtab_file_path="symbol_table.txt", littab_file_path="literal_table.txt"):
    """
    Displays program information, symbol table, and literals table in separate GUI windows.

    Args:
        PRGNAME (str): Program name.
        PRGLTH (str): Program length in hexadecimal format.
        LOCCTR (str): Location counter in hexadecimal format.
        symtab_file_path (str, optional): Path to the symbol table file. Defaults to "SymbolTab.txt".
        littab_file_path (str, optional): Path to the literals table file. Defaults to "LiteralTab.txt".
    """
    def display_screen(title, text, title_text):
        """
        Creates and displays a single GUI screen with title, text, and formatting.

        Args:
            title (str): Title of the screen window.
            text (str): Text content to be displayed.
            title_text (str): Title text for the label within the screen.
        """
        screen = Tk()
        screen.title(title)
        screen.configure(background='#F5EFE7')  # Set background color to #beb2d5
         # Set window position to center of the screen
        screen_width = screen.winfo_screenwidth()
        screen_height = screen.winfo_screenheight()
        window_width = 300  # Set your preferred window width
        window_height = 400  # Set your preferred window height
        x_coordinate = (screen_width - window_width) // 2
        y_coordinate = (screen_height - window_height) // 2
        screen.geometry(f"{window_width}x{window_height}+{x_coordinate}+{y_coordinate}")
        # Title label
        title_label = Label(screen, text=title_text, font=('Sourse Code Pro', 16), fg='#F5EFE7', bg='#4F709C')  # Set title text color to #F5EFE7 and background color to #4F709C
        title_label.pack(fill=BOTH)

        # Content label
        content_label = Label(screen, text=text, font=('Sourse Code Pro', 16), bg='#F5EFE7', fg='#4F709C')  # Set text color to #4F709C and background color to #F5EFE7
        content_label.pack(fill=BOTH)

        screen.mainloop()

    # Display first screen: Program Name, Program Length, Location Counter
    screen1_text = f"Program Name: {PRGNAME}\nProgram Length: {PRGLTH}\nLocation Counter: {LOCCTR}"
    display_screen("PRGINFO", screen1_text, 'Program Information')

    # Read the content of SymbolTab.txt for the second screen
    with open(symtab_file_path, "r") as symtab_file:
        screen2_text = symtab_file.read()
        display_screen("SYMTAB", screen2_text, 'Symbol Table')

    # Read the content of LiteralTab.txt for the third screen
    with open(littab_file_path, "r") as littab_file:
        screen3_text = littab_file.read()
        display_screen("LITTAB", screen3_text, 'Literals Table')

"""
 print_results: Displays the contents of the symbol table and literals table from pass_one
 results as a text format in a cell.
"""
def print_results(symtab_file_path="symbol_table.txt", littab_file_path="literal_table.txt"):
    """
    Displays the contents of the symbol table and literals table.

    Args:
        symtab_file_path (str, optional): Path to the symbol table file. Defaults to "symbol_table.txt".
        littab_file_path (str, optional): Path to the literals table file. Defaults to "literal_table.txt".
    """
    # Print contents of Symbol Table
    with open(symtab_file_path, "r") as symtab_file:
        print("Contents of Symbol Table:")
        for line in symtab_file:
            print(line.strip())

    # Print contents of Literals Table
    with open(littab_file_path, "r") as littab_file:
        print("\nContents of Literals Table:")
        for line in littab_file:
            print(line.strip())

# Pass Two
def pass_two(optab, start1, sym, proglen, objpgm_file_path="object_program.obj", listing_file_path="listing_file.lst", inter_file_path="intermediate_file.mdt"):
    """
    Args:
        optab (dict): Opcode table.
        start1 (str): Program start address.
        sym (dict): Symbols and litterals table.
        proglen (str): Program length.
        objpgm_file (str): Path to the object program file. Defaults to "object_program.obj".
        listing_file (str): Path to the listing file. Defaults to "listing_file.lst".
        inter_file (str): Path to the intermediate file. Defaults to "intermediate_file.mdt".
    """
    objpgm = open(objpgm_file_path, "w") # Write on this file to genrate object program file as the output of pass 2
    listing = open(listing_file_path, "w") # Write on this file to genrate listing file as the output of pass 2
    inter = open(inter_file_path, "r") # Read From intermediate file as input for pass 2

    l = [] # Used to append the object code to it
    addrlist = [] #List containig the addresses 

    # Read lines from intermediate file line by line
    for i in inter.readlines():
        ls = i # Store each line from the intermediate file
        dep = ls[:-1] 
        if len(dep) < 50:
            for j in range(50 - len(dep)):
                dep = dep + " " # Used for padding the line to ensure a consistent length.
        opcode = ls[20:29].strip()
        address = ls[0:5].strip()
        if opcode != "START":
            addrlist.append(address)
        label = ls[10:19].strip()
        operand = ls[30:39].strip()

        if operand[-2:] == ",X":
            operand = operand[:-2]
            sym[operand] = str(hex(int(sym[operand], 16) + int('8000', 16)))[2:]
        if opcode == "START":
            listing.write(ls)
            objpgm.write("H^" + label + "^00" + start1 + "^00" + proglen.upper())
        elif opcode == "END":
            l.append("")
            listing.write(ls)
            tempstr = "\nE^00" + start1
        else:
            if opcode in optab.keys():
                op = optab[opcode]

                if opcode == "RSUB":
                    op += "0000"
                elif operand in sym.keys():
                    op += sym[operand]
                l.append(op)
                listing.write(dep + op + '\n')
            elif opcode == "WORD":
                op = hex(int(operand))
                op1 = str(op)
                op1 = op1[2:]
                if len(op1) < 6:
                    for j in range(6 - len(op1)):
                        op1 = "0" + op1
                l.append(op1)
                listing.write(dep + op1 + '\n')
            elif opcode == "BYTE":
                temp = operand[2:len(operand) - 1]
                if operand[0] == "C":
                    f = ""
                    for j in temp:
                        hexcode = hex(ord(j))
                        tmp = str(hexcode)
                        f += tmp[2:]
                    l.append(f)
                    listing.write(dep + f + '\n')
                elif operand[0] == "X":
                    l.append(temp)
                    listing.write(dep + temp + '\n')
            elif label == "*":
                temp = opcode[3:len(opcode) - 1]
                if opcode[1] == "C":
                    f = ""
                    for j in temp:
                        hexcode = hex(ord(j))
                        tmp = str(hexcode)
                        f += tmp[2:]
                    l.append(f)
                    listing.write(dep + f + '\n')
                elif opcode[1] == "X":
                    l.append(temp)
                    listing.write(dep + temp + "\n")
            else:
                l.append("")
                listing.write(ls)
    i = 0
    while i < len(l):
        addr = addrlist[i]
        cont = 0
        if l[i] != "":
            objpgm.write("\nT^00" + addr.upper() + "^")
            tell = objpgm.tell()
            objpgm.write("  ")
            j = i
            obj_code_length = 0
            while i < len(l) and l[i] != "" and cont < 10:
                objpgm.write("^" + l[i].upper())
                obj_code_length += len(l[i])
                cont += 1
                i += 1
            i = i-1
            taddr = hex(obj_code_length // 2)[2:].upper().zfill(2)
            objpgm.seek(tell)
            objpgm.write(taddr.upper())
            objpgm.seek(0, 2)
        i += 1
    objpgm.write(tempstr)
    objpgm.close()
    inter.close()

"""
handle_errors: Write errors encountered during assembling to a text file.
"""
def handle_errors(error, error_file="error_file.txt"):
    """
    Args:
        error (list): A list containing the errors to be handled.
        error_file (str): The path to the text file where the errors will be written.
                          Defaults to "error_file.txt".
    """
    error_file_path = open(error_file, "w")
    for i in error:
        print(i)
        error_file_path.write(i + '\n')

    error_file_path.close()

"""
main:  Main function to execute the program, performing pass one, pass two, recording errors and displaying results using GUI and print.
"""
# Main function to run the program
def main():
    PRGNAME, PRGLTH, LOCCTR, SYMTAB, start,optab,error = pass_one()
    display_gui(PRGNAME, PRGLTH, LOCCTR)
    print_results()
    pass_two(optab, start, SYMTAB, PRGLTH)
    handle_errors(error)
if __name__ == "__main__":
    main()