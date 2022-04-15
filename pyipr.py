import numpy as np
import math

class IPR:
    
    def __init__(self):
        self.res_p = 0.0
        self.pi = 0.0
        self.test_bhp = 0.0
        self.test_ql = 0.0
        self.pbub = 0.0
        self.type = 'PI'
        self.rsi = 0.0
        self.oilapi = 0.0
        self.gassg = 0.0
        self.temp = 0.0

    def calc_pbub(self):
        if self.oilapi <= 30.0:
            C1 = 0.0362
            C2 = 1.0937
            C3 = 25.724
        else:
            C1 = 0.0178
            C2 = 1.187
            C3 = 23.931
        
        self.pbub = (self.rsi/(C1*self.gassg*math.exp(C3*(self.oilapi/(self.temp + 460)))))**(1/C2)

    def get_ipr(self):
        assert self.res_p > 0.0, 'IPR Invalid: Reservoir Pressure of %0.2f is low' % self.res_p
        assert self.pbub > 0.0, 'IPR Invald: Bubble Point Pressure of %0.2f is low' % self.pbub
        assert self.type == 'PI' or self.type == 'Test'

        if self.pbub > self.res_p: #ensure bubble point pressure is at most reservoir pressure
            self.pbub = self.res_p
            print('Warning: Bubble Point Pressure set to Reservoir Pressure of %0.2f' % self.res_p)
        
        if self.type == 'Test':
            assert self.test_ql > 0, 'Test Data Invalid: Liquid Rate of %0.2f is low' % self.test_ql
            assert self.test_bhp > 0, 'Test Data Invalid: BHP of %0.2f is low' % self.test_bhp
            assert self.test_bhp < self.res_p, 'Test Data Invalid: BHP of %0.2f is greater than Res Pressure of %0.2f' % (self.test_bhp, self.res_p)
            self.pi = self.test_ql / (self.res_p - self.test_bhp)

        assert self.pi > 0.0, 'IPR Invalid: PI of %0.2f is low' % self.pi
        
        ql_bub = self.pi*(self.res_p - self.pbub) #calcualte liquid flow rate at bubble point
        ql_max = ql_bub + self.pi*self.pbub/1.8 #calculate maximum liquid rate
        
        pwf = (np.linspace(0.001, self.res_p, num = 19)).tolist() #create pwf array
        pwf.append(self.pbub) #add bubble point to pwf array
        pwf = sorted(pwf) #sort pwf 

        ql_darcy = [(self.res_p - i) * self.pi for i in pwf if i >= self.pbub] #calculate darcy IPR
        ql_vogel = [(ql_bub + (ql_max - ql_bub)*(1-0.2*(i/self.pbub)-0.8*(i/self.pbub)**2)) for i in pwf if i < self.pbub] #calculate vogel IPR
        ql = ql_vogel + ql_darcy #combine IPRs into one

        ipr_arr = {'Pwf': pwf,
            'LiqRate': ql}
        return(ipr_arr)
    
    #def calc_pi(self, ql, bhp):
    #    assert self.test_ql > 0, 'Test Data Invalid: Liquid Rate of %0.2f is low' % self.test_ql
    #    assert self.test_bhp > 0, 'Test Data Invalid: BHP of %0.2f is low' % self.test_bhp
    #
    #    pi = self.test_ql


# oil pvt correlations: https://www.ihsenergy.ca/support/documentation_ca/Harmony_Enterprise/2019_3/content/html_files/ref_materials/calculations/oil_correlations.htm

# can also use import numpy as np
# from pvtcorrelation import *
# or this https://github.com/yohanesnuwara/pyreservoir/blob/master/notebooks/pvt_correlation_notebook.ipynb 

# gas pvt correlations: 