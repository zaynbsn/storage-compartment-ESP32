from time import sleep_ms

class Pulse:
  @staticmethod
  def pulseColor(i, ledsStrip, pixels, color='white'):
    for ledPixels in pixels:
      for pixel in ledPixels:
        if color == 'white':
          ledsStrip[pixel] = (i, i, i)
        else:
          ledsStrip[pixel] = (i, 0, 0)

    ledsStrip.write()
    sleep_ms(5)

  @staticmethod
  def animate(ledsStrip, pixels, duration, color='white'):
    while duration > 0:
        for i in range(0, 200):
          Pulse.pulseColor(i=i, ledsStrip=ledsStrip, pixels=pixels, color=color)
        
        for i in range(200, 0, -1):
          Pulse.pulseColor(i=i, ledsStrip=ledsStrip, pixels=pixels, color=color)

        sleep_ms(250)
        duration -= 1