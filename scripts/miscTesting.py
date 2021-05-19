x = ["a", "b", "c", "a"]
b = dict.fromkeys(x, [1])

temp = list(b.get("a"))
temp.extend([1,2,3])
b["a"] = temp

print(b)