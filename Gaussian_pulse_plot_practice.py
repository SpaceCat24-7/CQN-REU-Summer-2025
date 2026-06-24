# -*- coding: utf-8 -*-
"""
Created on Thu Jun 26 13:41:48 2025

@author: Riley
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.fft import fft, fftfreq
#from scipy.optimize import curve_fit

def make_gauss(freq):
    t1 = np.arange(-5,5,0.01)
    A_naught = 1
    tau = 1
    omega_0 = 2 * np.pi * freq
    y = A_naught * np.e ** (-t1**2 / tau**2) * np.e ** (omega_0*(0-1j)*t1)
    t = np.arange(-105,105,0.01)
    return [t,np.pad(y, (10000,10000))]

def plotting(data):
    horiz_axis = data[0]
    vert_axis = data[1]
    plt.plot(horiz_axis,vert_axis)
    
def fourier_transform(data):
    n = len(data[0])
    duration = data[0][n-1] - data[0][0]
    yf = fft(data[1])
    sample_rate = n/duration
    xf = fftfreq(n,1/sample_rate)
    return [xf, (np.abs(yf))**2]

def main():
    data = make_gauss(40)
    plotting(data)
    plt.show()
    trans_data = fourier_transform(data)
    trans_data = [trans_data[0][11000:13000],trans_data[1][11000:13000]]
    plotting(trans_data)
    plt.show()
    
main()
    
    
    
    
    
    
    
    