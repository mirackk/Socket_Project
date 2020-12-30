# socket project设计文档

题目：
设计一个类http协议
1，服务器端保存一份学生名单，包括学号、照片、姓名等。名单的存放方式随意
2，客户端针对学生名单进行各类请求，如增加，删除，查看等，每种请求通过头部字段进行具体的要求。
3，加入图形界面

## 1，总体思路

和所有socket编程的总体思路一样。为了实现这个任务，需要有一个server（简称为ser）还有一个client（简称为cli）。需要在ser和cli之间不断通信，传递文字、照片等数据。通过这样的递交处理实现cli在ser上的增加、删除、查看。

文件存放模式：在电脑的文件夹中，ser对应sdata，cli对应cdata

功能实现：一共对应有三种功能，add，delete，view。每次cli向ser发送改关键字，ser识别，并用if语句进入应该执行的代码段。设计的时候认为，学生的学号是唯一的表示学生个体的候选键。

多线程：不同的cli.py，并且对应自己的一个cdata，可以同时连接到一个ser中

图形界面：tkinter简单实现

## 2，代码实现

具体实现的时候，是client和server同步写的，因为要一个send，一个recv，必须要对应，要不然发送和接收就有问题。

以下为具体代码加上解释。

### server
ser里面我只有两个部分，一个是主函数__main__，另一个是自定义的函数link_handler。在main里面主要是启动server，然后启动多线程地接收client。每一个link_handler可以对一个连接服务。
	 
如图，一套bind和listen创建一个server，然后在一个while true里面不停地接收client的连接。每次accept之后就可以start一个thread，进而调用link_handler
	 
建立好了连接，就会发送一条成功给client
	 
第一个功能 view就是查看学生信息，按照路径打开sdata，里面有一个学号.txt和学号.jpg，txt里面是学号和姓名，读出来然后send给client，照片也是一样的。如果没有这个学生就发送no，有就发送yes，先判定一下。
	 
delete删除就很简单，用一个shutil的包就可以了。同样发送是不是删除完成了给client
	 
add功能就比较长一点，首先用户发来一个学号，检查是否存在，存在就不能增加。不存在的话，接收用户发来的学号、姓名、照片，前面两个写入到txt，后一个保存为jpg。最后返回给client一个success 

### client
client这边也是一个main函数和一个自定义的mainfunc。使用了tkinter包做前端，每次点击前端的按钮就会调用这个mainfunc和server交互。
	 
在view功能里，接收server发来的num、num、jpg，保存到本地。然后弹出一个message显示学号姓名，还要用pillow包的img.show()显示图片。

查询的时候会先问是否存在该学生
	 
add和delete相对简单。delete就是只用看是不是删除成功了。
add也是发送学号、姓名、照片。发之前检查有无该学生。

最后一个是前端。如上图是前端的代码和界面，非常简洁。基本上是tkinter的使用，主要是解决一些疑难杂症就可以了。当然还有很多细致的前端地方没有调，但是功能实现了。

## 3，使用说明
在两个代码文件夹sockS和sockC分别打开powershell或者cmd
	 
然后如图运行两个.py的文件。注意，要先启动server再启动cli连接。先启动cli是无效的。
然后打开cli后就能看到前端了。
还有一点是上传照片只能输入绝对路径`C:\A\vscode\mycodes\py\socket\socketC\cdata\10\10.jpg`这种。反正指向某个jpg就好了
