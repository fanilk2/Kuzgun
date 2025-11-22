#Method Nedir?
#Fonksiyonlara benzer yapılar. Ama methodlar bir nesneye bağlıdır.
#Nesneye bağlı oldukları için çağırma şekilleri farklıdır.
#Nesne.method()
#Örnek: string methodları
isim="Fehmi Anıl KARABIYIK"
result=isim.lower() #tüm harfleri küçültür
result=isim.upper() #tüm harfleri büyültür
result=isim.title() #her kelimenin ilk harfini büyültür
result=isim.strip() #başındaki ve sonundaki boşlukları siler
result=isim.replace(" ","-") #boşlukları - ile değiştirir
result=isim.split(" ") #boşluklardan bölüp liste yapar
result=isim.find("Anıl") #Anıl kelimesinin başladığı indexi verir
result=isim.startswith("F") #F ile başlıyor mu?
result=isim.endswith("K") #K ile bitiyor mu?
result=isim.isalpha() #sadece harflerden mi oluşuyor?
result=isim.isdigit() #sadece rakamlardan mı oluşuyor?
result=isim.index("A") #A harfinin indexini verir
result=isim.count("a") #isim içinde kaç tane a var?
result=len(isim) #isim değişkeninin karakter sayısını verir
#Örnek: liste methodları
numbers=[1,5,7,9,3,2,4,6,8]
numbers.append(10) #liste sonuna 10 ekle
numbers.insert(0,0) #0.indexe 0 ekle
numbers.insert(3,99) #3.indexe 99 ekle
numbers.remove(99) #ilk bulduğu 99'u siler
numbers.pop() #son elemanı siler
numbers.sort() #küçükten büyüğe sıralar
numbers.reverse() #listeyi ters çevirir
val=min(numbers) #küçük elemanı verir
val=max(numbers) #büyük elemanı verir
val=sum(numbers) #elemanları toplar
val=numbers.index(5) #5 sayısının indexini verir
val=numbers.count(9) #9 sayısının kaç tane olduğunu verir
#numbers.clear() #listeyi temizler
numbers.reverse() #listeyi ters çevirir
print(val)