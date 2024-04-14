# SIC Assembler

## Introduction
This project implements a two-pass assembler for the Simplified Instructional Computer (SIC) architecture. The assembler translates assembly language programs written in SIC assembly code into machine-readable object code.

## Features
* Pass One: Performs the first pass of the assembly process, creating the Symbol Table (SYMTAB), Literal Table (LITTAB), and Intermediate File (intermediate_file.mdt).
* Pass Two: Executes the second pass of the assembly process, generating the final object program file (object_program.obj) and the listing file (listing_file.lst).
* Error Handling: Detects and records errors encountered during the assembly process and stores them in an error file (error_file.txt).
* Graphical User Interface (GUI): Provides a GUI to display program information, symbol table, and literal table.

## Dependencies
* Python 3.x
* Tkinter library (for GUI)

## How to Use
1. Input Assembly Code: Create or provide an input assembly code file (sic_input.asm) in SIC assembly language format.
2. Execute the Assembler: Run the Python script sic_assembler.py.
3. View Results:
   - Program Information, Symbol Table, and Literals Table are displayed in separate windows using the GUI.
   - Additionally, the contents of the Symbol Table and Literals Table are printed in the console.
4. Output Files:
   - Object Program: object_program.obj
   - Listing File: listing_file.lst
   - Symbol Table: symbol_table.txt
   - Literal Table: literal_table.txt
   - Error Log: error_file.txt

## Usage
python sic_assembler.py

## Contributors
* Maria Abu Sammour
* mariaabusamoor@gmail.com
