#Object Oriented Programming
#nesne tabanlı programlama: farklı nesneler oluşturup, bu nesneler üzerinde işlemler yapma
#class: nesne şablonu
class Person:
    def __init__(self,name,age):
        self.name=name
        self.age=age
    def intro(self):
        print("My name is",self.name)
        print("My age is",self.age)

p1=Person("John",30)
p1.intro()

class Car:
    def __init__(self,brand,model,year):
        self.brand=brand
        self.model=model
        self.year=year
    def info(self):
        print(f"Car brand: {self.brand}")
        print(f"Car model: {self.model}")
        print(f"Car year: {self.year}")

c1=Car("Toyota","Corolla",2020)
c1.info()

class Student:
    def __init__(self,name,grade):
        self.name=name
        self.grade=grade
    def isPass(self):
        if self.grade>=50:
            return True
        else:
            return False
s1=Student("Ali",60)
s2=Student("Veli",40)
print(s1.isPass())
print(s2.isPass())

class person:
    #class attribute
    #tüm nesneler için ortak
    #örnek: insan türü
    #species
    #instance attribute
    #her nesne için ayrı
    #örnek: isim ve yaş
    def __init__(self,name,age):
        self.name=name
        self.age=age

#inheritance
class Employee(person):
    def __init__(self,name,age,salary):
        #person class'ının init methodunu çağır
        super().__init__(name,age)
        self.salary=salary
    def info(self):
        print(f"Name: {self.name}, Age: {self.age}, Salary: {self.salary}")

e1=Employee("Ayşe",28,5000)
e1.info()
e2=Employee("Fatma",32,6000)
e2.info()

#polymorphism (çok biçimlilik)
class Cat:
    def sound(self):
        return "Meow"
class Dog:
    def sound(self):
        return "Woof"
def animalSound(animal):
    print(animal.sound())
c1=Cat()
d1=Dog()
animalSound(c1)
animalSound(d1)

#Encapsulation (kapsülleme)
class BankAccount:
    def __init__(self,owner,balance):
        self.owner=owner
        self.__balance=balance #private attribute
    def deposit(self,amount):
        if amount>0:
            self.__balance+=amount
            print(f"{amount} deposited. New balance is {self.__balance}")
        else:
            print("Deposit amount must be positive")
    def withdraw(self,amount):
        if amount>0 and amount<=self.__balance:
            self.__balance-=amount
            print(f"{amount} withdrawn. New balance is {self.__balance}")
        else:
            print("Invalid withdraw amount")
    def getBalance(self):
        return self.__balance
    
#special methods
class Book:
    def __init__(self,title,author,year):
        self.title=title
        self.author=author
        self.year=year
    def __str__(self):
        return f"{self.title} by {self.author} ({self.year})"
    def __len__(self):
        return len(self.title)
b1=Book("1984","George Orwell",1949)
print(b1)
print(len(b1))
class Rectangle:
    def __init__(self,width,height):
        self.width=width
        self.height=height
    def area(self):
        return self.width*self.height
    def perimeter(self):
        return 2*(self.width+self.height)
    def __str__(self):
        return f"Rectangle(width={self.width}, height={self.height})"
