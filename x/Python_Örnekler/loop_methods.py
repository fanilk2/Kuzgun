#Loop Methods
#--------------------------------
#range (start,stop,step)
for i in range(1,11): #1'den 10'a kadar sayılar
    print(i)
#--------------------------------
#emumrate (iterable,start)
for index,value in enumerate(range(1,11),start=10):
    print(index,value)
#--------------------------------
#zip (iterables)
names=["Ali","Veli","Ayşe"]
ages=[25,30,22]
cities=["Ankara","İstanbul","İzmir"]
for name,age,city in zip(names,ages,cities):
    print(name,age,city)
#--------------------------------
#map (function,iterable)
def square(num):
    return num**2
numbers=[1,2,3,4,5]
squared_numbers=map(square,numbers)
for num in squared_numbers:
    print(num)
    