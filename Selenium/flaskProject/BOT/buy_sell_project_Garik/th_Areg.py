import threading
import time


class myThread1 (threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        self.__finish = False

    def run(self):
        while self.__finish is False:
            print("Thread 1")


    def finish(self):
        self.__finish = True

class myThread2 (threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        self.__finish = False

    def run(self):
        while self.__finish is False:
            print("Thread 2")


    def finish(self):
        self.__finish = True


thread1 = myThread1()
thread1.start()

thread2 = myThread2()
thread2.start()

time.sleep(10)

thread1.finish()
thread2.finish()
