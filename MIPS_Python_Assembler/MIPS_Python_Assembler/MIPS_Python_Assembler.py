# Author(s): Trung Le and Joe Komosa

# Remember where each of the jump label is, and the target location 
def saveJumpLabel(asm,labelIndex, labelName):
    lineCount = 0
    for line in asm:
        line = line.replace(" ","")
        if(line.count(":")):
            if(line.count("#") == 0): # Ensures ":" inside comment is not counted as label
                labelName.append(line[0:line.index(":")]) # append the label name
                labelIndex.append(lineCount) # append the label's index
                asm[lineCount] = line[line.index(":")+1:]
        lineCount += 1
    for item in range(asm.count('\n')): # Remove all empty lines '\n'
        asm.remove('\n')

def convertToHex(binary): # Function to convert binary to hex for easier debugging
    machineCode = format(int(binary, 2), "08x")
    machineCode = "0x" + machineCode + '\n'
    return machineCode

def getOffset(line): # Remove "0x" from offset, seperate from address, and convert to binary
    for item in range(line.count("0x")):
        offset = line.replace('0x','')
        offset = offset.split("(")
        offset = format(int(offset[0], 16), '016b')
    return offset


def main():
    lineCount = 0
    labelIndex = []
    labelName = []
    f = open("mc.txt","w+")
    h = open("project2_test.asm","r")
    asm = h.readlines()
    for item in range(asm.count('\n')): # Remove all empty lines '\n'
        asm.remove('\n')

    saveJumpLabel(asm,labelIndex,labelName) # Save all jump's destinations
    
    for line in asm:   
        if(line.count("#")): # Removes all comments
            line = line.replace(line[(line.index("#")):(line.index("\n"))], '')
        line = line.replace("\n","") # Removes extra chars
        line = line.replace("\t","") # Removes tabs
        line = line.replace("$","")
        line = line.replace(" ","")
        line = line.replace("zero","0") # assembly can also use both $zero and $0
        lineCount += 1 # Counts each line/iteration
        #print(line, lineCount)
        innerLineCnt = 0
        jumpAmount = 0

        if(line[0:5] == "addiu"): # addiu rt, rs, imm
            line = line.replace("addiu","")
            line = line.split(",")
            rt = format(int(line[0]),'05b')
            rs = format(int(line[1]),'05b')
            imm = format(int(line[2]),'016b')
            f.write(convertToHex(str('001001') + str(rs) + str(rt) + str(imm)))

        elif(line[0:4] == "addi"): # addi rt, rs, imm 
            line = line.replace("addi","")
            line = line.split(",")
            imm = line[2]
            if(imm.count("0x")): # If offset = hex value \/
                for item in range(imm.count("0x")):
                    imm = imm.replace('0x','')
                    imm = format(int(imm, 16), '016b')
            else: # If offset in decimal and/or negative
                imm = format(int(imm),'016b') if (int(imm) >= 0) else format(65536 + int(imm),'016b')
            rs = format(int(line[1]),'05b')
            rt = format(int(line[0]),'05b')
            f.write(convertToHex(str('001000') + str(rs) + str(rt) + str(imm)))

        elif(line[0:3] == "add"): # add rd, rs, rt
            line = line.replace("add","")
            line = line.split(",")
            rd = format(int(line[0]),'05b')
            rs = format(int(line[1]),'05b')
            rt = format(int(line[2]),'05b')
            f.write(convertToHex(str('000000') + str(rs) + str(rt) + str(rd) + str('00000100000')))

        elif(line[0:4] == "andi"): # andi rt, rs, imm
            line = line.replace("andi","")
            line = line.split(",")
            rt = format(int(line[0]),'05b')
            rs = format(int(line[1]),'05b')
            imm = line[2]
            if(imm.count("0x")): # If offset = hex value \/
                for item in range(imm.count("0x")):
                    imm = imm.replace('0x','')
                    imm = format(int(imm, 16), '016b')
            else: # If offset in decimal and/or negative
                imm = format(int(imm),'016b') if (int(imm) >= 0) else format(65536 + int(imm),'016b')
            f.write(convertToHex(str('001100') + str(rs) + str(rt) + str(imm)))

        elif(line[0:3] == "xor"): # xor rd, rs, rt
            line = line.replace("xor","")
            line = line.split(",")
            rd = format(int(line[0]),'05b')
            rs = format(int(line[1]),'05b')
            rt = format(int(line[2]),'05b')
            f.write(convertToHex(str('000000') + str(rs) + str(rt) + str(rd) + str('00000100110')))

        elif(line[0:3] == "ori"): # ori rt, rs, imm
            line = line.replace("ori","")
            line = line.split(",")
            rs = format(int(line[0]),'05b')
            rt = format(int(line[1]),'05b')
            imm = line[2]
            if(imm.count("0x")): # If offset = hex value \/
                for item in range(imm.count("0x")):
                    imm = imm.replace('0x','')
                    imm = format(int(imm, 16), '016b')
            else: # If offset in decimal and/or negative
                imm = format(int(imm),'016b') if (int(imm) >= 0) else format(65536 + int(imm),'016b')
            f.write(convertToHex(str('001101') + str(rs) + str(rt) + str(imm)))
            
        elif(line[0:1] == "j"): # JUMP
            line = line.replace("j","")
            line = line.split(",")

            # Since jump instruction has 2 options:
            # 1) jump to a label
            # 2) jump to a target (integer)
            # We need to save the label destination and its target location

            if(line[0].isdigit()): # First,test to see if it's a label or a integer
                f.write(convertToHex(str('000010') + str(format(int(line[0]),'026b'))))

            else: # Jumping to label
                for i in range(len(labelName)):
                    if(labelName[i] == line[0]):
                       f.write(convertToHex(str('000010') + str(format(int(labelIndex[i]),'026b'))))

        elif(line[0:5] == "multu"): # MULTU
            line = line.replace("multu","")
            line = line.split(",")
            rs = format(int(line[0]),'05b')
            rt = format(int(line[1]),'05b')
            f.write(convertToHex(str('000000') + str(rs) + str(rt) + str('0000000000') + str('011001')))

        elif(line[0:4] == "mult"): # MULT
            line = line.replace("mult","")
            line = line.split(",")
            rs = format(int(line[0]),'05b')
            rt = format(int(line[1]),'05b')
            f.write(convertToHex(str('000000') + str(rs) + str(rt) + str('0000000000') + str('011000')))

        elif(line[0:3] == "srl"): # SRL
            line = line.replace("srl","")
            line = line.split(",")
            rd = format(int(line[0]),'05b')
            rt = format(int(line[1]),'05b')
            shamt = format(int(line[2]),'05b')
            f.write(convertToHex(str('00000000000') + str(rt) + str(rd) + str(shamt) + str('000010')))

        elif(line[0:4] == "mfhi"): # mfhi rd
            line = line.replace("mfhi","")
            line = line.split(",")
            rd = format(int(line[0]),'05b')
            f.write(convertToHex(str('0000000000000000') + str(rd) + str('00000010000')))

        elif(line[0:4] == "mflo"): # mflo rd
            line = line.replace("mflo","")
            line = line.split(",")
            rd = format(int(line[0]),'05b')
            f.write(convertToHex(str('0000000000000000') + str(rd) + str('00000010010')))

        elif(line[0:3] == "lui"): # lui rt, imm
            line = line.replace("lui","")
            line = line.split(",")
            rt = format(int(line[0]),'05b')
            imm = line[1]
            if(imm.count("0x")): # If offset = hex value \/
                for item in range(imm.count("0x")):
                    imm = imm.replace('0x','')
                    imm = format(int(imm, 16), '016b')
            else: # If offset in decimal and/or negative
                imm = format(int(imm),'016b') if (int(imm) >= 0) else format(65536 + int(imm),'016b')
            f.write(convertToHex(str('00111100000') + str(rt) + str(imm)))

        elif(line[0:3] == "lbu"): # LBU
            line = line.replace("lbu","")
            line = line.split(",")
            rt = format(int(line[0]),'05b')
            addressAndOS = line[1]
            if(addressAndOS.count("0x")): # If offset = hex value \/
                f.write(convertToHex(str('10010000000') + str(rt) + str(getOffset(addressAndOS))))      
            else: # If offset = 0 \/
                f.write(convertToHex(str('10010000000') + str(rt) + str('0000000000000000')))

        elif(line[0:2] == "lb"): # LB
            line = line.replace("lb","")
            line = line.split(",")
            rt = format(int(line[0]),'05b')
            addressAndOS = line[1]
            if(addressAndOS.count("0x")): # If offset = hex value \/
                f.write(convertToHex(str('10000000000') + str(rt) + str(getOffset(addressAndOS))))   
            else: # If offset = 0 \/
                f.write(convertToHex(str('10000000000') + str(rt) + str('0000000000000000')))

        elif(line[0:2] == "sb"): # SB
            line = line.replace("sb","")
            line = line.split(",")
            rt = format(int(line[0]),'05b')
            addressAndOS = line[1]
            if(addressAndOS.count("0x")):
                f.write(convertToHex(str('10100000000') + str(rt) + str(getOffset(addressAndOS))))    
            else:
                f.write(convertToHex(str('10100000000') + str(rt) + str('0000000000000000')))

        elif(line[0:2] == "lw"): # LW
            line = line.replace("lw","")
            line = line.split(",")
            rt = format(int(line[0]),'05b')
            addressAndOS = line[1]
            if(addressAndOS.count("0x")):
                f.write(convertToHex(str('10001100000') + str(rt) + str(getOffset(addressAndOS))))    
            else:
                f.write(convertToHex(str('10001100000') + str(rt) + str('0000000000000000')))

        elif(line[0:2] == "sw"): # SW
            line = line.replace("sw","")
            line = line.split(",")
            rt = format(int(line[0]),'05b')
            addressAndOS = line[1]
            if(addressAndOS.count("0x")):
                f.write(convertToHex(str('10101100000') + str(rt) + str(getOffset(addressAndOS))))      
            else:
                f.write(convertToHex(str('10101100000') + str(rt) + str('0000000000000000')))

        elif(line[0:3] == "beq" or line[0:3] == "bne"): # beq rs, rt, label | bne rs, rt, label
            if (line[0:3] == "beq"):
                op = '000100'
                line = line.replace("beq","")
            else:
                op = '000101'
                line = line.replace("bne","")
            line = line.split(",")
            rs = format(int(line[0]),'05b')
            rt = format(int(line[1]),'05b')
            for i in range(len(labelName)):# Branching to label
                
                if(labelName[i] == line[2]): 
                    #print(labelName[i], labelIndex[i])
                    jumpAmount = labelIndex[i] - lineCount
                    #print(jumpAmount)
                    if(jumpAmount < 0):
                        for num in range((labelIndex[i] + 1), lineCount):
                            if num in labelIndex:
                                innerLineCnt += 1 # Counts the lines above current label until match starting from index
                        imm = jumpAmount + innerLineCnt
                        imm = 65536 + int(imm) # make negative
                    else:
                        for num in range(lineCount, (labelIndex[i] + 1)):
                            if num in labelIndex:
                                innerLineCnt += 1 # Counts the lines below current label until match starting from index
                        imm = jumpAmount - innerLineCnt
                    f.write(convertToHex(str(op) + str(rs) + str(rt) + str(format(int(imm),'016b'))))
                    #print(convertToHex(str(op) + str(rs) + str(rt) + str(format(int(imm),'016b'))))

        elif(line[0:4] == "sltu"): # SLTU
            line = line.replace("sltu","")
            line = line.split(",")
            rd = format(int(line[0]),'05b')
            rs = format(int(line[1]),'05b')
            rt = format(int(line[2]),'05b')
            f.write(convertToHex(str('000000') + str(rs) + str(rt) + str(rd) + str('00000101011')))

        elif(line[0:3] == "slt"): # SLT
            line = line.replace("slt","")
            line = line.split(",")
            rd = format(int(line[0]),'05b')
            rs = format(int(line[1]),'05b')
            rt = format(int(line[2]),'05b')
            f.write(convertToHex(str('000000') + str(rs) + str(rt) + str(rd) + str('00000101010')))

    f.close()

if __name__ == "__main__":
    main()
