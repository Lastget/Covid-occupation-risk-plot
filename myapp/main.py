import pandas as pd 
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from bokeh.io import output_file, show, curdoc
from bokeh.plotting import figure, save
from bokeh.models import ColumnDataSource, Select, Div, HoverTool, Label, LabelSet, FixedTicker
from bokeh.layouts import row, column
from bokeh.models.renderers import GlyphRenderer
from math import pi
pd.options.mode.chained_assignment = None

# Improt files
expose = pd.read_csv(r'data/Exposed_to_Disease_or_Infections.csv',encoding='gbk')
#expose.shape (968,3)

physical = pd.read_csv('data/Physical_Proximity.csv')
#physical.shape (967,3)

TW_job = pd.read_excel('data/Small_Chinese.xlsx')
#TW_job.shape (968,3)
TW_job = TW_job.iloc[:,:2]

#Merge
temp_df = pd.merge(expose,physical,on=['Code','Occupation'])
temp_df.columns=['Expose_frequency','Code','Occupation','Physical_proximity']
full_table = temp_df.merge(TW_job,how='left',on='Code')
#full_table.shape 967,5

# Delete Expose frequency for Rock splitter, timing deivce 
full_table = full_table.iloc[:965,:]

# change expose  to int64 
full_table['Expose_frequency']=full_table['Expose_frequency'].astype('int64')

# Start plotting 
source = ColumnDataSource(full_table) 
p = figure(title="各職業對新型冠狀病毒之風險", x_axis_label='工作時與人接近程度', y_axis_label='工作時暴露於疾病頻率',
            width=900, height=600, sizing_mode = "scale_both",active_drag=None)
p.circle('Physical_proximity','Expose_frequency',
            name = 'allcircle',
            size=10,fill_alpha=0.2, source=source, fill_color='gray', hover_fill_color='firebrick', hover_line_color="firebrick", line_color=None)
hover = HoverTool(tooltips=[('職業','@TW_Occupation'),('Occupation','@Occupation'),('暴露於疾病指數','@Expose_frequency'),('與人接近距離指數','@Physical_proximity')])
p.add_tools(hover)

# Plot medicals 
medical_professionals=['29-1141.01','29-2021.00','29-1062.00','29-1063.00','29-1141.03','29-1069.03','29-1022.00','29-1126.00','29-2054.00','29-1071.01','31-2012.00'
,'31-1015.00','31-9091.00','29-2011.00','29-1151.00','29-1069.12','29-1069.01','29-1021.00','29-1124.00','29-1141.00','29-2061.00','29-1064.00',
'29-1069.11','29-1069.02','29-2033.00','29-1071.00','29-2053.00','31-9093.00','29-1122.00','29-1069.06','29-1065.00'
,'29-2034.00','29-1141.04','29-1199.04','31-1013.00','29-2099.06','29-1061.00','29-1069.08','29-2041.00','29-1161.00',
'29-1131.00','21-1022.00','31-2011.00','31-9097.00','29-1024.00','29-2032.00','31-9099.02',
'29-1171.00','29-1081.00','29-2099.07','31-9096.00','31-2022.00','29-1067.00','29-1199.01',
'29-1069.10','29-2035.00','29-2011.01','39-4011.00','31-9092.00','31-1014.00',
'29-2099.05','19-1022.00','29-2055.00','29-2099.01','29-1069.05','29-1141.02','29-2011.02','29-1031.00','29-2091.00','29-1023.00','31-9095.00',
'29-1069.04','43-4051.03','29-1069.07','29-1051.00','31-2021.00','29-2011.03','29-1041.00',
'29-1199.05','29-2031.00','53-3011.00','51-9081.00','29-2052.00','29-1066.00','29-1181.00','29-1123.00','29-2056.00','19-4092.00',
'19-3031.02','19-3039.01','51-9082.00','29-9099.01','29-2057.00','29-1125.02','29-1125.00','13-1041.06','29-1011.00','29-1127.00','31-9099.01','29-1069.09']
teachers=['25-2012.00','25-2053.00','25-2022.00','25-2011.00','25-2051.00','25-2052.00','25-2021.00','25-9041.00','25-2054.00','25-2032.00',
'25-1051.00','25-1042.00','25-1071.00','25-1061.00','25-2023.00','25-1111.00','25-1053.00','25-3011.00','25-1193.00','25-1121.00','25-2031.00',
'25-1194.00','25-1022.00','25-1041.00','25-1066.00','25-1062.00','25-1122.00','25-1021.00','25-1124.00','25-1113.00','25-1063.00','25-1064.00',
'25-1081.00','25-1192.00','25-1032.00','25-1123.00','25-1067.00','25-1125.00','25-3021.00','25-1052.00','25-1054.00','25-1031.00','25-1043.00',
'25-1112.00','25-1065.00','25-1011.00','25-1126.00','25-1082.00']
transport=['43-5021.00','53-2011.00','53-2012.00','53-2031.00','53-3021.00','53-3022.00','53-3041.00','53-4011.00','53-4012.00','53-4013.00','53-4021.00','53-4031.00',
'53-4041.00','53-5011.00','53-5021.01','53-5021.02','53-5022.00','53-5031.00']
service_industry=['35-3011.00','35-3022.00','35-3031.00','35-3041.00','35-9011.00','35-9031.00','39-5011.00','39-5012.00','39-5092.00','39-5093.00','39-5094.00',
'39-7012.00','39-7011.00','39-6012.00','39-9031.00','41-2011.00']

all_color_code = medical_professionals + teachers + transport + service_industry

color_table=full_table[full_table.Code.isin(all_color_code)]

# Defining Labes  
def filter_label(job):
    if job in medical_professionals:
        return '醫療人員'
    elif job in teachers: 
        return '教師' 
    elif job in transport: 
        return '交通運輸業'
    elif job in service_industry: 
        return '服務業'            
    else:
        return ''

color_table['label'] = color_table['Code'].map(filter_label)

# Defining color 
c_med = '#51A8DD'
c_teach = '#FFB11B'
c_transport='#24936E'
c_service='#DB4D6D' 
c_other = '#707C74'

def filter_color(job):
    if job == '醫療人員':
        return c_med
    elif job == '教師': 
        return c_teach  
    elif job == '交通運輸業': 
        return c_transport
    elif job == '服務業': 
        return c_service   
    else:
        return c_other

color_table['color'] = color_table['label'].map(filter_color)

source_color = ColumnDataSource(color_table) 

p.circle('Physical_proximity','Expose_frequency',
            name = 'color_circle',line_color=None,legend_field='label',
            size=10,fill_alpha=0.5, source=source_color, color='color')
p.legend.location = "top_left"

# add circle outline
outline = ['29-1021.00','29-1141.00','29-2041.00','31-1011.00','33-3021.01','33-2011.01','53-2031.00','33-3021.05','37-1011.00','39-7011.00','41-2011.00','43-5021.00'] 
outline_table = full_table[full_table.Code.isin(outline)] 
outline_table.iloc[1,4]='護理師'
outline_table.iloc[5,4]='快遞'
outline_table.iloc[7,4]='海關'
outline_table.iloc[6,4]='居家看護'
outline_table.iloc[9,4]='清潔工'
outline_table.iloc[11,4]='導遊'
source_outline = ColumnDataSource(outline_table) 
p.circle('Physical_proximity','Expose_frequency',source=source_outline , name = 'outline_circle',line_color='#08192D',size=10, fill_color=None)


# layout 
dentist_labels = LabelSet(x='Physical_proximity',y='Expose_frequency', name='dentist_word', source=source_outline,
                 text='TW_Occupation',  text_font_size='8pt', text_color='#08192D',
                 x_offset=-20, y_offset=-20)
p.add_layout(dentist_labels)

p.title.text_font_size = '14pt'

p.xaxis.ticker = [0, 25, 50,75,100]
p.xaxis.major_label_overrides = {0:'獨自工作(0)',25: '不近(25)', 50: '稍微近(50)', 75: '中等距離(75)', 100:'非常近(100)'}
p.yaxis.ticker = [0, 25, 50,75,100]
p.yaxis.major_label_overrides = {0:'從不(0)',25: '一年一次(25)', 50: '一個月一次(50)', 75: '一週一次(75)', 100:'每天(100)'}
p.yaxis.major_label_orientation = pi/4

# remove tool bar 
p.toolbar.logo = None
p.toolbar_location = None

def remove_glyphs(figure, glyph_name_list):
    renderers = figure.select(dict(type=GlyphRenderer))
    for r in renderers:
        if r.name in glyph_name_list:
            col = r.glyph.y
            r.data_source.data[col] = [np.nan] * len(r.data_source.data[col])


# Define a callback function 
def update_plot(attr, old, new):
    remove_glyphs(p,['point_select','color_circle','outline_circle'])
    old_choice=full_table[full_table['TW_Occupation']==old]  

    choice=full_table[full_table['TW_Occupation']==new]
    a=choice['Physical_proximity']
    b=choice['Expose_frequency']
    p.circle(a,b,size=10,fill_alpha=1,fill_color='firebrick',line_color="firebrick", name='point_select')

# Add Select 
select = Select(title='請選擇工作', options=sorted(full_table['TW_Occupation'].tolist()), value='')

# Attach the update_plot callback to the 'value' property of select
select.on_change('value', update_plot)

# Add discription
div_help = Div(text="""
  <b><h3>哪些職業有較高感染風險？</b></h3>
  我的工作有多高接觸傳染病的風險？可藉由選單選取職業，查看工作感染疾病風險。
  <br></br> 橫軸表示工作者與人接觸的距離。縱軸表示工作者平時接觸到傳染疾病的頻率。滑鼠滑過該點可顯示其風險數值
  <br></br> 越右上角表示其接觸傳染病機率高和與人距離又近，所以我們可以看到醫療人員風險較高，另外像交通運輸業的空服員，教師族群，理髮師，消防，海關等也都是風險注意對象。
            風險也只能參考，低風險族群還是要做好防疫與衛生。
   """,sizing_mode="scale_both" )

div_reference = Div(text="""
<ul>
  <li>資料來自美國勞動部資料庫  <a href="https://www.onetonline.org/find/descriptor/result/4.C.2.c.1.b"> O*NET </a> </li>
  <li> 呈現參考 New York Times <a href="https://www.nytimes.com/interactive/2020/03/15/business/economy/coronavirus-worker-risk.html?smid=fb-nytimes&smtyp=cur&fbclid=IwAR0UG6dj1eqMilukx9wit5FX4P4TxAodtvW8b0toGyYDCKygM087uZr8P38">The Workers Who Face the Greatest Coronavirus Risk</a> by Lazaro Gamio  </li>
  <li> Author <a href="https://lastget.github.io/"> Richard Tsai </a></li>
</ul>
""")


layout = column(p, select, div_help, div_reference)   

# Add the plot to the current document
curdoc().add_root(layout)  


# save the results to a file
show(p)