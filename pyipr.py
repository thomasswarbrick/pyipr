import numpy as np
import math
import bo_pvt_funcs as bo

<<<<<<< HEAD
class IPR():
    def test():
        print("test")

    def set_params(self, res_p: float, res_t: float, pvt: bo.PVTModel):
        '''
        Initialises instance of ipr
        
        res_p = reservoir pressure, psig
        pi = productivity index, stb/d/psi
        test_bhp = test bottom hole pressure, psig
        test_ql = test liquid rate, stb/d
        pbub = bubble point pressure, psig
        type = 'PI' or 'Test', PI can be set manually or calculated from test parameters 
        '''
        self.res_p = res_p
        self.res_t = res_t
        self.pvtModel = pvt
=======
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
>>>>>>> e2f8c361511808c2355d1055d6a6dfa61cdcb025
        self.pi = 0.0
        self.test_bhp = 0.0
        self.test_ql = 0.0
        self.pbub = 0.0
        self.type = 'PI'
<<<<<<< HEAD
    
    def calc_PI (self, res_p, bhp, ql):
        '''
        function to calculate the PI from reservoir pressure, bottomhole pressure and rate

        res_p = reservoir pressure, psig
        bhp = bottomhole pressure, psig
        ql = liquid rate, stb/d

        pi = productivity index, stb/d/psi
        '''
        assert res_p > 0.0, 'IPR Invalid: Reservoir Pressure of %0.2f psig is low' % res_p
        assert self.pbub > 0.0, 'IPR Invald: Bubble Point Pressure of %0.2f psig is low' % self.pbub
        assert ql > 0, 'Test Data Invalid: Liquid Rate of %0.2f is low' % ql
        assert bhp > 0, 'Test Data Invalid: BHP of %0.2f psig is low' % bhp
        assert bhp < res_p, 'Test Data Invalid: BHP of %0.2f psig is greater than Res Pressure of %0.2f psig' % (bhp, res_p)

        #ensure bubble point pressure is at most reservoir pressure
        if self.pbub > res_p: 
            self.pbub = res_p
            print('Warning: Bubble Point Pressure set to Reservoir Pressure of %0.2f psig' % self.res_p)

        if bhp >= self.pbub:
            pi = ql / (res_p - bhp)
        else:
            vogel_drawdown = (res_p - self.pbub + (self.pbub/1.8)*(1-0.2*(bhp/self.pbub)-0.8*np.power(bhp/self.pbub, 2)))
            pi = ql / vogel_drawdown
        return pi
=======
>>>>>>> e2f8c361511808c2355d1055d6a6dfa61cdcb025

    def calc_res_p(self, pi, bhp, ql):
        '''
        function to calculate the reservoir pressure from PI, bottomhole pressure and rate

        pi = productivity index, stb/d/psi
        bhp = bottomhole pressure, psig
        ql = liquid rate, stb/d

        res_p = reservoir pressure, psig 
        '''
        assert self.pbub > 0.0, 'IPR Invald: Bubble Point Pressure of %0.2f psig is low' % self.pbub
        assert ql > 0, 'Test Data Invalid: Liquid Rate of %0.2f stb/d is low' % ql
        assert bhp > 0, 'Test Data Invalid: BHP of %0.2f psig is low' % bhp
        assert pi > 0, 'IPR Invalid: PI of %0.2f stb/d/psi is low' % pi

        if bhp > self.pbub:
            res_p = ql/pi + bhp
        else:
            res_p = ql/pi + self.pbub - (self.pbub/1.8)*(1-0.2*(bhp/self.pbub)-0.8*np.power(bhp/self.pbub, 2))
        return res_p
    
    def get_ipr(self):
        '''
        function to return dictionary of Pwf and Rate
        calculated based on what parameters are currently present for
        instance of ipr.

        IPR returned is composite:
<<<<<<< HEAD
        - using PI above bubble point, as flow will be single phase, i.e. Darcy IPR
        - using vogel below the bubble point, presence of gas reduces productivity due to relative
            permeability effects
        '''
        assert self.res_p > 0.0, 'IPR Invalid: Reservoir Pressure of %0.2f psig is low' % self.res_p
        assert self.pbub > 0.0, 'IPR Invald: Bubble Point Pressure of %0.2f psig is low' % self.pbub
=======
        - using PI above bubble point, as flow will be single phase
        - using vogel below the bubble point, presence of gas reduces productivity due to relative
            permeability effects
        '''
        assert self.res_p > 0.0, 'IPR Invalid: Reservoir Pressure of %0.2f is low' % self.res_p
        assert self.pbub > 0.0, 'IPR Invald: Bubble Point Pressure of %0.2f is low' % self.pbub
>>>>>>> e2f8c361511808c2355d1055d6a6dfa61cdcb025
        assert self.type == 'PI' or self.type == 'Test'

        #ensure bubble point pressure is at most reservoir pressure
        if self.pbub > self.res_p: 
            self.pbub = self.res_p
<<<<<<< HEAD
            print('Warning: Bubble Point Pressure set to Reservoir Pressure of %0.2f psig' % self.res_p)

        #ensure that PI is available, if type is test then calculate from well test information        
        if self.type == 'Test':
            assert self.test_ql > 0, 'Test Data Invalid: Liquid Rate of %0.2f is low' % self.test_ql
            assert self.test_bhp > 0, 'Test Data Invalid: BHP of %0.2f is low' % self.test_bhp
            assert self.test_bhp < self.res_p, 'Test Data Invalid: BHP of %0.2f psig is greater than Res Pressure of %0.2f psig' % (self.test_bhp, self.res_p)
=======
            print('Warning: Bubble Point Pressure set to Reservoir Pressure of %0.2f' % self.res_p)

        #ensure that PI is available, if type is test then calculate from well test information
        if self.type == 'Test':
            assert self.test_ql > 0, 'Test Data Invalid: Liquid Rate of %0.2f is low' % self.test_ql
            assert self.test_bhp > 0, 'Test Data Invalid: BHP of %0.2f is low' % self.test_bhp
            assert self.test_bhp < self.res_p, 'Test Data Invalid: BHP of %0.2f is greater than Res Pressure of %0.2f' % (self.test_bhp, self.res_p)
>>>>>>> e2f8c361511808c2355d1055d6a6dfa61cdcb025
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
<<<<<<< HEAD
        return(ipr_arr)

if __name__ == "__main__":
    pvt = bo.PVTModel()
    pvt.set_params(650, 0.75, 40.0)
    ipr = IPR()
    ipr.set_params(5000, 160, pvt=pvt)
    pi = ipr.calc_PI(4000, 2000 , 1000)
    print(pi)    
=======
        return(ipr_arr)
>>>>>>> e2f8c361511808c2355d1055d6a6dfa61cdcb025
