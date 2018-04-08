# -*- coding: utf-8 -*-

import json
import time
import simplejson

from django.http import HttpResponse
from django.http import HttpResponseForbidden
from django.http import HttpResponseBadRequest
from django.http import JsonResponse
from rest_framework.authtoken.models import Token

from lab1017.models import Course
from lab1017.models import Student
from lab1017.models import Teacher
from lab1017.models import Manager
from lab1017.models import TeacherCourse
from lab1017.models import Question
from lab1017.models import Login
from lab1017.models import TeacherCourseApply
from lab1017.models import TeacherNewCourseApply
from lab1017.models import ContractTeacherInfo
from lab1017.models import ContractCourseInfo
from lab1017.models import ContractTeacherCourseInfo

from HelloWorld.Common import AuthorizedTime
from HelloWorld.Common import tokenauth

# 数据库操作


def teacherinfoadd(request):
    dict = {}
    meta = {}
    dict["meta"] = meta
    try:
        if request.method == 'POST':
            reqbody = simplejson.loads(request.body)

            _requid = reqbody['uid']
            _reqtoken = reqbody['token']
            _txid = reqbody['Txid']

            teacher = reqbody['teacher']
            _id = teacher['teacher_id']
            _name = teacher['teacher_name']
            # _school = teacher['teacher_academy']
            _school = "信息与通信工程学院"
            _password = teacher['teacher_password_log']
            _uid = str(_id) + str(int(time.time()))

            if tokenauth(_requid, _reqtoken):

                if len(Teacher.objects.filter(tNo=_id)) == 0 and len(Login.objects.filter(account=_id)) == 0:
                    newteacher = Teacher(tNo=_id, tName=_name, tSchool=_school, LoginPassword=_password)
                    newteacher.save()

                    _type = "teacher"
                    newlogin = Login(uid=_uid, account=_id, accountType=_type, LoginPassword=_password,
                                     id=_id, password=_password, is_superuser=0, username=_id, first_name="blank",
                                     last_name="blank", email="null@null.com", is_staff=0, is_active=0,
                                     date_joined=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
                    newlogin.save()
                    newtx = ContractTeacherInfo(txid=_txid, times=0, tNo=_id, tName=_name)
                    newtx.save()

                    info = "Success"

                else:
                    info = "The teacher already exists"

            else:
                info = "NotAuthorized"

            # if time.time() - time.mktime(Token.objects.get(key=_reqtoken).created.timetuple()) > AuthorizedTime:
            #     Token.objects.filter(key=_reqtoken).delete()
            #     info = "NotAuthorized"
            #
            # elif len(Teacher.objects.filter(tNo=_id)) > 0 or len(Login.objects.filter(account=_id)) > 0:
            #     info = "The teacher already exists"
            #     # meta['code'] = "400"
            #     # meta['message'] = info
            #     # jsonr = simplejson.dumps(dict)
            #     # res = HttpResponseBadRequest(jsonr)
            #     # res.__setitem__('Access-Control-Allow-Origin', '*')
            #     # return res
            # else:
            #     newteacher = Teacher(tNo=_id, tName=_name, tSchool=_school,  LoginPassword=_password)
            #     newteacher.save()
            #
            #     _type = "teacher"
            #     # newlogin = Login(uid=_uid, account=_id, accountType=_type, LoginPassword=_password)
            #     newlogin = Login(uid=_uid, account=_id, accountType=_type, LoginPassword=_password,
            #                      id=_id, password=_password, is_superuser=0, username=_id, first_name="blank",
            #                      last_name="blank", email="null@null.com", is_staff=0, is_active=0,
            #                      date_joined=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
            #     newlogin.save()
            #
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


def adminteacherinfoquery(request):
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

            teacher_get = reqbody['teacher']
            _id = teacher_get['teacher_id']

            if tokenauth(_requid, _reqtoken):

                if len(Teacher.objects.filter(tNo=_id)) == 1:
                    teacher = Teacher.objects.get(tNo=_id)
                    data['teacher_id'] = _id
                    data['teacher_name'] = teacher.tName
                    data['teacher_academy'] = teacher.tSchool
                    data['teacher_password_log'] = teacher.LoginPassword
                    data['teacher_address'] = teacher.tAddress
                    data['teacher_password_unlock'] = teacher.tUnlockPassword
                    data['teacher_tel'] = teacher.tTelephone
                    # data['teacher_email'] = teacher.tEmail
                    info = "Success"
                else:
                    info = "Teacher not exist"

            else:
                info = "NotAuthorized"

            # if time.time() - time.mktime(Token.objects.get(key=_reqtoken).created.timetuple()) > AuthorizedTime:
            #     Token.objects.filter(key=_reqtoken).delete()
            #     info = "NotAuthorized"
            #
            # elif _id == "":
            #     info = "Missing parameter ID"
            #
            # elif len(Teacher.objects.filter(tNo=_id)) == 0:
            #     info = "Teacher not exist"
            #
            # else:
            #     teacher = Teacher.objects.get(tNo=_id)
            #     data['teacher_id'] = _id
            #     data['teacher_name'] = teacher.tName
            #     data['teacher_academy'] = teacher.tSchool
            #     data['teacher_password_log'] = teacher.LoginPassword
            #     data['teacher_address'] = teacher.tAddress
            #     data['teacher_password_unlock'] = teacher.tUnlockPassword
            #     data['teacher_tel'] = teacher.tTelephone
            #     # data['teacher_email'] = teacher.tEmail
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


def teacherinfomodify(request):
    dict = {}
    meta = {}
    dict["meta"] = meta
    try:
        if request.method == 'POST':
            reqbody = simplejson.loads(request.body)

            _requid = reqbody['uid']
            _reqtoken = reqbody['token']

            teacher = reqbody['teacher']
            _id = teacher['teacher_id']
            _name = teacher['teacher_name']
            # _school = teacher['teacher_academy']
            _school = "信息与通信工程学院"
            _password = teacher['teacher_password_log']
            _address = teacher['teacher_address']
            _unlockpassword = teacher['teacher_password_unlock']

            updateteacher = Teacher.objects.filter(tNo=_id)
            checkid = Login.objects.filter(account=_id)
            checkaddress = Login.objects.filter(address=_address)

            if tokenauth(_requid, _reqtoken):
                if len(checkid) == 1 and len(updateteacher) == 1:
                    if len(checkaddress) == 1 or (len(checkaddress) == 1 and Login.objects.get(account=_id).address == _address):
                        updateteacher.update(tName=_name, tSchool=_school, LoginPassword=_password, tAddress=_address,
                                             tUnlockPassword=_unlockpassword)
                        checkid.update(LoginPassword=_password, address=_address, unlockPassword=_unlockpassword)
                        info = "Success"
                    else:
                        info = "Address already exist"
                else:
                    info = "Teacher ID dose not exist"
            else:
                info = "NotAuthorized"

            # if time.time() - time.mktime(Token.objects.get(key=_reqtoken).created.timetuple()) > AuthorizedTime:
            #     Token.objects.filter(key=_reqtoken).delete()
            #     info = "NotAuthorized"
            #
            # elif len(checkid) == 0 or len(updateteacher) == 0:
            #     info = "Teacher ID dose not exist"
            #
            # elif len(checkaddress) > 0 and Login.objects.get(account=_id).address != _address:
            #     info = "Address already exist"
            #
            # else:
            #     updateteacher.update(tName=_name, tSchool=_school, LoginPassword=_password, tAddress=_address,
            #                          tUnlockPassword=_unlockpassword)
            #     checkid.update(LoginPassword=_password, address=_address, unlockPassword=_unlockpassword)
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


def adminteachercourseapplyquery(request):
    dict = {}
    meta = {}
    data = {}
    dict["meta"] = meta
    dict["data"] = data

    try:
        if request.method == "POST":
            reqbody = simplejson.loads(request.body)

            _requid = reqbody['uid']
            _reqtoken = reqbody['token']

            _page = int(reqbody['page'])
            _number = int(reqbody['number'])

            if tokenauth(_requid, _reqtoken):
                teachercourse_info = TeacherCourseApply.objects.all()
                teachernewcourse_info = TeacherNewCourseApply.objects.all()
                _count = 0
                temporary = {}
                content = {}
                for tci in teachercourse_info:
                    # single = {}
                    # single['new'] = "0"
                    # single['course_id'] = tci.cNo_id
                    # single['teacher_id'] = tci.tNo_id
                    # single['status'] = tci.status
                    # temporary[str(_count)] = single

                    temporary[str(_count)] = {}
                    temporary[str(_count)]['new'] = "0"
                    temporary[str(_count)]['course_id'] = tci.cNo_id
                    temporary[str(_count)]['teacher_id'] = tci.tNo_id
                    temporary[str(_count)]['status'] = tci.status
                    _count += 1

                for tnc in teachernewcourse_info:
                    temporary[str(_count)] = {}
                    temporary[str(_count)]['new'] = "1"
                    temporary[str(_count)]['course_id'] = str(tnc.ncacNo)
                    temporary[str(_count)]['course_name'] = tnc.ncacName
                    temporary[str(_count)]['credit'] = str(tnc.ncacCredit)
                    temporary[str(_count)]['academy'] = tnc.ncacMajor
                    temporary[str(_count)]['course_property'] = tnc.ncacNature
                    temporary[str(_count)]['grade'] = tnc.ncacGrade
                    temporary[str(_count)]['time'] = tnc.ncacTerm
                    temporary[str(_count)]['mark_element'] = tnc.ncacComposition
                    temporary[str(_count)]['teacher_id'] = str(tnc.ncatNo_id)
                    teacher_info = Teacher.objects.get(tNo=tnc.ncatNo_id)
                    temporary[str(_count)]['teacher_name'] = teacher_info.tName
                    temporary[str(_count)]['status'] = tnc.ncaStatus
                    _count += 1

                for t in range(0, len(temporary)):
                    if t >= _number * (_page - 1):
                        if t < _number * _page:
                            tt = {}
                            tt['new'] = temporary[str(t)]['new']
                            if temporary[str(t)]['new'] == "0":
                                _course_id = temporary[str(t)]['course_id']
                                _teacher_id = temporary[str(t)]['teacher_id']
                                course_info = Course.objects.get(cNo=_course_id)
                                teacher_info = Teacher.objects.get(tNo=_teacher_id)
                                tt['course_id'] = str(_course_id)
                                tt['course_name'] = course_info.cName
                                tt['credit'] = str(course_info.cCredit)
                                tt['academy'] = course_info.cMajor
                                tt['course_property'] = course_info.cNature
                                tt['grade'] = course_info.cGrade
                                tt['time'] = course_info.cTerm
                                tt['mark_element'] = course_info.cComposition
                                tt['teacher_id'] = str(_teacher_id)
                                tt['teacher_name'] = teacher_info.tName
                                tt['status'] = temporary[str(t)]['status']
                            else:
                                tt['course_id'] = temporary[str(t)]['course_id']
                                tt['course_name'] = temporary[str(t)]['course_name']
                                tt['credit'] = temporary[str(t)]['credit']
                                tt['academy'] = temporary[str(t)]['academy']
                                tt['course_property'] = temporary[str(t)]['course_property']
                                tt['grade'] = temporary[str(t)]['grade']
                                tt['time'] = temporary[str(t)]['time']
                                tt['mark_element'] = temporary[str(t)]['mark_element']
                                tt['teacher_id'] = temporary[str(t)]['teacher_id']
                                tt['teacher_name'] = temporary[str(t)]['teacher_name']
                                tt['status'] = temporary[str(t)]['status']
                            content[str(t % _number)] = tt

                data['content'] = content
                data['pages'] = len(temporary) // _number + 1
                info = "Success"
            else:
                info = "NotAuthorized"
            # if time.time() - time.mktime(Token.objects.get(key=_reqtoken).created.timetuple()) > AuthorizedTime:
            #     Token.objects.filter(key=_reqtoken).delete()
            #     info = "NotAuthorized"
            #
            # else:
            #     teachercourse_info = TeacherCourseApply.objects.all()
            #     teachernewcourse_info = TeacherNewCourseApply.objects.all()
            #     _count = 0
            #     temporary = {}
            #     content = {}
            #     for tci in teachercourse_info:
            #         # single = {}
            #         # single['new'] = "0"
            #         # single['course_id'] = tci.cNo_id
            #         # single['teacher_id'] = tci.tNo_id
            #         # single['status'] = tci.status
            #         # temporary[str(_count)] = single
            #
            #         temporary[str(_count)] = {}
            #         temporary[str(_count)]['new'] = "0"
            #         temporary[str(_count)]['course_id'] = tci.cNo_id
            #         temporary[str(_count)]['teacher_id'] = tci.tNo_id
            #         temporary[str(_count)]['status'] = tci.status
            #         _count += 1
            #
            #     for tnc in teachernewcourse_info:
            #         temporary[str(_count)] = {}
            #         temporary[str(_count)]['new'] = "1"
            #         temporary[str(_count)]['course_id'] = str(tnc.ncacNo)
            #         temporary[str(_count)]['course_name'] = tnc.ncacName
            #         temporary[str(_count)]['credit'] = str(tnc.ncacCredit)
            #         temporary[str(_count)]['academy'] = tnc.ncacMajor
            #         temporary[str(_count)]['course_property'] = tnc.ncacNature
            #         temporary[str(_count)]['grade'] = tnc.ncacGrade
            #         temporary[str(_count)]['time'] = tnc.ncacTerm
            #         temporary[str(_count)]['mark_element'] = tnc.ncacComposition
            #         temporary[str(_count)]['teacher_id'] = str(tnc.ncatNo_id)
            #         teacher_info = Teacher.objects.get(tNo=tnc.ncatNo_id)
            #         temporary[str(_count)]['teacher_name'] = teacher_info.tName
            #         temporary[str(_count)]['status'] = tnc.ncaStatus
            #         _count += 1
            #
            #     for t in range(0, len(temporary)):
            #         if t >= _number*(_page - 1):
            #             if t < _number*_page:
            #                 tt = {}
            #                 tt['new'] = temporary[str(t)]['new']
            #                 if temporary[str(t)]['new'] == "0":
            #                     _course_id = temporary[str(t)]['course_id']
            #                     _teacher_id = temporary[str(t)]['teacher_id']
            #                     course_info = Course.objects.get(cNo=_course_id)
            #                     teacher_info = Teacher.objects.get(tNo=_teacher_id)
            #                     tt['course_id'] = str(_course_id)
            #                     tt['course_name'] = course_info.cName
            #                     tt['credit'] = str(course_info.cCredit)
            #                     tt['academy'] = course_info.cMajor
            #                     tt['course_property'] = course_info.cNature
            #                     tt['grade'] = course_info.cGrade
            #                     tt['time'] = course_info.cTerm
            #                     tt['mark_element'] = course_info.cComposition
            #                     tt['teacher_id'] = str(_teacher_id)
            #                     tt['teacher_name'] = teacher_info.tName
            #                     tt['status'] = temporary[str(t)]['status']
            #                 else:
            #                     tt['course_id'] = temporary[str(t)]['course_id']
            #                     tt['course_name'] = temporary[str(t)]['course_name']
            #                     tt['credit'] = temporary[str(t)]['credit']
            #                     tt['academy'] = temporary[str(t)]['academy']
            #                     tt['course_property'] = temporary[str(t)]['course_property']
            #                     tt['grade'] = temporary[str(t)]['grade']
            #                     tt['time'] = temporary[str(t)]['time']
            #                     tt['mark_element'] = temporary[str(t)]['mark_element']
            #                     tt['teacher_id'] = temporary[str(t)]['teacher_id']
            #                     tt['teacher_name'] = temporary[str(t)]['teacher_name']
            #                     tt['status'] = temporary[str(t)]['status']
            #                 content[t] = tt
            #     data['content'] = content
            #     data['pages'] = len(temporary) // _number + 1
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


def teachercourseapplyapprove(request):
    dict = {}
    meta = {}
    dict["meta"] = meta
    try:
        if request.method == "POST":
            reqbody = simplejson.loads(request.body)

            _requid = reqbody['uid']
            _reqtoken = reqbody['token']
            _txid = reqbody['Txid']

            course_approve = reqbody['course_approve']
            _new = course_approve['new']
            course_id = course_approve['course_id']
            teacher_id = course_approve['teacher_id']
            _status = course_approve['status']

            if tokenauth(_requid, _reqtoken):
                if _status == "2":
                    if _new == "0":
                        if len(TeacherCourseApply.objects.filter(cNo_id=course_id, tNo_id=teacher_id, status="1")) == 1:
                            TeacherCourseApply.objects.filter(cNo_id=course_id, tNo_id=teacher_id,
                                                              status="1").update(status=_status)
                            newtc = TeacherCourse(cNo_id=course_id, tNo_id=teacher_id)
                            newtc.save()

                            course = Course.objects.get(cNo=course_id)
                            newtx = ContractCourseInfo(txid=_txid, times=0, cNo=course_id, cName=course.cName,
                                                       cCredit=course.cCredit, cNature=course.cNature,
                                                       cGrade=course.cGrade, cTerm=course.cTerm,
                                                       cComposition=course.cComposition)
                            newtx.save()

                            newtx2 = ContractTeacherCourseInfo(txid=_txid, times=0, cNo=course_id, tNo=teacher_id)
                            newtx2.save()

                            info = "Success"
                        else:
                            info = "Record not exist"
                    elif _new == "1":
                        if len(TeacherNewCourseApply.objects.filter(ncacNo=course_id, ncatNo_id=teacher_id,
                                                                    ncaStatus="1")) == 1:
                            if len(Course.objects.filter(cNo=course_id)) == 0:
                                TeacherNewCourseApply.objects.filter(ncacNo=course_id, ncatNo=teacher_id,
                                                                     ncaStatus="1").update(ncaStatus=_status)
                                tc_info = TeacherNewCourseApply.objects.get(ncacNo=course_id)
                                newcourse = Course(cNo=tc_info.ncacNo, cName=tc_info.ncacName,
                                                   cCredit=tc_info.ncacCredit,
                                                   cNature=tc_info.ncacNature, cNumber=tc_info.ncacNumber,
                                                   cMajor=tc_info.ncacMajor, cGrade=tc_info.ncacGrade,
                                                   cTerm=tc_info.ncacTerm,
                                                   cComposition=tc_info.ncacComposition,
                                                   cIntroduction=tc_info.ncacIntroduction)
                                newcourse.save()

                                newtc = TeacherCourse(cNo_id=course_id, tNo_id=teacher_id)
                                newtc.save()

                                newtx = ContractCourseInfo(txid=_txid, times=0, cNo=tc_info.ncacNo,
                                                           cName=tc_info.ncacName, cCredit=tc_info.ncacCredit,
                                                           cNature=tc_info.ncacNature, cGrade=tc_info.ncacGrade,
                                                           cTerm=tc_info.ncacTerm, cComposition=tc_info.ncacComposition)
                                newtx.save()

                                newtx2 = ContractTeacherCourseInfo(txid=_txid, times=0, cNo=course_id, tNo=teacher_id)
                                newtx2.save()

                                info = "Success"
                            else:
                                info = "Course ID exist"
                        else:
                            info = "Record not exist"
                        # elif len(Course.objects.filter(cNo=course_id)) == 0:
                        #     TeacherNewCourseApply.objects.filter(ncacNo=course_id, ncatNo=teacher_id,
                        #                                          ncaStatus="1").update(ncaStatus=_status)
                        #     tc_info = TeacherNewCourseApply.objects.get(ncacNo=course_id)
                        #     newcourse = Course(cNo=tc_info.ncacNo, cName=tc_info.ncacName, cCredit=tc_info.ncacCredit,
                        #                        cNature=tc_info.ncacNature, cNumber=tc_info.ncacNumber,
                        #                        cMajor=tc_info.ncacMajor, cGrade=tc_info.ncacGrade,
                        #                        cTerm=tc_info.ncacTerm,
                        #                        cComposition=tc_info.ncacComposition,
                        #                        cIntroduction=tc_info.ncacIntroduction)
                        #     newcourse.save()
                        #     newtc = TeacherCourse(cNo_id=course_id, tNo_id=teacher_id)
                        #     newtc.save()
                        #     info = "Success"
                        # else:
                        #     info = "Course ID exist"
                    else:
                        info = "Record not exist"
                elif _status == "3":
                    if _new == "0":
                        if len(TeacherCourseApply.objects.filter(cNo_id=course_id, tNo_id=teacher_id, status="1")) == 1:
                            TeacherCourseApply.objects.filter(cNo_id=course_id, tNo_id=teacher_id).update(status=_status)
                            info = "Success"
                        else:
                            info = "Record not exist"
                    elif _new == "1":
                        if len(TeacherCourseApply.objects.filter(cNo_id=course_id, tNo_id=teacher_id, status="1")) == 1:
                            TeacherNewCourseApply.objects.filter(ncacNo=course_id, ncatNo=teacher_id,
                                                                 status="1").update(ncaStatus=_status)
                            info = "Success"
                        else:
                            info = "Record not exist"
                    else:
                        info = "Record not exist"
                else:
                    info = "Wrong action"
                    # if _new == "0":
                    #     TeacherCourseApply.objects.filter(cNo_id=course_id, tNo_id=teacher_id,
                    #                                       status="1").update(status=_status)
                    #     info = "Success"
                    # elif _new == "1":
                    #     TeacherNewCourseApply.objects.filter(ncacNo=course_id, ncatNo=teacher_id,
                    #                                          ncaStatus="1").update(ncaStatus=_status)
                    #     info = "Success"
                    # else:
                    #     info = "Course ID exist"
            else:
                info = "NotAuthorized"

            # if time.time() - time.mktime(Token.objects.get(key=_reqtoken).created.timetuple()) > AuthorizedTime:
            #     Token.objects.filter(key=_reqtoken).delete()
            #     info = "NotAuthorized"
            #
            # elif _status == "2":
            #     if _new == "0":
            #         TeacherCourseApply.objects.filter(cNo_id=course_id, tNo_id=teacher_id,
            #                                           status="1").update(status=_status)
            #         newtc = TeacherCourse(cNo_id=course_id, tNo_id=teacher_id)
            #         newtc.save()
            #         info = "Success"
            #     elif _new == "1":
            #         if len(TeacherNewCourseApply.objects.filter(ncacNo=course_id, ncatNo_id=teacher_id)) == 0:
            #             info = "Record not exist"
            #         elif len(Course.objects.filter(cNo=course_id)) == 0:
            #             TeacherNewCourseApply.objects.filter(ncacNo=course_id, ncatNo=teacher_id,
            #                                                  ncaStatus="1").update(ncaStatus=_status)
            #             tc_info = TeacherNewCourseApply.objects.get(ncacNo=course_id)
            #             newcourse = Course(cNo=tc_info.ncacNo, cName=tc_info.ncacName, cCredit=tc_info.ncacCredit,
            #                                cNature=tc_info.ncacNature, cNumber=tc_info.ncacNumber,
            #                                cMajor=tc_info.ncacMajor, cGrade=tc_info.ncacGrade, cTerm=tc_info.ncacTerm,
            #                                cComposition=tc_info.ncacComposition, cIntroduction=tc_info.ncacIntroduction)
            #             newcourse.save()
            #             newtc = TeacherCourse(cNo_id=course_id, tNo_id=teacher_id)
            #             newtc.save()
            #             info = "Success"
            #         else:
            #             info = "Course ID exist"
            #     else:
            #         info = "Record not exist"
            # elif _status == "3":
            #     if _new == "0":
            #         TeacherCourseApply.objects.filter(cNo_id=course_id, tNo_id=teacher_id).update(status=_status)
            #         info = "Success"
            #     elif _new == "1":
            #         TeacherNewCourseApply.objects.filter(ncacNo=course_id, ncatNo=teacher_id).update(ncaStatus=_status)
            #         info = "Success"
            #     else:
            #         info = "Course ID exist"
            # else:
            #     if _new == "0":
            #         TeacherCourseApply.objects.filter(cNo_id=course_id, tNo_id=teacher_id,
            #                                           status="1").update(status=_status)
            #         info = "Success"
            #     elif _new == "1":
            #         TeacherNewCourseApply.objects.filter(ncacNo=course_id, ncatNo=teacher_id,
            #                                              ncaStatus="1").update(ncaStatus=_status)
            #         info = "Success"
            #     else:
            #         info = "Course ID exist"
        else:
            info = "Wrong request method."

    except Token.DoesNotExist:
        info = "NotAuthorized"

    except:
        import sys
        info = "%s || %s" % (sys.exc_info()[0], sys.exc_info()[1])
        # info = "Syntax Error Or Parameter Error"
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

