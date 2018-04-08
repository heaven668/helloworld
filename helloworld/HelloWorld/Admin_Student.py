# -*- coding: utf-8 -*-

import json
import time
import simplejson

import web3

from django.http import HttpResponse
from django.http import HttpResponseForbidden
from django.http import HttpResponseBadRequest
from django.http import JsonResponse
from rest_framework.authtoken.models import Token

from web3 import Web3, HTTPProvider, TestRPCProvider
from web3.contract import ConciseContract

from lab1017.models import Course
from lab1017.models import Student
from lab1017.models import Teacher
from lab1017.models import Manager
from lab1017.models import TeacherCourse
from lab1017.models import Question
from lab1017.models import Login
from lab1017.models import ContractStudentInfo

from HelloWorld.Common import AuthorizedTime
from HelloWorld.Common import tokenauth

# 数据库操作


# def testdbadd(request):
#     test1 = TestModel(name='runoob')
#     test1.save()
#     return HttpResponse("<p>数据添加成功！</p>")
#
#
# def testdbjsonadd(request):
#     dict = {}
#     info = 'Data log save success'
#     name = ""
#     try:
#         if request.method == 'POST':
#             req = simplejson.loads(request.body)
#             name = req['name']
#             password = req['password']
#             test2 = TestModel(name=name, password=password)
#             test2.save()
#     except:
#         import sys
#         info = "%s || %s" % (sys.exc_info()[0], sys.exc_info()[1])
#
#     dict['message'] = info
#     dict['name'] = name
#     dict['password'] = password
#     jsonr = simplejson.dumps(dict)
#     return HttpResponse(jsonr)
#
#
# def login(request):
#     dict = {}
#     meta = {}
#     data = {}
#     dict["meta"] = meta
#     dict["data"] = data
#     try:
#         if request.method == 'POST':
#             req = simplejson.loads(request.body)
#             _account = req['account']
#             _password = req['password']
#             if _account == "" or _password == "":
#                 info = "Syntax Error Or Parameter Error"
#                 return HttpResponseForbidden(info)
#             check = Login.objects.get(account=_account)
#             if check.LoginPassword == _password:
#                 info = "Success"
#                 _accounttype = check.accountType
#                 _uid = check.id
#                 if _accounttype == "student":
#                     _name = Student.objects.get(sNo=_account).sName
#                 elif _accounttype == "teacher":
#                     _name = Teacher.objects.get(tNo=_account).tName
#                 elif _accounttype == "administrator":
#                     _name = Manager.objects.get(mNo=_account).mName
#                 else:
#                     info = "Wrong type. Please notify the administrator."
#             else:
#                 info = "Wrong password."
#         else:
#             info = "Wrong request method."
#     except:
#         # import sys
#         # info = "%s || %s" % (sys.exc_info()[0], sys.exc_info()[1])
#         info = "Syntax error Or parameter error."
#         meta['message'] = info
#         meta['code'] = "400"
#         jsonr = simplejson.dumps(dict)
#         res = HttpResponseBadRequest(jsonr)
#         res.__setitem__('Access-Control-Allow-Origin', '*')
#         return res
#
#     if info == "Success":
#         data['uid'] = _uid
#         data['name'] = _name
#         data['type'] = _accounttype
#         meta['code'] = "200"
#         meta['message'] = "ok"
#         res = JsonResponse(dict)
#         res.__setitem__('Access-Control-Allow-Origin', '*')
#         return res
#     else:
#         meta['code'] = "400"
#         meta['message'] = info
#         jsonr = simplejson.dumps(dict)
#         res = HttpResponseBadRequest(jsonr)
#         res.__setitem__('Access-Control-Allow-Origin', '*')
#         return res
#


def studentinfoadd(request):
    dict = {}
    meta = {}
    dict["meta"] = meta
    try:

        if request.method == 'POST':
            reqbody = simplejson.loads(request.body)

            _requid = reqbody['uid']
            _reqtoken = reqbody['token']
            _txid = reqbody['Txid']

            stu_info = reqbody['student']
            _id = stu_info['student_id']
            _name = stu_info['student_name']
            _gender = stu_info['student_gender']
            _class = stu_info['student_class']
            _major = stu_info['student_major']
            _school = stu_info['student_school']
            _grade = stu_info['student_grade']
            _password = stu_info['student_password_log']
            _uid = str(_id) + str(int(time.time()))

            if tokenauth(_requid, _reqtoken):

                if len(Student.objects.filter(sNo=_id)) == 0 and len(Login.objects.filter(account=_id)) == 0:
                    newstudent = Student(sNo=_id, sName=_name, sGender=_gender, sClass=_class, sMajor=_major,
                                         sSchool=_school, sGrade=_grade, LoginPassword=_password)
                    newstudent.save()
                    _type = "student"
                    newlogin = Login(uid=_uid, account=_id, accountType=_type, LoginPassword=_password,
                                     id=_id, password=_password, is_superuser=0, username=_id, first_name="blank",
                                     last_name="blank", email="null@null.com", is_staff=0, is_active=0,
                                     date_joined=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
                    newlogin.save()
                    newtx = ContractStudentInfo(txid=_txid, times=0, sNo=_id, sName=_name, sClass=_class)
                    newtx.save()
                    info = "Success"

                else:
                    info = "ID exist"

            else:
                info = "NotAuthorized"
            # if time.time() - time.mktime(Token.objects.get(key=_reqtoken).created.timetuple()) > AuthorizedTime:
            #     Token.objects.filter(key=_reqtoken).delete()
            #     info = "NotAuthorized"
            #
            # elif _id == "" or _name == "" or _gender == "" or _class == "" or _major == "" or _school == "" \
            #         or _grade == "" or _password == "":
            #     info = "Syntax error or parameter error"
            #
            # elif len(Student.objects.filter(sNo=_id)) > 0 or len(Login.objects.filter(account=_id)) > 0:
            #     info = "ID exist"
            # elif _gender != "male" and _gender != "female":
            #     info = "Wrong gender"
            # else:
            #     newstudent = Student(sNo=_id, sName=_name, sGender=_gender, sClass=_class, sMajor=_major,
            #                          sSchool=_school, sGrade=_grade, LoginPassword=_password)
            #     newstudent.save()
            #     _type = "student"
            #     newlogin = Login(uid=_uid, account=_id, accountType=_type, LoginPassword=_password,
            #                      id=_id, password=_password, is_superuser=0, username=_id, first_name="blank",
            #                      last_name="blank", email="null@null.com", is_staff=0, is_active=0,
            #                      date_joined=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
            #     newlogin.save()
            #     info = "Success"
        else:
            info = "Wrong request method."

    except Token.DoesNotExist:
        info = "NotAuthorized"

    except:
        import sys
        info = "%s || %s" % (sys.exc_info()[0], sys.exc_info()[1])
        # info = "Syntax Error Or Parameter Error"
        # dict['message'] = info
        meta['code'] = "400"
        meta['message'] = info
        jsonr = simplejson.dumps(dict)
        res = HttpResponseBadRequest(jsonr)
        res.__setitem__('Access-Control-Allow-Origin', '*')
        return res
    if info == "Success":
        meta['code'] = "200"
        meta['message'] = "ok"
        res = JsonResponse(dict)
        res.__setitem__('Access-Control-Allow-Origin', '*')
        return res
    else:
        meta['code'] = "400"
        meta['message'] = info
        jsonr = simplejson.dumps(dict)
        res = HttpResponseBadRequest(jsonr)
        res.__setitem__('Access-Control-Allow-Origin', '*')
        return res


def studentinfoquery(request):
    dict = {}
    meta = {}
    data = {}
    dict["meta"] = meta
    dict["data"] = data
    try:
        if request.method == 'POST':
            reqbody = simplejson.loads(request.body)
            _requid = reqbody['uid']
            _reqtoken = reqbody['token']
            stu = reqbody['student']
            _id = stu['student_id']

            if tokenauth(_requid, _reqtoken):

                if len(Student.objects.filter(sNo=_id)) == 1:
                    stu_info = Student.objects.get(sNo=_id)
                    data['student_id'] = _id
                    data['student_name'] = stu_info.sName
                    data['student_gender'] = stu_info.sGender
                    data['student_class'] = stu_info.sClass
                    data['student_major'] = stu_info.sMajor
                    data['student_school'] = stu_info.sSchool
                    data['student_grade'] = stu_info.sGrade
                    data['student_password_log'] = stu_info.LoginPassword
                    data['student_address'] = stu_info.sAddress
                    data['student_password_unlock'] = stu_info.sUnlockPassword
                    data['student_tel'] = stu_info.sTelephone
                    data['student_email'] = stu_info.sEmail
                    info = "Success"

                else:
                    info = "Student not exist"

            else:
                info = "NotAuthorized"

            # if time.time() - time.mktime(Token.objects.get(key=_reqtoken).created.timetuple()) > AuthorizedTime:
            #     Token.objects.filter(key=_reqtoken).delete()
            #     info = "NotAuthorized"
            #
            # elif _id == "":
            #     info = "Missing parameter ID"
            #
            # elif len(Student.objects.filter(sNo=_id)) == 0:
            #     info = "Student not exist"
            #
            # else:
            #     stu_info = Student.objects.get(sNo=_id)
            #     data['student_id'] = _id
            #     data['student_name'] = stu_info.sName
            #     data['student_gender'] = stu_info.sGender
            #     data['student_class'] = stu_info.sClass
            #     data['student_major'] = stu_info.sMajor
            #     data['student_school'] = stu_info.sSchool
            #     data['student_grade'] = stu_info.sGrade
            #     data['student_password_log'] = stu_info.LoginPassword
            #     data['student_address'] = stu_info.sAddress
            #     data['student_password_unlock'] = stu_info.sUnlockPassword
            #     data['student_tel'] = stu_info.sTelephone
            #     data['student_email'] = stu_info.sEmail
            #     info = "Success"
        else:
            info = "Wrong request method"

    except Token.DoesNotExist:
        info = "NotAuthorized"

    except:
        import sys
        info = "%s || %s" % (sys.exc_info()[0], sys.exc_info()[1])
        # info = "Syntax error or parameter error"
        meta['code'] = "400"
        meta['message'] = info
        dict['data'] = {}
        jsonr = simplejson.dumps(dict)
        res = HttpResponseBadRequest(jsonr)
        res.__setitem__('Access-Control-Allow-Origin', '*')
        return res

    if info == "Success":
        meta['code'] = "200"
        meta['message'] = "ok"
        res = JsonResponse(dict)
        res.__setitem__('Access-Control-Allow-Origin', '*')
        return res
    else:
        meta['code'] = "400"
        meta['message'] = info
        dict['data'] = {}
        jsonr = simplejson.dumps(dict)
        res = HttpResponseBadRequest(jsonr)
        res.__setitem__('Access-Control-Allow-Origin', '*')
        return res


def studentinfomodify(request):
    dict = {}
    meta = {}
    dict["meta"] = meta
    try:
        if request.method == 'POST':
            reqbody = simplejson.loads(request.body)
            _requid = reqbody['uid']
            _reqtoken = reqbody['token']
            stu_info = reqbody['student']
            _id = stu_info['student_id']
            _name = stu_info['student_name']
            _gender = stu_info['student_gender']
            _class = stu_info['student_class']
            _major = stu_info['student_major']
            _school = stu_info['student_school']
            _grade = stu_info['student_grade']
            _password = stu_info['student_password_log']
            _address = stu_info['student_address']
            _unlockpassword = stu_info['student_password_unlock']

            updatestudent = Student.objects.filter(sNo=_id)
            checkid = Login.objects.filter(account=_id)
            checkaddress = Login.objects.filter(address=_address)

            if tokenauth(_requid, _reqtoken):

                if len(checkid) == 1 and len(updatestudent) == 1:

                    if len(checkaddress) == 0 or (len(checkaddress) == 1 and Login.objects.get(account=_id).address == _address):
                        updatestudent.update(sName=_name, sGender=_gender, sClass=_class, sMajor=_major,
                                             sSchool=_school,
                                             sGrade=_grade, LoginPassword=_password, sAddress=_address,
                                             sUnlockPassword=_unlockpassword)
                        checkid.update(LoginPassword=_password, address=_address, unlockPassword=_unlockpassword)
                        info = "Success"

                    else:
                        info = "Address already exist"

                else:
                    info = "Student ID not exist"

            else:
                info = "NotAuthorized"

            # if time.time() - time.mktime(Token.objects.get(key=_reqtoken).created.timetuple()) > AuthorizedTime:
            #     Token.objects.filter(key=_reqtoken).delete()
            #     info = "NotAuthorized"
            #
            # elif len(checkid) == 0 or len(updatestudent) == 0:
            #     info = "Student ID not exist"
            #
            # elif len(checkaddress) > 0 and Login.objects.get(account=_id).address != _address:
            #     info = "Address already exist"
            #
            # else:
            #     updatestudent.update(sName=_name, sGender=_gender, sClass=_class,  sMajor=_major, sSchool=_school,
            #                          sGrade=_grade, LoginPassword=_password, sAddress=_address,
            #                          sUnlockPassword=_unlockpassword)
            #     checkid.update(LoginPassword=_password, address=_address, unlockPassword=_unlockpassword)
            #     info = "Success"
        else:
            info = "Wrong request method"

    except Token.DoesNotExist:
        info = "NotAuthorized"

    except:
        # import sys
        # info = "%s || %s" % (sys.exc_info()[0], sys.exc_info()[1])
        info = "Syntax error or parameter error"
        meta['code'] = "400"
        meta['message'] = info
        jsonr = simplejson.dumps(dict)
        res = HttpResponseBadRequest(jsonr)
        return res

    if info == "Success":
        meta['code'] = "200"
        meta['message'] = "ok"
        res = JsonResponse(dict)
        res.__setitem__('Access-Control-Allow-Origin', '*')
        return res
    else:
        meta['code'] = "400"
        meta['message'] = info
        jsonr = simplejson.dumps(dict)
        res = HttpResponseBadRequest(jsonr)
        res.__setitem__('Access-Control-Allow-Origin', '*')
        return res


# def studentinfobatchadd(request):
#

# def studentmarkquery(request):
#     dict = {}
#     meta = {}
#     data = {}
#     dict["meta"] = meta
#     dict["data"] = data
#     try:
#         if request.method == "POST":
#             reqbody = simplejson.loads(request.body)
#             stu = reqbody['student']
#             _id = stu['student_id']
#         else:
#             info = "Wrong request method"
#     except:


#
#
#
# def testdbget(request):
#     response = ""
#     response1 = ""
#
#     # 通过objects这个模型管理器的all()获得所有数据行，相当于SQL中的SELECT * FROM
#     list1 = TestModel.objects.all()
#
#     # filter相当于SQL中的WHERE，可设置条件过滤结果
#     response2 = TestModel.objects.filter(name='runoob')
#
#     # 获取单个对象
#     # response3 = TestModel.objects.get(name='runoob')
#
#     # 限制返回的数据 相当于 SQL 中的 OFFSET 0 LIMIT 2;
#     TestModel.objects.order_by('name')[0:2]
#
#     # 数据排序
#     TestModel.objects.order_by("id")
#
#     # 上面的方法可以连锁使用
#     TestModel.objects.filter(name="runoob").order_by("id")
#
#     # 输出所有数据
#     for var in list1:
#         response1 += var.name + " "
#     response = response1
#     return HttpResponse("<p>" + response + "</p>")
#
#
# def testdbupdate(request):
#     # 修改其中一个id=1的name字段，再save，相当于SQL中的UPDATE
#     test1 = TestModel.objects.get(id=2)
#     test1.name = 'Google'
#     test1.save()
#
#     # 另外一种方式
#     # Test.objects.filter(id=1).update(name='Google')
#
#     # 修改所有的列
#     # Test.objects.all().update(name='Google')
#
#     return HttpResponse("<p>修改成功</p>")
#
#
# def testdbdelete(request):
#     # 删除id=1的数据
#     test1 = TestModel.objects.get(name='Google')
#     test1.delete()
#
#     # 另外一种方式
#     # Test.objects.filter(id=1).delete()
#
#     # 删除所有数据
#     # Test.objects.all().delete()
#
#     return HttpResponse("<p>删除成功</p>")
