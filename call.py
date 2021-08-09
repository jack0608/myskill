from function import * 

####################################################################################
## Call DataFrame
####################################################################################


####################################################################################
## 1. 데이터 정제

cf = commonClass()

indir = 'C:/Users/Jack/Downloads/call1.txt'
outdir = 'C:/Users/Jack/Downloads/call2.txt'
deltxt = '01071723028'

cf.dataCleaning(indir, outdir, deltxt)

####################################################################################


####################################################################################
## 2. dataframe 생성

path = 'C:/Users/Jack/Downloads/call2.txt'
dfc = DataFrameClass(path)
df = dfc.makeCallDF()

print(df.head())

df_date = df['date']
df_day = df['day']
df_time = df['time']
df_type = df['type']
df_second = df['second'].astype('int')

df_nobal = df.loc[(df_type == '발신') & (df_second == 0)]

####################################################################################


####################################################################################
## 3. pie 차트 그리기

init = initFunc()
chart = Chart()
#chart.drawPieChart(df_type.value_counts().keys(), df_type.value_counts().values)

####################################################################################

# 테스트 입니다