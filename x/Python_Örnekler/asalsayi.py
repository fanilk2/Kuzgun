x=input("bir sayı giriniz:")
for i in range(2,int(x)):
    if int(x)%i==0:
        print("Sayı asal değildir.")
        break
    else:
        print("Sayı asaldir.")
        break