# app django echarts

django: https://docs.djangoproject.com/zh-hans/4.0/
https://juejin.cn/post/6844904085217509390
echarts: https://github.com/apache/echarts/blob/5.3.1/dist/echarts.js

## 创建项目

```bash
# pip3 install django

# 1 创建 django project
django-admin startproject app_django_echarts

# 2 部署服务
python manage.py runserver
# 0:8080 0.0.0.0:8080
# python manage.py runserver 0:8080

#打开 http://127.0.0.1:8000/

# 3 创建 django project 下的 app
python manage.py startapp trade


```

- views.py 写接口函数

```python
# polls/views.py
from django.http import HttpResponse


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")
```

- urls.py 绑定接口 url

```python
# polls/urls.py
from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
]
```

```python
# app_django/urls.py
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('polls/', include('polls.urls')),
    path('admin/', admin.site.urls),
]
```

## app trade

https://mp.weixin.qq.com/s?src=11&timestamp=1648615852&ver=3707&signature=I0y*eOYRVZ6fgeJnoKdack7fuLOtnS8V*FqWfncwmRKPQm-Jy2-*K8BE-nKM3YmO16*mBnoU21RGSaI1lKax1BX8*NjFrGKxkEE92GkpJnh0jjYnV38sEMrwjh2LGLYr&new=1

## 数据库与管理后台

- 设置数据库

- 创建模型

```python
from django.db import models


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
```

- 激活模型

```python
# settings.py
INSTALLED_APPS = [
    # 'polls.apps.PollsConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]
```

- 使 django 知道 polls, 为这些修改创建迁移文件

```bash

python manage.py makemigrations app_django

```

- 接收迁移文件的名字并返回它们的SQL语句

```
python manage.py sqlmigrate polls 0001
```

```sql
BEGIN;
--
-- Create model Question
--
CREATE TABLE "polls_question" (
    "id" serial NOT NULL PRIMARY KEY,
    "question_text" varchar(200) NOT NULL,
    "pub_date" timestamp with time zone NOT NULL
);
--
-- Create model Choice
--
CREATE TABLE "polls_choice" (
    "id" serial NOT NULL PRIMARY KEY,
    "choice_text" varchar(200) NOT NULL,
    "votes" integer NOT NULL,
    "question_id" integer NOT NULL
);
ALTER TABLE "polls_choice"
  ADD CONSTRAINT "polls_choice_question_id_c5b4b260_fk_polls_question_id"
    FOREIGN KEY ("question_id")
    REFERENCES "polls_question" ("id")
    DEFERRABLE INITIALLY DEFERRED;
CREATE INDEX "polls_choice_question_id_c5b4b260" ON "polls_choice" ("question_id");

COMMIT;
```

- 将这些改变更新到数据库中

```bash
python manage.py migrate
```

- play with api 

```bash
python manage.py shell
```

- django admin 

```bash

python manage.py createsuperuser

```

## 视图和模板

- views.py

```python
def detail(request, question_id):
    return HttpResponse("You're looking at question %s." % question_id)

def results(request, question_id):
    response = "You're looking at the results of question %s."
    return HttpResponse(response % question_id)

def vote(request, question_id):
    return HttpResponse("You're voting on question %s." % question_id)
```

- urls.py

```python
from django.urls import path

from . import views

urlpatterns = [
    # ex: /polls/
    path('', views.index, name='index'),
    # ex: /polls/5/
    path('<int:question_id>/', views.detail, name='detail'),
    # ex: /polls/5/results/
    path('<int:question_id>/results/', views.results, name='results'),
    # ex: /polls/5/vote/
    path('<int:question_id>/vote/', views.vote, name='vote'),
]
```

- app_django/templates/app_django/index.html

```python

{% if latest_question_list %}
    <ul>
    {% for question in latest_question_list %}
        <li><a href="/polls/{{ question.id }}/">{{ question.question_text }}</a></li>
    {% endfor %}
    </ul>
{% else %}
    <p>No polls are available.</p>
{% endif %}

```

- views & templates 

```python
from django.http import HttpResponse
from django.template import loader

from .models import Question


def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    template = loader.get_template('polls/index.html')
    context = {
        'latest_question_list': latest_question_list,
    }
    return HttpResponse(template.render(context, request))
```

- render()

```python

from django.shortcuts import render

from .models import Question

def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    context = {'latest_question_list': latest_question_list}
    return render(request, 'polls/index.html', context)

```

- 404

```python
from django.http import Http404
from django.shortcuts import render

from .models import Question
# ...
def detail(request, question_id):
    try:
        question = Question.objects.get(pk=question_id)
    except Question.DoesNotExist:
        raise Http404("Question does not exist")
    return render(request, 'polls/detail.html', {'question': question})
```

- 使用模板系统

```html
# polls/templates/polls/detail.html
<h1>{{ question.question_text }}</h1>
<ul>
{% for choice in question.choice_set.all %}
    <li>{{ choice.choice_text }}</li>
{% endfor %}
</ul>
```

## 表单与通用模板

## 测试

## 静态文件

## 自定义管理后台