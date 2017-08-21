
# calculates optimal numbers of representives for hemicycle chart
import math
import csv
import numpy as np
import timeit

start = timeit.default_timer()
#benchmark:
#n0 = 200 : 4:23s, 5:52s, 6:132s, 7:285s, 8:579s, 9:1167s , 10:2342s, 11: 4632s
#n0=751 : 7:217s, 8:570s, 9:1331, 10:2816s, 11: 5686s, 12: 10905s, 13:21918s,14:44362s


# number of representatives
n0=513


optim = {}

# loss function 1 (gaps between rows)
def loss1(g):
  return (g-1.2)*(g-1.2) #looks best

# loss function 2 (spaces in rows)
def loss2(w,s,n):
  n0 = sum(n)
  l2 = 0
  i = 0
  ln = len(n)
  for item in n:
    if s[i] > 0:
      #l2 = l2 + item*(s[i] - 0.1*w)*(s[i] - 0.1*w)/n0
      l2 = l2 + (s[i] - 0.1*w)*(s[i] - 0.1*w)/ln
    else:
      l2 = l2 + 10
    i = i + 1
  return l2

# loss function
def lossf(w,g,s,n):
  l1 = loss1(g)
  l2 = loss2(w,s,n)
  l = l1 + l2 + (l1 - l2)*(l1 - l2)
  return l

# spaces in rows
def ss(w,g,n):
  s = [0]*len(n)
  i = 0
  for item in n:
    s[i] = (math.pi/w + math.pi*i*g-n[i])/(n[i] - 1)
    i = i + 1 
  return s

# max n in row for grid search
def nmax(k,n):
  return math.floor(n-((k-1)*k/2))/k

# nrow for grid search
def nrow(n):
  return {'max':round(math.sqrt(n)*3/4),'min':round(max(math.sqrt(n)/4,1))}

# grid search
def grid(n):
  out = []
  for k in np.arange (0.01,1,0.01): #(0.01,1,0.005):
    for kk in np.arange (1.15,1.25,0.01): #(1,1.35,0.01)
      g = kk
      w = k
      s = ss(w,g,n)
      l1 = loss1(g)
      l2 = loss2(w,s,n)
      l = l1 + l2 + (l1-l2)*(l1-l2)
      try:
        if l < mmin:
          out = [w,g]
          mmin = l
      except:
        out = [w,g]
        mmin = l
  #print(out,mmin)
  return {'w':out[0],'g':out[1],'loss':mmin}     
    #outwriter.writerow(row)

# recursion
def go(level,n,nrows,n0):
#  print(n,level)
  global optim
#  print('optim:',optim)
  global ll
  while level < (nrows-1):
    #conservative (slow):
#    jmin = max(level+2,n[level-1]+1)
#    jmax = int(nmax(nrows-level,n0-sum(n[0:level]))+1)
    #faster (aritmetic series):
    if level > 0:
      if (nrows>1):
        q = 2*(n0-nrows*n[0])/(nrows-1)/nrows
        jmin = math.floor(n[0] + level*q - 0.5) #better with  -1, but slower
        jmax = math.ceil(n[0] + level*q + 0.5) #better with  +1, but slower
      else:
        jmin = max(level+2+round(sqrt(level)),n[level-1]+1)
        jmax = int(nmax(nrows-level,n0-sum(n[0:level]))+1)
    else:
      jmin = max(level+2,n[level-1]+1)
      jmax = int(nmax(nrows-level,n0-sum(n[0:level]))+1)
    for j in range(jmin,jmax):
      n[level] = j
      go(level+1,n,nrows,n0)
    return False
  n[level] = n0-sum(n)
#  print("calculating:",level,k,n)
  opt = grid(n)
#  print(opt,ll)
  try:
    if ll > opt['loss']:
      optim = opt.copy()
      optim['n'] = n.copy()
      ll = optim['loss']
  except:
    optim = opt.copy()
    optim['n'] = n.copy()
    ll = optim['loss']
#  print('optim2:',optim)
  n[level] = 0
  return True

# for each reasonable number of rows:
nr = nrow(n0)
for k in range(nr['min'],nr['max']+1):
  n = [0]*k
  optim = {}
  ll = 100000000
  go(0,n,k,n0)
  print("final optim:",optim)
  print("time:",timeit.default_timer() - start)


    
#example of results:
#n = 200:
#final optim: {'n': [44, 48, 52, 56], 'loss': 6.0494609377272378e-05, 'w': 0.069999999999999993, 'g': 1.2000000000000002}
#time: 23.457229251012905
#final optim: {'n': [34, 37, 40, 43, 46], 'loss': 0.003021820005212728, 'w': 0.089999999999999997, 'g': 1.1900000000000002}
#time: 51.52483937999932
#final optim: {'n': [24, 28, 31, 35, 39, 43], 'loss': 0.0009935459225664401, 'w': 0.13, 'g': 1.2300000000000002}
#time: 131.58585535301245
#final optim: {'n': [18, 21, 25, 29, 32, 36, 39], 'loss': 0.000796945129917957, 'w': 0.17000000000000001, 'g': 1.1900000000000002}
#time: 284.771323367022
#final optim: {'n': [12, 16, 19, 23, 27, 31, 34, 38], 'loss': 0.00031275649495655434, 'w': 0.25, 'g': 1.2000000000000002}
#time: 579.2367971060157
#final optim: {'n': [8, 11, 15, 19, 22, 26, 29, 33, 37], 'loss': 0.00043985954926300044, 'w': 0.39000000000000001, 'g': 1.2000000000000002}
#time: 1167.0518377900007
#final optim: {'n': [4, 8, 11, 15, 18, 22, 25, 29, 32, 36], 'loss': 0.00064177079858304589, 'w': 0.72999999999999998, 'g': 1.2000000000000002}
#time: 2341.9838014570123
#final optim: {'n': [3, 6, 9, 12, 15, 18, 21, 24, 27, 30, 35], 'loss': 0.0087001372112743003, 'w': 0.98999999999999999, 'g': 1.1400000000000001}
#time: 4631.68083341801


#n = 751 (Euro Parliament)
#final optim: {'n': [98, 101, 104, 107, 110, 113, 118], 'loss': 0.0062929076050250469, 'w': 0.029999999999999999, 'g': 1.1899999999999999}
#time: 217.3275479080039
#final optim: {'n': [85, 88, 90, 93, 95, 98, 100, 102], 'loss': 0.068194024500854655, 'w': 0.029999999999999999, 'g': 1.1599999999999999}
#time: 570.2674658489996
#final optim: {'n': [71, 74, 77, 80, 83, 87, 90, 93, 96], 'loss': 0.014035298736485213, 'w': 0.040000000000000001, 'g': 1.1799999999999999}
#time: 1331.067573258013
#final optim: {'n': [60, 63, 67, 70, 73, 77, 80, 83, 87, 91], 'loss': 0.0032756194901112823, 'w': 0.050000000000000003, 'g': 1.1899999999999999}
#time: 2816.806992516009
#final optim: {'n': [51, 54, 58, 61, 65, 68, 72, 75, 79, 82, 86], 'loss': 0.0013354982259395371, 'w': 0.060000000000000005, 'g': 1.1899999999999999}
#time: 5686.576568382996
#final optim: {'n': [44, 47, 51, 54, 57, 61, 64, 68, 71, 74, 78, 82], 'loss': 0.0016497989012379932, 'w': 0.069999999999999993, 'g': 1.1899999999999999}
#time: 10905.816249452997
#final optim: {'n': [34, 38, 42, 46, 50, 54, 58, 62, 66, 70, 73, 77, 81], 'loss': 0.0025690587369525267, 'w': 0.089999999999999997, 'g': 1.25}
#time: 21918.771677729994
#final optim: {'n': [31, 34, 38, 41, 45, 48, 52, 55, 59, 62, 66, 69, 73, 78], 'loss': 0.00099189844185821208, 'w': 0.099999999999999992, 'g': 1.1899999999999999}
#time: 44362.27788667599
# ...

# n = 81 (CZ Senate)
#final optim: {'n': [39, 42], 'loss': 0.00015113520955957024, 'w': 0.080000000000000002, 'g': 1.2}
#time: 2.056351581995841
#final optim: {'n': [23, 27, 31], 'loss': 0.00074731223308436374, 'w': 0.13, 'g': 1.2}
#time: 3.672953786997823
#final optim: {'n': [15, 18, 22, 26], 'loss': 0.0017986444368775138, 'w': 0.20000000000000001, 'g': 1.1899999999999999}
#time: 5.949895355995977
#final optim: {'n': [9, 13, 16, 20, 23], 'loss': 0.0004283781313137963, 'w': 0.34000000000000002, 'g': 1.2}
#time: 10.962005101988325
#final optim: {'n': [5, 8, 12, 15, 19, 22], 'loss': 0.0011676166427925727, 'w': 0.62, 'g': 1.1899999999999999}
#time: 21.31037131600897
#final optim: {'n': [3, 6, 9, 12, 14, 17, 20], 'loss': 0.017012374030482232, 'w': 0.98999999999999999, 'g': 1.1499999999999999}
#time: 41.0609374709893
