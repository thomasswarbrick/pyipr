import numpy as np
import math

class IPR:
    
    def __init__(self):
        '''
        Initialises instance of ipr
        
        res_p = reservoir pressure, psia
        pi = productivity index, stb/d/psi
        test_bhp = test bottom hole pressure, psia
        test_ql = test liquid rate, stb/d
        pbub = bubble point pressure, psia
        type = 'PI' or 'Test', PI can be set manually or calculated from test parameters 
        '''
        self.res_p = 0.0
        self.pi = 0.0
        self.test_bhp = 0.0
        self.test_ql = 0.0
        self.pbub = 0.0
        self.type = 'PI'

    def get_ipr(self):
        '''
        function to return dictionary of Pwf and Rate
        calculated based on what parameters are currently present for
        instance of ipr.

        IPR returned is composite:
        - using PI above bubble point, as flow will be single phase
        - using vogel below the bubble point, presence of gas reduces productivity due to relative
            permeability effects
        '''
        assert self.res_p > 0.0, 'IPR Invalid: Reservoir Pressure of %0.2f is low' % self.res_p
        assert self.pbub > 0.0, 'IPR Invald: Bubble Point Pressure of %0.2f is low' % self.pbub
        assert self.type == 'PI' or self.type == 'Test'

        #ensure bubble point pressure is at most reservoir pressure
        if self.pbub > self.res_p: 
            self.pbub = self.res_p
            print('Warning: Bubble Point Pressure set to Reservoir Pressure of %0.2f' % self.res_p)

        #ensure that PI is available, if type is test then calculate from well test information
        if self.type == 'Test':
            assert self.test_ql > 0, 'Test Data Invalid: Liquid Rate of %0.2f is low' % self.test_ql
            assert self.test_bhp > 0, 'Test Data Invalid: BHP of %0.2f is low' % self.test_bhp
            assert self.test_bhp < self.res_p, 'Test Data Invalid: BHP of %0.2f is greater than Res Pressure of %0.2f' % (self.test_bhp, self.res_p)
            if self.test_bhp >= self.pbub:
                self.pi = self.test_ql / (self.res_p - self.test_bhp)
            else:
                vogel_drawdown = (self.res_p - self.pbub + (self.pbub/1.8)*(1-0.2*(self.test_bhp/self.pbub)-0.8*np.power(self.test_bhp/self.pbub, 2)))
                self.pi = self.test_ql / vogel_drawdown
        #check PI is above 0
        assert self.pi > 0.0, 'IPR Invalid: PI of %0.2f is low' % self.pi
        #calcualte liquid flow rate at bubble point
        if self.pbub < self.res_p:
            ql_bub = self.pi*(self.res_p - self.pbub) 
        else:
            ql_bub = 0.0
        #calculate maximum liquid rate, aofp
        ql_max = ql_bub + self.pi*self.pbub/1.8 
        #create array of pressures, current length of array fixed at 19, includes Pbub
        pwf = (np.linspace(0.001, self.res_p, num = 19)).tolist() #create pwf array
        pwf.append(self.pbub) #add bubble point to pwf array
        pwf = sorted(pwf) #sort pwf 

        ql_darcy = [(self.res_p - i) * self.pi for i in pwf if i >= self.pbub] #calculate darcy IPR
        ql_vogel = [(ql_bub + (ql_max - ql_bub)*(1-0.2*(i/self.pbub)-0.8*np.power(i/self.pbub,2))) for i in pwf if i < self.pbub] #calculate vogel IPR
        ql = ql_vogel + ql_darcy #combine IPRs into one

        ipr_arr = {'Pwf': pwf,
            'LiqRate': ql}
        return(ipr_arr)