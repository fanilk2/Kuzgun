def yazdır(mesaj,adet):
    while adet>0:
        print(mesaj)
        adet-=1

# yazdır("Merhaba",5)

def  listeolustur(adet):
    liste=[]
    while adet>0:
        liste.append(input("Eleman:"))
        adet-=1
    return liste

# print(listeolustur(3))

def asalhesapla(sayi,sayi2):
    for sayi in range(sayi,sayi2+1):
        if sayi>1:
            for i in range(2,sayi):
                if sayi%i==0:
                    break
            else:
                print(sayi)
        
def tambölenler(sayi):
    liste=[]
    for i in range(1,sayi+1):
        if sayi%i==0:
            liste.append(i)
    return liste

#lambda fonksiyonları
def square(x):
    return x*x

result=square(5)
num=[1,3,5,7,9]
result=list(map(square,num))
result=list(map(lambda x:x*x,num))

result=list(filter(lambda x:x%2==0,[1,2,3,4,5,6,7,8,9,10]))
#scope
x=5
def func():
    x=10
    print(x)
print(x)
func()
def func2():
    global x
    x=10
    print(x)

func2()

def func3():
    x=10
    def func4():
        print(x)
    func4()

func3()

def outer():
    x=10
    def inner():
        nonlocal x
        x=20
        print(x)
    inner()
    print(x)
outer()
print(result)
