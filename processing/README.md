```Text
Case 1: Not share memory among each process

N processes -> N caches
Every process just has only 1 Thread -> Single Thread
Number of lock(s): 0
```
```Text
Case 2: Not share memory among each process

N processes -> N caches
Every process has many M Thread(s) -> Multi-thread
Number of locks(s): N locks
```
```Text
Case 3: Share memory among each process

N processes -> 1 cache
Every process just has only 1 Thread -> Single Thread
Number of lock(s): 1 lock
```
```Text
Case 4: Share memory among each process

N processes -> 1 cache
Every process has many M Thread(s) -> Multi-thread
Number of lock(s): 1 lock
```
