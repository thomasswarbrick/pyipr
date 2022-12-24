import math

class PVTModel:

    def set_params(self, rsi: float, gasSG: float, oilAPI: float):
        """
        Helper function to set PVT properties

        inputs
        -----
        rsi: initial gas-oil ratio, scf/stb
        gasSG: gas specific gravity @ standard conditions, air = 1.0
        oilAPI: oil density @ standard conditions, deg API
        """
        self.rsi = rsi
        self.gasSG = gasSG
        self.oilAPI = oilAPI
    
    def calc_pbub_glaso(self, tempF: float) -> float:
        '''
        Function to calculate Bubble Point Pressure
        Taken from Glaso, O. 'Generalised-Pressure-Temperature Correlations'
        JPT. Vol 32 (1980) 785-795
        
        inputs
        -----
        tempF: temperature, degrees Fahrenheit

        outputs
        -----
        pbub: bubble point pressure, psig
        '''
        logA = math.log10(math.pow((self.rsi/self.gasSG), 0.816)*math.pow(tempF, 0.172)/math.pow(self.oilAPI, 0.989))
        pbub = math.pow(10, 1.7669+1.7447*logA-0.30218*math.pow(logA, 2)) - 14.7
        return pbub

    def calc_rs_glaso(self, p_psig: float, tempF: float) -> float:
        '''
        Function to calculate Solution Gas Oil Ratio. Function will return Rs = Rsi 
        if pressure is > calcualted Pb

        Taken from Glaso, O. 'Generalised-Pressure-Temperature Correlations'
        JPT. Vol 32 (1980) 785-795
        
        inputs
        -----
        p_psig: pressure, psig
        tempF: temperature, degrees Fahrenheit

        outputs
        -----
        rs: solution gor, scf/stb
        '''
        # if oil above bubble point, rs = rsi
        p_psia = p_psig + 14.7
        if p_psig >= self.calc_pbub_glaso(tempF):
            rs = self.rsi
        else:
            X = 14.1811-3.3093*math.log10(p_psia)
            if X < 0.0:
                X = 0.0
            A = math.pow(10, 2.8869-math.pow(X, 0.5))
            rs = self.gasSG*math.pow(A * math.pow(self.oilAPI, 0.989)/math.pow(tempF, 0.172), 1.2255)
        return rs

    def calc_bo_glaso(self, p_psig: float, tempF: float):
        '''
        Function to calculate Saturated Oil Formation Volume Factor (i.e. below the bubble point pressure)
        Above the bubble point pressure, Oil FVF is calculated via Oil Compressibility

        Taken from Glaso, O. 'Generalised-Pressure-Temperature Correlations'
        JPT. Vol 32 (1980) 785-795

        inputs
        -----
        p_psig: pressure, psig
        rs: solution gas oil ratio, scf/stb
        gasSG: gas specific gravity at standard conditions, air = 1.0
        oilAPI: oil density at standard conditions, deg API
        tempF: temperature, degrees Fahrenheit

        outputs
        -----
        bo: oil formation volume factor , rb/stb
        '''
        oilSG = 141.5/(self.oilAPI + 131.5)
        pbub_psig = self.calc_pbub_glaso(tempF)
        if p_psig <= pbub_psig: # if below bubble point pressure
            rs = self.calc_rs_glaso(p_psig, tempF)
            G = math.log10(rs*math.pow(self.gasSG/oilSG, 0.526)+0.968*tempF)
            bo = 1.0 + math.pow(10.0,-6.58511+2.91329*G-0.27683*math.pow(G, 2))
        else: 
            co = self.calc_co_vasquez_beggs(p_psig, tempF)#calculate oil compressibility
            G = math.log10(self.rsi*math.pow(self.gasSG/oilSG, 0.526)+0.968*tempF)
            bo_bub = 1.0 + math.pow(10.0,-6.58511+2.91329*G-0.27683*G*G) #calculate bo @ bubble point pressure
            bo = bo_bub*math.exp(-co*(p_psig - pbub_psig))
        return bo

    def calc_co_vasquez_beggs(self, p_psig: float, tempF: float):
        '''
        Function to calculate undersaturated Oil Compressibility (i.e. above bubble point)
        Taken from Vazquez, M.E. and Beggs, H.D. "Correlations for Fluid Physical Property Prediction",
        JPT. Vol 32 (1980) 968-970

        inputs
        -----
        p_psig: pressure, psig
        tempF: temperature, degrees Fahrenheit

        outputs
        -----
        co: oil compressibility, 1/psi
        '''
        co = 5*self.rsi + 17.2*tempF - 1180*self.gasSG + 12.61*self.oilAPI - 1433
        co = co / ((p_psig + 14.7)*math.pow(10, 5))
        return co

    def calc_dead_oil_visc_beggs(self, tempF: float):
        '''
        Function to calculate Dead Oil Viscosity 
        Beggs & Robinson (1975)

        inputs
        -----
        oilAPI: oil density at standard conditions, deg API
        tempF: temperature, degrees Fahrenheit
        
        outputs
        -----
        mu_od: dead oil viscosity, cP
        '''
        a = math.pow(10, (3.0324 - 0.02023*self.oilAPI))
        x = a * math.pow(tempF, -1.163)
        mu_od = math.pow(10, x) - 1
        return mu_od

    def calc_oil_visc_beggs(self, p_psig: float, rs: float, tempF: float):
        '''
        Function to calculate Oil Viscosity 
        Saturated Oil Viscosity (i.e. under Pb) uses Beggs & Robinson (1975)
        Under-Saturated Oil Viscosity (i.e. above Pb) uses Vasquez & Beggs (1980)

        inputs
        -----
        p_psig: pressure, psig
        rs: solution gas oil ratio, scf/stb
        tempF: temperature, degrees Fahrenheit

        outputs
        -----
        mu_o: oil viscosity, cP
        '''
        mu_od = self.calc_dead_oil_visc_beggs(tempF)
        pbub_psig = self.calc_pbub_glaso(tempF)
        if p_psig <= pbub_psig:
            A = 10.715 * (rs + 100)**(-0.515)
            B = 5.44 * (rs + 150)**(-0.338)
            mu_o = A * mu_od ** (B)
        else:
            A = 10.715 * (self.rsi + 100)**(-0.515)
            B = 5.44 * (self.rsi + 150)**(-0.338)
            mu_o_pbub = A * mu_od ** (B)
            m = (2.6*(p_psig+14.7)**1.187*math.exp(-11.513 - (8.98e-5)*(p_psig+14.7)))
            mu_o = mu_o_pbub*((p_psig+14.7)/(pbub_psig+14.7))**m
        return mu_o