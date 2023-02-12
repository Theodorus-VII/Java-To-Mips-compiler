.text 
.globl main 

main:

    #PRINT STATEMENT. USES DIFFERENT OPCODE FOR INT AND STRINGS
    li $v0 4
    la $a0 ToPrint0
    syscall

    li $v0 4
    la $a0 newline
    syscall

    li $t0 4
    li $t1 2
    li $s0 16
    mul $t1 $t1 $s0

    #PRINT STATEMENT. USES DIFFERENT OPCODE FOR INT AND STRINGS
    li $v0 1
    move $a0 $t1
    syscall

    li $v0 4
    la $a0 newline
    syscall

    li $s0 3
    div $t1 $t1 $s0
    li $s0 2
    div $t0 $t0 $s0

    #PRINT STATEMENT. USES DIFFERENT OPCODE FOR INT AND STRINGS
    li $v0 1
    move $a0 $t1
    syscall

    li $v0 4
    la $a0 newline
    syscall


    #PRINT STATEMENT. USES DIFFERENT OPCODE FOR INT AND STRINGS
    li $v0 4
    la $a0 y
    syscall

    li $v0 4
    la $a0 newline
    syscall


    #PRINT STATEMENT. USES DIFFERENT OPCODE FOR INT AND STRINGS
    li $v0 1
    li $a0 123
    syscall

    li $v0 4
    la $a0 newline
    syscall

    
#IF CONDITION BEGINS HERE
    move $t7 $t0
    beq $t7 2 if0
    j else0
if0:
    li $s0 1
    add $t1 $t1 $s0

    #PRINT STATEMENT. USES DIFFERENT OPCODE FOR INT AND STRINGS
    li $v0 4
    la $a0 ToPrint1
    syscall

    li $v0 4
    la $a0 newline
    syscall

    j normal0
else0:
    #ELSE CONDITION. ONLY REACHED IF [IF] ISNT EXECUTED.
    li $s0 100
    add $t1 $t1 $s0

    #PRINT STATEMENT. USES DIFFERENT OPCODE FOR INT AND STRINGS
    li $v0 4
    la $a0 ToPrint2
    syscall

    li $v0 4
    la $a0 newline
    syscall

normal0:
    li $t2 2
    
#WHILE LOOP. LINK IS THE CONDITION. WHILE IS THE BODY OF THE LOOP. NORMAL IS THE REST OF THE PROGRAM
    #NUMBERED LABELS TO AVOID CONFLICTS IF THERE IS ANOTHER LOOP
link2:
    ble $t2 4 while2
    j normal2
while2:

    #PRINT STATEMENT. USES DIFFERENT OPCODE FOR INT AND STRINGS
    li $v0 4
    la $a0 ToPrint3
    syscall

    li $v0 4
    la $a0 newline
    syscall

    li $s0 1
    add $t2 $t2 $s0
    j link2
normal2: 
    
#FOR LOOP
#INITIALIZE FIRST
    li $t9 0
link3:
    blt $t9 4 while3
    j normal3
while3:

    #PRINT STATEMENT. USES DIFFERENT OPCODE FOR INT AND STRINGS
    li $v0 4
    la $a0 ToPrint4
    syscall

    li $v0 4
    la $a0 newline
    syscall


    #PRINT STATEMENT. USES DIFFERENT OPCODE FOR INT AND STRINGS
    li $v0 1
    move $a0 $t9
    syscall

    li $v0 4
    la $a0 newline
    syscall

    addi $t9 $t9 1
    j link3
normal3:

    #PRINT STATEMENT. USES DIFFERENT OPCODE FOR INT AND STRINGS
    li $v0 1
    move $a0 $t1
    syscall

    li $v0 4
    la $a0 newline
    syscall


    li $v0 10
    syscall


#beginning of data segment
.data 
newline:
    .asciiz "\n"
ToPrint0:
    .asciiz "HELLO FIRST ATTEMPT"
y:
    .asciiz "Hello World"
ToPrint1:
    .asciiz "NO"
ToPrint2:
    .asciiz "YEEEES"
ToPrint3:
    .asciiz "yes*3"
ToPrint4:
    .asciiz "yeeeeeees*4"



#VARIABLE MAPPINGS:  {'x': '$t0', 'p': '$t1', 'y': 'y', 'i': '$t2', 'k': '$t9'}