# -*- coding: utf-8 -*-

"""HelloWorld URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import url
from HelloWorld.views import hello

from HelloWorld.Common import login
from HelloWorld.Common import addresspasswordsent
from HelloWorld.Common import addresspasswordquery
from HelloWorld.Common import supermanager
from HelloWorld.Common import auth
from HelloWorld.test import get_balance

from HelloWorld.Admin_Student import studentinfoadd
from HelloWorld.Admin_Student import studentinfoquery
from HelloWorld.Admin_Student import studentinfomodify
from HelloWorld.test import exceltest

from HelloWorld.Admin_Teacher import teacherinfoadd
from HelloWorld.Admin_Teacher import adminteacherinfoquery
from HelloWorld.Admin_Teacher import teacherinfomodify
from HelloWorld.Admin_Teacher import adminteachercourseapplyquery
from HelloWorld.Admin_Teacher import teachercourseapplyapprove

from HelloWorld.Admin_Course import courseinfoadd
from HelloWorld.Admin_Course import courseinfoquery
from HelloWorld.Admin_Course import courseinfomodify

from HelloWorld.Admin_Manager import administratorinfoadd
from HelloWorld.Admin_Manager import administratorinfoquery
from HelloWorld.Admin_Manager import administratorinfomodify

from HelloWorld.Teacher import teacherinfoquery
from HelloWorld.Teacher import teachercoursequery
from HelloWorld.Teacher import teachercourseapplysubmit
from HelloWorld.Teacher import teachercourseapplyquery
from HelloWorld.Teacher import teachernewcourseapply
from HelloWorld.Teacher import teachermaterialsquery
from HelloWorld.Teacher import teachermaterialdelete
from HelloWorld.Teacher import teachermaterialadd
from HelloWorld.Teacher import teachercoursestudentquery
from HelloWorld.Teacher import teachersubmitmark

from HelloWorld.Student import stuinfoquery
# from HelloWorld.Student import stuinfomodify
from HelloWorld.Student import coursedetailQuery
from HelloWorld.Student import courseQuery
from HelloWorld.Student import courseSelect
from HelloWorld.Student import courseSelected

from HelloWorld.CheckTransactions import checkall

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^hello/$', hello),

    url(r'^start/$', supermanager),

    url(r'^user/login_control/', auth),

    url(r'^user/login/$', login),
    url(r'^user/addressunlock_password/sent/$', addresspasswordsent),
    url(r'^user/addressunlock_password/query/$', addresspasswordquery),

    url(r'^admin/student/info/add/$', studentinfoadd),
    url(r'^admin/student/info/query/$', studentinfoquery),
    url(r'^admin/student/info/modify/$', studentinfomodify),

    url(r'^admin/teacher/info/add/$', teacherinfoadd),
    url(r'^admin/teacher/info/query/$', adminteacherinfoquery),
    url(r'^admin/teacher/info/modify/$', teacherinfomodify),
    url(r'^admin/teacher/course/apply/query/$', adminteachercourseapplyquery),
    url(r'^admin/teacher/course/apply/approve/$', teachercourseapplyapprove),

    url(r'^admin/course/info/add/$', courseinfoadd),
    url(r'^admin/course/info/query/$', courseinfoquery),
    url(r'^admin/course/info/modify/$', courseinfomodify),

    url(r'^admin/administrator/info/add/$', administratorinfoadd),
    url(r'^admin/administrator/info/query/$', administratorinfoquery),
    url(r'^admin/administrator/info/modify/$', administratorinfomodify),

    url(r'^teacher/info/query/$', teacherinfoquery),
    url(r'^teacher/course/query/$', teachercoursequery),
    url(r'^teacher/courseapply/submit/$', teachercourseapplysubmit),
    url(r'^teacher/courseapply/query/$', teachercourseapplyquery),
    url(r'^teacher/course/add/$', teachernewcourseapply),
    url(r'^teacher/document/obtain/$', teachermaterialsquery),
    url(r'^teacher/document/delete/$', teachermaterialdelete),
    url(r'^teacher/document/add/$', teachermaterialadd),
    url(r'^teacher/studentlist/query/$', teachercoursestudentquery),
    url(r'^teacher/studentGrade/submit/$', teachersubmitmark),

    url(r'^user/info/query/$', stuinfoquery),
    # url(r'^user/info/update/$', stuinfomodify),
    url(r'^student/course/select/list/query/$', courseQuery),
    url(r'^student/course/detail/query/$', coursedetailQuery),
    url(r'^student/course/select/$', courseSelect),
    url(r'^student/course/selected/$', courseSelected),

    url(r'^test/', exceltest),
    url(r'^check/', checkall),

]


