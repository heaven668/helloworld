# -*- coding: utf-8 -*-

import json
import math
import time
import simplejson

from django.http import HttpResponse
from django.http import HttpResponseForbidden
from django.http import HttpResponseBadRequest
from django.http import JsonResponse
from rest_framework.authtoken.models import Token

from lab1017.models import Course
from lab1017.models import Student
from lab1017.models import CourseMaterial
from lab1017.models import Teacher
from lab1017.models import TeacherCourse
from lab1017.models import Question
from lab1017.models import Login
from lab1017.models import StudentCourse
from lab1017.models import ContractSelectCourse

from HelloWorld.Common import AuthorizedTime
from HelloWorld.Common import tokenauth


# 个人信息查询
def stuinfoquery(request):
    dict = {}
    meta = {}
    data = {}
    dict["meta"] = meta
    dict["data"] = data

    try:
        if request.method == "POST":
            reqbody = simplejson.loads(request.body)
            # stu = reqbody['student']
            _token = reqbody['token']
            _uid = reqbody['uid']

            if tokenauth(_uid, _token):
                _id = Login.objects.get(uid=_uid).account
                if len(Student.objects.filter(sNo=_id)) == 1:
                    stu_info = Student.objects.get(sNo=_id)
                    data['id'] = _id
                    data['name'] = stu_info.sName
                    data['gender'] = stu_info.sGender
                    data['class'] = stu_info.sClass
                    data['major'] = stu_info.sMajor
                    data['school'] = stu_info.sSchool
                    data['grade'] = stu_info.sGrade
                    data['tel'] = stu_info.sTelephone
                    data['email'] = stu_info.sEmail
                    data['type'] = Login.objects.get(uid=_uid).accountType
                    info = "Success"
                else:
                    info = "Student not exist"
            # if time.time() - time.mktime(Token.objects.get(key=_token).created.timetuple()) > AuthorizedTime:
            #     Token.objects.filter(key=_token).delete()
            #     info = "NotAuthorized"
            # elif len(Login.objects.filter(uid=_uid)) == 1:
            #     _login = Login.objects.get(uid=_uid)
            #     _id = int(_login.account)
            #     if _id == "":
            #         info = "Missing parameter ID"
            #     elif len(Student.objects.filter(sNo=_id)) == 0:
            #         info = "Student not exist"
            #     else:
            #         stu_info = Student.objects.get(sNo=_id)
            #         data['id'] = _id
            #         data['name'] = stu_info.sName
            #         data['gender'] = stu_info.sGender
            #         data['class'] = stu_info.sClass
            #         data['major'] = stu_info.sMajor
            #         data['school'] = stu_info.sSchool
            #         data['grade'] = stu_info.sGrade
            #         data['tel'] = stu_info.sTelephone
            #         data['email'] = stu_info.sEmail
            #         data['type'] = _login.accountType
            #         info = "Success"
            # else:
            #     info = "Student not exist"
            # else:
            #     info = "Wrong accounttype,please notify administrator"
            else:
                info = "NotAuthorized"
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
#
#
# #个人信息修改
# def stuinfomodify(request):
#     dict = {}
#     meta = {}
#     dict["meta"] = meta
#     try:
#         if request.methon == "POST":
#             reqbody = simplejson.loads(request.body)
#             user = reqbody['student']
#             _uid = reqbody['uid']
#             _name = user['user_name']
#             _tel = user['user_tel']
#             _email = user['user_email']
#             _password = user['user_password_log']
#             _login = Login.objects.get(id=int(_uid))
#             _id = int(_login.account)
#             if _id == "":
#                 info = "Missing parameter ID"
#             elif len(Student.objects.filter(sNo=_id)) == 0:
#                 info = "Student not exist"
#             else:
#                 updatestudent = Student.objects.get(sNo=_id)
#                 updatestudent.update(sName=_name,sTel=_tel,sEmail=_email,LoginPassword=_password)
#                 info = "Success"
#         else:
#             info = "Wrong request method"
#     except:
#         # import sys
#         # info = "%s || %s" % (sys.exc_info()[0], sys.exc_info()[1])
#         info = "Syntax error or parameter error"
#         meta['code'] = "400"
#         meta['message'] = info
#         jsonr = simplejson.dumps(dict)
#         res = HttpResponseBadRequest(jsonr)
#         return res
#
#     if info == "Success":
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


#可选课查询
def courseQuery(request):
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

            _uid = reqbody['uid']
            _token = reqbody['token']
            _page = int(reqbody['page'])
            _number = int(reqbody['number'])

            if tokenauth(_uid, _token):
                _sid = Login.objects.get(uid=_uid).account
                if len(Student.objects.filter(sNo=_sid)) == 1:
                    stu_info = Student.objects.get(sNo=_sid)
                    s_major = stu_info.sMajor
                    s_grade = stu_info.sGrade
                    courselist = Course.objects.filter(cGrade=s_grade, cMajor=s_major)

                    _count = 0
                    for cl in courselist:
                        if len(TeacherCourse.objects.filter(cNo_id=cl.cNo)) > 0:
                            c = {}
                            # course = Course.objects.get(cNo=cl.cNo)
                            c['course_id'] = str(cl.cNo)
                            c['course_name'] = cl.cName
                            # c['course_num'] = ""
                            # c['course_avater'] = ""
                            c['abstract'] = cl.cIntroduction
                            c['time'] = cl.cTerm
                            c['credit'] = str(cl.cCredit)
                            c['mark_element'] = cl.cComposition
                            c['type'] = cl.cNature
                            tc = TeacherCourse.objects.filter(cNo=cl.cNo)
                            for tcs in tc:
                                teacher = Teacher.objects.get(tNo=tcs.tNo_id)
                                c['teacher_name'] = teacher.tName
                                c['teacher_tel'] = teacher.tTelephone
                                c['teacher_email'] = teacher.tEmail
                                break
                            sc = StudentCourse.objects.filter(cNo=cl.cNo, sNo=_sid)
                            if len(sc) == 0:
                                c['status'] = "0"
                            else:
                                c['status'] = "1"
                            temporary[str(_count)] = c
                            _count += 1

                    data['pages'] = math.ceil(float(len(temporary) / _number))

                    for t in range(0, len(temporary)):
                        if t >= _number * (_page - 1):
                            if t < _number * _page:
                                content[str(t)] = temporary[str(t)]
                    info = "Success"
                    data['content'] = content

                else:
                    info = "Student not exist"
            else:
                info = "NotAuthorized"

            # if time.time() - time.mktime(Token.objects.get(key=_token).created.timetuple()) > AuthorizedTime:
            #     Token.objects.filter(key=_token).delete()
            #     info = "NotAuthorized"
            #
            # elif len(Login.objects.filter(uid=_uid)) == 1:
            #     _sid = Login.objects.get(uid=_uid).account
            #     _page = int(reqbody['page'])
            #     _number = int(reqbody['number'])
            #     if _uid == "":
            #         info = "Missing parameter ID"
            #     elif len(Student.objects.filter(sNo=_sid)) == 0:
            #         info = "Student not exist"
            #     else:
            #         stu_info = Student.objects.get(sNo=_sid)
            #         s_major = stu_info.sMajor
            #         s_grade = stu_info.sGrade
            #         courselist = Course.objects.filter(cGrade=s_grade).filter(cMajor=s_major)
            #
            #         _count = 0
            #         for cl in courselist:
            #             if len(TeacherCourse.objects.filter(cNo_id=cl.cNo)) > 0:
            #                 c = {}
            #                 # course = Course.objects.get(cNo=cl.cNo)
            #                 c['course_id'] = str(cl.cNo)
            #                 c['course_name'] = cl.cName
            #                 # c['course_num'] = ""
            #                 # c['course_avater'] = ""
            #                 c['abstract'] = cl.cIntroduction
            #                 c['time'] = cl.cTerm
            #                 c['credit'] = str(cl.cCredit)
            #                 c['mark_element'] = cl.cComposition
            #                 c['type'] = cl.cNature
            #                 tc = TeacherCourse.objects.filter(cNo=cl.cNo)
            #                 for tcs in tc:
            #                     teacher = Teacher.objects.get(tNo=tcs.tNo_id)
            #                     c['teacher_name'] = teacher.tName
            #                     c['teacher_tel'] = teacher.tTelephone
            #                     c['teacher_email'] = teacher.tEmail
            #                     break
            #                 sc = StudentCourse.objects.filter(cNo=cl.cNo, sNo=_sid)
            #                 if len(sc) == 0:
            #                     c['status'] = "0"
            #                 else:
            #                     c['status'] = "1"
            #                 temporary[str(_count)] = c
            #                 _count += 1
            #
            #         data['pages'] = math.ceil(float(len(temporary) / _number))
            #
            #         for t in range(0, len(temporary)):
            #             if t >= _number * (_page - 1):
            #                 if t < _number * _page:
            #                     content[str(t)] = temporary[str(t)]
            #         info = "Success"
            #         data['content'] = content
            # else:
            #     info = "Student not exist"
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


def courseSelect(request):
    dict = {}
    meta = {}
    dict["meta"] = meta
    try:
        if request.method == "POST":
            reqbody = simplejson.loads(request.body)

            # info = "Success"
            _uid = reqbody['uid']
            _token = reqbody['token']
            _cid = reqbody['courseId']
            _txid = reqbody['Txid']
            _timestamp = reqbody['requestTime']

            if tokenauth(_uid, _token):
                _stu_id = Login.objects.get(uid=_uid).account
                if len(Course.objects.filter(cNo=int(_cid))) == 1:
                    if len(StudentCourse.objects.filter(cNo_id=int(_cid), sNo_id=_stu_id, status="1")) == 0:
                        selectcourse = StudentCourse(cNo_id=int(_cid), sNo_id=_stu_id, status="1")
                        selectcourse.save()

                        contractsc = ContractSelectCourse(txid=_txid, times=0, cNo=int(_cid), sNo=_stu_id,
                                                          timestamp=_timestamp)
                        contractsc.save()

                        info = "Success"
                    else:
                        info = "You have selected the course"
                else:
                    info = "Course not exist"
            else:
                info = "NotAuthorized"

            # if time.time() - time.mktime(Token.objects.get(key=_token).created.timetuple()) > AuthorizedTime:
            #     Token.objects.filter(key=_token).delete()
            #     info = "NotAuthorized"
            #
            # elif len(Login.objects.filter(uid=_uid)) == 1:
            #     _cid = reqbody['courseId']
            #     _stu_id = Login.objects.get(uid=_uid).account
            #     if _cid == "":
            #         info = "Missing parameter"
            #     elif len(Course.objects.filter(cNo=int(_cid))) == 0:
            #         info = "Course not exist"
            #     elif len(StudentCourse.objects.filter(cNo_id=int(_cid), sNo_id=_stu_id, status="1")) != 0:
            #         info = "You have selected the course"
            #     else:
            #         selectcourse = StudentCourse(cNo_id=int(_cid), sNo_id=_stu_id, status="1")
            #         selectcourse.save()
            #         info = "Success"
            # else:
            #     info = "Student not exist"
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


def courseSelected(request):
        dict = {}
        meta = {}
        data = {}
        dict["meta"] = meta
        dict["data"] = data

        content = {}
        data['content'] = content

        try:
            if request.method == "POST":
                reqbody = simplejson.loads(request.body)
                _uid = reqbody['uid']
                _token = reqbody['token']
                # _page = int(reqbody['page'])
                # _number = int(reqbody['number'])

                if tokenauth(_uid, _token):
                    _sid = Login.objects.get(uid=_uid).account
                    if len(Student.objects.filter(sNo=_sid)) == 1:
                        courses = StudentCourse.objects.filter(sNo=_sid).filter(status=2)
                        data['num'] = len(courses)

                        _count = 0

                        for courselist in courses:
                            c = {}
                            cl = Course.objects.get(cNo=courselist.cNo_id)
                            # len(Course.objects.filter(cNo=cl.cNo)) == 1:
                            c['course_id'] = cl.cNo
                            c['name'] = cl.cName
                            # c['course_num'] = ""
                            # c['course_avater'] = ""
                            c['abstract'] = cl.cIntroduction
                            c['time'] = cl.cTerm
                            c['credit'] = str(cl.cCredit)
                            c['mark_element'] = cl.cComposition
                            c['type'] = cl.cNature
                            tc = TeacherCourse.objects.get(cNo=cl.cNo)
                            teacher = Teacher.objects.get(tNo=tc.tNo_id)
                            c['teacher_name'] = teacher.tName
                            content[str(_count)] = c
                            _count += 1
                        info = "Success"
                    else:
                        info = "Student not exist"
                else:
                    info = "NotAuthorized"

            #     if time.time() - time.mktime(Token.objects.get(key=_token).created.timetuple()) > AuthorizedTime:
            #         Token.objects.filter(key=_token).delete()
            #         info = "NotAuthorized"
            #
            #     elif len(Login.objects.filter(uid=_uid)) == 1:
            #         _sid = Login.objects.get(uid=_uid).account
            #
            #         if _sid == "":
            #             info = "Missing parameter ID"
            #         elif len(Student.objects.filter(sNo=_sid)) == 0:
            #             info = "Student not exist"
            #         else:
            #             courses = StudentCourse.objects.filter(sNo=_sid).filter(status=2)
            #             data['num'] = len(courses)
            #
            #             _count = 0
            #
            #             for courselist in courses:
            #                 c = {}
            #                 cl = Course.objects.get(cNo=courselist.cNo_id)
            #                 # len(Course.objects.filter(cNo=cl.cNo)) == 1:
            #                 c['course_id'] = cl.cNo
            #                 c['name'] = cl.cName
            #                 # c['course_num'] = ""
            #                 # c['course_avater'] = ""
            #                 c['abstract'] = cl.cIntroduction
            #                 c['time'] = cl.cTerm
            #                 c['credit'] = str(cl.cCredit)
            #                 c['mark_element'] = cl.cComposition
            #                 c['type'] = cl.cNature
            #                 tc = TeacherCourse.objects.get(cNo=cl.cNo)
            #                 teacher = Teacher.objects.get(tNo=tc.tNo_id)
            #                 c['teacher_name'] = teacher.tName
            #                 content[str(_count)] = c
            #                 _count += 1
            #                 # for tcs in tc:
            #                 #     teacher = Teacher.objects.get(tNo=tcs.tNo_id)
            #                 #     c['teacher_name'] = teacher.tName
            #                 #     c['teacher_tel'] = teacher.tTelephone
            #                 #     c['teacher_email'] = teacher.tEmail
            #                 #     break
            #                 info = "Success"
            #                 # sc = StudentCourse.objects.filter(cNo=cl.cNo, sNo=_sid)
            #                 # if len(sc) == 0:
            #                 #     c['status'] = "1"
            #                 # else:
            #                 #     c['status'] = "2"
            #                 # temporary[str(_count)] = c
            #                 # _count += 1
            #
            #                 # data['pages'] = math.ceil(float(len(temporary) / _number))
            #                 #
            #                 # for t in range(0, len(temporary)):
            #                 #     if t >= _number * (_page - 1):
            #                 #         if t < _number * _page:
            #                 #             content[str(t)] = temporary[str(t)]
            #                 #     info = "Course not exist"
            #                 # data['content'] = content
            #
            #     else:
            #         info = "Student not exist"
            # else:
            #     info = "Wrong request method"
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


# def courseSelected(request):
#     dict = {}
#     meta = {}
#     data = {}
#     dict["meta"] = meta
#     dict["data"] = data
#     c = {}
#     content = {}
#     data['content'] = content
#     temporary = {}
#     try:
#         if request.method == "POST":
#             reqbody = simplejson.loads(request.body)
#             _id_list = reqbody["course_id_list"]
#             _page = int(reqbody['page'])
#             _number = int(reqbody['number'])
#             for _id in _id_list:
#                 if _id == "":
#                     info = "Missing parameter ID"
#                 elif len(Course.objects.filter(cNo=_id)) == 0:
#                     info = "Course not exist"
#                 else:
#                     course = Course.objects.get(cNo=_id)
#                     data['pages'] = len(course)
#                     _count = 0
#                     for cl in course:
#                         # course = Course.objects.get(cNo=cl.cNo)
#                         c['course_id'] = cl.cNo
#                         c['course_name'] = cl.cName
#                         c['course_num'] = ""
#                         c['course_avater'] = ""
#                         c['abstract'] = cl.cIntroduction
#                         c['time'] = cl.cTerm
#                         c['credit'] = cl.cCredit
#                         c['mark_element'] = cl.cComposition
#                         c['type'] = cl.cNature
#                         tc = TeacherCourse.objects.filter(cNo=cl.cNo)
#                         teacher = Teacher.objects.filter(tNo=tc.tNo_id)
#                         c['teacher_name'] = teacher.tName
#                         c['teacher_tel'] = teacher.tTelephone
#                         c['teacher_email'] = teacher.tEmail
#                       #  c['teacher'] = {'teacher_name':teacehr.name,'teacehr_tel':teacher.tTelephone,'teacher_email':teacher.tEmail}
#                         temporary[str(_count)] = c
#                         _count += 1
#                     for t in range(0, len(temporary)):
#                         if t >= _number * (_page - 1):
#                             if t < _number * _page:
#                                 content[str(t)] = temporary[str(t)]
#                     info = "Success"
#                     data['content'] = content
#         else:
#             info = "Wrong request method"
#     except:
#         # import sys
#         # info = "%s || %s" % (sys.exc_info()[0], sys.exc_info()[1])
#         info = "Syntax error or parameter error"
#         meta['code'] = "400"
#         meta['message'] = info
#         jsonr = simplejson.dumps(dict)
#         res = HttpResponseBadRequest(jsonr)
#         res.__setitem__('Access-Control-Allow-Origin', '*')
#         return res
#
#     if info == "Success":
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


#课程详情查询
def coursedetailQuery(request):
    dict = {}
    meta = {}
    data = {}
    dict["meta"] = meta
    dict["data"] = data
    try:
        if request.method == "POST":
            reqbody = simplejson.loads(request.body)
            _uid = reqbody['uid']
            _token = reqbody['token']
            if time.time() - time.mktime(Token.objects.get(key=_token).created.timetuple()) > AuthorizedTime:
                Token.objects.filter(key=_token).delete()
                info = "NotAuthorized"
            elif len(Login.objects.filter(uid=_uid)) == 1:
                _id = int(reqbody['course_id'])
                # _name = reqbody['course_name']
                if _id == "":
                    info = "Missing parameter"
                elif len(Course.objects.filter(cNo=_id)) == 0:
                    info = "Course not exist"
                else:
                    course = Course.objects.get(cNo=_id)
                    data['course_id'] = str(_id)
                    data['course_name'] = course.cName
                    # data['course_num'] = ""
                    # data['course_avater'] = ""
                    data['abstract'] = course.cIntroduction
                    data['type'] = course.cNature
                    data['time'] = course.cTerm
                    data['grade'] = course.cGrade
                    data['major'] = course.cMajor
                    data['credit'] = str(course.cCredit)
                    tc = TeacherCourse.objects.filter(cNo=_id)
                    # teacher = Teacher.objects.filter(tNo=tc.tNo_id)
                    # data['teacher_name'] = teacher.tName
                    # data['teacher_tel'] = teacher.tTelephone
                    # data['teacher_email'] = teacher.tEmail
                    if len(tc) > 0:
                        for tcs in tc:
                            teacher = Teacher.objects.filter(tNo=tcs.tNo_id)
                            data['teacher_name'] = teacher.tName
                            data['teacher_tel'] = teacher.tTelephone
                            data['teacher_email'] = teacher.tEmail
                            break
                    else:
                        data['teacher_name'] = ""
                        data['teacher_tel'] = ""
                        data['teacher_email'] = ""
                    info = "Success"
            else:
                "Student not exist"
            # elif len(Course.objects.filter(cNo=_id)) != 0:
            #     selected = Course.objects.get(cNo=_id)
            #     data['course_id'] = _id
            #     data['course_name'] = selected.cName
            #     data['course_num'] = selected.cNum
            #     #data['course_avater'] =
            #     data['abstract'] = selected.cIntroduction
            #     data['type'] = selected.cNature
            #     data['time'] = selected.cTerm
            #     data['grade'] = selected.cGrade
            #     data['credit'] = selected.cCredit
            #     check = TeacherCourse.objects.filter(cNo=_id)
            #     teacher = Teacher.objects.filter(tNo=check.tNo_id)
            #     data['teacher'] = {teacher.tName,teacher.tNo,teacher.tTelephone}
            #     info = "Success"
            # elif len(Course.objects.filter(cName=_name)) !=0:
            #     selected = Course.objects.get(cName=_name)
            #     selected = Course.objects.get(cNo=_id)
            #     data['course_id'] = _id
            #     data['course_name'] = selected.cName
            #     data['course_num'] = selected.cNum
            #     #data['course_avater'] =
            #     data['abstract'] = selected.cIntroduction
            #     data['type'] = selected.cNature
            #     data['time'] = selected.cTerm
            #     data['grade'] = selected.cGrade
            #     data['credit'] = selected.cCredit
            #     check = TeacherCourse.objects.filter(cNo=_id)
            #     teacher = Teacher.objects.filter(tNo=check.tNo_id)
            #     data['teacher'] = {teacher.tName,teacher.tNo,teacher.tTelephone}
            #     info = "Success"
            # else:
            #     info = "Course not exist"
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


#
# #课程材料列表
# def courseMaterials(request):
#     dict = {}
#     meta = {}
#     data = {}
#     dict["meta"] = meta
#     dict["data"] = data
#     c = {}
#     content = {}
#     data["content"] = content
#     temporary = {}
#     try:
#         if request.method =="POST":
#             reqbody = simplejson.loads(request.body)
#             _uid = reqbody['uid']
#             _id = reqbody['course_id']
#             if _id == "":
#                 info = "Missing parameter ID"
#             elif len(Course.objects.filter(cNo=_id)) == 0:
#                 info = "Course not exist"
#             else:
#                 data['pages'] = math.ceil(float(len(course) / _number))
#                 _count = 0
#                 material = CourseMaterial.objects.get(cNo=_id)
#                 for ml in material:
#                     c['doc_id'] = ml.cMaterialsHash
#                     c['doc_name'] = ml.cMaterialsName
#                     c['type'] = ml.cMaterialsType
#                     c['doc_size'] = ml.cMaterialsSize
#                     #data['download_url'] =Null
#                     temporary[str(_count)] = c
#                     _count += 1
#                 for t in range(0, len(temporary)):
#                     if t >= _number * (_page - 1):
#                         if t < _number * _page:
#                             content[str(t)] = temporary[str(t)]
#                 info = "Success"
#                 data['content'] = content
#         else:
#             info = "Wrong request method"
#     except:
#         # import sys
#         # info = "%s || %s" % (sys.exc_info()[0], sys.exc_info()[1])
#         info = "Syntax error or parameter error"
#         meta['code'] = "400"
#         meta['message'] = info
#         jsonr = simplejson.dumps(dict)
#         res = HttpResponseBadRequest(jsonr)
#         res.__setitem__('Access-Control-Allow-Origin', '*')
#         return res
#
#     if info == "Success":
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
#
# #测试题列表
# def questionlist(request):
#     dict = {}
#     meta = {}
#     data = {}
#     dict['meta'] = meta
#     dict['data'] = data
#     c = {}
#     content = {}
#     data["content"] = content
#     temporary = {}
#     try:
#         if request.method == "POST":
#             reqbody = simplejson.loads(request.body)
#             _uid = reqbody['uid']
#             _id = reqbody['course_id']
#             if _id == "":
#                 info = "Missing parameter ID"
#             elif len(Course.objects.filter(cNo=_id)) == 0:
#                 info = "Course not exist"
#             else:
#                 question = Question.objects.get(cNo=_id)
#                 data['pages'] = math.ceil(float(len(course) / _number))
#                 _count = 0
#                 for ql in question:
#                     c['exam_id'] = ql.qNo
#                     c['exam_name'] = ql.qQuestion
#                     c['exam_option'] = ql.qOption
#                     temporary[str(_count)] = c
#                     _count += 1
#                 for t in range(0, len(temporary)):
#                     if t >= _number * (_page - 1):
#                         if t < _number * _page:
#                             content[str(t)] = temporary[str(t)]
#                 info = "Success"
#                 data['content'] = content
#         else:
#             info = "Wrong request method"
#     except:
#         # import sys
#         # info = "%s || %s" % (sys.exc_info()[0], sys.exc_info()[1])
#         info = "Syntax error or parameter error"
#         meta['code'] = "400"
#         meta['message'] = info
#         jsonr = simplejson.dumps(dict)
#         res = HttpResponseBadRequest(jsonr)
#         res.__setitem__('Access-Control-Allow-Origin', '*')
#         return res
#
#     if info == "Success":
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