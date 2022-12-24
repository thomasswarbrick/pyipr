import numpy as np
import math
import bo_pvt_funcs as bo
class IPR:
    
    def __init__(self):
        '''
        Initialises instance of ipr
        
        res_p: reservoir pressure, psig
        pi: productivity index, stb/d/psi
        test_bhp: test bottom hole pressure, psig
        test_ql: test liquid rate, stb/d
        pbub: bubble point pressure, psig
        type: {'PI' or 'Test'}, PI can be set manually or calculated from test parameters 
        '''
        self.res_p = 0.0
        self.pi = 0.0
        self.test_bhp = 0.0
        self.test_ql = 0.0
        self.pbub = 0.0
        self.res_t = 0.0
        self.pvt_model = None
        self.type = "PI"

    def set_params(self, res_p: float, res_t: float, pvt: bo.PVTModel):
        """
        helper function to set parameters

        inputs
        -----
        res_p: reservoir pressure, psig
        res_t: reservoir temperature, degrees Fahrenheit
        pvt: black oil pvt model
        """
        self.res_p = res_p
        self.res_t = res_t
        self.pvt_model = pvt
        self.pbub = pvt.calc_pbub_glaso(self.res_t)
    
    def calc_PI (self, bhp: float, ql: float) -> float:
        '''
        function to calculate the PI from reservoir pressure, bottomhole pressure and rate

        inputs
        -----
        bhp: bottomhole pressure, psig
        ql: liquid rate, stb/d
        
        outputs
        -----
        pi: productivity index, stb/d/psi
        '''
        assert self.res_p > 0.0, 'IPR Invalid: Reservoir Pressure of %0.2f psig is low' % self.res_p
        assert self.pbub > 0.0, 'IPR Invald: Bubble Point Pressure of %0.2f psig is low' % self.pbub
        assert ql > 0, 'Test Data Invalid: Liquid Rate of %0.2f is low' % ql
        assert bhp > 0, 'Test Data Invalid: BHP of %0.2f psig is low' % bhp
        assert bhp < self.res_p, 'Test Data Invalid: BHP of %0.2f psig is greater than Res Pressure of %0.2f psig' % (bhp, self.res_p)

        # ensure bubble point pressure is at most reservoir pressure
        if self.pbub > self.res_p: 
            self.pbub = self.res_p
            print('Warning: Bubble Point Pressure set to Reservoir Pressure of %0.2f psig' % self.res_p)
        # if test above bubble point, use Darcy IPR, else use Vogel
        if bhp >= self.pbub:
            pi = ql / (self.res_p - bhp)
        else:
            vogel_drawdown = (self.res_p - self.pbub + (self.pbub/1.8)*(1-0.2*(bhp/self.pbub)-0.8*math.pow(bhp/self.pbub, 2)))
            pi = ql / vogel_drawdown
        return pi

    def calc_res_p(self, bhp: float, ql: float, pi = None) -> float:
        '''
        function to calculate the reservoir pressure from PI, bottomhole pressure and rate

        inputs
        -----
        bhp: bottomhole pressure, psig
        ql = liquid rate, stb/d
        pi: productivity index, stb/d/psi

        outputs
        -----
        res_p: reservoir pressure, psig 
        '''
        assert self.pbub > 0.0, 'IPR Invald: Bubble Point Pressure of %0.2f psig is low' % self.pbub
        assert ql > 0, 'Test Data Invalid: Liquid Rate of %0.2f stb/d is low' % ql
        assert bhp > 0, 'Test Data Invalid: BHP of %0.2f psig is low' % bhp

        if pi == None:
            pi = self.pi
        assert pi > 0, 'IPR Invalid: PI of %0.2f stb/d/psi is low' % pi
        if bhp > self.pbub:
            res_p = ql/pi + bhp
        else:
            res_p = ql/pi + self.pbub - (self.pbub/1.8)*(1-0.2*(bhp/self.pbub)-0.8*math.pow(bhp/self.pbub, 2))
        return res_p
    
    def get_ipr(self) -> dict:
        '''
        function to return dictionary of Pwf and Rate
        calculated based on what parameters are currently present for instance of ipr.

        IPR returned is composite:
        - using PI above bubble point, as flow will be single phase, i.e. Darcy IPR
        - using vogel below the bubble point, presence of gas reduces productivity due to relative
            permeability effects
        
        outputs
        -----
        ipr_arr = {
            'Pwf': bottomhole pressure, psig
            'LiqRate': liquid rate, stb/d
            }
        '''
        assert self.res_p > 0.0, 'IPR Invalid: Reservoir Pressure of %0.2f psig is low' % self.res_p
        assert self.pbub > 0.0, 'IPR Invald: Bubble Point Pressure of %0.2f psig is low' % self.pbub
        assert self.type in ["Test", "PI"], 'IPR Invald: Type of %0.2f must be either "Test" or "PI"' % self.pbub
        # ensure bubble point pressure is at most reservoir pressure
        if self.pbub > self.res_p: 
            self.pbub = self.res_p
            print('Warning: Bubble Point Pressure set to Reservoir Pressure of %0.2f psig' % self.res_p)

        #ensure that information available to calc IPR
        if self.type == "Test":
            assert self.test_ql > 0, 'Test Data Invalid: Liquid Rate of %0.2f is low' % self.test_ql
            assert self.test_bhp > 0, 'Test Data Invalid: BHP of %0.2f is low' % self.test_bhp
            assert self.test_bhp < self.res_p, 'Test Data Invalid: BHP of %0.2f psig is greater than Res Pressure of %0.2f psig' % (self.test_bhp, self.res_p)
            if self.test_bhp >= self.pbub:
                self.pi = self.test_ql / (self.res_p - self.test_bhp)  
            else:
                vogel_drawdown = (self.res_p - self.pbub + (self.pbub/1.8)*(1-0.2*(self.test_bhp/self.pbub)-0.8*math.pow(self.test_bhp/self.pbub, 2)))
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
    