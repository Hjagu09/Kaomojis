import random
import json
from copy import deepcopy as copy
import sys

uniqe = 0


def get_uniqe() -> int:
	global uniqe
	uniqe += 1
	return uniqe


def combinations(data, op, opi, total, defined={}):
	ops = op[opi]
	opd = str(get_uniqe())
	if type(op[opi]) == list:
		ops = op[opi][0]
		opd = op[opi][1]

	if opd in defined:
		try:
			if len(op) != opi + 1:
				for c in combinations(
					data,
					op,
					opi + 1,
					total + data[ops][defined[opd]],
					defined):
					yield c
			else:
				yield total + data[ops][defined[opd]]
		except IndexError:
			return
	else:
		for i in range(len(data[ops])):
			v = data[ops][i]
			if type(v) == str:
				ndef = copy(defined)
				ndef[opd] = i
				if opi + 1 == len(op):
					yield total + v
				else:
					for c in combinations(
						data,
						op,
						opi + 1,
						total + v,
						ndef):
						yield c
			else:
				for c in combinations(data, v, 0, total):
					if opi + 1 == len(op):
						yield c
					else:
						for cc in combinations(
							data,
							op,
							opi + 1,
							c,
							defined):
							yield cc


with open("smiles.json") as file:
	data = json.loads(file.read())
	smiles = []
	smile_type = sys.argv[1]
	for op in data[1][int(smile_type)]:
		for c in combinations(data[0], op, 0, ""):
			smiles.append(c)

	random.shuffle(smiles)
	for smile in smiles:
		print(smile)
