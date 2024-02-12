<hr>
TO RUN THE PROGRAM, RUN GUI.PY

SAMPLE JAVA CODE IS PROVIDED IN BACKUPJAVA.JAVA TO DEMONSTRATE OUR CODE.
THIS CAN BE USED TO DEMONSTRATE ALL THE STRUCTURES THAT OUR CODE CAN HANDLE

JAVA CODE HAS TO BE IN A CLASS CALLED JAVA
<hr>

# Java to MIPS compiler

Our project is a simple python script that translates java code into mips assembly code.

The source code is divided into 2 main parts. _j2m_parser.py_ and _gui.py_. 
    it writes the java code provided into _java.java_ and the translated mips code into assembly.asm

j2m_parser.py handles the actual code translation while gui.py is our user interface

parser()
Inside j2m_parser.py are 3 methods. this function is more like a combination of a parser and a lexer. 
It goes through our Java input line by line and separates, tokenizes and classifies the input.

We mainly used WHITESPACE to achieve this, so statements such as conditionals require care when writing. 
        
        for instance if(3<4) will give an error while if(3 < 4) will work fine

This section of our code also handles ARITHMETIC and VARIABLE ASSIGNMENT as well.
If it runs into any special functions, such as System.out.println() or a [for] loop, it passes that line into the functions j2m_parser method.

function_translator()
The function translator method then determines what kind of operation the Java code maps to and translates it.
labels are numbered to keep them unique.

    for the if conditions:
    conditionals are checked before the if label, the if label is executed if they evaluate to true, and the else statement are only executed if false. similar structure is used for while loops and for loops
    normal label is used to resume normal program execution in the mentioned structures

reset()
is a helper function, it only helps reset our global variables. 


For variables, we used temporary registers, so the number of variables available is limited. $t8 and $t9 are also reserved for conditionals and for lops and 

Inside the data segment, we store string values, be it variables or strings that were directly printed.
There is also a line at the end of the mips output that shows our variable mappings. Number variables are set to temporary registers 0-7. $t8 and $t9 are reserved as mentioned.
String variables are mapped to labels. the code handles this automatically

## Screenshots
![alt text](<./screenshots/Screenshot 2024-02-12 195439.png>) 
![alt text](<./screenshots/Screenshot 2024-02-12 195456.png>)
![alt text](<./screenshots/Screenshot 2024-02-12 195534.png>) 