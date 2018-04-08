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

from HelloWorld.Common import AuthorizedTime
from HelloWorld.Common import tokenauth

# 数据库操作


def courseinfoadd(request):
    dict = {}
    meta = {}
    dict["meta"] = meta
    try:
        if request.method == 'POST':
            reqbody = simplejson.loads(request.body)

            _requid = reqbody['uid']
            _reqtoken = reqbody['token']

            course = reqbody['course']
            _id = course['course_id']
            _name = course['course_name']
            _major = course['academy']
            _grade = course['grade']
            _term = course['course_time']
            _credit = course['credit']
            _composition = course['mark_element']
            _nature = course['course_property']
            # _number = course['course_number']
            _number = 200

            if tokenauth(_requid, _reqtoken):

                if len(Course.objects.filter(cNo=_id)) == 0:
                    newcourse = Course(cNo=_id, cName=_name, cCredit=_credit, cNature=_nature, cNumber=_number,
                                       cMajor=_major, cGrade=_grade, cTerm=_term, cComposition=_composition)
                    newcourse.save()
                    info = "Success"

                else:
                    info = "ID exist"

            else:
                info = "NotAuthorized"

            # if time.time() - time.mktime(Token.objects.get(key=_reqtoken).created.timetuple()) > AuthorizedTime:
            #     Token.objects.filter(key=_reqtoken).delete()
            #     info = "NotAuthorized"
            #
            # elif len(Course.objects.filter(cNo=_id)) > 0:
            #     info = "ID exist"
            #     # meta['code'] = "400"
            #     # meta['message'] = info
            #     # jsonr = simplejson.dumps(dict)
            #     # res = HttpResponseBadRequest(jsonr)
            #     # res.__setitem__('Access-Control-Allow-Origin', '*')
            #     # return res
            # else:
            #     newcourse = Course(cNo=_id, cName=_name, cCredit=_credit, cNature=_nature, cNumber=_number,
            #                        cMajor=_major, cGrade=_grade, cTerm=_term, cComposition=_composition)
            #     newcourse.save()
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


def courseinfoquery(request):
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

            course = reqbody['course']
            _id = course['course_id']

            if tokenauth(_requid, _reqtoken):

                if _id != "":

                    if len(Course.objects.filter(cNo=_id)) == 1:
                        course_info = Course.objects.get(cNo=_id)
                        data['course_id'] = str(course_info.cNo)
                        data['course_name'] = course_info.cName
                        data['academy'] = course_info.cMajor
                        data['grade'] = course_info.cGrade
                        data['course_time'] = course_info.cTerm
                        data['credit'] = str(course_info.cCredit)
                        data['mark_element'] = course_info.cComposition
                        data['course_property'] = course_info.cNature
                        data['course_number'] = course_info.cNumber
                        teacher_info = TeacherCourse.objects.filter(cNo=_id).values()
                        _teacherid = {}
                        _teachername = {}
                        count = 0
                        for t in teacher_info:
                            _teacherid[count] = str(t['tNo_id'])
                            _teachername[count] = Teacher.objects.get(tNo=t['tNo_id']).tName
                            count = count + 1
                        data['teacher_id'] = _teacherid
                        data['teacher_name'] = _teachername
                        info = "Success"

                    else:
                        info = "Course not exist"

                else:
                    info = "Missing parameter ID"

            else:
                info = "NotAuthorized"
            # if time.time() - time.mktime(Token.objects.get(key=_reqtoken).created.timetuple()) > AuthorizedTime:
            #     Token.objects.filter(key=_reqtoken).delete()
            #     info = "NotAuthorized"
            #
            # elif _id == "":
            #     info = "Missing parameter ID"
            #
            # elif len(Course.objects.filter(cNo=_id)) == 0:
            #     info = "Course not exist"
            #
            # else:
            #     course_info = Course.objects.get(cNo=_id)
            #     data['course_id'] = str(course_info.cNo)
            #     data['course_name'] = course_info.cName
            #     data['academy'] = course_info.cMajor
            #     data['grade'] = course_info.cGrade
            #     data['course_time'] = course_info.cTerm
            #     data['credit'] = str(course_info.cCredit)
            #     data['mark_element'] = course_info.cComposition
            #     data['course_property'] = course_info.cNature
            #     data['course_number'] = course_info.cNumber
            #     teacher_info = TeacherCourse.objects.filter(cNo=_id).values()
            #     _teacherid = {}
            #     _teachername = {}
            #     count = 0
            #     for t in teacher_info:
            #         _teacherid[count] = str(t['tNo_id'])
            #         _teachername[count] = Teacher.objects.get(tNo=t['tNo_id']).tName
            #         count = count+1
            #     data['teacher_id'] = _teacherid
            #     data['teacher_name'] = _teachername
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


def courseinfomodify(request):
    dict = {}
    meta = {}
    dict["meta"] = meta
    try:
        if request.method == 'POST':
            reqbody = simplejson.loads(request.body)

            _requid = reqbody['uid']
            _reqtoken = reqbody['token']

            course = reqbody['course']
            _cid = course['course_id']
            _name = course['course_name']
            _credit = course['credit']
            _nature = course['course_property']
            _major = course['academy']
            _grade = course['grade']
            _term = course['course_time']
            # _number = course['course_number']
            _number = 200
            _composition = course['mark_element']
            _teacherchange = course['teacher_id_change']
            _formerteacherid = _teacherchange['former']
            _newteacherid = _teacherchange['new']

            updatecourse = Course.objects.filter(cNo=int(_cid))
            updatecourseteacher = TeacherCourse.objects.filter(cNo=int(_cid), tNo=int(_formerteacherid))
            checkformerteacherid = Teacher.objects.filter(tNo=int(_formerteacherid))
            checknewteacherid = Teacher.objects.filter(tNo=int(_newteacherid))
            checknewcourseteacherid = TeacherCourse.objects.filter(cNo_id=int(_cid), tNo_id=int(_newteacherid))

            if tokenauth(_requid, _reqtoken):

                if len(checkformerteacherid) == 1 and len(checknewteacherid) == 1 and len(updatecourseteacher) == 1:

                    if len(updatecourse) == 1:

                        if len(checknewcourseteacherid) == 0:
                            updatecourse.update(cName=_name, cCredit=_credit, cNature=_nature, cNumber=_number,
                                                cMajor=_major, cGrade=_grade, cTerm=_term, cComposition=_composition)
                            updatecourseteacher.update(tNo=int(_newteacherid))
                            info = "Success"

                        else:
                            info = "Already the teacher of the course"

                    else:
                        info = "Course ID not exist"

                else:
                    info = "Teacher ID not exist"

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
