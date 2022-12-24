# pyipr
python based inflow performance model (IPR) tool

The IPR in pyipr is a composite model, using the Darcy IPR above the bubble point and Vogel IPR below. 

pyipr uses the Glaso black oil correlation for calculating:
 - bubble point pressure
 - solution gas oil ratio
 - formation volume factor

The Beggs correlation is used for estimating Oil Viscosity

To get started, see the jupyter notebook primer

![ipr](./data/ipr.png)

## References
<a id="1">[1]</a> 
Dake, L. P. (1983). 
Fundamentals of Reservoir Engineering. 
Elsevier Science B.V.

<a id="1">[2]</a> 
Glaso, O. (1980). 
'Generalised-Pressure-Temperature Correlations' 
JPT. Vol 32 (1980) 785-795

<a id="1">[3]</a> 
Vazquez, M.E. and Beggs, H.D.
'Correlations for Fluid Physical Property Prediction' 
JPT. Vol 32 (1980) 968-970