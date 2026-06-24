# -*- coding: utf-8 -*-
"""
Created on Wed Jun 25 13:16:30 2025

@author: Riley
"""

'''
Riley Hebert
CQN REU Summer 2025
Project Goal: create and use an interferometer to measure the spectra of 
ultrafast light pulses
This program contains ten functions that create random sinusoidal data,
add noise, and plot the original data as well as its Fourier transform.
It also fits the scatter plot to a sinusoidal function.
'''
# importing function/ graph library
import numpy as np
import matplotlib.pyplot as plt
from scipy.fft import rfft, rfftfreq
from scipy.optimize import curve_fit



def make_sine_data():
    '''
    This function creates pure sinusoidal data. The x values start at
    zero and end at 4pi, with a step of 0.1. Then they are input into 
    the numpy sine function to find the corresponding y values.
     Args:
         none
     Returns:
         [x,y]: 2D array containing pure sinusoidal data
    '''
    # set up an array with the numbers that will become our x values
    x = np.arange(0, 4*(np.pi), 0.1) 
    # create another array containing the output of putting our x values
    # in the sine function
    y = np.sin(x) 
    # return both arrays in the form of a 2D list
    return [x,y]


def plotting(data):
    '''
    This function creates pure sinusoidal data. The x values start at
    zero and end at 4pi, with a step of 0.1. Then they are input into 
    the numpy sine function to find the corresponding y values.
     Args:
         none
     Returns:
         [x,y]: 2D array containing pure sinusoidal data
    '''
    x = data[0]
    y = data[1]
    plt.plot(x,y)
    plt.xlabel("x-axis")
    plt.ylabel("y-axis")
    plt.title("Sine Wave")
    plt.show()
    

def make_noisy(sine_array):
    x = sine_array[0]
    y = sine_array[1]
    data_num = len(y)
    noise = np.random.normal(0, 0.2, data_num)
    with_noise = y + noise
    return [x, with_noise]

def fourier_analysis(data):
    n = len(data[0])
    duration = data[0][n-1] - data[0][0]
    yf = rfft(data[1])
    sample_rate = n/duration
    xf = rfftfreq(n,1/sample_rate)
    return [xf, yf]

def fourier_plot(trans_data):
    plt.plot(trans_data[0], np.abs(trans_data[1]))
    plt.xlabel("x-axis")
    plt.ylabel("y-axis")
    plt.title("Fourier Transform")
    plt.show()

def fit_to_sine(data):
    x = data[0]
    y = data[1]
    #max_y = max(y)
    #n = len(x)
    #cycle_amt = (x[n-1] - x[0]) / (2*(np.pi))
    #guess = [max_y, cycle_amt]
    parameters, covariance = curve_fit(sine, x, y) #, p0 = guess)
    A_fit = parameters[0]
    omega_fit = parameters[1]
    fitted_y = sine(x, A_fit, omega_fit)
    return [x,y,fitted_y]
    
def sine(x, A, omega):
    y = A*np.sin(omega*x)
    return y  
    
def plot_together(unfit, fit):
    plt.plot(unfit[0],unfit[1],"o")
    plt.plot(fit[0],fit[1],"-")
    plt.show()
    
def main_1():
    pure_data = make_sine_data()
    noisy_data = make_noisy(pure_data)
    plotting(noisy_data)
    trans_data = fourier_analysis(noisy_data)
    fourier_plot(trans_data)
    i, j = np.where(np.abs(trans_data) == max(np.abs(trans_data[1])))
    print("The central frequency is "+str(trans_data[0][j]))

def main_2():
    pure_data = make_sine_data()
    noisy_data = make_noisy(pure_data)
    fits = fit_to_sine(noisy_data) 
    unfitted_data = [fits[0], fits[1]]
    fitted_data = [fits[0], fits[2]]
    plot_together(unfitted_data, fitted_data)


main_1()   

 
main_2()



 

