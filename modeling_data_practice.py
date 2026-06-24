# -*- coding: utf-8 -*-
"""
Created on Fri Jun 27 14:37:41 2025

@author: Riley
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.fft import rfft, rfftfreq
from scipy.optimize import curve_fit


def make_fake_data():
    tau = np.arange(-163.4,163.4,0.000517)
    #x = 300 * tau / (2)
    C = 0
    A = 5
    omega = 2 *np.pi* 400
    #noisy_tau = tau + np.random.normal(0,.0004,len(tau))
    #plot_noisy_data([tau, noisy_tau])
    output = C + A**2*g_of_tau(tau)*np.cos(omega*tau)
    data = make_noisy([tau,output])
    return data

def plot_noisy_data(data):
    x = data[0]
    y = data[1]
    plt.plot(x,y,"-")
    #plt.xlim(-80,80)
    plt.xlabel("Tau")
    plt.ylabel("Intensity")
    plt.title("Noisy Simulated Data")
    plt.show()
    
def make_noisy(pure_data):
    x = pure_data[0]
    y = pure_data[1]
    data_num = len(y)
    noise = np.random.normal(0,250, data_num)
    with_noise = y + noise
    return [x, with_noise]
    
def g_of_tau(tau):
    sigma = 33.973
    A = np.sqrt(np.pi/2)*sigma
    g = gauss(tau, A,1/sigma**2 ,0)
    #g = np.sqrt(np.pi/2)*sigma*np.e**(-tau**2/(sigma**2))
    return g

def fourier_transform(data):
    n = len(data[0])
    duration = data[0][n-1] - data[0][0]
    yf = rfft(data[1])
    sample_rate = n/duration
    xf = rfftfreq(n,1/sample_rate)
    return [xf, np.abs(yf)**2]

def plot_fourier(data):
    x = data[0]
    y = data[1]
    plt.plot(x,y,"-")
    plt.xlim(399.90,400.10)
    plt.xlabel("Frequency")
    plt.ylabel("Spectral Intensity")
    plt.title("Fourier Transform of Noisy Simulated Data")
    plt.show()
    
def fit_to_fourier(data):
    x = data[0]
    y = data[1]
    par1 = max(y)
    par2 = 100
    c = 400
    guess = [par1,par2,c]
    parameters, covariance = curve_fit(gauss,x,y,p0=guess)
    A = parameters[0]
    B = parameters[1]
    c = parameters[2]
    print(parameters)
    fit_y = gauss(x, A, B,c)
    plt.plot(x, y, 'o', label='data')
    plt.plot(x, fit_y, '-', label='fit')
    plt.xlim(399.985,400.015)
    
    freq = np.arange(399.985,400.015,0.0005)
    expect = gauss(freq, A,B,c)#61984130.6694018, 45564.59/4, 4.00000125e+02)
    plt.plot(freq,expect)
    plt.show()

    
def gauss(x, A, B,c):
    #x = np.longdouble(x)
    y = A*np.e**(-1*B*(x-c)**2)
    return y
    

    
def main():
    data = make_fake_data()
    plot_noisy_data(data)
    trans_data = fourier_transform(data)
    #plot_fourier(trans_data)
    fit_to_fourier(trans_data)
    
    
    
main()







