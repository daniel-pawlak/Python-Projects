import time

def func_timer(func, val):
    print('Function name: ', func.__name__)
    start_time = time.perf_counter()
    print('Result is: ', func(val))
    end_time = time.perf_counter()
    run_time = end_time - start_time
    print('Runtime is: ', run_time, end='\n\n')

def fibonacci(num):
    if num < 2:
        return num
    return fibonacci(num - 1) + fibonacci(num - 2)

def fibonacci_loop(num):
    if 0 < num <= 2:
        return 1
    elif num == 0:
        return 0
    else:
        x = 2
        a = 1
        b = 1
        for i in range(2, num):
            x = a + b
            a, b = b, x
            # print(x)
        return x

def fib(n, memo = {}):
    if n in memo:
        return memo[n]
    elif n <= 2:
        return 1

    memo[n] = fib(n - 1, memo) + fib(n - 2, memo)
    return memo[n]

x = 30
func_timer(fibonacci, x)
func_timer(fibonacci_loop, x)
func_timer(fib, x)