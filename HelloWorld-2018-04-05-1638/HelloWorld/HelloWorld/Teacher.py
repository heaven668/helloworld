# -*- coding: utf-8 -*-

import json
import time
import simplejson
import math

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
from lab1017.models import CourseMaterial
from lab1017.models import StudentCourse
from lab1017.models import ContractMark

from HelloWorld.Common import AuthorizedTime
from HelloWorld.Common import tokenauth

# 数据库操作


def teacherinfoquery(request):
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

            if tokenauth(_requid, _reqtoken):
                _id = int(Login.objects.get(uid=_requid).account)

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
            # elif len(Login.objects.filter(uid=int(_requid))) == 1:
            #     _id = int(Login.objects.get(uid=int(_requid)).account)
            #
            #     if _id == "":
            #         info = "Missing parameter ID"
            #     elif len(Teacher.objects.filter(tNo=_id)) == 0:
            #         info = "Teacher not exist"
            #     else:
            #         teacher = Teacher.objects.get(tNo=_id)
            #         data['teacher_id'] = _id
            #         data['teacher_name'] = teacher.tName
            #         data['teacher_academy'] = teacher.tSchool
            #         data['teacher_password_log'] = teacher.LoginPassword
            #         data['teacher_address'] = teacher.tAddress
            #         data['teacher_password_unlock'] = teacher.tUnlockPassword
            #         data['teacher_tel'] = teacher.tTelephone
            #         # data['teacher_email'] = teacher.tEmail
            #         info = "Success"
            # else:
            #     info = "Teacher not exist"
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


def teachercoursequery(request):
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

            if tokenauth(_requid, _reqtoken):
                _id = int(Login.objects.get(uid=int(_requid)).account)

                if len(Teacher.objects.filter(tNo=_id)) == 1:
                    teachercourse = TeacherCourse.objects.filter(tNo=_id)
                    _count = 0
                    for tc in teachercourse:
                        c = {}
                        course_info = Course.objects.get(cNo=tc.cNo_id)
                        c['courseId'] = tc.cNo_id
                        c['name'] = course_info.cName
                        c['time'] = course_info.cTerm
                        c['type'] = course_info.cNature
                        c['score'] = course_info.cCredit
                        c['object'] = course_info.cMajor
                        c['description'] = course_info.cIntroduction
                        # c['grade'] = course_info.cGrade
                        # c['mark_element'] = course_info.cComposition
                        data[str(_count)] = c
                        _count += 1
                    info = "Success"
                else:
                    info = "Teacher not exist"
            else:
                info = "NotAuthorized"

            # if time.time() - time.mktime(Token.objects.get(key=_reqtoken).created.timetuple()) > AuthorizedTime:
            #     Token.objects.filter(key=_reqtoken).delete()
            #     info = "NotAuthorized"
            #
            # elif len(Login.objects.filter(uid=int(_requid))) == 1:
            #     _id = int(Login.objects.get(uid=int(_requid)).account)
            #
            #     if _requid == "":
            #         info = "Missing parameter ID"
            #     elif len(Teacher.objects.filter(tNo=_id)) == 0:
            #         info = "Teacher not exist"
            #     else:
            #         teachercourse = TeacherCourse.objects.filter(tNo=_id)
            #         _count = 0
            #         for tc in teachercourse:
            #             c = {}
            #             course_info = Course.objects.get(cNo=tc.cNo_id)
            #             c['courseId'] = tc.cNo_id
            #             c['name'] = course_info.cName
            #             c['time'] = course_info.cTerm
            #             c['type'] = course_info.cNature
            #             c['score'] = course_info.cCredit
            #             c['object'] = course_info.cMajor
            #             c['description'] = course_info.cIntroduction
            #             # c['grade'] = course_info.cGrade
            #             # c['mark_element'] = course_info.cComposition
            #             data[str(_count)] = c
            #             _count += 1
            #         info = "Success"
            # else:
            #     info = "Teacher not exist"
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


def teachercourseapplysubmit(request):
    dict = {}
    meta = {}
    dict["meta"] = meta
    try:
        if request.method == 'POST':
            reqbody = simplejson.loads(request.body)

            _requid = reqbody['uid']
            _reqtoken = reqbody['token']

            course_id = int(reqbody['courseId'])

            if tokenauth(_requid, _reqtoken):
                teacher_id = int(Login.objects.get(uid=int(_requid)).account)

                if len(Teacher.objects.filter(tNo=teacher_id)) == 1:

                    if len(TeacherCourse.objects.filter(cNo=course_id, tNo=teacher_id)) == 0:

                        if len(TeacherCourseApply.objects.filter(cNo=course_id, tNo=teacher_id)) == 0:
                            newapplication = TeacherCourseApply(cNo_id=course_id, tNo_id=teacher_id, status="1")
                            newapplication.save()
                            info = "Success"

                        else:
                            if TeacherCourseApply.objects.get(cNo=course_id, tNo=teacher_id).status == "1":
                                info = "You have already submitted the application"

                            elif TeacherCourseApply.objects.get(cNo=course_id, tNo=teacher_id).status == "2":
                                info = "You are already the teacher of this course"

                            else:
                                # newapplication = TeacherCourseApply(cNo_id=course_id, tNo_id=teacher_id, status="1")
                                # newapplication.save()
                                TeacherCourseApply.objects.filter(cNo_id=course_id, tNo_id=teacher_id,
                                                                  status="3").update(status="1")
                                info = "Success"

                        #     if len(TeacherCourseApply.objects.filter(cNo=course_id, tNo=teacher_id, status="2")) == 0:
                        #         newapplication = TeacherCourseApply(cNo_id=course_id, tNo_id=teacher_id, status="1")
                        #         newapplication.save()
                        #         info = "Success"
                        #     else:
                        #         info = "You are already the teacher of this course"
                        #
                        # else:
                        #     info = "You have already submitted the application"
                    else:
                        info = "You are already the teacher of this course"

                else:
                    info = "Teacher not exist"

            else:
                info = "NotAuthorized"

            # if time.time() - time.mktime(Token.objects.get(key=_reqtoken).created.timetuple()) > AuthorizedTime:
            #     Token.objects.filter(key=_reqtoken).delete()
            #     info = "NotAuthorized"
            #
            # elif len(Login.objects.filter(uid=int(_requid))) == 1:
            #     teacher_id = int(Login.objects.get(uid=int(_requid)).account)
            #
            #     if _requid == "":
            #         info = "Missing parameter ID"
            #     elif len(Teacher.objects.filter(tNo=teacher_id)) == 0:
            #         info = "Teacher not exist"
            #     elif len(TeacherCourse.objects.filter(cNo=course_id, tNo=teacher_id)) != 0:
            #         info = "You are already the teacher of this course"
            #     elif len(TeacherCourseApply.objects.filter(cNo=course_id, tNo=teacher_id, status="1")) != 0:
            #         info = "You have already submitted the application"
            #     else:
            #         newapplication = TeacherCourseApply(cNo_id=course_id, tNo_id=teacher_id, status="1")
            #         newapplication.save()
            #         info = "Success"
            # else:
            #     info = "Teacher not exist"
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


def teachercourseapplyquery(request):
    dict = {}
    meta = {}
    data = {}
    dict["meta"] = meta
    dict["data"] = data
    content = {}
    data['content'] = content
    temporary = {}
    try:
        if request.method == 'POST':
            reqbody = simplejson.loads(request.body)

            _requid = reqbody['uid']
            _reqtoken = reqbody['token']
            _page = int(reqbody['page'])
            _number = int(reqbody['number'])

            if tokenauth(_requid, _reqtoken):
                _id = int(Login.objects.get(uid=_requid).account)

                if len(Teacher.objects.filter(tNo=_id)) == 1:
                    course = Course.objects.all()
                    data['pages'] = math.ceil(float(len(course) / _number))
                    _count = 0
                    for course_info in course:
                        c = {}
                        c['courseId'] = str(course_info.cNo)
                        c['name'] = course_info.cName
                        c['time'] = course_info.cTerm
                        c['type'] = course_info.cNature
                        c['score'] = str(course_info.cCredit)
                        c['object'] = course_info.cMajor
                        c['description'] = course_info.cIntroduction
                        # tc = TeacherCourse.objects.filter(cNo=course_info.cNo, tNo=_id)
                        # tca = TeacherCourseApply.objects.filter(cNo=course_info.cNo, tNo=_id)
                        # c['status'] = "1"
                        if len(TeacherCourse.objects.filter(cNo=course_info.cNo, tNo=_id)) == 0:
                            if len(TeacherCourseApply.objects.filter(cNo=course_info.cNo, tNo=_id)) == 0:
                                c['status'] = "0"
                            else:
                                c['status'] = TeacherCourseApply.objects.get(cNo=course_info.cNo, tNo=_id).status
                                # for tcas in tca:
                                #     c['status'] = tcas.status
                                # if tcas.status == "1":
                                #     c['status'] = "2"
                                #     break
                        else:
                            c['status'] = "2"
                        # c['grade'] = course_info.cGrade
                        # c['mark_element'] = course_info.cComposition
                        temporary[str(_count)] = c
                        _count += 1

                    for t in range(0, len(temporary)):
                        if t >= _number * (_page - 1):
                            if t < _number * _page:
                                content[str(t)] = temporary[str(t)]

                    info = "Success"
                    data['content'] = content
                else:
                    info = "Teacher not exist"

            else:
                info = "NotAuthorized"

            # if time.time() - time.mktime(Token.objects.get(key=_reqtoken).created.timetuple()) > AuthorizedTime:
            #     Token.objects.filter(key=_reqtoken).delete()
            #     info = "NotAuthorized"
            #
            # elif len(Login.objects.filter(uid=int(_requid))) == 1:
            #     _id = int(Login.objects.get(uid=int(_requid)).account)
            #
            #     _page = int(reqbody['page'])
            #     _number = int(reqbody['number'])
            #     if _requid == "":
            #         info = "Missing parameter ID"
            #     elif len(Teacher.objects.filter(tNo=_id)) == 0:
            #         info = "Teacher not exist"
            #     else:
            #         course = Course.objects.all()
            #         data['pages'] = math.ceil(float(len(course) / _number))
            #         _count = 0
            #         for course_info in course:
            #             c = {}
            #             c['courseId'] = str(course_info.cNo)
            #             c['name'] = course_info.cName
            #             c['time'] = course_info.cTerm
            #             c['type'] = course_info.cNature
            #             c['score'] = str(course_info.cCredit)
            #             c['object'] = course_info.cMajor
            #             c['description'] = course_info.cIntroduction
            #             tc = TeacherCourse.objects.filter(cNo=course_info.cNo, tNo=_id)
            #             tca = TeacherCourseApply.objects.filter(cNo=course_info.cNo, tNo=_id)
            #             c['status'] = "1"
            #             if len(tc) == 0:
            #                 if len(tca) == 0:
            #                     c['status'] = "1"
            #                 else:
            #                     for tcas in tca:
            #                         if tcas.status == "1":
            #                             c['status'] = "2"
            #                             break
            #             else:
            #                 c['status'] = "3"
            #             # c['grade'] = course_info.cGrade
            #             # c['mark_element'] = course_info.cComposition
            #             temporary[str(_count)] = c
            #             _count += 1
            #
            #         for t in range(0, len(temporary)):
            #             if t >= _number * (_page - 1):
            #                 if t < _number * _page:
            #                     content[str(t)] = temporary[str(t)]
            #
            #         info = "Success"
            #         data['content'] = content
            # else:
            #     info = "Teacher not exist"
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


def teachernewcourseapply(request):
    dict = {}
    meta = {}
    dict["meta"] = meta
    try:
        if request.method == 'POST':
            reqbody = simplejson.loads(request.body)

            _requid = reqbody['uid']
            _reqtoken = reqbody['token']
            _newcourseinfo = reqbody['newCourseInfo']

            if tokenauth(_requid, _reqtoken):
                teacher_id = int(Login.objects.get(uid=_requid).account)

                if len(Teacher.objects.filter(tNo=teacher_id)) == 1:

                    if len(Course.objects.filter(cNo=_newcourseinfo['courseId'])) == 0:
                        tnc = TeacherNewCourseApply(ncacNo=_newcourseinfo['courseId'], ncatNo_id=teacher_id,
                                                    ncacName=_newcourseinfo['name'], ncacCredit=_newcourseinfo['score'],
                                                    ncacNature=_newcourseinfo['course_property'],
                                                    ncacMajor=_newcourseinfo['object'],
                                                    ncacGrade=_newcourseinfo['grade'],
                                                    ncacTerm=_newcourseinfo['time'], ncacNumber=200,
                                                    ncacComposition=_newcourseinfo['mark_element'],
                                                    ncacIntroduction=_newcourseinfo['introduction'], ncaStatus="1")
                        tnc.save()
                        info = "Success"
                    else:
                        info = "CourseID already exist"

                else:
                    info = "Teacher not exist"

            else:
                info = "NotAuthorized"

            # if time.time() - time.mktime(Token.objects.get(key=_reqtoken).created.timetuple()) > AuthorizedTime:
            #     Token.objects.filter(key=_reqtoken).delete()
            #     info = "NotAuthorized"
            #
            # elif len(Login.objects.filter(uid=int(_requid))) == 1:
            #     teacher_id = int(Login.objects.get(uid=int(_requid)).account)
            #
            #     if _requid == "":
            #         info = "Missing parameter ID"
            #     elif len(Teacher.objects.filter(tNo=teacher_id)) == 0:
            #         info = "Teacher not exist"
            #     elif len(Course.objects.filter(cNo=_newcourseinfo['courseId'])) != 0:
            #         info = "CourseID already exist"
            #     else:
            #         tnc = TeacherNewCourseApply(ncacNo=_newcourseinfo['courseId'], ncatNo_id=teacher_id,
            #                                     ncacName=_newcourseinfo['name'], ncacCredit=_newcourseinfo['score'],
            #                                     ncacNature=_newcourseinfo['course_property'],
            #                                     ncacMajor=_newcourseinfo['object'], ncacGrade=_newcourseinfo['grade'],
            #                                     ncacTerm=_newcourseinfo['time'], ncacNumber=200,
            #                                     ncacComposition=_newcourseinfo['mark_element'],
            #                                     ncacIntroduction=_newcourseinfo['introduction'], ncaStatus="1")
            #         tnc.save()
            #         info = "Success"
            # else:
            #     info = "Teacher not exist"
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


def teachermaterialadd(request):
    dict = {}
    meta = {}
    dict["meta"] = meta
    try:
        if request.method == 'POST':
            reqbody = simplejson.loads(request.body)

            _requid = reqbody['uid']
            _reqtoken = reqbody['token']

            course_id = int(reqbody['courseId'])
            _file_hash = reqbody['file_hash']
            _file_name = reqbody['file_name']
            _type = reqbody['type']
            _size = reqbody['size']
            _time = reqbody['time']

            if tokenauth(_requid, _reqtoken):
                teacher_id = int(Login.objects.get(uid=int(_requid)).account)

                if len(Teacher.objects.filter(tNo=teacher_id)) == 1:

                    if len(CourseMaterial.objects.filter(cNo_id=course_id, cMaterialsHash=_file_hash)) == 0:
                        newm = CourseMaterial(cNo_id=course_id, cMaterialsHash=_file_hash,
                                              cMaterialsName=_file_name, cMaterialsType=_type,
                                              cMaterialsSize=_size, cMaterialsTime=_time)
                        newm.save()
                        info = "Success"
                    else:
                        info = "File already exist"

                else:
                    info = "Teacher not exist"
            else:
                info = "NotAuthorized"

            # if time.time() - time.mktime(Token.objects.get(key=_reqtoken).created.timetuple()) > AuthorizedTime:
            #     Token.objects.filter(key=_reqtoken).delete()
            #     info = "NotAuthorized"
            #
            # elif len(Login.objects.filter(uid=int(_requid))) == 1:
            #     teacher_id = int(Login.objects.get(uid=int(_requid)).account)
            #
            #     if _requid == "" or course_id == "":
            #         info = "Missing parameter"
            #     elif len(Teacher.objects.filter(tNo=teacher_id)) == 0:
            #         info = "Teacher not exist"
            #     elif len(CourseMaterial.objects.filter(cNo_id=course_id, cMaterialsHash=reqbody['documentId'])) > 0:
            #         info = "Document already exist"
            #     else:
            #         newm = CourseMaterial(cNo_id=course_id, cMaterialsHash=reqbody['documentId'],
            #                               cMaterialsName=reqbody['name'], cMaterialsType=reqbody['type'],
            #                               cMaterialsSize=reqbody['size'], cMaterialsTime=reqbody['time'])
            #         newm.save()
            #         info = "Success"
            # else:
            #     info = "Teacher not exist"
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


def teachermaterialsquery(request):
    dict = {}
    meta = {}
    data = {}
    dict["meta"] = meta
    dict["data"] = data
    content = {}
    try:
        if request.method == 'POST':
            reqbody = simplejson.loads(request.body)

            _requid = reqbody['uid']
            _reqtoken = reqbody['token']

            _page = int(reqbody['page'])
            _number = int(reqbody['number'])
            course_id = reqbody['courseId']

            if tokenauth(_requid, _reqtoken):
                teacher_id = int(Login.objects.get(uid=_requid).account)

                if len(Teacher.objects.filter(tNo=teacher_id)) == 1:
                    material = CourseMaterial.objects.filter(cNo_id=course_id)
                    data['pages'] = math.ceil(len(material) / _number)
                    if len(material) > 0:
                        _count = 0
                        temporary = {}
                        for m in material:
                            mt = {}
                            mt['name'] = m.cMaterialsName
                            mt['time'] = m.cMaterialsTime
                            mt['documentId'] = m.cMaterialsHash
                            mt['type'] = m.cMaterialsType
                            mt['size'] = m.cMaterialsSize
                            temporary[str(_count)] = mt
                            _count += 1

                        for c in range(0, len(material)):
                            if c >= _number * (_page - 1):
                                if c < _number * _page:
                                    content[str(c)] = temporary[str(c)]
                    else:
                        content = {}
                    data['content'] = content
                    info = "Success"
                else:
                    info = "Teacher not exist"
            else:
                info = "NotAuthorized"

            # if time.time() - time.mktime(Token.objects.get(key=_reqtoken).created.timetuple()) > AuthorizedTime:
            #     Token.objects.filter(key=_reqtoken).delete()
            #     info = "NotAuthorized"
            #
            # elif len(Login.objects.filter(uid=int(_requid))) == 1:
            #     _id = int(Login.objects.get(uid=int(_requid)).account)
            #
            #     if _requid == "" or course_id == "":
            #         info = "Missing parameter"
            #     elif len(Teacher.objects.filter(tNo=teacher_id)) == 0:
            #         info = "Teacher not exist"
            #     elif len(CourseMaterial.objects.filter(cNo_id=course_id)) == 0:
            #         info = "No materials"
            #     else:
            #         material = CourseMaterial.objects.filter(cNo_id=course_id)
            #         data['pages'] = math.ceil(len(material) / _number)
            #         _count = 0
            #         temporary = {}
            #         for m in material:
            #             mt = {}
            #             mt['name'] = m.cMaterialsName
            #             mt['time'] = m.cMaterialsTime
            #             mt['documentId'] = m.cMaterialsHash
            #             mt['type'] = m.cMaterialsType
            #             mt['size'] = m.cMaterialsSize
            #             temporary[str(_count)] = mt
            #             _count += 1
            #
            #         for c in range(0, len(material)):
            #             if c >= _number * (_page - 1):
            #                 if c < _number * _page:
            #                     content[str(c)] = temporary[str(c)]
            #         data['content'] = content
            #         info = "Success"
            # else:
            #     info = "Teacher not exist"
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


def teachermaterialdelete(request):
    dict = {}
    meta = {}
    dict["meta"] = meta
    try:
        if request.method == 'POST':
            reqbody = simplejson.loads(request.body)

            _requid = reqbody['uid']
            _reqtoken = reqbody['token']
            _file_hash = reqbody['file_hash']
            course_id = int(reqbody['courseId'])

            if tokenauth(_requid, _reqtoken):
                teacher_id = int(Login.objects.get(uid=_requid).account)

                if len(Teacher.objects.filter(tNo=teacher_id)) == 1:

                    if len(CourseMaterial.objects.filter(cNo_id=course_id, cMaterialsHash=_file_hash)) == 1:
                        mdelete = CourseMaterial.objects.get(cNo_id=course_id, cMaterialsHash=_file_hash)
                        mdelete.delete()
                        info = "Success"
                    else:
                        info = "File not exist"

                else:
                    info = "Teacher not exist"

            else:
                info = "NotAuthorized"

            # if time.time() - time.mktime(Token.objects.get(key=_reqtoken).created.timetuple()) > AuthorizedTime:
            #     Token.objects.filter(key=_reqtoken).delete()
            #     info = "NotAuthorized"
            #
            # elif len(Login.objects.filter(uid=int(_requid))) == 1:
            #     teacher_id = int(Login.objects.get(uid=int(_requid)).account)
            #     _hash = reqbody['documentId']
            #     if _requid == "":
            #         info = "Missing parameter ID"
            #     elif len(Teacher.objects.filter(tNo=teacher_id)) == 0:
            #         info = "Teacher not exist"
            #     elif len(CourseMaterial.objects.filter(cNo_id=course_id, cMaterialsHash=_hash)) == 0:
            #         info = "Document not exist"
            #     else:
            #         mdelete = CourseMaterial.objects.get(cNo_id=course_id, cMaterialsHash=_hash)
            #         mdelete.delete()
            #         info = "Success"
            # else:
            #     info = "Teacher not exist"
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


def teachercoursestudentquery(request):
    dict = {}
    meta = {}
    data = {}
    dict["meta"] = meta
    dict["data"] = data
    content = {}
    try:
        if request.method == 'POST':
            reqbody = simplejson.loads(request.body)

            _requid = reqbody['uid']
            _reqtoken = reqbody['token']

            _course_id = reqbody['courseId']
            _page = int(reqbody['page'])
            _number = int(reqbody['number'])

            if tokenauth(_requid, _reqtoken):
                teacher_id = int(Login.objects.get(uid=int(_requid)).account)

                if len(Teacher.objects.filter(tNo=teacher_id)) == 1:

                    if len(Course.objects.filter(cNo=_course_id)) == 1:

                        if len(TeacherCourse.objects.filter(tNo_id=teacher_id, cNo_id=_course_id)) == 1:
                            students = StudentCourse.objects.filter(cNo_id=_course_id, status=1)
                            data['pages'] = math.ceil(float(len(students) / _number))
                            if len(students) > 0:
                                _count = 0
                                temporary = {}
                                for s in students:
                                    st = {}
                                    st['name'] = Student.objects.get(sNo=s.sNo_id).sName
                                    st['studentId'] = s.sNo_id
                                    temporary[str(_count)] = st
                                    _count += 1

                                for c in range(0, len(students)):
                                    if c >= _number * (_page - 1):
                                        if c < _number * _page:
                                            content[str(c)] = temporary[str(c)]

                            else:
                                content = {}

                            data['content'] = content
                            info = "Success"
                        else:
                            info = "You are not the teacher of this course"
                    else:
                        info = "Course not exist"
                else:
                    info = "Teacher not exist"

            else:
                info = "NotAuthorized"

            # if time.time() - time.mktime(Token.objects.get(key=_reqtoken).created.timetuple()) > AuthorizedTime:
            #     Token.objects.filter(key=_reqtoken).delete()
            #     info = "NotAuthorized"
            #
            # elif len(Login.objects.filter(uid=int(_requid))) == 1:
            #     teacher_id = int(Login.objects.get(uid=int(_requid)).account)
            #
            #     if _requid == "":
            #         info = "Missing parameter ID"
            #     elif len(Teacher.objects.filter(tNo=teacher_id)) == 0:
            #         info = "Teacher not exist"
            #     elif len(Course.objects.filter(cNo=_course_id)) == 0:
            #         info = "Course not exist"
            #     elif len(TeacherCourse.objects.filter(tNo_id=teacher_id, cNo_id=_course_id)) == 0:
            #         info = "You are not the teacher of this course"
            #     else:
            #         students = StudentCourse.objects.filter(cNo_id=_course_id, status=1)
            #         data['pages'] = math.ceil(float(len(students) / _number))
            #         _count = 0
            #         temporary = {}
            #         for s in students:
            #             st = {}
            #             st['name'] = Student.objects.get(sNo=s.sNo_id).sName
            #             st['studentId'] = s.sNo_id
            #             temporary[str(_count)] = st
            #             _count += 1
            #
            #         for c in range(0, len(students)):
            #             if c >= _number * (_page - 1):
            #                 if c < _number * _page:
            #                     content[str(c)] = temporary[str(c)]
            #         data['content'] = content
            #         info = "Success"
            # else:
            #     info = "Teacher not exist"
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


def teachersubmitmark(request):
    dict = {}
    meta = {}
    dict["meta"] = meta
    try:
        if request.method == "POST":
            reqbody = simplejson.loads(request.body)
            _uid = reqbody['uid']
            _txid = reqbody['Txid']
            _token = reqbody['token']
            _mark = reqbody['studentGrade']
            _cid = reqbody['courseId']
            _sid = reqbody['studentId']

            if tokenauth(_uid, _token):
                _tid = Login.objects.get(uid=_uid).account
                if len(Teacher.objects.filter(tNo=int(_tid))) == 1:
                    if len(Course.objects.filter(cNo=int(_cid))) == 1:
                        if len(Student.objects.filter(sNo=int(_sid))) == 1:
                            if len(TeacherCourse.objects.filter(cNo=int(_cid), tNo=int(_tid))) == 1:
                                if len(StudentCourse.objects.filter(sNo=int(_sid), cNo=int(_cid))) == 1:
                                    contractsubmitmark = ContractMark(txid=_txid, times=0, tNo=int(_tid), cNo=int(_cid),
                                                                      sNo=int(_sid), mark=_mark)
                                    contractsubmitmark.save()
                                    info = "Success"
                                else:
                                    info = "The student does not select this course"
                            else:
                                info = "You are not the teacher of this course"
                        else:
                            info = "Student not exist"
                    else:
                        info = "Course not exist"
                else:
                    info = "Teacher not exist"
            else:
                info = "NotAuthorized"
            # if time.time() - time.mktime(Token.objects.get(key=_token).created.timetuple()) > AuthorizedTime:
            #     Token.objects.filter(key=_token).delete()
            #     info = "NotAuthorized"
            #
            # elif len(Login.objects.filter(uid=_uid)) == 1:
            #     _cid = reqbody['courseId']
            #     _sid = reqbody['studentId']
            #     _tid = Login.objects.get(uid=_uid).account
            #     if _cid == "" or _sid == "":
            #         info = "Missing parameter"
            #     elif len(Course.objects.filter(cNo=int(_cid))) == 0:
            #         info = "Course not exist"
            #     elif len(Student.objects.filter(sNo=int(_sid))) == 0:
            #         info = "Student not exist"
            #     elif len(TeacherCourse.objects.filter(cNo=int(_cid), tNo=int(_tid))) == 0:
            #         info = "You are not the teacher of this course"
            #     elif len(StudentCourse.objects.filter(sNo=int(_sid), cNo=int(_cid))) == 0:
            #         info = "the student not select this course"
            #     else:
            #         contractsubmitmark = ContractMark(txid=_txid, times=0, tNo=int(_tid), cNo=int(_cid), sNo=int(_sid),
            #                                           mark=_mark)
            #         contractsubmitmark.save()
            #         info = "Success"
            # else:
            #     info = "Teacher not exist"
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
