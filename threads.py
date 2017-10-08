import threading


def c(f):
    return input(f+'>>')


def f():
    t1=threading.Thread(target=c,args='f')
    t1.start()
    t1.join()
    print('f fin')



f()