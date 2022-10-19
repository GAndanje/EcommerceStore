class Mixin:
    def largest(a,b):
        if a>b:
            return a
        if b>a:
            return b
        print(f'{a} equals {b}')
    
    def smallest(a,b):
        if a>b:
            return a
        if b>a:
            return b
        print(f'{a} equals {b}')

    def add(a,b):
        return a+b

    def subtract(a,b):
        return a-b