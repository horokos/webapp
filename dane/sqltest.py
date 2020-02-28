from time import strptime


d1 = strptime('2020-10-2', '%Y-%m-%d')
print(d1)
d2 = strptime('2020-11-2', '%Y-%m-%d')
print(d1)

if d1 < d2:
    print('tak')
else:
    print('nie')
