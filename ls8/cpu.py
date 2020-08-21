"""CPU functionality."""

import sys

# Instantiate instruction codes
HLT = 0b00000001 # exits emulator
LDI = 0b10000010 # sets a specified register to a value
PRN = 0b01000111 # print value stored in register
ADD = 0b10100000 # add value of two registers & store result in registerA
SUB = 0b10100001 # subtract the value in the second register from the first & store result in registerA
MUL = 0b10100010 # multiply the values in two registers & store result in registerA
PUSH = 0b01000101 # push onto the stack
POP = 0b01000110 # pop off the stack
CALL = 0b01010000 # calls a subroutine at address stored in register
RET = 0b00010001 # return from subroutine
CMP = 0b10100111 # compare values in two registers
JMP = 0b01010100 # jump to address stored in given register
JEQ = 0b01010101 # equal if flag is set true
JNE = 0b01010110 # not equal if flag is clear
AND = 0b10101000 # bitwise-AND values in registerA and registerB
OR = 0b10101010 # bitwise-OR values in registerA and registerB
XOR = 0b10101011 # bitwise-XOR values in registerA and registerB
NOT = 0b01101001 # bitwise-NOT on value in a register
SHL = 0b10101100 # shift value in registerA by # of bits specified in registerB
SHR = 0b10101101 # shift value in registerA by # of bits specified in registerB
MOD = 0b10100100 # divide value in registerA by registerB, store remainder

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        # Able to hold 256 bytes of memeory
        self.ram = [0] * 256
        # Able to hold 8 general-purpose registers
        self.reg = [0] * 8
        # Program counter
        self.pc = 0
        # Stack pointer (R7 is reserved as the stack pointer)
        self.sp = 7
        # CPU running
        self.running = True
        # Branch table for run function
        self.branchtable = {
            HLT: self.HLT,
            LDI: self.LDI,
            PRN: self.PRN,
            ADD: self.ADD,
            SUB: self.SUB, 
            MUL: self.MUL,
            PUSH: self.PUSH,
            POP: self.POP,
            CALL: self.CALL,
            RET: self.RET,
            CMP: self.CMP,
            JMP: self.JMP,
            JEQ: self.JEQ,
            JNE: self.JNE,
            AND: self.AND, 
            OR: self.OR,
            XOR: self.XOR,
            NOT: self.NOT,
            SHL: self.SHL,
            SHR: self.SHR,
            MOD: self.MOD,
        }

    def ram_read(self, address):
        """Accept address to read and return stored value"""
        return self.ram[address]

    def ram_write(self, value, address):
        """Accept a value to write, and the address to write it to"""
        self.ram[address] = value
    
    def HLT(self, operand_a=None, operand_b=None):
        """Halt the CPU (and exit the emulator)"""
        self.running = False

    def LDI(self, operand_a, operand_b):
        """Set the value of a register to an integer"""
        # Registers[reg_num] = value
        self.reg[operand_a] = operand_b
        # Increment the program counter 
        self.pc += 3

    def PRN(self, operand_a, operand_b=None):
        """Print numeric value stored in the given register"""
        # Print value in given register
        print(self.reg[operand_a])
        # Increment the program counter
        self.pc += 2

    def ADD(self, operand_a, operand_b):
        """Add value of two registers & store result in registerA"""
        self.alu("ADD", operand_a, operand_b)
        self.pc += 3

    def SUB(self, operand_a, operand_b):
        """Subtract the value in the second register from the first & store result in registerA"""
        self.alu("SUB", operand_a, operand_b)
        self.pc += 3

    def MUL(self, operand_a, operand_b):
        """Multiply the values in two registers & store result in registerA"""
        self.alu("MUL", operand_a, operand_b)
        self.pc += 3

    def PUSH(self, operand_a, operand_b=None):
        """Push the value in the given register on the stack"""
        # Decrement the stack pointer
        self.reg[self.sp] -= 1
        # Take value in register, push it to the top of the stack in memory
        self.ram_write(self.reg[operand_a], self.reg[self.sp])
        # Increment the program counter 
        self.pc += 2

    def POP(self, operand_a, operand_b=None):
        """Pop the value at the top of the stack into the given register"""
        # Take the value off the top of the stack, put it into given register
        self.reg[operand_a] = self.ram_read(self.reg[self.sp])
        # Increment the stack pointer
        self.reg[self.sp] += 1
        # Increment the program counter
        self.pc += 2
    
    def CALL(self, operand_a, operand_b=None):
        """Calls a subroutine (function) at the address stored in the register."""
        # Decrement the stack pointer 
        self.reg[self.sp] -= 1
        # Take the value at pc + 2, store it at the stack pointer
        self.ram_write(self.pc + 2, self.reg[self.sp])
        # Set PC to address stored in given register
        self.pc = self.reg[operand_a]
    
    def RET(self, operand_a=None, operand_b=None):
        """Return from subroutine, pop the value from the top of the stack and store it in pc"""
        # Take the value stored at the stack pointer and put it in pc 
        self.pc = self.ram_read(self.reg[self.sp])
        # Increment the stack pointer
        self.reg[self.sp] += 1
    
    def CMP(self, operand_a, operand_b):
        """Compare the values in two registers"""
        self.alu("CMP", operand_a, operand_b)
        self.pc += 3
    
    def JMP(self, operand_a, operand_b=None):
        """Jump to address stored in the given register, set PC to address stored in given register"""
        self.pc = self.reg[operand_a]

    def JEQ(self, operand_a, operand_b=None):
        """If equal flag is set (true), jump to the address stored in the given register"""
        # If flag is set to equal
        if self.fl == 0b00000001:
            # Jump there (set pc to address stored in register)
            self.pc = self.reg[operand_a]
        else:
            self.pc += 2
    
    def JNE(self, operand_a, operand_b=None):
        """If equal flag is clear (false, 0), jump to the address stored in the given register"""
        # If flag is set to g or l
        if self.fl != 0b00000001:
            # Jump there (set pc to address stored in register)
            self.pc = self.reg[operand_a]
        else:
            self.pc += 2
    
    def AND(self, operand_a, operand_b):
        """Bitwise-AND the values in registerA and registerB, then store the result in registerA"""
        self.alu("AND", operand_a, operand_b)
        self.pc += 3

    def OR(self, operand_a, operand_b):
        """Perform a bitwise-OR between the values in registerA and registerB, storing the result in registerA"""
        self.alu("OR", operand_a, operand_b)
        self.pc += 3
    
    def XOR(self, operand_a, operand_b):
        """Perform a bitwise-XOR between the values in registerA and registerB, storing the result in registerA"""
        self.alu("XOR", operand_a, operand_b)
        self.pc += 3
    
    def NOT(self, operand_a, operand_b=None):
        """Perform a bitwise-NOT on the value in a register, storing the result in the register."""
        self.alu("NOT", operand_a, operand_b)
        self.pc += 2
    
    def SHL(self, operand_a, operand_b):
        """Shift the value in registerA left by the number of bits specified in registerB, filling the low bits with 0."""
        self.alu("SHL", operand_a, operand_b)
        self.pc += 3
    
    def SHR(self, operand_a, operand_b):
        """Shift the value in registerA right by the number of bits specified in registerB, filling the high bits with 0."""
        self.alu("SHR", operand_a, operand_b)
        self.pc += 3
    
    def MOD(self, operand_a, operand_b):
        """Divide the value in the first register by the value in the second, storing the remainder of the result in registerA."""
        self.alu("MOD", operand_a, operand_b)
        self.pc += 3

    def load(self, filename=None):
        """Load a program into memory."""

        address = 0

        # If not being fed 2 programs 
        if len(sys.argv) != 2:
            print("usage: comp.py progname")
            sys.exit(1)

        try:
            with open(filename, 'r') as f:
                for line in f:
                    # Split line at # character, use elements be4 split
                    line = line.split("#")[0].strip()
                    if len(line) == 0:
                        continue
                    # If first character starts with #, ignore it
                    if line[0][0] == '#':
                        continue
                    # Since we're working in binary, have to set base to 2
                    try:
                        self.ram[address] = int(line, 2)
                    # Raise error if not fed appropriate int
                    except ValueError:
                        print(f'Invalid number: {line}')
                        sys.exit(1)
                
                    address += 1
        
        # Not given a valid filename
        except FileNotFoundError:
            print(f"Couldn't open {sys.argv[1]}")
            sys.exit(2)

        # No instructions given
        if address == 0:
            print("Program was empty!")
            sys.exit(3)

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        elif op =='SUB':
            self.reg[reg_a] -= self.reg[reg_b]
        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]
        elif op == "CMP":
            """0b00000LGE"""
            if self.reg[reg_a] == self.reg[reg_b]:
                self.fl = 0b00000001
            elif self.reg[reg_a] < self.reg[reg_b]:
                self.fl = 0b00000100
            elif self.reg[reg_a] > self.reg[reg_b]:
                self.fl = 0b00000010
        elif op == "AND":
            self.reg[reg_a] = self.reg[reg_a] & self.reg[reg_b]
        elif op == "OR":
            self.reg[reg_a] = self.reg[reg_a] | self.reg[reg_b]
        elif op == "XOR":
            self.reg[reg_a] = self.reg[reg_a] ^ self.reg[reg_b]
        elif op == "NOT":
            self.reg[reg_a] = ~self.reg[reg_a]
        elif op == "SHL":
            self.reg[reg_a] = self.reg[reg_a] >> self.reg[reg_b]
        elif op == "SHR":
            self.reg[reg_a] = self.reg[reg_a] << self.reg[reg_b]
        elif op == "MOD":
            if self.reg[reg_b] == 0:
                print("ERROR: Undefined, cannot divide by 0")
                self.running = False
            else:
                self.reg[reg_a] = self.reg[reg_a] % self.reg[reg_b]
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""

        while self.running:
            # Instantiate the instruction register
            ir = self.ram_read(self.pc)
            # Instantiate operand_a, operand_b (reg_num, value) to read bytes at PC+1 and PC+2 
            operand_a, operand_b = self.ram_read(self.pc + 1), self.ram_read(self.pc + 2)
            self.branchtable[ir](operand_a, operand_b)
