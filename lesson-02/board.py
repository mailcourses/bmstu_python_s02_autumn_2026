import time
from collections import deque


def time_counter(k: int):
    if not isinstance(k, int) or k < 0:
        raise TypeError("k must be int")

    counter: int = 0
    time_of_work: deque[float] = deque(maxlen=k)
    sum_of_time: float = 0

    def deck(func):
        def inner(*args, **kwargs):
            nonlocal counter, time_of_work, sum_of_time
            t_start = time.time()
            try:
                result = func(*args, **kwargs)
                return result
            finally:
                t_end = time.time()
                if counter < k:
                    counter+=1
                else:
                    sum_of_time -= time_of_work.popleft()
                time_of_work.append(t_end - t_start)
                sum_of_time += t_end - t_start
                average = sum_of_time / counter
                print(f"average time = {average}, func name: {func.__name__}")
        return inner
    return deck


@time_counter(2)
def add(a, b):
    return a + b
    
"""@time_counter(1)
def exc():
    raise Exception"""

# add = time_counter(add)


for i in range(5):
    add(i**2, (i+1)**2)
#exc()


# a + b
# 0 + 1 = 1
# 1 + 1 = 2
# 2 + 1 = 3

# [1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377, 610, 987, 1597, 2584, 4181, 6765]

def fib(n: int, min_value: int, max_value: int):
    a, b = 0, 1
    count = 0
    while count < n:
        a, b = b, a + b
        if min_value <= a <= max_value:
            continue
        yield a
        count += 1

print(list(fib(20, 12, 150)))



class TimeCounter:
    def __init__(self):
        self._start_time = 0
        
    def __enter__(self):
        self._start_time = time.time()
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        print(time.time() - self._start_time)


with TimeCounter():
    time.sleep(1)




# aaaaaaaabbc -> iter[('a', 8), ('b', 2), ('c', 1)]

def compress(items):
    count = 0
    current = None
    
    for item in items:
        if current is None:
            count += 1
            current = item
        elif item == current:
            count += 1
        else:
            yield current, count
            
            current = item
            
            count = 1
    
    if current is not None:
        yield current, count
    
    
    
print(list(compress(fib(4, 10, 20))))
print(list(compress("aaaabbc")))
print(list(compress([1,1,1,2,2,3])))
print(list(compress("1")))
print(list(compress([])))

