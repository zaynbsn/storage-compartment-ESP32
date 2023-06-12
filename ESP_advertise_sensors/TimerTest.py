from machine import Timer

def mycallback(t, stop):
    print('helo')
    if  not stop:
      timer_0.init(mode=Timer.ONE_SHOT, period=1000, callback=mycallback)
# one shot firing after 1000ms
timer_0 = Timer(0)
timer_0.init(mode=Timer.ONE_SHOT, period=1000, callback=mycallback)