#--------------------------------
#assignment operators
#--------------------------------
x,y,z=5,10,15
x+=3 #x=x+3 toplama
y*=2 #y=y*2 çarpma
z/=5 #z=z/5 bölme
x-=4 #x=x-4 çıkarma
y//=3 #y=y//3 tam bölme
z**=2 #z=z**2 üs alma
x%=3 #x=x%3 mod alma
y&=2 #y=y&2 bitwise and
values=1,2,3 
x,y,z=values #values listesindeki elemanları sırayla x,y,z değişkenlerine atar

#--------------------------------
#comparison operators
#--------------------------------
a=5
b=10
result=a==b #eşit mi
result=a!=b #eşit değil mi
result=a>b #büyük mü
result=a<b #küçük mü
result=a>=b #büyük eşit mi
result=a<=b #küçük eşit mi
result=a is b #a,b aynı mı
result=a is not b #a,b aynı değil mi

#--------------------------------
#logical operators
#--------------------------------
k=5
l=10
result=(k<l) and (k==5) #and operatörü
result=(k<l) or (k==5) #or operatörü
result=not(k<l) #not operatörü

#--------------------------------
#bitwise operators
#--------------------------------
m=5  #binary: 0101
n=3  #binary: 0011
result=m & n #bitwise and 0001=1
result=m | n #bitwise or  0111=7
result=m ^ n #bitwise xor 0110=6
result=~m #bitwise not -6
result=m << 1 #bitwise left shift 1010=10
result=m >> 1 #bitwise right shift 0010=2

#--------------------------------
#identity & Membership operators
# --------------------------------
p=5
q=5
result=p is q #p,q aynı mı  
result=p is not q #p,q aynı değil mi
result='a' in 'Anil' #a,Anıl içinde mi 
result='a' not in 'Anil' #a,Anıl içinde değil mi