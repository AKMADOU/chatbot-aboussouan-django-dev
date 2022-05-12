from typing import Container
from django.shortcuts import render
from rest_framework import viewsets
from bs4.element import Comment
from bs4 import BeautifulSoup
import urllib.request as urllib2
import html2text

from urllib.request import Request, urlopen
from string import punctuation
import string
import speech_recognition as sr
import moviepy.editor as me
import os,re
from backend.settings import MEDIA_ROOT
from urllib.request import urlopen 
from socket import timeout
from api.models import *
from api.serializers import *
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import generics, permissions, status
import json
from icecream import ic

from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import requests
import webbrowser

import pyttsx3 as ttx
import speech_recognition as sr

from bs4 import BeautifulSoup



  



class UrlAPIListView(generics.CreateAPIView):
    permission_classes=()
    queryset =Url.objects.all()
    serializer_class = UrlSerializer

    def get(self, request, format=None):
        items = Url.objects.order_by('pk')
        
        serializer = UrlSerializer(items, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = UrlSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)



class UrlAPIView(generics.CreateAPIView):
    permission_classes=(
          
    )
    queryset = Url.objects.all()
    serializer_class = UrlSerializer
    def get(self, request, id, format=None):
        try:
            item = Url.objects.get(pk=id)
            serializer = UrlSerializer(item)
            return Response(serializer.data)
        except Url.DoesNotExist:
            return Response(status=404)

    def put(self, request, id, format=None):
        try:
            item = Url.objects.get(pk=id)
        except Url.DoesNotExist:
            return Response(status=404)
        self.data = request.data.copy()      
        serializer = UrlSerializer(item, data= self.data, partial= True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def delete(self, request, id, format=None):
        try:
            item = Url.objects.get(pk=id)
        except Url.DoesNotExist:
            return Response(status=404)
        item.delete()
        return Response(status=204)   


class UrlByWordAPIView(generics.CreateAPIView):
    permission_classes=()
    queryset = Url.objects.all()
    serializer_class = WordSerializer         
    def post(self, request, format=None):
        url_list=Url.objects.all() 
        hdr = requests.utils.default_headers()        
        hdr.update({'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
            'Accept-Encoding': 'none',
            'Accept-Language': 'fr-FR,en;q=0.8',
            'Connection': 'keep-alive'})
        the_word = request.data['word']              
        data1=[]
        
        total_words = ["cette page ne contient pas votre question"]
        
        for url in url_list:
            request = Request(url.url, headers=hdr)
            
            try:
                page = urlopen(request)
            except urllib2.HTTPError as e:
                e.fp.read()
            content = page.read()    
            soup =  BeautifulSoup(content, 'html.parser')  
                      
            words = soup.find_all(text=lambda text: text and the_word.lower() in text)
            output = ''
            blacklist = ['header','style','[document]','noscript','title']

            for t in words:
                if t.parent.name not in blacklist:
                    output += '{} '.format(t)
            words_list = (output[:500] + '..') if len(output) > 500 else output
            print(output)
            count = len(output)       
                      
            resultat='\nUrl: {}\ncontains {} of word: {}'.format(url.url, count, the_word) 
            if len(str(words_list))==0:
                print("vide")
            else:                   
                data1.append({
                    "Url": url.url, 
                    "Word":the_word,                         
                    "Résultat":words_list
                    })  
        return Response(data1) 

            
                      
        
    

class AudioByWordAPIView(generics.CreateAPIView):
    permission_classes=()
    queryset = Url.objects.all()
    serializer_class = AudioSerializer
    def post(self, request, format=None): 
        url_list=Url.objects.all()                             
        hdr={'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,/;q=0.8',
            'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
            'Accept-Encoding': 'none',
            'Accept-Language': 'fr-FR,en;q=0.8',
            'Connection': 'keep-alive'}
        the_word = request.data['audio']              
        data1=[]   

        audio = request.FILES['audio']                 
        audio_file = default_storage.save('audios/'+audio.name,ContentFile(audio.read()))    
        url= MEDIA_ROOT+"/"+audio_file
        #url= "http://192.168.1.59:8000/uploads/"+audio_file
        VIDEO_FILE = url
        OUTPUT_AUDIO_FILE = " converted.wav"
        OUTPUT_TEXT_FILE = " recognized.txt"        
        try:
            video_clip = me.AudioFileClip(r"{}".format(VIDEO_FILE))
            video_clip.write_audiofile(r"{}".format(OUTPUT_AUDIO_FILE))
            recognizer =  sr.Recognizer()
            audio_clip = sr.AudioFile("{}".format(OUTPUT_AUDIO_FILE))           
            with audio_clip as source:
                audio_file = recognizer.record(source)
            print("Please wait ...")
            the_word = recognizer.recognize_google(audio_file,language="fr-FR")            
            with open(OUTPUT_TEXT_FILE, 'w') as file:
                file.write(the_word) 
                print(the_word) 
        except Exception as e:
            {"message":str(e)} 
        data1=[]
        
        
        for url in url_list:
            request = Request(url.url, headers=hdr)                
            try:
                page = urlopen(request)
            except urllib2.HTTPError as e:
                e.fp.read()
            content = page.read()    
            soup =  BeautifulSoup(content, 'html.parser')  
                    
            words = soup.find_all(text=lambda text: text and the_word.lower() in text)
            output = ''
            blacklist = ['header','style','[document]','noscript','title']

            for t in words:
                if t.parent.name not in blacklist:
                    output += '{} '.format(t)
            words_list = (output[:500] + '..') if len(output) > 500 else output
            print(output)
            count = len(output)       
                    
            resultat='\nUrl: {}\ncontains {} of word: {}'.format(url.url, count, the_word)                
            if len(str(words_list))==0:
                print("vide")
            else:        
                data1.append({
                "Url": url.url, 
                "Word":the_word,                         
                "Résultat":words_list
                }) 
                                                                                                                    
         
        return Response(data1)

class UserAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    def get(self, request, id, format=None):
        try:
            item = User.objects.get(pk=id)
            serializer = UserSerializer(item)
            return Response(serializer.data)
        except User.DoesNotExist:
            return Response(status=404)

    def put(self, request, id, format=None):
        try:
            item = User.objects.get(pk=id)
        except User.DoesNotExist:
            return Response(status=404)
        self.data = request.data.copy()      
        serializer = UserSerializer(item, data= self.data, partial= True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def delete(self, request, id, format=None):
        try:
            item = User.objects.get(pk=id)
        except User.DoesNotExist:
            return Response(status=404)
        item.delete()
        return Response(status=204)   



class UserAPIListView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get(self, request, format=None):
        items = User.objects.order_by('pk')
        serializer = UserSerializer(items, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)        


class UserRegisterView(generics.CreateAPIView):
    
    permission_classes = ()
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer

    def post(self, request, *args, **kwargs):
       
        serializer = UserRegisterSerializer(data=request.data)
       
        if not serializer.is_valid():
            return Response({
                "status": "failure",
                "message": "invalid data",
                "error": serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()

        return Response({
            "status": "success",
            "message": "item successfully created",
            'data': serializer.data
        }, status=status.HTTP_201_CREATED)

