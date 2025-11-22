#Bankamatik örneği
def menu():
    print("1-Bakiye Sorgulama")
    print("2-Para Yatırma")
    print("3-Para Çekme")
    print("4-Çıkış")

def bakiye_sorgula(bakiye):
    print("Bakiyeniz:",bakiye)

def para_yatir(bakiye):
    miktar=int(input("Yatırmak istediğiniz miktar:"))
    bakiye+=miktar
    print("Yeni bakiyeniz:",bakiye)
    return bakiye

def para_cek(bakiye):
    miktar=int(input("Çekmek istediğiniz miktar:"))
    if miktar>bakiye:
        print("Yetersiz bakiye.")
    else:
        bakiye-=miktar
        print("Yeni bakiyenz:",bakiye)
    return bakiye
bakiye=10000

while True:
    menu()
    secim=input("Seçiminiz:")
    if secim=="1":
        bakiye_sorgula(bakiye)
    elif secim=="2":
        bakiye=para_yatir(bakiye)
    elif secim=="3":
        bakiye=para_cek(bakiye)
    elif secim=="4":
        print("Çıkış yapılıyor...")
        break
    else:
        print("Geçersiz seçim.")