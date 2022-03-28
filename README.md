# 图数据挖掘系统（FMDVS）

配置环境：

- python：3.7.5


- MySQL



启动步骤：

1.创建虚拟环境，终端运行pip install -r requirements.txt，安装requirements.txt支持

2.打开主文件夹下的config文件，修改connect_mysql函数中的字符串，改为自己的数据库信息

3.运行db文件夹下的create_table.py。用途：此步在mysql中创建一个background数据库，建两个表，名字分别为NodeInfo和user

4.运行db文件夹下的cal.py。用途：此步进行计算，将计算出来的数据存储入background的NodeInfo表中

5.运行main.py文件。运行后控制台输出如下图

![image-20211028221621702](https://horacehhtbucket.oss-cn-guangzhou.aliyuncs.com/img/image-20211028221621702.png)

点击该网址，即可进入项目



## 项目页面介绍

### 登录注册页

需要先注册账号，进行登录。

![image-20211030145453010](https://horacehhtbucket.oss-cn-guangzhou.aliyuncs.com/img/image-20211030145453010.png)

输入账号密码，登录成功后即可进入主页

### 主页

![image-20211028222121918](https://horacehhtbucket.oss-cn-guangzhou.aliyuncs.com/img/image-20211028222121918.png)

下拉网页，可见三个数据统计图

![image-20211028222206986](https://horacehhtbucket.oss-cn-guangzhou.aliyuncs.com/img/image-20211028222206986.png)

![image-20211028222214835](https://horacehhtbucket.oss-cn-guangzhou.aliyuncs.com/img/image-20211028222214835.png)

![image-20211028222225299](https://horacehhtbucket.oss-cn-guangzhou.aliyuncs.com/img/image-20211028222225299.png)

### 学者个人页

![image-20211028222413501](https://horacehhtbucket.oss-cn-guangzhou.aliyuncs.com/img/image-20211028222413501.png)

通过点击节点信息栏下的个人主页或是搜索学者id可进入学者个人页

此处以7034为例

![image-20211028222512393](https://horacehhtbucket.oss-cn-guangzhou.aliyuncs.com/img/image-20211028222512393.png)

左侧展示该节点的信息，右侧展示以7034节点为中心点的图状数据

点击**预测**则可显示与7034节点可能有关联的节点（此结果通过算法计算得出）

![image-20211030145752908](https://horacehhtbucket.oss-cn-guangzhou.aliyuncs.com/img/image-20211030145752908.png)

