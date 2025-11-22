import math

value =dir(math) #math modülündeki tüm özellikleri listele
print(value)
result=math.factorial(5) #5'in faktöriyeli
math.ceil(3.14) #3.14'ü yukarı yuvarla
math.floor(3.14) #3.14'ü aşağı yuvarla
math.sqrt(16) #16'nın karekökü
math.gcd(12,8) #12 ve 8'in ebob'u
math.lcm(12,8) #12 ve 8'in ekok'u
math.sin(90) #90'ın sinüsü
math.cos(90) #90'ın kosinüsü
math.tan(90) #90'ın tanjantı
math.log10(100) #100'ün logaritması
math.log2(100) #100'ün logaritması
math.pow(2,3) #2 üzeri 3
math.pi #pi sayısı
math.e #e sayısı
math.radians(90) #90'ı radyana çevirir
math.degrees(3.14) #3.14'ü dereceye çevirir
math.copysign(3,-2) #3'ün işaretini -2 yapar
math.isfinite(3) #3 sayısı sonlu mu?
math.isinf(3) #3 sayısı sonsuz mu?
math.isnan(3) #3 sayısı tanımsız mı?
math.trunc(3.14) #3.14'ün tam sayı kısmını alır
math.fabs(-3) #-3'ün mutlak değeri
math.modf(3.14) #3.14'ü tam ve ondalık kısma ayırır
math.exp(3) #e üzeri 3
math.dist([1,2],[3,4]) #[1,2] ve [3,4] noktaları arasındaki mesafe
math.hypot(3,4) #dik üçgende hipotenüs uzunluğu
math.prod([1,2,3,4]) #1*2*3*4 çarpımı
math.comb(5,2) #5'in 2'li kombinasyonu
math.perm(5,2) #5'in 2'li permütasyonu
math.factorial(5) #5'in faktöriyeli
math.gamma(5) #5'in gamma fonksiyonu
math.lgamma(5) #5'in log gamma fonksiyonu
math.fsum([1,2,3,4]) #1+2+3+4 toplamı
math.isclose(3.14,3.14159,rel_tol=1e-5) #3.14 ve 3.14159 yakın mı?
math.nextafter(1,2) #1'den 2'ye en yakın float sayı
math.ulp(1) #1 sayısının en küçük farkı
math.perm(5,3) #5'in 3'lü permütasyonu
math.comb(5,3) #5'in 3'lü kombinasyonu
math.remainder(5,3) #5'in 3'e bölümünden kalan
math.gcd(48,18) #48 ve 18'in ebob'u
math.lcm(48,18) #48 ve 18'in ekok'u
math.ulp(1.0) #1.0 sayısının en küçük farkı
math.dist((1,2),(4,6)) # (1,2) ve (4,6) noktaları arasındaki öklidyen mesafe
math.hypot(3,4,5) #3,4,5 dik üçgeninde hipotenüs uzunluğu
from math import * 
value=hypot(14,52,36)
print(value)