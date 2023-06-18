a = int(input("enter your number"))
if a < 10:
    print("single")
elif a < 100:
    print("double")
elif a < 1000:
    print("triple")
else:
    print("not any")


b = input("enter number for fact")
if b.isdigit():
    b = int(b)
    x = 1
    for i in range(1,b+1):
       x *= i
    print(x)
else:
    print("invalid input")

Computers={
    "laptop1":{"brand" :"DELL","OS":"Windows"},
    "laptop2":{"brand" :"HP" ,"OS":"Linux"},
    "Desktop":{"brand" :"Apple" ,"OS":"Mac-OS"}
}
brands = []
OS = []
for i in Computers:
    brands.append(Computers[i]["brand"])
    OS.append(Computers[i]["OS"])
print(brands)
print(OS)