
import array

def main2(steps_per_insert, total_times):

    nxt = array.array('l',[-1] * (total_times+1))

    cdef int zero
    cdef int ptr

    zero = 0
    nxt[0] = 0
    ptr = nxt[0]

    for i in range(1,total_times+1):
        if i % 100000 == 0:
            print(i)
        for _ in range(steps_per_insert):
            ptr = nxt[ptr]
        nxt[i] = nxt[ptr]
        nxt[ptr] = i
        ptr = i

    return nxt[zero]

print( main2( 345, 50*1000*1000))    
