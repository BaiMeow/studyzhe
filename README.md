## 在浙学刷课

市面上似乎并没有这种冷门平台的刷课脚本，

于是乎，就手搓了一个

需要修改代码中的`account`,`passwd`,`courseId`为账号密码课程id

关于课程id的获取，只需要去掉代码中的注释部分,像下面这种做
```python
# 去除下方代码注释可以在程序运行时打印出课程列表
resp = requests.get(coursesUrl, headers=headers)
for course in resp.json()['data']:
    print('%s %s' % (course['courseName'],course['id']))
    exit(0)
```
运行的时候就会打印所有课程及其id，左边课程名右边id，

把id记下来赋给courseId即可