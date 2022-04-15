import numpy as np
import math
import matplotlib.pyplot as plt

#oilAPI = 40.0 
#gasSG = 0.75
#gor = 800.0
#temp = 130.0

def calc_pbub1(rsi, gasSG, oilAPI, temp):
    if oilAPI <= 30.0:
        C1 = 0.0362
        C2 = 1.0937
        C3 = 25.724
    else:
        C1 = 0.0178
        C2 = 1.187
        C3 = 23.931
    
    pbub = (rsi/(C1*gasSG*math.exp(C3*(oilAPI/(temp + 460)))))**(1/C2)
    return pbub

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

for rs in rs_list:
    press = np.linspace(100, 5000, 19).tolist()
    press.append(calc_pbub1(rs, 0.75, 40.0, 130.0))
    press = sorted(press)
    rs_arr = calc_rs(press, 0.75, 40.0, rs, 130.0)

    plt.plot(press, rs_arr, label=rs)
    plt.scatter(press, rs_arr)
    plt.legend()
plt.show()

