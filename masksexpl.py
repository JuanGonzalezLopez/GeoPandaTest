import numpy as np

array = np.array([['Aguadilla', 'Guaynabo', 'Aguada','Bayamon','Cidra'],['polygon1','polygon2','polygon3','polygon4','polygon5']])

# 'Ten' == 'Ten': True
# 'four' == 'Ten': False
print(array)

mask = array[0]=='Aguada'

print(mask)

print(array[1][mask])
