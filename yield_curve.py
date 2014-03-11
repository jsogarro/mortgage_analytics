

tr = [] # times to maturity
yr = [] # yields

for b in bonds:
  ttm = (b.bid + b.ask) / 2
  price = (b.bid + b.ask) / 2
  ytm = TVM(n = ttm * b.freq, pv = -price, pmt = b.couponRate / b.freq, fv = 1).calc_r() * b.freq
  tr.append(ttm)
  yr.append(ytm)

## Yield curve interpolation
t = list(i for in in range(1, 30)) # curve from 1 to 30 years
y = []

interp = scipy.interpolate.interp1d(tr, yr, bounds_error = False, fill_value = scipy.nam)
for i in t:
  value = float(interp(i))
  if not scipy.isnan(value):
    y.append(value)


