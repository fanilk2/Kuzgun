arabalar=["BMW","Mercedes","Opel","Mazda"]
kactane=len(arabalar) #listedeki eleman sayısı
#print("Listedeki araba sayısı:",kactane)
#print(arabalar[0],arabalar[-1])
arabalar[-1]="Toyota" #son elemanı değiştirir
result=arabalar 
result=arabalar[-2] #sondan ikinci eleman
result=arabalar[0:3] #0,1,2.indexleri verir  
arabalar[-2:]=["Renault","Toyota"] #son iki elemanı değiştirir
arabalar.append("Audi") #liste sonuna ekler
del arabalar[0] #0.indexi siler
result=arabalar
result=arabalar[::-1] #listeyi ters çevirir
#print(result)

#--------------------------------
#List Methods
#--------------------------------

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

#--------------------------------
#Tuple
#--------------------------------
tuple=(1,2,3,4,5)
tip=type(tuple)
print(tip)