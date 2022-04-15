from cProfile import label
import pyipr
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
sns.set()

ipr_obj = pyipr.IPR() #create instance of IPR object

#------------- set pvt properties
ipr_obj.rsi = 800.0 #initial solution gor
ipr_obj.oilapi = 40.0 #oil api
ipr_obj.gassg = 0.75 #gassg
ipr_obj.temp = 140.0 #temperature

ipr_obj.calc_pbub() #calculate bubble point
print('Bubble Point Pressure of %0.2f' % ipr_obj.pbub)

ipr_obj.res_p = 4000.0 #set reservoir pressure
ipr_obj.type = 'Test' #set ipr type

ipr_obj.test_ql = 1000.0 #set test rate
ipr_obj.test_bhp = 3000.0 #set test bhp
well_1A_ipr = pd.DataFrame(ipr_obj.get_ipr())
print('Well 1A PI is %0.2f' % ipr_obj.pi)

ipr_obj.rsi = 200.0
ipr_obj.calc_pbub()
print('Bubble Point Pressure of %0.2f' % ipr_obj.pbub)

ipr_obj.test_ql = 1000.0
ipr_obj.test_bhp = 3500.0
well_2A_ipr = pd.DataFrame(ipr_obj.get_ipr())
print('Well 2A PI is %0.2f' % ipr_obj.pi)

ipr_obj.test_ql = 1000.0
ipr_obj.test_bhp = 2000.0
well_3A_ipr = pd.DataFrame(ipr_obj.get_ipr())
print('Well 3A PI is %0.2f' % ipr_obj.pi)

well_1A_ipr['Well'] = "Well 1A"
well_2A_ipr['Well'] = "Well 2A"
well_3A_ipr['Well'] = "Well 3A"

all_iprs = pd.concat([well_1A_ipr, well_2A_ipr, well_3A_ipr], ignore_index=True)

sns.lineplot(data=all_iprs, x='LiqRate', y = 'Pwf', hue='Well')
sns.scatterplot(data=all_iprs, x='LiqRate', y = 'Pwf')

plt.show()
