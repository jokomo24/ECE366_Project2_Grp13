# parses hex input into component instruction parts
class instruction():
    func_dict = {'100010':'sub',
                 '100000':'add',
                 '100110':'xor',
                 '011001':'multu',
                 '011000':'mult',
                 '000010':'srl',
                 '010000':'mfhi',
                 '010010':'mflo',
                 '101011':'sltu',
                 '101010':'slt',
                 '001000':'addi',
                 '000100':'beq',
                 '000101':'bne',
                 '001101':'ori',
                 '101011':'sw',
                 '001001':'addiu',
                 '001100':'andi',
                 '001111':'lui',
                 '100100':'lbu',
                 '100000':'lb',
                 '100011':'lw',
                 '101000':'sb',
                 '101011':'sw'}

    def __init__(self, hex_num):
        temp_num = int(hex_num, 16) # convert the input string to type int

        self.hex_num = hex_num # this just makes the hex number pretty with the 0x

        #make a binary string, the format gets rid of the 0b prefix in the string
        self.binary_string = format(temp_num, '0{}b'.format(32))
        # the string[0:3] syntax means the first 4 characters of string, use this fact to decode the binary
        self.opcode = self.binary_string[0:6]
        if self.opcode == '000000': # all r_types have this opcode, and function is the last 5 bits
            self.func = self.binary_string[26:32]
            self.type = 'r_type'
        else: # in this case type i
            self.func = self.opcode
            self.type = 'i_type'
        self.rs = int(self.binary_string[6:11], 2)
        self.rt = int(self.binary_string[11:16], 2)
        self.rd = int(self.binary_string[16:21], 2)
        self.shamt = int(self.binary_string[21:26], 2) # shift amount
        if self.binary_string[16] == '1': # check the immediate for negative numbers and convert if needed
            self.imm = -((int(self.binary_string[16:32], 2) ^ 0xFFFF) + 1)
        else:
            self.imm = int(self.binary_string[16:32], 2)
        try:
            self.name = func_dict[self.func] # this will lookup the string name of the function in func_dict
        except:
            self.name = 'null'
    def print(self):
        if self.type == 'r_type':
            print(self.hex_num + ' is ' + self.name + ' $' + str(self.rd) + ', $' + str(self.rs) + ', $' + str(self.rt))
        else:
            print(self.hex_num + ' is ' + self.name + ' $' + str(self.rt) + ', $' + str(self.rs) + ', ' + str(self.imm))
    def shiftopprint(self):
        print(self.hex_num + ' is ' + self.name + ' $' + str(self.rt) + ', $' + str(self.rs) + ', ' + str(self.shamt))

def sextb(num, bits):
    if (num < 0): # signed extension
       imm = 65536 + num # removes negative sign
       imm = str(format(int(imm),'0' + bits + 'b'))
       i = 0
       zeros = 0
       ones = str()
       while imm[i] != '1':
           zeros += 1
           ones = ones + '1'
           i += 1
       imm = ones + imm[zeros:] 
    else:
        imm = str(format(int(num),'0' + bits + 'b'))
    return imm

def print_all(registers, memory):
    print('Register Contents:')
    for value in registers.items():
        if value[1] != None:
            print(value)
    print('Memory Contents:')
    for value in memory.items():
        print(value)

# supported instruction functions
def andi(instruction, registers, debug, memory):
    operand1 = registers[instruction.rs]
    operand2 = instruction.imm
    registers[instruction.rt] = operand1 & operand2
    if debug:
        instruction.print()
        print_all(registers, memory)
    registers['PC'] += 4
    return registers

def addi(instruction, registers, debug, memory): # Done/Working
    operand1 = registers[instruction.rs]
    operand2 = instruction.imm
    operand1 = int(operand1)
    operand2 = int(operand2)
    registers[instruction.rt] = operand1 + operand2
    if debug:
        instruction.print()
        print_all(registers, memory)
    registers['PC'] += 4
    return registers

def addiu(instruction, registers, debug, memory): # Done/Working????
    operand1 = registers[instruction.rs]
    operand2 = instruction.imm
    registers[instruction.rt] = operand1 + operand2
    if debug:
        instruction.print()
        print_all(registers, memory)
    registers['PC'] += 4
    return registers

def add(instruction, registers, debug, memory): # Done/Working
    operand1 = registers[instruction.rs]
    operand2 = registers[instruction.rt]
    registers[instruction.rd] = operand1 + operand2
    if debug:
        instruction.print()
        print_all(registers, memory)
    registers['PC'] += 4
    return registers

def sub(instruction, registers, debug, memory): # Done/Working
    operand1 = registers[instruction.rs] #value in rs
    operand2 =  registers[instruction.rt] #value in rt
    registers[instruction.rd] = operand1 - operand2
    if debug:
        instruction.print()
        print_all(registers, memory)
    registers['PC'] += 4
    return registers

def beq(instruction, registers, debug, memory): # Done/Working
    operand1 = registers[instruction.rs]
    operand2 = registers[instruction.rt]
    if debug:
        instruction.print()
        print_all(registers, memory)
    if (operand1 == operand2):
        registers['PC'] += (4 + (instruction.imm << 2))
    else:
        registers['PC'] += 4
    return registers

def bne(instruction, registers, debug, memory): # Done/Working
    operand1 = registers[instruction.rs]
    operand2 = registers[instruction.rt]
    if debug:
        instruction.print()
        print_all(registers, memory)
    if (operand1 != operand2):
        registers['PC'] += (8 + (instruction.imm << 2))
    else:
        registers['PC'] += 4
    return registers

def ori(instruction, registers, debug, memory): # Done/Working
    operand1 = registers[instruction.rs]
    imm = instruction.imm
    imm = sextb(int(imm), '16')
    operand2 = '0000000000000000' + imm 
    oriVal = str()
    i = 0
    while i < 32:
        if (operand1[i] == '1' or operand2[i] == '1'):
            oriVal = oriVal + '1'
        else:
            oriVal = oriVal + '0'
        i += 1
    registers[instruction.rt] = oriVal
    if debug:
        instruction.print()
        print_all(registers, memory)
    registers['PC'] += 4
    return registers

def xor(instruction, registers, debug, memory): # FIX ME!!
    operand1 = registers[instruction.rs]
    operand2 = registers[instruction.rt]
    #print(operand1+'hi'+operand2)
    xorVal = str()
    i = 0
    while i < 32:
        if (operand1[i] != operand2[i]):
            xorVal = xorVal + '1'
        else:
            xorVal = xorVal + '0'
        i += 1
    registers[instruction.rd] = xorVal

    #print(operand1,operand2,xorVal)

    if debug:
        instruction.print()
        print_all(registers, memory)
    registers['PC'] += 4
    return registers

def multu(instruction, registers, debug, memory): # Done/Working
    operand1 = registers[instruction.rs]
    operand2 = registers[instruction.rt]
    product = str(int(operand1) * int(operand2))
    #print(product)
    bits64 = 64 - len(product)
    product =   (bits64 * '0') + product # "bits64" adds the extra bits 
    registers['hi'] = product[0:32]
    registers['lo'] = product[32:64]
    #print(product)
    if debug:
        instruction.print()
        print_all(registers, memory)
    registers['PC'] += 4
    return registers

def mult(instruction, registers, debug, memory): # Done/Working
    operand1 = registers[instruction.rs]
    operand2 = registers[instruction.rt]
    product = str(int(operand1) * int(operand2))
    bits64 = 64 - len(product)
    if(product[0] == '1'): # unsigned
        product =   (bits64 * '1') + product # "bits64" adds the extra bits 
    else:
        product = (bits64 * '0') + product
    registers['hi'] = product[0:32]
    registers['lo'] = product[32:64]
    if debug:
        instruction.print()
        print_all(registers, memory)
    registers['PC'] += 4
    return registers

def mfhi(instruction, registers, debug, memory): # Done/Working
    registers[instruction.rd] = registers['hi']
    #print('hi'+registers['hi'])
    if debug:
        instruction.print()
        print_all(registers, memory)
    registers['PC'] += 4
    return registers

def mflo(instruction, registers, debug, memory): # Done/Working
    registers[instruction.rd] = registers['lo']
    #print('lo'+registers['lo'])
    if debug:
        instruction.print()
        print_all(registers, memory)
    registers['PC'] += 4
    return registers

def sltu(instruction, registers, debug, memory):
    operand1 = registers[instruction.rs]
    operand2 = registers[instruction.rt]
    registers[instruction.rd] = operand1 < operand2
    if debug:
        instruction.print()
        print_all(registers, memory)
    registers['PC'] += 4
    return registers

def slt(instruction, registers, debug, memory):
    operand1 = registers[instruction.rs]
    operand2 = registers[instruction.rt]
    registers[instruction.rd] = operand1 < operand2
    if debug:
        instruction.print()
        print_all(registers, memory)
    registers['PC'] += 4
    return registers

def srl(instruction, registers, debug, memory): # Done/Working
    operand1 = registers[instruction.rt]
    operand2 = instruction.shamt          # good catch!
    registers[instruction.rd] = (operand1 % 0x100000000) >> operand2
    if debug:
        instruction.shiftopprint()
        print_all(registers, memory)
    registers['PC'] += 4
    return registers

def lui(instruction, registers, debug, memory): # Done/Working
    imm = instruction.imm
    imm = sextb(imm, '16')
    registers[instruction.rt] = str(imm) + '0000000000000000'
    if debug:
        instruction.print()
        print_all(registers, memory)
    registers['PC'] += 4
    return registers

def lbu(instruction, registers, debug, memory): # FIX ME!! needs to be unsigned operation
    address = registers[instruction.rs]
    offset = registers[instruction.imm]
    byteLoc = int(hex(0x00000011), 16) << offset   # Correct???
    byte = int(hex(memory[address]), 16) & byteLoc
    registers[instruction.rt] = byte
    if debug:
        instruction.print()
        print_all(registers, memory)
    registers['PC'] += 4
    return registers

def lb(instruction, registers, debug, memory): # Correct??
    address = registers[instruction.rs]
    offset = registers[instruction.imm]
    byteLoc = int(hex(0x00000011), 16) << offset
    byte = memory[address] & byteLoc
    registers[instruction.rt] = byte
    if debug:
        instruction.print()
        print_all(registers, memory)
    registers['PC'] += 4
    return registers

def lw(instruction, registers, debug, memory):
    offset = registers[instruction.imm]
    registers[instruction.rt] = memory[hex(offset)]
    if debug:
        instruction.print()
        print_all(registers, memory)
    registers['PC'] += 4
    return registers

def sw(instruction, registers, debug, memory):
    addr_index = registers[instruction.rs]
    offset = instruction.imm
    memory[hex(addr_index + offset)] = registers[instruction.rt]
    if debug:
        instruction.print()
        print_all(registers, memory)
    registers['PC'] += 4
    return memory

def sb(instruction, registers, debug, memory):
    addr_index = registers[instruction.rs]
    offset = instruction.imm
    memory[hex(addr_index + offset)] = registers[instruction.rt]
    if debug:
        instruction.print()
        print_all(registers, memory)
    registers['PC'] += 4
    return memory

# dictionaries of functions
r_types = {'100010':sub,
           '100000':add,
           '100110':xor,
           '011001':multu,
           '011000':mult,
           '000010':srl,
           '010000':mfhi,
           '010010':mflo,
           '101011':sltu,
           '101010':slt}
i_types = {'001000':addi,
           '000100':beq,
           '000101':bne,
           '001101':ori,
           '101011':sw,
           '001001':addiu,
           '001100':andi,
           '001111':lui,
           '100100':lbu,
           '100000':lb,
           '100011':lw,
           '101000':sb,
           '101011':sw}

