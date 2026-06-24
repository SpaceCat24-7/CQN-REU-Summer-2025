'''
Riley Hebert
CQN REU Summer 2025
Project Goal: create and use an interferometer to measure the spectra of 
ultrafast light pulses
This program contains

'''
# importing function/ graph library
import numpy as np
import matplotlib.pyplot as plt



def plot_practice():
  x = np.arange(0, 4*(np.pi), 0.05) 
  y = np.sin(x) 
  plt.plot(x,y)

# plot_practice()

def polarpoint():
  transmitted = np.array([7.50, 12.19, 15.7, 15.9, 12.95, 7.95, 3.35, 1.217, 2.61,
    6.84, 11.93, 15.6, 15.8, 12.72, 7.67, 3.15, 0.808, 2.21, 6.54])

  reflected = np.array([9.48, 4.55, 1.165, 0.962, 3.92, 8.84, 13.26, 15.33, 13.16,
    9.25, 4.82, 1.194, 0.889, 3.96, 8.98, 13.45, 15.43, 14.47, 10.18])

  return transmitted, reflected

def polarplot(horiz, vert):
    x = np.arange(0, 190, 10)
    y1 = horiz
    y2 = vert
    plt.plot(x,y1, label = "Transmitted Power")
    plt.plot(x, y2, label = "Reflected Power")
    plt.xlabel("Angle (degrees)")
    plt.ylabel("Power Emitted (mW)")
    plt.title("Power Emission vs. Half-Wave Plate Angle")
    #plt.legend()
    plt.show()

def make_noisy(trans, refl):
    trans_noise = np.random.normal(0, 0.7, 19)
    refl_noise = np.random.normal(0, 0.7, 19)
    trans = trans + trans_noise
    refl = refl + refl_noise
    return trans, refl
    
    
def main():    
    tuples = polarpoint()
    noise_tuple = make_noisy(tuples[0],tuples[1])
    polarplot(noise_tuple[0], noise_tuple[1])
    
main()


 

