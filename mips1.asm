.text 
.globl main 

main:

#PRINT STATEMENT. USES DIFFERENT OPCODE FOR INT AND STRINGS
    li $v0 4
    la $a0 ToPrint0
    syscall

    li $t0 4
    li $t1 2
    li $s0 16
    mul $t1 $t1 16

#PRINT STATEMENT. USES DIFFERENT OPCODE FOR INT AND STRINGS
    li $v0 1
    move $a0 $t1
    syscall

    li $s0 3
    div $t1 $t1 3
    li $s0 2
    div $t0 $t0 2

#PRINT STATEMENT. USES DIFFERENT OPCODE FOR INT AND STRINGS
    li $v0 1
    move $a0 $t1
    syscall


#PRINT STATEMENT. USES DIFFERENT OPCODE FOR INT AND STRINGS
    li $v0 4
    la $a0 y
    syscall


#IF CONDITION BEGINS HERE
    move $t7 $t0
    beq $t7 2 if0
    j else0
if0:
    li $s0 1
    add $t1 $t1 1

#PRINT STATEMENT. USES DIFFERENT OPCODE FOR INT AND STRINGS
    li $v0 4
    la $a0 ToPrint1
    syscall

    j normal0
else0:
#ELSE CONDITION. ONLY REACHED IF [IF] ISNT EXECUTED.
    li $s0 100
    add $t1 $t1 100

#PRINT STATEMENT. USES DIFFERENT OPCODE FOR INT AND STRINGS
    li $v0 4
    la $a0 ToPrint2
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

    li $s0 1
    add $t2 $t2 1
    j link2
normal2: 

#FOR LOOP
#INITIALIZE FIRST
    li $t9 0
link3:
    blt $t9 4 while3
    j normal3
while3:
    addi $t9 $t9 1

#PRINT STATEMENT. USES DIFFERENT OPCODE FOR INT AND STRINGS
    li $v0 4
    la $a0 ToPrint4
    syscall

    j link3
normal3:

#PRINT STATEMENT. USES DIFFERENT OPCODE FOR INT AND STRINGS
    li $v0 1
    move $a0 $t1
    syscall


#PRINT STATEMENT. USES DIFFERENT OPCODE FOR INT AND STRINGS
    li $v0 1
    li $a0 123
    syscall


    li $v0 10
    syscall


#beginning of data segment
.data 
ToPrint0:
    .asciiz "HELLO FIRST ATTEMPT\n"
y:
    .asciiz "Hello World\n"
ToPrint1:
    .asciiz "NO\n"
ToPrint2:
    .asciiz "YEEEES\n"
ToPrint3:
    .asciiz "yes*3\n"
ToPrint4:
    .asciiz "yeeeeeees*4\n"



#VARIABLE MAPPINGS:  {'x': '$t0', 'p': '$t1', 'y': 'y', 'i': '$t2'}