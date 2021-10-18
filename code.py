import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl

# --------------------

# USER INPUT SECTION

util_report_path = '/Users/dfreely001/Documents/Python Scripts/Utilisation Dashboard/Util report - 042019_062020.csv'
time_report_path = '/Users/dfreely001/Documents/Python Scripts/Utilisation Dashboard/Personal Timesheet Report - 042019_062020 - dummy data.csv'

# --------------------

pd.options.mode.chained_assignment = None
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

# Create new column headers
util_column_headers = ['Date', 'Utilisation (%)', 'Target Chargeable', 'Chargeable Hours', 'BD', 'People Management', 'Training', 'Holiday & Other Leave', 'Sick', 'Other', 'Planned Hours', 'Overtime']
time_column_headers = ['Engagement Type', 'Client', 'WBS Name', 'WBS Code', 'Hours']

# Read in utilisation and time reports
df_util = pd.read_csv(util_report_path, index_col=False, skiprows=[0,1,3, 4], names=util_column_headers, header=0)
df_util_overall = pd.read_csv(util_report_path, index_col=False, skiprows=[0,1,3], names=util_column_headers, header=0)
df_time = pd.read_csv(time_report_path, index_col=False, skiprows=[0,1,2,4], names=time_column_headers, header=0)

# Clean reports
df_time = df_time.drop(df_time[(df_time['Client'] == 'Result') | (df_time['WBS Name'] == 'Result')].index)

# ------------------------------------------------------------------------------------------

# Create bar chart of hours split for period

mpl.rcParams['axes.prop_cycle'] = mpl.cycler(color=['DarkTurquoise', 'Salmon', 'Gold', 'DarkSlateGray', 'Tan', 'DarkOliveGreen', 'DarkOrchid', 'Maroon', 'Tan'])

fig, ax = plt.subplots(2,2, gridspec_kw={'height_ratios': [3, 2]})

str_date = df_util['Date'].tolist()
str_date_ref1 = [x.lower() for x in str_date]
date_clean = [x[0].upper() + x[1:] for x in str_date_ref1]

date_col = df_util['Date']
req_columns = ['Chargeable Hours', 'BD', 'Training', 'Holiday & Other Leave', 'Other']

for column in req_columns:
    ax[0,0].bar(date_col, df_util[column], label=column)

ax[0,0].plot(df_util['Date'], df_util['Planned Hours'], label='Planned Hours', color='Purple')

ax[0,0].legend(loc='upper center', bbox_to_anchor=(0.5, 1.12), ncol=3, fancybox=True, fontsize=9)
ax[0,0].set_xticks(date_col)
ax[0,0].set_xticklabels(labels=date_clean, rotation=45)
ax[0,0].tick_params(axis='both', which='major', labelsize=8)
ax[0,0].set_ylabel('Hours', size=10)

fig = plt.gcf()
fig.set_size_inches(18.5, 10.5)
fig.savefig('test2png.png', dpi=100)
fig.set_size_inches(18.5, 10.5, forward=True)

# ------------------------------------------------------------------------------------------

# Create a pie chart for chargeable hours split by project description

df_pie = df_time[df_time['Engagement Type'] == 'External Projects']

def clean_str(str):
    if ',' in str:
        n_str = str.replace(',', '')
    else:
        n_str = str
    return n_str

df_pie['Hours'] = df_pie.apply(lambda x: clean_str(x['Hours']), axis=1)
df_pie['Hours'] = pd.to_numeric(df_pie['Hours'])
df_pie.sort_values(by=['Hours'], ascending=False, inplace=True)
pie_labels = df_pie['WBS Name'].tolist()

ax[1,1].pie(df_pie['Hours'], labels = pie_labels, textprops={'fontsize': 8})
ax[1,1].set_title('Chargeable Hours by WBS Name', size=10)

# ------------------------------------------------------------------------------------------

# Create a table of overall summed chargeable/BD/Other hours

data = [[df_util['Chargeable Hours'].sum(), df_util['BD'].sum(), df_util['Training'].sum(), df_util['Other'].sum()]]
column_labels = ['Chargeable Hours', 'BD', 'Training', 'Other']

ax[1,0].axis('tight')
ax[1,0].axis('off')
table = ax[1,0].table(cellText=data, colLabels=column_labels, loc="center", cellLoc='center', colColours=['PaleTurquoise']*4)
table.scale(1, 2)

# ------------------------------------------------------------------------------------------

# Create horizontal bar graph of utilisation percentage w/ average line

xlabel_lst = [0, 25, 50, 75, 100]
xlabel_lst_str = [str(x) +'%' for x in xlabel_lst]
average_util_series = df_util_overall.loc[df_util_overall['Date'] == 'Overall Result']['Utilisation (%)']
average_util = average_util_series.iloc[0]


ax[0,1].barh(df_util['Date'], df_util['Utilisation (%)'])
ax[0,1].set_xticks(xlabel_lst)
ax[0,1].set_xticklabels(xlabel_lst_str, fontsize=8)
ax[0,1].set_yticks(df_util['Date'])
ax[0,1].set_yticklabels(date_clean, fontsize=8)
ax[0,1].invert_yaxis()
ax[0,1].set_title('Utilisation (%) Per Month', fontsize=10)
ax[0,1].axvline(average_util, color='Tomato', linestyle='--')
ax[0,1].annotate(str('{:.0f}'.format(average_util)) + '%' + ' Average',
             xy=(average_util, 0),
             xytext=(average_util, 0),
             xycoords='data',
             textcoords='offset pixels',
             arrowprops=dict(arrowstyle="->", color='Tomato', linestyle='--'),
             color='Tomato')

# ------------------------------------------------------------------------------------------

df_util['Date'] = pd.to_datetime(df_util['Date'])
date_lst = df_util['Date'].tolist()
date_lst_reformat = [x.strftime('%m/%Y') for x in date_lst]

title = 'Performance Data Visualisation (' + date_lst_reformat[0] + ' - ' + date_lst_reformat[-1] +')'
fig.suptitle(title, fontsize=14)
plt.show()
