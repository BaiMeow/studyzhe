import time

import requests

# 在浙学手机号密码
account = 123456
passwd = ''

# 刷课速度,默认两倍速，想秒过的可以改成一个极大的数字
speed = 2

loginUrl = r'http://service.zjooc.cn/service/centro/api/auth/app/authorize'
coursesUrl = r'http://service.zjooc.cn/service/jxxt/api/app/course/student/course?publishStatus=3&pageNo=1&pageSize=10'
chapterUrl = r'http://service.zjooc.cn/service/jxxt/api/app/course/chapter/getStudentCourseChapters'
videoUrl = r'http://service.zjooc.cn/service/learningmonitor/api/learning/monitor/videoPlaying'
textUrl = r'http://service.zjooc.cn/service/learningmonitor/api/learning/monitor/finishTextChapter'

# 课程id
courseId = r''

headers = {}


def finish_video(chapter):
    length = chapter['vedioTimeLength']
    chapter_id = chapter['id']
    for i in range(int(length / (10 * speed))):
        r = requests.get(videoUrl, params={
            'chapterId': chapter_id,
            'playTime': i * 20,
            'percent': int(i * (10 * speed) / length * 100),
            'quitFlag': 0,
            'thisWatchTime': 0,
            'courseId': courseId
        }, headers=headers)
        if r.status_code != 200 or r.json()['success'] is False:
            raise Exception(r.json()['message'])
        print('%d%%' % int(i * (10 * speed) / length * 100))
        time.sleep(10)
    r = requests.get(videoUrl, params={
        'chapterId': chapter_id,
        'playTime': length,
        'percent': 100,
        'quitFlag': 1,
        'thisWatchTime': length,
        'courseId': courseId
    }, headers=headers)
    if r.status_code != 200 or r.json()['success'] is False:
        raise Exception(r.json()['message'])


def finish_text(chapter):
    chapter_id = chapter['id']
    r = requests.get(textUrl, params={
        'courseId': courseId,
        'chapterId': chapter_id
    }, headers=headers)
    if r.status_code != 200 or r.json()['success'] is False:
        raise Exception(r.json()['message'])


resp = requests.post(loginUrl, json={"login_name": account, "password": passwd, "type": 1})

if resp.status_code != 200:
    print('登陆失败')
    exit(0)

headers['openid'] = resp.json()['data']['loginResult']['openid']

# 去除下方代码注释可以在程序运行时打印出课程列表
# resp = requests.get(coursesUrl, headers=headers)
# for course in resp.json()['data']:
#     print('%s %s' % (course['courseName'],course['id']))
# exit(0)

resp = requests.get(chapterUrl, params={
    'courseId': courseId,
    'source': 1,
    'urlNeed': 1
}, headers=headers)

chapterList = []

for v in resp.json()['data']:
    for u in v['children']:
        chapterList.extend(u['children'])

for chapter in chapterList:
    print("开始学习%s" % chapter['name'])
    if chapter['learnStatus'] == 2:
        print("已学习，跳过")
        continue
    if chapter['resourceType'] == 1:
        try:
            finish_video(chapter)
        except Exception as err:
            print(err)
    elif chapter['resourceType'] == 3:
        try:
            finish_text(chapter)
        except Exception as err:
            print(err)
    print("学习完成")
