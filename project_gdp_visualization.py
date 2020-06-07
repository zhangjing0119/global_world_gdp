#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Filename: project_gdp_visualization.py
# @Author: zhangjing
import sys 
reload(sys) 
sys.setdefaultencoding('utf8') 
import csv
import math
import pygal
import pygal_maps_world  #导入需要使用的库
from pygal.maps.world import COUNTRIES


def read_csv_as_nested_dict(filename, keyfield, separator, quote): #读取原始csv文件的数据，格式为嵌套字典

    result={}
    with open(filename)as csvfile:
        csvreader=csv.DictReader(csvfile,delimiter=separator,quotechar=quote)
        for row in csvreader:
            rowid=row[keyfield]
            result[rowid]=row
    return result
    
#pygal_countries = pygal.maps.world.COUNTRIES #读取pygal.maps.world中国家代码信息（为字典格式），其中键为pygal中各国代码，值为对应的具体国名(建议将其显示在屏幕上了解具体格式和数据内容）

def get_country_code(country_name):   #根据指定的国家，返回Pygal使用的两个字的国别码
    for code, name in COUNTRIES.items():
        if name == country_name:
            return code
    #如果没有找到指定的国家,就返回None
    return None

def get_gdp_contries(gdp_info):    #获取世行各国数据，嵌套字典格式，其中外部字典的键为世行国家代码，值为该国在世行文件中的行数据（字典格式)
    
    gdp_countries = {}
    err_countries = []
    for country_name, info in gdp_info.items():
        #print(country_name)
        code = get_country_code(country_name)
        if code:
            gdp_countries[code] = info
        if (code == None):
                err_countries.append(info)
    #print gdp_countries
    return gdp_countries
            

 
def reconcile_countries_by_name(gdpinfo, gdp_countries): #返回在世行有GDP数据的绘图库国家代码字典，以及没有世行GDP数据的国家代码集合

    all_gdp_data = {}
    gdp_data = {}
    i_no_gdp_data = []
    p_gdp_data = {}
    no_gdp_data = {}
    for c_code, c_data in gdp_countries.items():
        #print c_data
        gdp_value = 0
        for year in range(gdpinfo["min_year"], gdpinfo["max_year"]):
            i_gdp_value = 0
            year = str(year)
            #print(year)
            if (c_data[year]):
                i_gdp_value = math.log10(int(float(c_data[year])))
                c_data[year] = i_gdp_value
                gdp_value += i_gdp_value
            else:
                c_data[year] = 0
            #print i_gdp_value
        if (gdp_value > 0):
            gdp_data[c_code] = c_data
        else:
            i_no_gdp_data.append(c_code)

    no_gdp_data[0] = i_no_gdp_data   #完全没用GDP数据的国家代码

    p_gdp_data[1] = gdp_data         #有GDP数据的国家代码

    all_gdp_data = dict(p_gdp_data,**no_gdp_data)

    #print all_gdp_data

    return all_gdp_data

    
    


def build_map_dict_by_name(gdpinfo, all_gdp_data, year):

    f_gdp_data = {}
    z_gdp_data = []
    a_gdp_data = {}
    year = str(year)
    for b_code, b_info in all_gdp_data[1].items():
        if (b_info[year] > 0):
            f_gdp_data[b_code] = b_info[year]
        else:
            z_gdp_data.append(b_code)
    a_gdp_data[0] = f_gdp_data            #在某一年份有GDP数据的国家代码
    a_gdp_data[1] = z_gdp_data            #在某一年份暂时没有GDP数据的国家代码
    a_gdp_data[2] = all_gdp_data[0]       #完全没有GDP数据的国家代码

    #print a_gdp_data

    return a_gdp_data


def render_world_map(gdpinfo,year): #将具体某年世界各国的GDP数据(包括缺少GDP数据以及只是在该年缺少GDP数据的国家)以地图形式可视化

    worldmap_chart = pygal.maps.world.World()
    worldmap_chart.title = 'GLOBAL WORLD GDP'
    worldmap_chart.add(str(year)+' GDP',gdpinfo[0])
    worldmap_chart.add(str(year)+' MISS GDP DATA',gdpinfo[1])
    worldmap_chart.add('NO GDP DATA',gdpinfo[2])
    worldmap_chart.render_to_file('isp_gdp_world_name_'+str(year)+'.svg')


def build_gdp_data(year):  
    gdpinfo = {
        "gdpfile": "isp_gdp.csv",
        "separator": ",",
        "quote": '"',
        "min_year": 1960,
        "max_year": 2016,
        "country_name": "Country Name",
        "country_code": "Country Code"
    } #定义数据字典
  

    wd_gdp_data= read_csv_as_nested_dict(gdpinfo["gdpfile"], gdpinfo["country_name"], gdpinfo["separator"], gdpinfo["quote"])

    gdp_countries = get_gdp_contries(wd_gdp_data)

    all_gdp_data = reconcile_countries_by_name(gdpinfo, gdp_countries)

    build_data = build_map_dict_by_name(gdpinfo,all_gdp_data,year)

    render_world_map(build_data,year)

    

    




#程序运行
print("欢迎使用世行GDP数据可视化查询")
print("----------------------")
year=input("请输入需查询的具体年份:")
build_gdp_data(year)
