# -*- coding: utf-8 -*-
"""
Created on Sun Mar 10 10:58:32 2019

@author: ylf
"""

#任意image和xml文件生成Voc2007数据集
#部分代码参考了 https://blog.csdn.net/weixin_38124357/article/details/78425890 该博客

import os
import re
import sys
import shutil
import xml.etree.ElementTree as ET
import random


def Choose_image(JPEGImages_voc, path_label, path_src, Test_path):
    
    #JPEGImages_voc为voc2007数据集中的JPEGImages文件夹
    #path_label为原始标记文件路径
    #path_src为原始图像文件夹路径
    #Test_path为测试图像文件夹路径
    #从原始图像文件夹中筛选有标记图像放入JPEGImages文件夹，并重命名为00000x.jpg
    #没有标记图像放入Test文件夹
    
    if not os.path.exists(JPEGImages_voc):
        os.makedirs(JPEGImages_voc)
    if not os.path.exists(Test_path):
        os.makedirs(Test_path)
        
    fileList_label = os.listdir(path_label)
    os.chdir(path_label)
    name_label = []
    for fileName_label in fileList_label:	
        pat=".+\.(xml)"
        #pattern_label = re.findall(pat,fileName_label) 		
        name_label.append(os.path.splitext(fileName_label)[0])   
    fileList_src = os.listdir(path_src)
    os.chdir(path_src)
    name_src = []
    for fileName_src in fileList_src:		
        pat=".+\.(jpg|png|gif)"		
        pattern_src = re.findall(pat,fileName_src)
        name_src.append(os.path.splitext(fileName_src)[0])   
    j = 1
    for i in range(len(name_src)):
        if name_src[i] in name_label:
            new_file_path = JPEGImages_voc+ '\\'+ "%06d"%j + '.jpg'
            shutil.copy(path_src + '/' + name_src[i] + '.' + pattern_src[0], new_file_path)
            j += 1
        else:
            shutil.copy(path_src + '/' + name_src[i] + '.' + pattern_src[0], Test_path + '/')
    return 0
            
def Change_xml(Annotations_voc, path_label):
    
    #Annotations_voc为voc2007数据集中Annotations文件夹
    #path_label为原始标记文件路径
    #修改xml文件中的path和filename并重命名为00000x.xml
    #change_exl_path设置为要修改的path
    
    if not os.path.exists(Annotations_voc):
        os.makedirs(Annotations_voc)
        
    change_exl_path = r'E:\faster-rcnn\data\VOCdevkit2007\VOC2007\JPEGImages'
    os.chdir(path_label)
    xmlList = os.listdir(path_label)
    j = 1
    for i in xmlList:
        #pat=".+\.(jpg|png|gif)"	
        #pattern = re.findall(pat,i)
        #os.rename(fileName,("%06d"%j + '.' + pattern[0]))
        a, b = os.path.splitext(i)
        tree = ET.parse(path_label + '\\' + a + b)
        root = tree.getroot()
        for path in root.iter('path'):
            #older_path = str(path.text)
            new_path = change_exl_path + '\\' + "%06d"%j +'.jpg'
            path.text = str(new_path)
        for name in root.iter('filename'):
            #older_name = str(name.text)
            new_name = "%06d"%j + '.jpg'
            name.text = str(new_name)
        tree.write(Annotations_voc + '\\'+ "%06d"%j + b)
        j = j + 1
    return 0

def Make_val(ImageSets_voc, Annotations_voc):
    
    #ImageSets_voc为voc2007数据集中的ImageSets文件夹
    #在ImageSets/main下生成test.txt, train.txt, trainvel.txt, val.txt文件
    if not os.path.exists(ImageSets_voc):
        os.makedirs(ImageSets_voc)
    ImageSets_Main_voc = ImageSets_voc + '\Main'
    if not os.path.exists(ImageSets_Main_voc):
        os.makedirs(ImageSets_Main_voc)
    ImageSets_Segmentation_voc = ImageSets_voc + '\Segmentation'
    if not os.path.exists(ImageSets_Segmentation_voc):
        os.makedirs(ImageSets_Segmentation_voc)  
    
    os.chdir(ImageSets_Main_voc)
    #make val train
    trainval_percent = 0.66  
    train_percent = 0.5  
    total_xml = os.listdir(Annotations_voc)  
    num = len(total_xml)  
    list = range(num)  
    tv = int(num * trainval_percent)  
    tr = int(tv * train_percent)  
    trainval = random.sample(list, tv)  
    train = random.sample(trainval, tr)  
    ftrainval = open('trainval.txt', 'w')  
    ftest = open('test.txt', 'w')  
    ftrain = open('train.txt', 'w')  
    fval = open('val.txt', 'w')  
    for i  in list:  
        name = total_xml[i][:-4]+'\n'  
        if i in trainval:  
            ftrainval.write(name)  
            if i in train:  
                ftrain.write(name)  
            else:  
                fval.write(name)  
        else:  
            ftest.write(name)  
    ftrainval.close()  
    ftrain.close()  
    fval.close()  
    ftest .close()
    return 0 

if __name__ == '__main__':
    path_src = input('挑选图片文件的路径是：')
    path_label = input('挑选标记文件的路径是：')
    path_voc = input('VOC数据集存放位置：')
    save_voc = path_voc + '\VOCdevkit2007\VOC2007'
    Annotations_voc = save_voc + '\Annotations'
    ImageSets_voc = save_voc + '\ImageSets'
    JPEGImages_voc = save_voc + '\JPEGImages'
    Test_path = save_voc + '\Test'
    if not os.path.exists(save_voc):
        os.makedirs(save_voc)
    Choose_image(JPEGImages_voc, path_label, path_src, Test_path)
    Change_xml(Annotations_voc, path_label)
    Make_val(ImageSets_voc, Annotations_voc)