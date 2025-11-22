def sayHello():
    print("Hello")

def sayhi(name):
    return "Hi "+name

msg=sayhi("John")

#function parameters
def add(x,y):
    return x+y

result=add(3,5)

def evenCheck(x):
    if x%2==0:
        return True
    else:
        return False
    
result=evenCheck(5)

def factorial(x):
    result=1
    for i in range(1,x+1):
        result*=i
    return result

result=factorial(5)

def listSum(params):
    result=0
    for i in params:
        result+=i
    return result

result=listSum([1,3,5,7,9]) 

print(result)