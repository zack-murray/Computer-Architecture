"""CPU functionality."""

import sys

# Instantiate instruction codes
HLT = 0b00000001 # exits emulator
LDI = 0b10000010 # sets a specified register to a value
PRN = 0b01000111 # print value stored in register
ADD = 0b10100000 # add value of two registers & store result in registerA
SUB = 0b10100001 # subtract the value in the second register from the first & store result in registerA
MUL = 0b10100010 # multiply the values in two registers & store result in registerA

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
        # CPU running
        self.running = True

    def ram_read(self, address):
        """Accept address to read and return stored value"""
        return self.ram[address]

    def ram_write(self, value, address):
        """Accept a value to write, and the address to write it to"""
        self.ram[address] = value

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
            # Halt the CPU (and exit the emulator)
            if ir == HLT:
                self.running = False
            # Set the value of a register to an integer
            elif ir == LDI:
                # Registers[reg_num] = value
                self.reg[operand_a] = operand_b
                # Increment the counter
                self.pc += 3
            # Print numeric value stored in the given register
            elif ir == PRN:
                print(self.reg[operand_a])
                # Increment the counter
                self.pc += 2
            # Add value of two registers & store result in registerA    
            elif ir == ADD:
                self.alu("ADD", operand_a, operand_b)
                # Increment the counter
                self.pc += 3
            # Subtract the value in the second register from the first & 
            # store result in registerA
            elif ir == SUB:
                self.alu("SUB", operand_a, operand_b)
                # Increment the counter
                self.pc += 3
            # Multiply the values in two registers & store result in registerA
            elif ir == MUL:
                self.alu("MUL", operand_a, operand_b)
                # Increment the counter
                self.pc += 3
