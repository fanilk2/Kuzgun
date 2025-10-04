#List Comprehensions
numbers=[1,2,3,4,5]
squared=[n**2 for n in numbers] #her sayının karesi
print(squared)
even=[n for n in numbers if n%2==0] #çift sayılar
print(even)
odd=[n for n in numbers if n%2==1] #tek sayılar
print(odd)
cubes=[n**3 for n in numbers ] #sayıların küpleri
print(cubes)
names=["Ali","Veli","Ayşe","Fatma","Oya"]
short_names=[name for name in names if len(name)<=3] #3 veya daha az harfli isimler
print(short_names)
a_names=[name.upper() for name in names if name.startswith("A")] #A ile
print(a_names)