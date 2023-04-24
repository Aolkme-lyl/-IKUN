'''
项目名称：灌溉旱情识别
版本： v1.0
日期： 2023.04
作者： @liuyulou
详情： 针对2023年电赛灌溉组的旱情识别，仅对于此题目要求下的ABC三组的旱情识别。
'''

import sensor,lcd,time

###############################################################
Group_CX=[[40,100],[120,190],[210,280]]                 #三个组A、B、C对应的色块区域中心CX的范围，3组数对应三个组的范围
PXT=1000                                                #对应pixels_threshold的值，即识别到的最小像素阈值
draw_pixel=1000                                         #lcd画框的最小像素大小
PL=12                                                   #单个色块Y坐标上下减少的范围
##############################################################



Cl=['red','green','blue']
red_blob = None                                 ###
green_blob = None                                 ## 定义三个空的变量，用来盛放下面寻找到的色块的信息
blue_blob = None                                  #  以及定义一个色块组blobs_group
blobs_group = [red_blob,green_blob,blue_blob]   ### 分别存放寻找到的三种色块

A_area = [[],[]]                                   ###
B_area = [[],[]]                                #定义三个空变量盛放ABC三组的旱情的色块
C_area = [[],[]]                               #色块组
drought_area = [A_area,B_area,C_area]          ### 旱情色块总组（存放ABC三个区域）

A_group = ['']*6                                 ###
B_group = ['']*6                                       #定义三个变量盛放ABC三组每组6个的旱情
C_group = ['']*6                                       #色块组
drought_group = [A_group,B_group,C_group]          ### 旱情信息总组 （存放详细旱情）


#摄像头初始化
sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)                       #像素320*240=7680
sensor.set_vflip(1)                                     #后置模式，所见即所得

#lcd初始化
lcd.init()

clock=time.clock()

# 颜色识别阈值 (L Min, L Max, A Min, A Max, B Min, B Max) LAB模型
# 下面的阈值元组是用来识别 红、绿、蓝三种颜色，当然你也可以调整让识别变得更好。
thresholds = [(30, 100, 15, 127, 15, 127), # 红色阈值
              (51, 100, -64, -15, 1, 43), # 绿色阈值
              (71, 20, -23, 64, -128, -18)] # 蓝色阈值


def Find_MAX_MIN(group):        #找出？组下 通过最大Y和最小Y,以确定总范围
    Max_value=None
    Min_value=None
    max_b = None
    min_b = None
    #迭代每一个色块的CY
    for b in drought_area[group][1]:
        current_value=b[1]
        # 如果max_value是空的，或者当前值大于max_value，更新max_value
        if Max_value is None or current_value > Max_value:
            Max_value = current_value
            max_b=b
        # 如果min_value是空的，或者当前值小于min_value，更新min_value
        if Min_value is None or current_value < Min_value:
            Min_value = current_value
            min_b=b
    return max_b,min_b,Max_value+max_b[3],Min_value
def Group_drought_into_blocks():                    #将分为ABC三组每一组的色块分为6个块，针对每个区域的6个样本。
    color=[[0,0]for i in range(6)]
    lenth_group=None
    group=0
    while group<3:
        B_max,B_min,Y_max,Y_min=Find_MAX_MIN(group)
        lenth_unit_group=int((Y_max-Y_min)/6)
        for i in range(6):                              #确定一组每个色块的y值上下沿（阈值）
            color[i][0]=B_min[1]+lenth_unit_group*i+PL
            color[i][1]=B_min[1]+lenth_unit_group*(i+1)-PL

        k=0                                             #对每组色块进行分为6个：从组色块中提取一个判断是否属于第1~6
        for b in drought_area[group][1]:
            for j in range(6):
                if b[1]<color[j][0]<b[1]+b[3]:
                    drought_group[group][j]=drought_area[group][0][k]
            k+=1
        group+=1
def Find_group():#找色块
    a=0
    t=0
    while t<3:
        blobs_group[t] = img.find_blobs([thresholds[t]],pixels_threshold=PXT) # 0,1,2分别表示红，绿，蓝色;最小像素阈值PXT
        if len(blobs_group[t])>0:
            for b in blobs_group[t]:            # 色块分组,根据识别到色块的中心X坐标分为三组
                if Group_CX[0][0] < b[5] < Group_CX[0][1]:
                    drought_area[0][0].append(Cl[t])
                    drought_area[0][1].append(b)
                    a+=1
                elif Group_CX[1][0] < b[5] < Group_CX[1][1]:
                    drought_area[1][0].append(Cl[t])
                    drought_area[1][1].append(b)
                    a+=1
                elif Group_CX[2][0] < b[5] < Group_CX[2][1]:
                    drought_area[2][0].append(Cl[t])
                    drought_area[2][1].append(b)
                    a+=1

                if b[4]>draw_pixel:   #如果像素的大小大于？？打印（画）

                    img.draw_rectangle(b[0:4])     #画边框

        lcd.display(img)     #LCD显示图片
        t+=1
    if a>10:            #还需优化
        Group_drought_into_blocks()

while True:
    clock.tick()
    img=sensor.snapshot() #抓取照片
    Find_group()
    #print(drought_group)

    A_area = [[], []]  ###
    B_area = [[], []]  # 定义三个空变量盛放ABC三组的旱情的色块
    C_area = [[], []]  # 色块组
    drought_area = [A_area, B_area, C_area]  ### 旱情色块总组（存放ABC三个区域）

print('ok')




