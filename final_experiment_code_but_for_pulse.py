# -*- coding: utf-8 -*-
"""
Created on Wed Jul 30 17:39:41 2025

@author: Riley
"""

# -*- coding: utf-8 -*-
"""
Created on Mon Jul 14 11:21:39 2025

@author: Riley
"""

'''
This will hopefully actually be the code I use to anaylize my data!!
'''
#import necessary packages
import numpy as np
import matplotlib.pyplot as plt
from scipy.fft import rfft, rfftfreq
from scipy.optimize import curve_fit
from scipy.interpolate import make_smoothing_spline
from itertools import islice
import csv


def x_to_tau(x_values):
    '''
    This function returns the corresponding time
    shift values for each position
    Args:
        x: float representing position on the table relative to 
        starting point
        lightspeed: float representing the speed of light in a vacuum
    Returns:
        tau: float representing then corresponding time shift in 
        the interferometer
    '''
    # this is the mathematical relationship between x and tau
    tau_values = []
    for x in x_values:
        tau = x/lightspeed * 2
        tau_values.append(tau)
    return tau_values
    
    
#global variables for now
motor_velocity = 0.0014 #m/s
freq_0 = 391.9e12 #Hz
lightspeed = 2.998e8 #m/s
wave_0 = lightspeed/freq_0 #m
n = 10 #resolution
SR = 40000 #samples per second
motor_accl = 0.008 #m/s^2 
sigma = 33.973e-12 #s

def t_to_tau(times):
    x_values = []
    wibbly_indices = int((motor_velocity/motor_accl)*SR) 
    speeding = wibbly_indices+1
    slowing = len(times)-wibbly_indices
    t_speed = times[speeding]
    t_slow = times[slowing]
    for i in range(speeding):
        t = times[i]
        x = 0.5*motor_accl*t**2
        x_values.append(x)
    x_shift1 = x
    for i in range(speeding,slowing):
        t = times[i]-t_speed
        x = motor_velocity*t+x_shift1
        x_values.append(x)
    x_shift2 = x
    for i in range(slowing,len(times)):
        t = times[i]-t_slow
        x = motor_velocity*t+0.5*-1*motor_accl*t**2+x_shift2
        x_values.append(x)
    taus = x_to_tau(x_values)
    return taus
    
    
    
    
def get_data(filename):
    '''
    This function reads a .csv file containing the intensity 
    measurements recorded by the photodiode, extracts the
    values, and assigns the corresponding time shift value
    Args:
        filename: name of the file with the intensity values
        tau_range: the total shift in time experienced by one beam
            relative to the other
        step_size: the change in time shift per data point
    Returns:
        real_data: a 2D dictionary holding a dictionary of the independent 
        variables, the time shift, at index zero and a dictionary of
        the corresponding intensity of the overlapping beam at index 1
    '''
    # this section grabs the y values, the intensities for each shift
    with open(filename,"r") as file:
        reader = csv.reader(file)
        y_values = []
        times = []
        for line in islice(reader, 8, None):
            times.append(float(line[0]))
            y_values.append(float(line[1]))
    # this section calculates what those shifts are based on how fast 
    #the motor moves 
    taus = t_to_tau(times)
   # i = taus.index(300)
    tau_values = taus[0:1080000]
    ys = y_values[0:1080000]
    # this is the data set the rest of the code analyzes
    real_data = [taus, y_values]
    return real_data
    
def g_of_tau(tau):
    '''
    This function calculates the correlation between the Gaussian 
    components of each (pulsed) beam based on given information about
    the laser, which depends on the relative temporal shift
    Args:
        tau: the time delay from one beam relative to the other
        sigma: the standard deviation of the Gaussian function that 
        describes the pulse in time, which has a full width half max of 80
        picoseconds
    Returns:
        g: the numerical value of the correlation
    '''
    A = np.sqrt(np.pi/2)*sigma
    g = gauss(tau, A,1/sigma**2 ,0)
    return g

    
def plot_data(data):
    x = []
    for val in data[0]:
        x.append(val*1e12)
    y = []
    for val in data[1]:
        y.append(val)   
    plt.plot(x,y,"-")
    plt.xlabel("Tau (ps)")
    plt.ylabel("Intensity (a.u.)")
    #plt.ylim(0,2e5)
    plt.xlim(175.65,177)
    #plt.xlim(1.9995e2,2.0e2)
    #plt.title("Experimental Data for "+input("Pulsed or Continuous?\n")+" Wave")
    plt.show()
    
def fourier_transform(data):
    n = len(data[0])
    duration = data[0][n-1] - data[0][0]
    yf = rfft(data[1])
    sample_rate = n/duration
    xf = rfftfreq(n,1/sample_rate)
    return [xf, np.abs(yf)**2]

def fit_to_fourier(data):
    x = data[0]
    data[1][0] = 0
    y = data[1]
    #smoothed = make_smoothing_spline(x,y)
    par1 = max(y[1:])
    par2 = 2*np.pi**2*sigma**2
    c = freq_0
    guess = [par1,par2,c]
    parameters, covariance = curve_fit(gauss,x,y,p0=guess)
    A = parameters[0]
    B = parameters[1]
    c = parameters[2]
    print(parameters)
    #fit_y = gauss(x, A, B,c)
    plt.plot(x*1e-12, y, 'o', label='data', markersize=0.5)
    #plt.plot(x, fit_y, '-', label='fit')
    #plt.xlim(391.885e12,391.915e12)
    plt.ylim(0,0.08e7)
    #plt.xlim(3.519e2,4.319e2)
    #plt.xlim(391.8,392)
    #plt.xlim(375,415)
    plt.xlim(380,390)
    
    freq = np.arange(3e14,5e14,0.0005e12)
    expect = gauss(freq, A, B, c)
    #plt.title("FT of "+input("Pulse or CW?\n")+" Experimental Data")
    plt.xlabel("Frequency (THz)")
    plt.ylabel("Spectral Intensity (a.u.)")
    #plt.axvline(freq_0/1e12, color = "black")
    #plt.plot(freq*1e-12,expect*1/7*1e-7, color = "black")
    plt.show()

def gauss(x, A, B,c):
    y = A*np.exp(-1*B*(x-c)**2)
    return y    
    
def main():
    #file = "D:\\CarvePulseTest_19700101_120301.csv"
    #file = "C:\\Users\\janet\\OneDrive\\Summer 2025 REU Project\\Actual_Pulse_19700101_130321.csv"
    file = "C:\\Users\\janet\\OneDrive\\Summer 2025 REU Project\\Actual_FemtoPulse_19700101_131343.csv"
    data = get_data(file)
    plot_data(data)
    trans_data = fourier_transform(data)
    #plot_data(trans_data)
    fit_to_fourier(trans_data)
    
main()
    
    
    
    
    
    
    
    
    
    
  
    
  
    
  
  