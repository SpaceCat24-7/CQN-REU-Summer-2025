# -*- coding: utf-8 -*-
"""
Created on Mon Jul  7 16:11:10 2025

@author: Riley
"""

'''
This will hopefully be the code I use to anaylize my data!!
'''

import numpy as np
import matplotlib.pyplot as plt
from scipy.fft import rfft, rfftfreq
from scipy.optimize import curve_fit



def x_to_tau(x):
    tau = x/lightspeed * 2
    return tau
    
    
#global variables for now
motor_velocity = 0.0014 #m/s
freq_0 = 391.9e12 #Hz
lightspeed = 2.998e8 #m/s
wave_0 = lightspeed/freq_0 #m
SR = 10000 #samples per second
n = SR*2*wave_0/motor_velocity #resolution
motor_accl = 0.004 #m/s^2
#x_weird = 4 * motor_velocity**2 / (2*motor_accl) #m
#tau_weird = x_to_tau(x_weird) #s
x_range = 0.05 #- x_weird #m
tau_range = x_to_tau(x_range) #s
step_size = x_to_tau(wave_0/(2*n))
sigma = 33.973e-12

def make_fake_pulse():
    tau = np.arange(-tau_range/2,tau_range/2,step_size) 
    C = 0
    A = 5
    omega = 2 *np.pi* freq_0
    output = C + A**2*g_of_tau(tau,sigma)*np.cos(omega*tau)
    pulse = make_noisy([tau,output])
    return pulse

def make_fake_mono():
    tau = np.arange(-tau_range/2,tau_range/2,step_size)
    C = 0
    A = 5
    omega = 2 *np.pi* freq_0
    output = C + A**2*np.cos(omega*tau)
    mono = make_noisy([tau,output])
    return mono

def make_fake_cw():
    tau = np.arange(-tau_range/2,tau_range/2,step_size)
    C = 0
    A = 5
    omega = 2 *np.pi* freq_0
    sig = 1e-6
    output = C + A**2*g_of_tau(tau,sig)*np.cos(omega*tau)
    pulse = make_noisy([tau,output])
    return pulse

def make_noisy(pure_data):
    x = pure_data[0]
    y = pure_data[1]
    data_num = len(y)
    noise = np.random.normal(0,250e-12, data_num)
    with_noise = y + noise
    return [x, with_noise]
    
def g_of_tau(tau,sig):
    A = np.sqrt(np.pi/2)*sig
    g = gauss(tau, A,1/sig**2 ,0)
    return g

    
def plot_noisy_data(data):
    x = data[0]
    y = data[1]
    plt.plot(x*1e12+150,y/20*1e10,"-")
    plt.xlabel("Tau (ps)")
    plt.ylabel("Intensity (a.u.)")
    #plt.xlim(0,290)
    #plt.title("Noisy Simulated Data for "+input("Pulsed or Continuous?\n")+" Wave")
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
    y = data[1]
    par1 = max(y)
    par2 = 2*np.pi**2*sigma**2
    c = freq_0
    guess = [par1,par2,c]
    parameters, covariance = curve_fit(gauss,x,y,p0=guess)
    A = parameters[0]
    B = parameters[1]
    c = parameters[2]
    print(parameters)
    fit_y = gauss(x, A, B,c)
    plt.plot(x*1e-12,y/1.75, 'o', label='data')
    #plt.plot(x*1e-12,fit_y/1.75, '-', label='fit')
    plt.xlim(391.88,391.92)
    
    freq = np.arange(3e14,5e14,1e8)
    expect = gauss(freq, A,B,c)
    #plt.title("FT of Simulated "+input("Pulse or CW?\n")+" Data")
    plt.xlabel("Frequency (THz)")
    plt.ylabel("Spectral Intensity (a.u.)")
    #plt.axvline(freq_0/1e12)
    plt.plot(freq*1e-12,expect/1.75, color="green")
    #check = 5**2*sigma**2*np.pi*np.exp(-2*np.pi**2*sigma**2*(freq_0-x)**2)
    #print(sigma**2*(freq_0-freq))
    #print(np.exp(-2*np.pi**2*sigma**2*(freq_0-freq)**2))
    #plt.plot(x,check)
    plt.show()

def gauss(x, A, B,c):
    y = A*np.e**(-1*B*(x-c)**2)
    return y    
    
def main():
    
    #m_data = make_fake_mono()
    p_data = make_fake_pulse()
    '''
    plot_noisy_data(m_data)
    m_trans = fourier_transform(m_data)
    fit_to_fourier(m_trans)
    '''
    plot_noisy_data(p_data)
    p_trans = fourier_transform(p_data)
    fit_to_fourier(p_trans)
    '''
    cw_data = make_fake_cw()
    plot_noisy_data(cw_data)
    cw_trans = fourier_transform(cw_data)
    fit_to_fourier(cw_trans)
    '''
main()
           
    
    
    
    
    
    
    
    


    