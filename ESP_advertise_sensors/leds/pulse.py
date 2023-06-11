from time import sleep_ms

class Pulse:
  @staticmethod
  def pulseColor(i, ledsStrip, pixels):
    for slot in pixels:
      if slot['color'] == 'white':
        for pixel in slot['pixels']:
          ledsStrip[pixel] = (i, i, i)
      else:
        for pixel in slot['pixels']:
          ledsStrip[pixel] = (i, 0, 0)

    ledsStrip.write()
    sleep_ms(5)

  @staticmethod
  def animate(ledsStrip, pixels, duration):
    '''
    @params : {
      pixels: {
        {color : 'red', pixels: [0, 1, 2] }, 
        {color : 'white', pixels: [3, 4, 5, 6] }
      }
    }
    }
    '''
    while duration > 0:
        for i in range(0, 200):
          Pulse.pulseColor(i=i, ledsStrip=ledsStrip, pixels=pixels)
        
        for j in range(200, 0, -1):
          Pulse.pulseColor(i=j, ledsStrip=ledsStrip, pixels=pixels)

        duration -= 1