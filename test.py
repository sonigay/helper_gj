import discord
import asyncio
import random
import openpyxl
from discord import Member
from discord.ext import commands
import youtube_dl
from urllib.request import urlopen, Request
import urllib
import urllib.request
import bs4
import os
import sys
import json
from selenium import webdriver
import time
import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials

scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('gjhelper-cc7069273059.json', scope)
client = gspread.authorize(creds)
doc = client.open_by_url('https://docs.google.com/spreadsheets/d/1PA2WP-aQ-d8TlGubOSpUJwHoH8VZfiTwIFPO3eYGnIs')



client = discord.Client()

countG = 0
client = discord.Client()
players = {}
queues= {}
musiclist=[]
mCount=1
searchYoutube={}
searchYoutubeHref={}

def check_queue(id):
    if queues[id]!=[]:
        player = queues[id].pop(0)
        players[id] = player
        del musiclist[0]
        player.start()

@client.event
async def on_ready():
    print("login")
    print(client.user.name)
    print(client.user.id)
    print("------------------")
    await client.change_presence(game=discord.Game(name='업무보조', type=1))



@client.event
async def on_message(message):
    global gc #정산
    global creds	#정산
    global channel
    
    if message.content.startswith('!재고'):
        SearchID = message.content[len('!재고')+1:]
        gc = gspread.authorize(creds)
        wks = gc.open('GJ재고관리').worksheet('영업재고출력')
        wkstime = gc.open('GJ재고관리').worksheet('재고데이터')
        wks.update_acell('A1', SearchID)
        result = wks.acell('B1').value
        result1 = wks.acell('C1').value
        result2 = wkstime.acell('A1').value
        
        embed1 = discord.Embed(
            title = ' :calling:  ' + SearchID + ' 재고현황! ',
            description= '**```css\n' + SearchID + ' 재고현황 입니다.\n마지막 데이터 업로드시간은\n'+ result2 + ' 입니다.' + result + '```**',
            color=0x50508C
            )
        embed2 = discord.Embed(
            title = '',
            description= '**```css\n' + result1 + '실시간조회가 아니라서 다소 차이가 있을수 있습니다. ```**',
            color=0x50508C
            )        
        await client.send_message(message.channel, embed=embed1)
        await client.send_message(message.channel, embed=embed2)
        
        
    if message.content.startswith('!전월실적'):
        SearchID = message.content[len('!전월실적')+1:]
        gc = gspread.authorize(creds)
        wks = gc.open('GJ재고관리').worksheet('전월실적출력')
        wks.update_acell('A1', SearchID)
        result = wks.acell('B1').value

        
        embed1 = discord.Embed(
            title = ' 📈 ' + SearchID + ' 전월실적! ',
            description= '**```css\n' + SearchID + '2ND/중고/선불개통제외 전월마감실적 입니다.\n중도 취소발생시 실적에서 차이가 생길수 있습니다.\n'+ result + '\n\n입니다. 한달동안 고생 많으셨습니다. ```**',
            color=0x50508C
            )
        await client.send_message(message.channel, embed=embed1)

        
    if message.content.startswith('!당월실적'):
        SearchID = message.content[len('!당월실적')+1:]
        gc = gspread.authorize(creds)
        wks = gc.open('GJ재고관리').worksheet('당월실적출력')
        wkstime = gc.open('GJ재고관리').worksheet('당월모바일개통데이터')
        wks.update_acell('A1', SearchID)
        result2 = wkstime.acell('C1').value        
        result = wks.acell('B1').value

        
        embed1 = discord.Embed(
            title = ' 📈 ' + SearchID + ' 당월실적! ',
            description= '**```css\n' + SearchID + '2ND/중고/선불개통제외 당월실적 입니다.\n마지막 데이터 업로드시간은\n'+ result2 + ' 입니다.' + result + '\n\n입니다. 실시간조회가 아니라서 다소 차이가 있습니다.\n이번달도 끝까지 화이팅입니다!! ```**',
            color=0x50508C
            )
        await client.send_message(message.channel, embed=embed1)        

        
        
    if message.content.startswith('!거래처'):
        SearchID = message.content[len('!거래처')+1:]
        gc = gspread.authorize(creds)
        wks = gc.open('GJ재고관리').worksheet('거래처코드출력')
        wks.update_acell('A1', SearchID)
        result1 = wks.acell('B1').value
        result2 = wks.acell('C1').value
        result3 = wks.acell('D1').value
        result4 = wks.acell('E1').value
        
        embed1 = discord.Embed(
            title = ' :printer:  거래처 코드 리스트 ',
            description= '**```css\n' + SearchID + ' 거래처 코드는 ' + result1 + ' ```**',
            color=0x00Bfff
            )
        embed2 = discord.Embed(
            title = '',
            description= '**```css\n' + result2 + '```**',
            color=0x00Bfff
            )
        embed3 = discord.Embed(
            title = '',
            description= '**```css\n' + result3 + ' ```**',
            color=0x00Bfff
            )
        embed4 = discord.Embed(
            title = '',
            description= '**```css\n' + result3 + ' ```**',
            color=0x00Bfff
            )        
        await client.send_message(message.channel, embed=embed1)
        await client.send_message(message.channel, embed=embed2)
        await client.send_message(message.channel, embed=embed3)
        await client.send_message(message.channel, embed=embed4)
        
    if message.content.startswith('!유심'):
        SearchID = message.content[len('!유심')+1:]
        gc = gspread.authorize(creds)
        wks = gc.open('GJ재고관리').worksheet('유심출력')
        wkstime = gc.open('GJ재고관리').worksheet('재고데이터')
        wks.update_acell('A1', SearchID)
        result2 = wkstime.acell('a1').value        
        result = wks.acell('B1').value
        result3 = wks.acell('C1').value
        result4 = wks.acell('D1').value
        result5 = wks.acell('E1').value
        
        embed1 = discord.Embed(
            title = ' 📈 ' + SearchID + '유심현황! ',
            description= '**```css\n' + SearchID + '잔여 유심현황 입니다.\n마지막 데이터 업로드시간은\n'+ result2 + ' 입니다.\n' + result + '```**',
            color=0x50508C
            )
        embed2 = discord.Embed(
            title = '',
            description= '**```css\n ' + result3 + ' ```**',
            color=0x50508C
            )
        embed3 = discord.Embed(
            title = '',
            description= '**```css\n ' + result4 + ' ```**',
            color=0x50508C
            )
        embed4 = discord.Embed(
            title = '',
            description= '**```css\n' + result5 + ' 입니다. 실시간조회가 아니라서 다소 차이가 있습니다. ```**',
            color=0x50508C
            )
        await client.send_message(message.channel, embed=embed1)        
        await client.send_message(message.channel, embed=embed2)
        await client.send_message(message.channel, embed=embed3)
        await client.send_message(message.channel, embed=embed4)        
        
        
    if message.content.startswith('!불량'):
        SearchID = message.content[len('!불량')+1:]
        gc = gspread.authorize(creds)
        wks = gc.open('GJ재고관리').worksheet('불량출력')
        wkstime = gc.open('GJ재고관리').worksheet('재고데이터')
        wks.update_acell('A1', SearchID)
        result2 = wkstime.acell('a1').value        
        result = wks.acell('B1').value
        result3 = wks.acell('C1').value
        result4 = wks.acell('D1').value
        result5 = wks.acell('E1').value
        
        embed1 = discord.Embed(
            title = ' 📈 ' + SearchID + ' !불량현황 ',
            description= '**```css\n' + SearchID + '불량형황 입니다.\n마지막 데이터 업로드시간은\n'+ result2 + ' 입니다.\n' + result + '```**',
            color=0x50508C
            )
        embed2 = discord.Embed(
            title = '',
            description= '**```css\n ' + result3 + ' ```**',
            color=0x50508C
            )
        embed3 = discord.Embed(
            title = '',
            description= '**```css\n ' + result4 + ' ```**',
            color=0x50508C
            )
        embed4 = discord.Embed(
            title = '',
            description= '**```css\n ' + result5 + ' 입니다. 실시간조회가 아니라서 다소 차이가 있습니다. ```**',
            color=0x50508C
            )
        await client.send_message(message.channel, embed=embed1)        
        await client.send_message(message.channel, embed=embed2)
        await client.send_message(message.channel, embed=embed3)
        await client.send_message(message.channel, embed=embed4)        
        
        
        
    
    


access_token = os.environ["BOT_TOKEN"]
client.run(access_token)
