import random #rastgele sayı üretmek için
x=random.randint(1,100) #1-100 arasında rastgele sayı üret
i=0
while i<10:
    y=int(input("Bir sayı giriniz:"))
    if x==y:
        print(f"{i} seferde bildiniz.")
    elif x>y:
        print("Yukarı")
    else:
        print("Aşağı")
    i+=1
print(f"Doğru sayı:{x}")