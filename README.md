# Easy House

![Language](https://img.shields.io/badge/Language-Python-blue)
![flask](https://img.shields.io/badge/package-Flask-black)
![database](https://img.shields.io/badge/database-MySQL-green)
![license](https://img.shields.io/badge/License-MIT-red)

一个基于Flask的智能租房Web应用

A Flask based intelligent rental web application

---

正在新建文件夹...

---

## 如何使用

### 数据准备

既然是“智能租房”项目，那么显然需要房源数据，而为了方便，本项目使用的示例数据来源于网络。数据内容可以查看`database`文件夹下的`house.sql`文件，其中包含建库语句与许多的插入语句

首先在`MySQL`建立一个新的数据库，然后导入`house.sql`脚本，注意在执行脚本之前修改脚本中第一行的数据库名称为你自己建立的数据库名称，我这里的名字叫`easyhouse`

当脚本中的内容全部执行完毕之后，查看数据表中的内容，如果数据无误则数据准备完成

### 隐私保护

在连接数据库的代码中你会看到其中的URI中包含了你的数据库的用户名和密码，这显然不应该直接写在代码里，因此这里我借助`dotenv`以加载环境变量的方式对其进行保护，你可以在项目的根目录下新建`.env`文件并在其中写入你自己的数据库账户信息：

```python
DB_USERNAME=YOUR_USERNAME
DB_PASSWORD=YOUR_PASSWORD
DB_DATABASE=YOUR_DATABASE
```
