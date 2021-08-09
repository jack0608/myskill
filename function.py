import folium
import pandas as pd
import urllib.request
import datetime
import time
import json
import webbrowser
import numpy as np
import firebase_admin
import matplotlib.pyplot as plt
import os, ssl

from folium.plugins import HeatMap
from firebase_admin import credentials, initialize_app
from firebase_admin import firestore
from matplotlib import font_manager, rc

class initFunc:
    def __init__(self):
        self.initialize()
    
    def initialize(self):
        font_path = "C:/Windows/Fonts/NGULIM.TTF"
        font = font_manager.FontProperties(fname=font_path).get_name()
        rc('font', family=font)

        if (not os.environ.get('PYTHONHTTPSVERIFY', '') and
            getattr(ssl, '_create_unverified_context', None)): 
            ssl._create_default_https_context = ssl._create_unverified_context

class NaverAPI:
    def __init__(self):
        print('Naver API Used')

    def get_request_url(address, url, clientId, clientSecret):
        req = urllib.request.Request(url)
        req.add_header("X-NCP-APIGW-API-KEY-ID", clientId)
        req.add_header("X-NCP-APIGW-API-KEY", clientSecret)
        try:
            response = urllib.request.urlopen(req)
            if response.getcode() == 200:
                print ("[%s] Url Request Success : [%s]" % (datetime.datetime.now(), address))
                return response.read().decode('utf-8')
        except Exception as e:
            print(e)
            print("[%s] Error for URL : %s" % (datetime.datetime.now(), url))
            return None

    def getGeoData(address):
        base = "https://naveropenapi.apigw.ntruss.com/map-geocode/v2/geocode"

        try:
            parameters = "?query=%s" % urllib.parse.quote(address)
        except:
            return None

        url = base + parameters

        retData = NaverAPI.get_request_url(address, url, 'qh2cl6dxpw', 'u5b7JtT9I2bs7cvWnFrOKDwoPTf6rs0UnNuW4sLF')
        if retData == None:
            return None

        jsonAddress = json.loads(retData)
        
        if 'addresses' in jsonAddress.keys():
            latitude = jsonAddress['addresses'][0]['y']
            longitude = jsonAddress['addresses'][0]['x']
        else:
            return None

        return [latitude, longitude]

class FoilumMap:

    def drawHeatMap(df):

        geoData = []
        npGeoData= []

        map = folium.Map(location=[37.5103, 126.982], zoom_start=12)

        for i, row in df.iterrows():
            address = row['주소']    
            geoData = NaverAPI.getGeoData(address)

            if geoData != None:
                folium.Marker(
                    geoData, 
                    popup=row['장소'], 
                    icon=folium.Icon(color='red')
                ).add_to(map)        
                npGeoData.append(geoData)

        npGeoData = np.array(npGeoData)
        HeatMap(npGeoData).add_to(map)

        svFilename = 'date.html'
        map.save(svFilename)

class Chart:
   
    def drawPieChart(self, keys, values):
        explode = [0.05, 0.05, 0.05, 0.05]
        plt.pie(values, labels=keys, autopct='%.1f%%', startangle=260, counterclock=False, explode=explode)
        plt.show()

class DataFrameClass:
    def __init__(self, path):
        self.path = path

    def makeCallDF(self):
        df = pd.DataFrame(columns = ["date", "day", "time", "type", 'phone', 'second'])
        with open(self.path, 'rt', encoding='utf8') as f:
            lines = f.readlines()
            for line in lines:  
                splitLine = line.split(" : ")
                df.loc[len(df)] = splitLine
        
        return df

class commonClass:
    def dataCleaning(self, indir, outdir, deltxt):
        edited_lines = []

        with open(indir, 'rt', encoding='utf8') as f:
            lines = f.readlines()
            for line in lines:  
                if deltxt in line:
                    edited_lines.append(line)

        with open(outdir, 'w', encoding='utf8') as f:
            f.writelines(edited_lines)

        print('done')
