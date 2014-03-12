from math import floor, ceil
from datetime import datetime
from pylab import *
import scipy.interpolate
from tvm import TVM
import io

# Import our Treasury data
f = io.open('treasuries.csv', 'r')
data = f.read()
bonds = []
i = 0
for line in data.split('\n'):
    i += 1
    if (i == 1):
    continue
    entries = line.split(',')
    if (len(entries) != 9):
    continue
    b = Bond()
    b.freq = 2
    b.epic = entries[0]
    b.desc = entries[1]
    b.couponRate = float(entries[2]) / 100.0
    b.maturity = datetime.strptime(entries[3], '%d-%b-%y')
    b.bid = float(entries[4]) / 100
    b.ask = float(entries[5]) / 100
    bonds.append(b)
f.close()

tr = [] # times to maturity
yr = [] # yields

for b in bonds:
    ttm = (b.maturity - localtime).days / 360
    price = (b.bid + b.ask) / 2
    ytm = TVM(n = ttm * b.freq, pv = -price, pmt = b.couponRate / b.freq, fv = 1).calc_r() * b.freq
    tr.append(ttm)
    yr.append(ytm)

# print our yield curve to the command line
print('Yield Curve Rates:')
for i in range(0, len(tr)):
    print("%.2f\t %.2f%%" % (tr[i], 100*yr[i]))


## Yield curve interpolation
t = list(i for i in range(1, 30)) # curve from 1 to 30 years
y = []

interp = scipy.interpolate.interp1d(tr, yr, bounds_error = False, fill_value = scipy.nam)
for i in t:
    value = float(interp(i))
    if not scipy.isnan(value):
    y.append(value)

print('Interpolated Yield Curve Rates:')
for i in range(0, len(t)):
    print("%.2f\t %.2f%%" % (t[i], 100*y[i]))


# Bootstrap our yield curve
s = [] # spot rates

for i in range(0, len(t)):
    sum = 0
    for j in range(0, i):
    sum += y[i] / (1 + s[j])**t[j]
    value = ((1 + y[i]) / (1 - sum))**(1/t[i]) - 1
    s.append(value)

print('Spot Rates:')
for i in range(0, len(t)):
    print("%.2f\t %.2f%%" % (t[i], 100*s[i]))


# Plot our curves
p1 = plot(tr, array(yr) * 100, marker = '^'), xlabel('Time to Maturity'), grid(True)
p2 = plot(t, array(y) * 100, marker = '^'), xlabel('Time to Maturity'), grid(True)
p3 = plot(t, array(s) * 100, marker = 'o') , xlabel('Time to Maturity'), grid(True)
legend([ p1[0][0], p2[0][0], p3[0][0] ], ['Original Yield Curve', 'Interpolated Yield Curve', 'Spot Rate Curve'], 4)
show()  
