
import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.reg = [0] * 0x08
        # holds ff= 255 bytes
        self.ram = [0] * 0xff
        #Program Counter, address of the currently executing instruction
        self.pc = 0x00 
        #Instruction Register, contains a copy of the currently executing instruction
        self.ir = 0x00
        #opcodes to 1
        self.h = 0b00000001 
        #flag
        self.fl = 0*00

    def ram_read(self, current):
        return self.ram[current]
    def ram_write(self, write, current):
        self.ram[current] = write

    def load(self):
        """Load a program into memory."""
        address = 0
        # For now, we've just hardcoded a program:
        program = [
            # From print8.ls8
            0b10000010, # LDI R0,8
            0b00000000,
            0b00001000,
            0b01000111, # PRN R0
            0b00000000,
            0b00000001, # HLT
        ]

        for instruction in program:
            self.ram[address] = instruction
            address += 1

    def increment_pc(self, op_code):
        add_to_pc = (op_code >> 6) + 1
        self.pc += add_to_pc

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
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
        HLT = 0b00000001
        CMP = 0b10100111 
        JEQ = 0b01010101
        JNE = 0b01010110
        JMP = 0b01010100
        run_cpu = True
        
        while run_cpu:
            self.ir = self.pc
            command = self.ram_read(self.pc)

            o1 = self.ram_read(self.pc + 1)
            o2 = self.ram_read(self.pc + 2)

            if self.ram[self.ir] == self.h:
                run_cpu = False

            elif command == HLT:  # HLT (halt)
                run_cpu = False
                sys.exit(1)

            elif command == CMP:
                if self.reg[o1] == self.reg[o2]:
                    self.fl = 1
                elif self.reg[o1] < self.reg[o2]:
                    self.fl = 4
                elif self.reg[o1] > self.reg[o2]:
                    self.fl = 2
            elif command == JMP:  # jump
                # get the register address out of the memory
                reg_address = self.ram_read(self.pc + 1)
                self.pc = self.registers[reg_address]

            elif command == JEQ:
                reg_address = self.ram_read(self.pc +1) # getting register address from memory
                if self.fl == 1:  #check if equal is true
                    self.pc = self.reg[reg_address]
                else:
                    self.increment_pc(command)
            elif command == JNE:
                reg_address = self.ram_read(self.pc + 1)
                if self.fl != 1:
                    self.pc = self.reg[reg_address]
                else:
                    self.increment_pc(command)

            else:
                run_cpu== False
                break
                print(f"You have entered an invalid command: {self.ram[self.PC]}. Program exiting...")
