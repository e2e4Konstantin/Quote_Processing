
n = 'Отдел  1. Железобетонные и бетонные конструкции мостов и труб'
ns = str(n).split()
print(ns)
number = ns[1][:-1]
print(number, " ".join(ns[2:]))

code = str('3.30').strip()
print(code)
print(f"{code}-{number}")
