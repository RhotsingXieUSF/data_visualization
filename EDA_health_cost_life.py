import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import math
%config InlineBackend.figure_format = 'retina'

# read data
df_life = pd.read_csv('life_expectancy.csv')
df_cost = pd.read_csv('health_spending.csv')


# The original data contains 50+ countries, filter the countries
counties = ['Mexico', 'Poland', 'Hungary', 'Slovak Republic', 'Czech Republic', 'South Korea', 'Portugal',
 'New Zealand', 'Japan', 'Spain', 'Finland', 'United Kingdom', 'Australia', 'Sweden', 'Denmark', 'France',
 'Austria', 'Canada', 'Luxembourg', 'Switzerland', 'United States']

df_life_new = df_life[['2007', 'country']][df_life['country'].isin(counties)]
df_cost_new = df_cost[['2007', 'country']][df_cost['country'].isin(counties)]

df = df_cost_new.merge(df_life_new, how = 'outer', on = 'country')
df.columns = ['cost', 'country', 'life_ep']
df = df.sort_values('cost').reset_index(drop=True)

# resign new weight for the graph
lwtest = [0.5, 0.5, 1, 1, 1,1,1, 0.5, 1, 1, 1, 1.5, 2, 1, 1, 1.5, 2, 1.5, 1.5,  1, 0.5] # from the graph
lw=[]
for i in lwtest:
    lw.append(i*3)
df['lw'] = lw[::-1]

df.sort_values(by='life_ep')

# Perform Log to better scale data interval (Here assume cost is already sorted)
cost_temp = np.array(df['cost'])
cost_with_log_diff = [0]
for i in range(1, len(cost_temp)):
    lastOne = cost_with_log_diff[-1]
    diff = cost_temp[i] - cost_temp[i-1]
    if diff <= 50:
        log_diff = (cost_temp[i] - cost_temp[i-1]) + 80
    else:
        log_diff = cost_temp[i] - cost_temp[i-1]
    cost_with_log_diff.append(lastOne + log_diff)

cost_map = {cost_temp[i]: cost_with_log_diff[i] for i in range(len(cost_temp))}
df['cost_temp'] = df['cost'].map(cost_map)

lower_bound = 0.0
upper_bound = 0.6
m_cost = min(df['cost_temp']) # df['cost'].mean()
sd_cost = (max(df['cost_temp']) - min(df['cost_temp'])) # df['cost'].std()
m_life = min(df['life_ep']) # df['life_ep'].mean()
sd_life = (max(df['life_ep']) - min(df['life_ep'])) / (upper_bound - lower_bound) # df['life_ep'].std()

health_data = {}

for i in df['country']:
 health_data[i] = ((df['cost_temp'][df['country'] == i].values[0] - m_cost) / sd_cost,
                   (df['life_ep'][df['country'] == i].values[0] - m_life) / sd_life + lower_bound,
                   df['cost'][df['country'] == i].values[0],
                   df['life_ep'][df['country'] == i].values[0],
                   df['lw'][df['country'] == i].values[0])

######### Visualization ###########
# visualization
fig, ax = plt.subplots(figsize=(11, 16))
plt.axis('off')

for item in health_data:
 a, b, c, d, e = health_data[item]
 clr = '#457b9d'
 clr_label = '#6c757d'
 life_label = ''
 text_clr = '#6e6f71'
 zorder = 2
 # if standout line --> make orange
 if item == 'United States' or item == 'Mexico':
  clr = '#e93c16'
  clr_label = '#e93c16'
  text_clr = '#e93c16'
  life_label = round(d, 0)
  zorder = 10
 # make lines
 ax.plot([0, 1], [a, b], 'o-', lw=e, c=clr, zorder=zorder)

 # add cost number labels
 ax.text(0 - .02, a, "$" + f"{c:.0f}", color=clr_label, horizontalalignment='right', verticalalignment='center',
         fontsize=10)
 ax.text(1 + .03, b, life_label, color=clr, horizontalalignment='left', verticalalignment='center',
         fontsize=10, fontweight='bold')
 # add name labels
 ax.text(0 - .15, a, item, color=text_clr, horizontalalignment='right', verticalalignment='center',
         fontsize=11, fontweight='bold')

ep_range = [0, 0.07, 0.15, 0.22, 0.3, 0.38, 0.45, 0.53, 0.6]
# add life label and sticks
for i in ep_range:
 ax.hlines(i, 1 + .02, 1 + 0.03, color='#a2a3a5')

ax.text(1 + 0.045, ep_range[0], '74', horizontalalignment='left', verticalalignment='center',
        fontsize=9, color='#6c757d')
ax.text(1 + 0.045, ep_range[-1], '82', horizontalalignment='left', verticalalignment='center',
        fontsize=9, color='#6c757d')
# add average number
ax.text(1 + 0.045, ep_range[5], '79 - Avg life', horizontalalignment='left', verticalalignment='center',
        fontsize=10, fontweight='bold', color='#457b9d')
ax.text(0 - 0.02, 0.37, 'Avg cost - $3069', horizontalalignment='right', verticalalignment='center',
        fontsize=10, fontweight='bold', color='#457b9d')

# add  y title
ax.text(0 - 0.02, 1.07, "Health care", horizontalalignment='right', verticalalignment='center',
        fontsize=11, fontweight='bold')
ax.text(0 - 0.01, 1.055, "spending per person,", horizontalalignment='right', verticalalignment='center',
        fontsize=11, fontweight='bold')
ax.text(0 - 0.02, 1.037, "in U.S. dollors", horizontalalignment='right', verticalalignment='center',
        fontsize=11, fontweight='bold')

ax.text(0.88, 0.7, "Average", horizontalalignment='left', verticalalignment='center',
        fontsize=11, fontweight='bold')
ax.text(0.88, 0.68, "life expectancy", horizontalalignment='left', verticalalignment='center',
        fontsize=11, fontweight='bold')
ax.text(0.88, 0.66, "at birth", horizontalalignment='left', verticalalignment='center',
        fontsize=11, fontweight='bold')

# add side note
ax.text(0.56, 1.07, "Nation with", horizontalalignment='left', verticalalignment='center',
        fontsize=10, fontweight='bold', color='#457b9d')
ax.text(0.56, 1.055, "universal Health", horizontalalignment='left', verticalalignment='center',
        fontsize=10, fontweight='bold', color='#457b9d')
ax.text(0.56, 1.037, "coverage", horizontalalignment='left', verticalalignment='center',
        fontsize=10, fontweight='bold', color='#457b9d')
ax.hlines(1.072, 0.525, 0.545, lw=2, color='#457b9d')

ax.text(0.86, 1.07, "Nation without", horizontalalignment='left', verticalalignment='center',
        fontsize=10, fontweight='bold', color='#e93c16')
ax.text(0.86, 1.055, "Universal health", horizontalalignment='left', verticalalignment='center',
        fontsize=10, fontweight='bold', color='#e93c16')
ax.text(0.86, 1.037, "coverage", horizontalalignment='left', verticalalignment='center',
        fontsize=10, fontweight='bold', color='#e93c16')
ax.hlines(1.072, 0.825, 0.845, lw=2, color='#e93c16')

# add lw ledgend
ax.text(0.09, 1.07, "Average number", horizontalalignment='left', verticalalignment='center',
        fontsize=10, fontweight='bold')
ax.text(0.09, 1.055, "of dotor visit a year", horizontalalignment='left', verticalalignment='center',
        fontsize=10, fontweight='bold')
linebar = [(0.15, '4'), (0.25, '8'), (0.35, '12+')]
for tp in linebar:
 i, t = tp
 ax.vlines(i, 1.045, 1.03, lw=.5)
 ax.text(i - 0.01, 1.015, t)
ax.hlines(1.04, 0.09, 0.14, lw=1.5, color='#6e6f71')
ax.hlines(1.04, 0.16, 0.24, lw=2, color='#6e6f71')
ax.hlines(1.04, 0.26, 0.34, lw=3, color='#6e6f71')
ax.hlines(1.04, 0.36, 0.41, lw=6, color='#6e6f71')

# add title
rect = patches.Rectangle(xy=(-0.5, 1.093 + 0.01), width=0.05, height=0.055,
                         facecolor='#e63946')
ax.hlines(1.093 + 0.01, -.5, 0.8, lw=0.7, color='#e63946')
ax.add_patch(rect)
ax.text(0 - 0.44, 1.12 + 0.01, "U.S. has the highest cost in health", fontsize=17,
        fontweight='bold', horizontalalignment='left', verticalalignment='bottom', )
ax.text(0 - 0.44, 1.095 + 0.01, "but lower life expectancy", fontsize=17,
        fontweight='bold', horizontalalignment='left', verticalalignment='bottom', )
plt.show()
