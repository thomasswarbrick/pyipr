import numpy as np
import math
import matplotlib.pyplot as plt

def calc_pbub_standing(rsi, gasSG, oilAPI, tempF):
    '''
    Function to calculate Bubble Point Pressure
    Taken from Standing, M.B., 'A Pressure-Volume-Temperature Correlation for Mixtures of California Oils and Gases'
    Drilling and Production Practice, 1947. 275 - 287

    oilAPI = oil density at standard conditions, deg API
    gasSG = gas specific gravity at standard conditions, air = 1.0
    tempF = temperature, degrees Fahrenheit
    rsi = initial solution gas oil ratio, scf/stb
    pbub = bubble point pressure, psia
    '''
    a = 0.00091 * (tempF) - 0.0125 * oilAPI
    return 18.2 * ((np.power((rsi/gasSG),0.83) * np.power(10,a)) - 1.4) 

def calc_pbub_vazquezbeggs(rsi, gasSG, oilAPI, tempF):
    '''
    Function to calculate Bubble Point Pressure
    Taken from Vazquez, M.E. and Beggs, H.D. "Correlations for Fluid Physical Property Prediction",
    JPT. Vol 32 (1980) 968-970

    rsi = initial solution gas oil ratio, scf/stb
    gasSG = gas specific gravity at standard conditions, air = 1.0
    oilAPI = oil density at standard conditions, deg API
    tempF = temperature, degrees Fahrenheit
    sg100 = separator specific gas gravity at 100 psig
    pbub = bubble point pressure, psia
    '''
    if oilAPI <= 30.0:
        C1 = 0.0362
        C2 = 1.0937
        C3 = 25.724
    else:
        C1 = 0.0178
        C2 = 1.187
        C3 = 23.931
    #fixed conditions to standard of 60 F and 14.7 psia
    sg100 = gasSG*(1+(0.00005912*oilAPI*(60)*math.log10(14.7/114.7)))
    C = C1*sg100*math.exp((C3*oilAPI)/(tempF+460))
    pbub = (rsi/C)**(1/C2)
    return pbub

def calc_pbub_glaso(rsi, gasSG, oilAPI, tempF):
    '''
    Function to calculate Bubble Point Pressure
    Taken from Glaso, O. 'Generalised-Pressure-Temperature Correlations'
    JPT. Vol 32 (1980) 785-795

    rsi = initial solution gas oil ratio, scf/stb
    gasSG = gas specific gravity at standard conditions, air = 1.0
    oilAPI = oil density at standard conditions, deg API
    tempF = temperature, degrees Fahrenheit
    pbub = bubble point pressure, psia
    '''
    logA = np.log10(np.power((rsi/gasSG), 0.816)*np.power(tempF, 0.172)/np.power(oilAPI, 0.989))
    pbub = np.power(10, 1.7669+1.7447*logA-0.30218*np.power(logA, 2))
    return pbub

def calc_rs_glaso(p_psia, rsi, gasSG, oilAPI, tempF):
    '''
    Function to calculate Solution Gas Oil Ratio
    Taken from Glaso, O. 'Generalised-Pressure-Temperature Correlations'
    JPT. Vol 32 (1980) 785-795

    p_psia = pressure, psia
    rsi = initial solution gas oil ratio, scf/stb
    gasSG = gas specific gravity at standard conditions, air = 1.0
    oilAPI = oil density at standard conditions, deg API
    tempF = temperature, degrees Fahrenheit
    rs = solution gor, scf/stb
    '''
    if p_psia >= calc_pbub_glaso(rsi, gasSG, oilAPI, tempF):
        rs = rsi
    else:
        X = 14.1811-3.3093*np.log10(p_psia)
        if X < 0.0:
            X = 0.0
        A = np.power(10, 2.8869-np.sqrt(X))
        rs = gasSG*np.power(A * np.power(oilAPI, 0.989)/np.power(tempF, 0.172), 1.2255)
    return rs

def calc_rs(pres, gasSG, oilAPI, rsi, temp):
    assert isinstance(press, (list)), 'pressure should be a list, instead a %s was provided' % type(press)

    pbub = calc_pbub1(rsi, gasSG, oilAPI, temp)
    print('Calculated Bubble Point Pressre as %0.2f' % pbub)

    if oilAPI <= 30.0:
        C1 = 0.0362
        C2 = 1.0937
        C3 = 25.724
    else:
        C1 = 0.0178
        C2 = 1.187
        C3 = 23.931
    rs = []

    for p in pres:
        if p < pbub:
            rs.append(C1*gasSG*p**C2*math.exp(C3*(oilAPI/(temp+460))))
        else:
            rs.append(rsi)
    return rs


rs_list = [600, 800, 1200]

#for rs in rs_list:
#    press = np.linspace(100, 5000, 19).tolist()
#    press.append(calc_pbub1(rs, 0.75, 40.0, 130.0))
#    press = sorted(press)
#    rs_arr = calc_rs(press, 0.75, 40.0, rs, 130.0)

#    plt.plot(press, rs_arr, label=rs)
#    plt.scatter(press, rs_arr)
#    plt.legend()
#plt.show()
pbub = calc_pbub_glaso(800, 0.75, 40, 160)
print('Bubble Point Pressure using Glaso is %0.2f psia' % pbub)
print('GOR at %0.0f psia using Glaso is %0.2f scf/stb' % (3100, calc_rs_glaso(3100, 800.0, 0.75, 40.0, 160)))
