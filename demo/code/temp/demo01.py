import copy

a = [1,2,3,[4]]
b = copy.deepcopy(a)
b[3].append(5)

print (a)
print (b)