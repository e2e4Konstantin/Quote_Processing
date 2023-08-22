import pandas as pd
from pandas import Series, DataFrame
import numpy as np

# data = 'Молодая княгиня Болконская приехала с работой в шитом золотом бархатном мешке. Ее хорошенькая, с чуть черневшимися усиками верхняя губка была коротка по зубам, но тем милее она открывалась и тем еще милее вытягивалась иногда и опускалась на нижнюю. Как это бывает у вполне привлекательных женщин, недостаток ее — короткость губы и полуоткрытый рот — казались ее особенною, собственно ее красотой. Всем было весело смотреть на эту полную здоровья и живости хорошенькую будущую мать, так легко переносившую свое положение. Старикам и скучающим, мрачным молодым людям казалось, что они сами делаются похожи на нее, побыв и поговорив несколько времени с ней. Кто говорил с ней и видел при каждом слове ее светлую улыбочку и блестящие белые зубы, которые виднелись беспрестанно, тот думал, что он особенно нынче любезен. И это думал каждый.'
#
# s = Series(data.split())
# print(s.info)
# print(s.info(verbose=False, memory_usage=True, show_counts=True))
# print(s[s.str.contains('ш')])
# print(s.loc[s.str.contains('ш') | s.str.contains('ю')])
# print(s.loc[s.str.contains('[шю]', regex=True)])
# print(s.loc[s.str.contains('^[б|м]\s*', regex=True)])

# a = Series([10, 20, 30, 40, 40, 60])
# print(a.info(verbose=False, memory_usage=True, show_counts=True))
# print(a)
# print(a.loc[[True, False, True, False, True, False]])
# print(a+5)
# print(a == 30)
# print(a.loc[[False, False, True, False, False, False]])
# print(a.loc[a == 30])
# print(a.loc[a < 30])
# print(a.loc[(20 < a) | (a>40)])

df = DataFrame(np.random.randint(0, 1000, [6, 6]), index=list('abcdef'), columns=list('UVWXYZ'))
print(df.info(verbose=False, memory_usage=True, show_counts=True))
print(df)

print( df.loc[:, ['W', 'Y']])
print( df.loc[['c', 'd'], :])
print( df.iloc[[2, 3], :])


# print(df['Y'] % 2 == 0 )
# print(df.loc[df['Y'] % 2 == 0] )
# print(df.loc[df['Y'] % 2 == 0, 'Y'] )
# print(df.loc[df['Y'] % 2 == 0, ['W', 'Y']] )
# print(df.loc['c'] < 500)
# print( (df.loc['c'] < 500) | (df.loc['c'] > 700) )
print(df.loc['c'].isin([641, 793, 212]))

