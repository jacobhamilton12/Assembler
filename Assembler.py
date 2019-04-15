import sys
import re
import os

compDict = {
	"0": "101010",
	"1": "111111",
	"-1": "111010",
	"D": "001100",
	"A": "110000",
	"M": "110000",
	"!D": "001101",
	"!A": "110001",
	"!M": "110001",
	"-D": "001111",
	"-A": "110011",
	"-M": "110011",
	"D+1": "011111",
	"A+1": "110111",
	"M+1": "110111",
	"D-1": "001110",
	"A-1": "110010",
	"M-1": "110010",
	"D+A": "000010",
	"D+M": "000010",
	"A+D": "000010",
	"M+D": "000010",
	"D-A": "010011",
	"D-M": "010011",
	"A-D": "000111",
	"M-D": "000111",
	"D&A": "000000",
	"D&M": "000000",
	"D|A": "010101",
	"D|M": "010101"
}

destDict = {
	"": "000",
	"M": "001",
	"D": "010",
	"MD": "011",
	"A": "100",
	"AM": "101",
	"AD": "110",
	"AMD": "111"
}

jumpDict = {
	"": "000",
	"JGT": "001",
	"JEQ": "010",
	"JGE": "011",
	"JLT": "100",
	"JNE": "101",
	"JLE": "110",
	"JMP": "111"
}

symbolTable = {
	"R0": "0",
	"R1": "1",
	"R2": "2",
	"R3": "3",
	"R4": "4",
	"R5": "5",
	"R6": "6",
	"R7": "7",
	"R8": "8",
	"R9": "9",
	"R10": "10",
	"R11": "11",
	"R12": "12",
	"R13": "13",
	"R14": "14",
	"R15": "15",
	"KBD": "24576",
	"SCREEN": "16384",
	"SP": "0",
	"LCL": "1",
	"ARG": "2",
	"THIS": "3",
	"THAT": "4"
}

def firstPass(fileName): # removes labels and adds to symbol table, removes comments and whitespace
	inFile = open(fileName, "r")
	outFile = open("tempFile", "w")

	with inFile as f:
		lineNum = 0
		for line in f:
			code = ""
			line = line.strip()
			line = line.replace(" ","") #removes whitespace
			if(line[:1] != "/" and line != ""): #ignores comments, and empty lines
				if(line[:1] == "("): #ignores number addresses, and c instructions
					symbolTable[line[1:-1]] = str(lineNum)
					lineNum = lineNum - 1
				else:
					if("//" in line): #removes comments after commands
						code = code + line[:line.find("/")] + "\n"
					else:
						code = code + line + "\n"

				lineNum += 1
			if(code != ""):
				outFile.write(code)






def Assembler(fileName):
	firstPass(fileName) #creates tempFile. Same file but with labels removed and added to symbol table

	#opens infile with filename. Converts to .hack and opens outfile with new name
	inFile = open("tempFile", "r")
	newFileName = fileName.split(".")[0] + ".hack"
	outFile = open(newFileName, "w")
	
	with inFile as f:
		#stripped = ""
		symNumber = 16
		for line in f: #iterate line by line
			code = ""
			jump = ""
			dest = ""
			comp = ""
			addrNum = ""
			line = line.strip() #removes whitespace	
			if(line != ""): #ignores empty line

				#handles A instructions
				if(line[:1] == "@"):
					if(not line[1:].isnumeric()):
						if(line[1:] not in symbolTable): #if symbol isnt in it adds it to the table
							symbolTable[line[1:]] = str(symNumber)
							symNumber += 1
						addrNum = symbolTable[line[1:]]   
						code = code + bin(int(addrNum, 10)).replace("0b","").zfill(16) + "\n"
					else:
						code = code + bin(int(line[1:], 10)).replace("0b","").zfill(16) + "\n"
					#stripped = stripped + "@" + addrNum + "\n"

					


				#handles C intructions
				else:
					#stripped = stripped + line + "\n"
					#first 3 equals 111
					code = code + "111"

					#sets jump, comp, and dest strings or leaves blank
					temp = re.split("=|;", line)
					if("=" in line):
						dest = temp[0]
						comp = temp[1]
						if(";" in line):
							jump = temp[2]
					else:
						comp = temp[0]
						if(";" in line):
							jump = temp[1]

					#sets "a" bit
					if("M" in comp):
						code = code + "1"
					else:
						code = code + "0"

					#sets comp bits
					code = code + compDict[comp]

					#sets destination bits
					code = code + destDict[dest]

					#sets jump bits
					code = code + jumpDict[jump]

					code = code + "\n"
			outFile.write(code) #adds line to outFile

	#os.remove("tempFile")
	#print(stripped)
	outFile.close()


Assembler(sys.argv[1])
