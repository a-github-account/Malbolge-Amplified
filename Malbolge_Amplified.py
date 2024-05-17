# This is copylefted, and anybody may distribute, modify, or otherwise use this freely (keep in note that this is copylefted).
# Made by MilkyWay90 in 2019.


import sys, subprocess

debug = '-d' in sys.argv

if debug:
	try:
		import keyboard
	except:
		print("You do not have a required module named keyboard. Use python3 (or whatever the environment var/python executable is) -m pip install keyboard")

normalized_malbolge = ""
xlat1 = "+b(29e*j1VMEKLyC})8&m#~W>qxdRp0wkrUo[D7,XTcA\"lI.v%{gJh4G\\-=O@5`_3i<?Z';FNQuY]szf$!BS/|t:Pn6^Ha"
xlat2 = "H&*i:r\"h$Z0R1x`tXoPpcY8/NTL%yBOw6!vku)A~@#.?QV'Ca{<Wd[}f;2El9]mI3(7|_s5z>gnbS4qej^D,MK+U-=FG\\J"


def crazy_op(x, y):
	pow_3 = [1, 3, 9, 27, 81, 243, 729, 2187, 6561]
	table = [
		[2, 1, 0],
		[0, 2, 1],
		[1, 0, 2]
	]
	result = 0
	for i in range(len(pow_3)):
		result += table[y // pow_3[i] % 3][x // pow_3[i] % 3] * pow_3[i]
	return result

def execute(mem):
	global normalized_malbolge
	a, c, d, pos = 0, 0, 0, 0
	output, inst_exec = "", ""
	while True:
		mem[c] = ord(xlat2[mem[c] - 33])
		if debug:
			subprocess.run("cls || clear", shell = True)
			print(f"C = {c}, D = {d}, A = {a}\n")
			print(f"[C] = {mem[c]}, [D] = {mem[d]}")
			print("Normalized Malbolge:")
			print(normalized_malbolge)
			print(" " * (c - 1) + "C\n")
			print("Memory:")
			print(hex(65536 | (d - d % 30))[3:], "".join(map(lambda x:chr(x)if 32 < x < 127 else "?", mem[d - d % 30: d - d % 30 + 30])))
			print(" " * (d % 30 + 5) + "D\n")
			print("Output:")
			print(output if output else "(nothing)", "\n")
			print("Instructions Executed:")
			print(inst_exec)
			print("Press the enter key to continue.")
			keyboard.wait("enter")
		if mem[c] < 33 or mem[c] > 126:
			continue
		switch = xlat1[(mem[c] - 33 + c) % 94]
		if switch == "j":
			if debug: inst_exec += f"MOVE_D: D was {d}, now {mem[d]}\n"
			d = mem[d]
		elif switch == "i":
			if debug: inst_exec += f"JUMP: C was {c}, now {mem[d]}\n"
			c = mem[d]
		elif switch == "*":
			if debug: inst_exec += f"ROTATE: A, [D] was {a}, {mem[d]}, now {mem[d] // 3 + mem[d] % 3 * 19683}\n"
			mem[d] = mem[d] // 3 + mem[d] % 3 * 19683
			a = mem[d]
			if debug:
				if d < len(normalized_malbolge):
					if xlat1[(mem[d] - 33 + pos) % 94] not in "ji*p</vo":
						if 32 < ord(xlat1[(mem[d] - 33 + pos) % 94]) < 127: 
							normalized_malbolge = normalized_malbolge[:c] + "o" + normalized_malbolge[c+1:]
						else:
							normalized_malbolge = normalized_malbolge[:c] + "?" + normalized_malbolge[c+1:]
					else:
						normalized_malbolge = normalized_malbolge[:c] + xlat1[(mem[c] - 33 + pos) % 94] + normalized_malbolge[c+1:]
		elif switch == "p":
			if debug: inst_exec += f"CRAZY OP: A, [D] was {a}, {mem[d]}, now A and [D] are {crazy_op(a, mem[d])}\n"
			mem[d] = crazy_op(a, mem[d])
			a = mem[d]
			if debug:
				if d < len(normalized_malbolge):
					if xlat1[(mem[d] - 33 + pos) % 94] not in "ji*p</vo":
						if 32 < ord(xlat1[(mem[d] - 33 + pos) % 94]) < 127: 
							normalized_malbolge = normalized_malbolge[:c] + "o" + normalized_malbolge[c+1:]
						else:
							normalized_malbolge = normalized_malbolge[:c] + "?" + normalized_malbolge[c+1:]
					else:
						normalized_malbolge = normalized_malbolge[:c] + xlat1[(mem[c] - 33 + pos) % 94] + normalized_malbolge[c+1:]
		elif switch == "<":
			if debug: inst_exec += f"PRINT: Printed {a%256}, or {chr(a%256)}\n"
			if debug:
				output += chr(a % 256)
			else:
				sys.stdout.write(chr(a % 256))
		elif switch == "/":
			char = sys.stdin.read(1)
			if debug: inst_exec += f"INPUT: A was {a}, now {ord(char)} or {char}\n"
			if ord(char) == 0:
				a = 59048
			else:
				a = ord(char)
		elif switch == "v":
			if debug: inst_exec += "HALT: Program halted!\n"
			return
		else:
			if debug: inst_exec += "NO-OP\n"
		del switch
		if debug:
			if xlat1[(mem[c] - 33 + pos) % 94] not in "ji*p</vo":
				normalized_malbolge = normalized_malbolge[:c] + "o" + normalized_malbolge[c+1:]
			else:
				normalized_malbolge = normalized_malbolge[:c] + xlat1[(mem[c] - 33 + pos) % 94] + normalized_malbolge[c+1:]
		c += 1
		d += 1
		c %= 59049
		d %= 59049
		pos += 1

def main():
	global normalized_malbolge
	normalized_malbolge = ""
	if len(sys.argv) < 2:
		print("invalid command line", file = sys.stderr)
		sys.exit()
	try:
		prog_contents = open(sys.argv[1]).read()
	except FileNotFoundError:
		print("can't open file", file = sys.stderr)
		sys.exit()

	mem = [0] * 59049

	pos = 0
	for i in prog_contents:
		if i in " \t\n":
			continue
		if xlat1[(ord(i) - 33 + pos) % 94] not in "ji*p</vo":
			print("invalid character in source file", file = sys.stderr)
		if pos == 59049:
			print("input file too long", file = sys.stderr)
		if debug:
			normalized_malbolge += xlat1[(ord(i) - 33 + pos) % 94]
		mem[pos] = ord(i)
		pos += 1

	while pos < 59049:
		mem[pos] = crazy_op(mem[pos - 1], mem[pos - 2])
		pos += 1
	execute(mem)

if __name__ == "__main__":
	main()