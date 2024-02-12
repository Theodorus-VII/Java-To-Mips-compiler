class Parser():

    def __init__(self):
        self.count = 0       #make sure the label names are unique among loops
        self.pcount = 0      #For Asciiz labels on print calls

        self.tokens = ['+','/','*','-']          
        #the 4 basic ops. should maybe add modulo and ground
        self.types = ["String", "int", "char"]   
        #declerations

        self.line_end = ""
        self.indent_size = " "*4

        self.variables = {}
        self.var_count = 0
        self.variable_mapping = []
            

        # what the program will translate
        # only these will be supported
        self.functions = ["System.out.println", "if", "else", "while", "for"]
        # DONE: PRINT, IF, WHILE

        # maps operations to their mips equivalent
        # just access token[the operation] to get its mips equivalent
        self.token = {
            "+":"add",
            "-": "sub",
            "/": "div",
            "*": "mul"
        }
        
        # not in the scope of what we're doing. skip line if found
        self.useless = ["public", "class", "static"]

        self.operations = {'>':"bgt", '>=':'bge', '<':'blt', '<=':'ble', '==':'beq'}

        self.mips_data_segment = "\n\n#beginning of data segment\n.data \n"  + self.indent_size + r'.asciiz "\n"' +'\n'

    # ````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````
    def convert_function(self, function):
        # isolates the function
        l = function
        function = function.split('\n')
        solution = ''
        for i in range(len(function)):
            function[i] = function[i].strip()

        if 'for' in function[0]:
            solution+=self.indent_size + "\n#FOR LOOP\n#INITIALIZE FIRST\n"
            term = l.strip().translate( { ord(")"): " ", ord("("): " ", ord("}"): None, ord("{"): None }).split()
            initial = term[3]   #variable
            init = term[4]  #value for the variable
            
            # initialize
            solution += self.indent_size + "li {i} {val}\n".format(i = "$t9", val = init.translate({ord(';'): None}))        

            op = term[5]
            o = term[6]
            op2 = term[7]

            # print(term)
            solution += "link{count}:\n".format(count = self.count)
            solution += self.indent_size+"{op} {op1} {op2} while{count}\n".format(op = self.operations[o], op1 = "$t9", op2 = op2.translate({ord(';'): None}), count = self.count)
            solution += self.indent_size+"j normal{count}\n".format(count=self.count)
            solution += "while{count}:\n".format(count = self.count)
            self.line_end += self.indent_size + "addi $t9 $t9 {val}\n".format(val = term[12])
            self.line_end += self.indent_size + "j link{count}\nnormal{count}:\n".format(count = self.count)

            self.variables[term[2]] = "$t9"

            # solution += indent + "{o} {op} {op2} loop{count}\n".format(o = operations[o], op = op, op2 = op2, count = count)
            return solution
        
        
        if ('if') in function[0]:
            solution+=(self.indent_size + "\n#IF CONDITION BEGINS HERE\n")
            op = ''
            term = l.strip().translate( { ord(")"): " ", ord("("): " ", ord("}"): None, ord("{"): None }).split()
            # print(term)
            op1 = term[1]
            op2 = term[3]

            if '<=' in l:
                op = 'ble'
            elif '<' in l:
                op = 'blt'
            if '>=' in l:
                op = 'bge'
            elif '>' in l:
                op = 'bgt'
            if '==' in l:
                op = 'beq'

            operation1 = "li"
            operation2 = "li"
            if op2 in self.variables:
                op2 = self.variables[op2]
                operation2 = "move"
                solution += self.indent_size+"{operation} $t8 {op2}\n".format(op2 = op2, operation = operation2)
            if op1 in self.variables:
                op1 = self.variables[op1]
                operation1 = "move"

            solution += self.indent_size+"{operation} $t7 {op}\n".format(op = op1, operation = operation1)
            

            solution += self.indent_size+"{op} $t7 {op2} if{count}\n".format(op = op, count = self.count, op2=op2)
            solution += self.indent_size+"j else{count}\n".format(count = self.count)
            solution += "if{count}:\n".format(count = self.count)
            self.line_end = self.indent_size+"j normal{count}\nelse{count}:\n".format(count=self.count)
            return(solution)


        if ('else') in function[0]:
            self.line_end = "normal{count}:\n".format(count=self.count-1)
            solution = self.indent_size + "#ELSE CONDITION. ONLY REACHED IF [IF] ISNT EXECUTED.\n"
            return solution


        if ('System.out.println') in function[0]:
            solution += "\n" + self.indent_size + "#PRINT STATEMENT. USES DIFFERENT OPCODE FOR INT AND STRINGS\n"

            term = l.strip().split('"')
            term2 = l.strip().translate( { ord(")"): "|", ord("("): "|", ord("}"): None, ord("{"): None }).split('|')


            if '()' in l:
                solution += self.indent_size+'li $v0 4\n'
                solution += self.indent_size+ 'la $a0 newline\n'
                solution += self.indent_size+"syscall\n\n"
                return(solution)

            if '"' not in term2[1]:
                # determine if the variable is a string or a number
                if term2[1] in self.variables:
                    x = self.variables[term2[1]]
                    if '$t' in x:
                        op = 1
                        load = "move"
                    else:
                        op = 4
                        load = "la"
                else:
                    x = int(term2[1])
                    op = 1
                    load = "li"

            else:
                x = "ToPrint{pcount}".format(pcount = self.pcount)
                # print("TERM",term)
                self.mips_data_segment = self.mips_data_segment + "ToPrint{pcount}:\n".format(pcount=self.pcount)
                op = 4
                load = "la"
                # data_segment += (indent+ r'.asciiz "{string}\n"'.format(string = term[1])+"\n")
                self.mips_data_segment += (self.indent_size+ r'.asciiz "{string}"'.format(string = term[1])+"\n")
                self.pcount+=1
            
            solution += self.indent_size+'li $v0 {op}\n'.format(op = op)
            solution += self.indent_size+ '{load} $a0 {val}\n'.format(val = x, load = load)
            solution += self.indent_size+"syscall\n\n"

            solution += self.indent_size+'li $v0 4\n'
            solution += self.indent_size+ 'la $a0 newline\n'
            solution += self.indent_size+"syscall\n\n"
            return(solution)


        if 'while' in function[0]:
            solution += self.indent_size + "\n#WHILE LOOP. LINK IS THE CONDITION. WHILE IS THE BODY OF THE LOOP. NORMAL IS THE REST OF THE PROGRAM\n"
            solution += self.indent_size + "#NUMBERED LABELS TO AVOID CONFLICTS IF THERE IS ANOTHER LOOP\n"
            op = ''
            term = l.strip().translate( { ord(")"): " ", ord("("): " ", ord("}"): None, ord("{"): None }).split()
            # print("term = ", term)
            op = ''
            if '<=' in l:
                op = 'ble'
            elif '<' in l:
                op = 'blt'
            if '>=' in l:
                op = 'bge'
            elif '>' in l:
                op = 'bgt'
            if '==' in l:
                op = 'beq'

            op1 = term[1]
            op2 = term[3]
            
            if op2 in self.variables:
                op2 = self.variables[op2]
            if op1 in self.variables:
                op1 = self.variables[op1]
            
            solution += "link{count}:\n".format(count = self.count)
            solution += self.indent_size+"{op} {op1} {op2} while{count}\n".format(op = op, op1 = op1, op2 = op2, count = self.count)
            solution += self.indent_size+"j normal{count}\n".format(count=self.count)
            solution += "while{count}:\n".format(count = self.count)
            self.line_end = self.indent_size + "j link{count}\n".format(count = self.count)
            self.line_end += "normal{i}: \n".format(i=str(self.count))
            return(solution)
        
    # ````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````

    # PARSER
    def parser(self, java_code):
        with open('assembly.asm', 'w') as asm_file:
            data_variables = []

            # trackers for functions
            function = ''
            mode = 0
            stor = 'a'

            #Opens java file to write mode so that it can write the input in the java file
            with open('java.java', 'w') as write_java:
                write_java.write(java_code)

            with open('java.java') as java:
                asm_file.write(".text \n.globl main \n\nmain:\n")

                while line := java.readline():
                    temp = line


                    if line.strip() == '':
                        continue

                    if '//' in line:
                        asm_file.write(self.indent_size + "#" + line.translate({ord('/'): ""}).strip() + "\n")
                        continue

                    line = line.translate( { ord(";"): None } )
                    mapping = []
                    strings = {}
                    op = ""     #stores the operation we're using(add, sub,...)

                    ln = line.split()
                    ln[:] = (value for value in ln if value != '')

                    # found one of the functions. sent its first line to the translator function
                    if ln[0] in self.functions or "System.out.println" in ln[0] or 'else' in ln[0]:
                        mode = 1
                        function += temp
                        sol = self.convert_function(function)
                        asm_file.write(sol)
                        function = ''
                        continue


                    if mode == 1:   #function termination check
                        if '}' in line:
                            asm_file.write(self.line_end)
                            self.line_end = ""
                            # asm_file.write("normal{i}: \n".format(i=str(count)))
                            mode = 0
                            self.count += 1
                            pass


                    l = line.strip().translate( { ord(")"): None, ord("("): " ", ord("}"): None, ord("{"): None }).split()


                    if len(l)>0 and l[0] in self.functions:
                        mode = 1

                    operand_stack = []

                    # print(ln)


                    for i in range(len(ln)):
                        term = ln[i]
                        # print(ln)

                        if term == "String":
                            # found a string
                            #only thing doable in this line is assigning a string
                            chk = line.strip().translate({ ord('"'): "|"}).strip('|').split('|')
                            stor = ln[i+1]
                            val = '"{x}"'.format(x=chk[1])
                            self.mips_data_segment += "{stor}:\n".format(stor = stor) + self.indent_size + ".asciiz {val}\n".format(val=val)
                            self.variables[stor] = stor
                            break         
                        
                        if ';' in term:
                            term = term.split(';')[0]
                            continue

                        if term in self.types:
                            continue

                        if term in self.tokens:
                            op = self.token[term]
                            continue

                        if term in self.useless:
                            # a class declaration of a method decleration. Not in the scope of this program
                            # expects all code to be translated to be in one class
                            break

                        if term == "=":
                            stor = ln[i-1]
                            # if there is no operation in the line, its assignment
                            continue

                        try:
                            # check if uve run into a number(int)
                            x = int(term)
                            # uve run into a number
                            # store it in operands
                            operand_stack.append(x)

                        except:
                            if term in self.variables:
                                operand_stack.append(term)
                            if (term =="\n" or term =="}\n" or term =="}"):
                                continue
                            # not a number. must be a var
                            if term not in self.variables:
                                self.variables[term] = "$t{count}".format(count=self.var_count)
                                self.var_count += 1
                            pass


                    # if (op):
                    #     # print(operand_stack)
                    #     # print(op)
                    #     second = operand_stack.pop()
                    #     first = operand_stack.pop()
                    #     if second in variables:
                    #         second = variables[second]
                    #     else:
                    #         asm_file.write(indent+"li $s0 {var}\n".format(var = second))

                    #     if first in variables:
                    #         first = variables[first]
                    #     else: 
                    #         asm_file.write(indent+"li {stor} {var}".format(var = first, stor = variables[stor]))

                    #     asm_file.write(indent + "{op} {stor} {first} {second}\n".format(op = op, stor = variables[stor], second = second, first = first))
                    if (op):
                        second = operand_stack.pop()
                        first = operand_stack.pop()
                        if second in self.variables:
                            second = self.variables[second]
                        else:
                            asm_file.write(self.indent_size+"li $s0 {var}\n".format(var = second))
                            second = '$s0'

                        if first in self.variables:
                            first = self.variables[first]
                        else: 
                            asm_file.write(self.indent_size+"li {stor} {var}\n".format(var = first, stor = self.variables[stor]))
                            first = self.variables[stor]

                        asm_file.write(self.indent_size + "{op} {stor} {first} {second}\n".format(op = op, stor = self.variables[stor], second = second, first = first))
                    else: 
                        if len(operand_stack) > 0 and stor:
                            val = operand_stack.pop()
                            try:
                                val = int(val)
                                asm_file.write(self.indent_size + "li {stor} {val}\n".format(stor = self.variables[stor], val = val))
                            except:
                                asm_file.write(self.indent_size + "la {stor} {val}\n".format(stor = self.variables[stor], val = val))                        
                        # if term isnt in any of the fields
                        # it has to be a variable
                        # again, no error checking. wont check if its preceded by a type declaration


            finale = "\n"+self.indent_size+"li $v0 10\n"+self.indent_size+"syscall\n"
            asm_file.write(finale)
            asm_file.write(self.mips_data_segment)
            print_variables = "\n\n\n#VARIABLE MAPPINGS:  " + str(self.variables)
            asm_file.write(print_variables)
            
        with open('assembly.asm') as asm_file:               
            return asm_file.read()



    # ````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````

    def reset(self):
        self.indent_size = " "*4
        self.mips_data_segment = "\n\n#beginning of data segment\n.data \n" + 'newline:\n' + self.indent_size +r'.asciiz "\n"' +'\n'
        self.count = 0       #make sure the label names are unique among loops
        
        self.pcount = 0      #For Asciiz labels on print calls

        self.line_end = ""

        self.variables = {}
        self.var_count = 0
        self.variable_mapping = []

