class C:
    def __init__(self,i,res):
        self.i=i
        self.j=res
        self.c=0
    def inc(self):
        self.c+=1
        self.j.append(self.c)

def create(i,j):
    c=C(i,j)
    c.inc()

import multiprocessing
from multiprocessing import Manager

if __name__=='__main__':
    manager = Manager()
    return_dict = manager.list()
    print (return_dict.__dict__)

    jobs = []
    for i in range(5):
        p = multiprocessing.Process(target=create, args=(i,return_dict))
        jobs.append(p)
        p.start()

    for proc in jobs:
        proc.join()
    print(return_dict)


