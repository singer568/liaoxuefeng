B = []


def move(n, a, b, c):
    if n == 1:
        buzhou = a+str(n)+'---->'+c+str(n)   #一个圆盘需要从A到C的操作步骤
        B.append(buzhou)   #向列表中添加操作步骤
        return
    else:
        move(n-1, a, c, b)  #将A柱n-1个盘移到B柱
        buzhou = a+str(n)+'---->'+c+str(n)   #将A柱的n个盘子移动到c柱操作步骤
        B.append(buzhou)
        move(1, a, b, c)   #将A柱上最后一个盘子移动到C柱子
        move(n-1, b, a, c)   #将过渡柱子B上n-1个圆盘B移动到目标柱子C


move(6, 'A', 'B', 'C')    #2**64-1,64次太大，这里用6个盘子
print('共需要操作' + str(len(B)) + '次', '操作过程为：', B)

