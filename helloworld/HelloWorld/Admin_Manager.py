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
from lab1017.models import ContractManagerInfo

from HelloWorld.Common import AuthorizedTime
from HelloWorld.Common import tokenauth

# 数据库操作


def administratorinfoadd(request):
    dict = {}
    meta = {}
    dict["meta"] = meta
    try:
        if request.method == 'POST':
            reqbody = simplejson.loads(request.body)

            _requid = reqbody['uid']
            _reqtoken = reqbody['token']
            _txid = reqbody['Txid']

            manager = reqbody['administrator']
            _id = manager['administrator_id']
            _name = manager['administrator_name']
            _password = manager['administrator_password_log']
            _uid = str(_id) + str(int(time.time()))

            if tokenauth(_requid, _reqtoken):

                if len(Manager.objects.filter(mNo=_id)) == 0 and len(Login.objects.filter(account=_id)) == 0:
                    newmanager = Manager(mNo=_id, mName=_name, LoginPassword=_password)
                    newmanager.save()

                    _type = "administrator"
                    # newlogin = Login(uid=_uid, account=_id, accountType=_type, LoginPassword=_password)
                    newlogin = Login(uid=_uid, account=_id, accountType=_type, LoginPassword=_password,
                                     id=_id, password=_password, is_superuser=0, username=_id, first_name="blank",
                                     last_name="blank", email="null@null.com", is_staff=0, is_active=0,
                                     date_joined=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
                    newlogin.save()

                    newtx = ContractManagerInfo(txid=_txid, times=0, mNo=_id)
                    newtx.save()

                    info = "Success"

                else:
                    info = "The manager already exists"

            else:
                info = "NotAuthorized"

            # if time.time() - time.mktime(Token.objects.get(key=_reqtoken).created.timetuple()) > AuthorizedTime:
            #     Token.objects.filter(key=_reqtoken).delete()
            #     info = "NotAuthorized"
            #
            # elif len(Manager.objects.filter(mNo=_id)) > 0 or len(Login.objects.filter(account=_id)) > 0:
            #     info = "The manager already exists"
            #     # meta['code'] = "400"
            #     # meta['message'] = info
            #     # jsonr = simplejson.dumps(dict)
            #     # res = HttpResponseBadRequest(jsonr)
            #     # res.__setitem__('Access-Control-Allow-Origin', '*')
            #     # return res
            # else:
            #     newmanager = Manager(mNo=_id, mName=_name, LoginPassword=_password)
            #     newmanager.save()
            #
            #     _type = "administrator"
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
        # import sys
        # info = "%s || %s" % (sys.exc_info()[0], sys.exc_info()[1])
        info = "Syntax Error Or Parameter Error"
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


def administratorinfoquery(request):
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

            manager_req = reqbody['administrator']
            _id = manager_req['administrator_id']

            if tokenauth(_requid, _reqtoken):

                if _id != "":

                    if len(Manager.objects.filter(mNo=_id)) == 1:
                        manager = Manager.objects.get(mNo=_id)
                        data['administrator_id'] = _id
                        data['administrator_name'] = manager.mName
                        data['administrator_password_log'] = manager.LoginPassword
                        data['administrator_address'] = manager.mAddress
                        data['administrator_password_unlock'] = manager.mUnlockPassword
                        data['administrator_tel'] = manager.mTelephone
                        # data['administrator_email'] = manager.mEmail
                        info = "Success"

                    else:
                        info = "Manager not exist"

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
            # elif len(Manager.objects.filter(mNo=_id)) == 0:
            #     info = "Manager not exist"
            # else:
            #     manager = Manager.objects.get(mNo=_id)
            #     data['administrator_id'] = _id
            #     data['administrator_name'] = manager.mName
            #     data['administrator_password_log'] = manager.LoginPassword
            #     data['administrator_address'] = manager.mAddress
            #     data['administrator_password_unlock'] = manager.mUnlockPassword
            #     data['administrator_tel'] = manager.mTelephone
            #     # data['administrator_email'] = manager.mEmail
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


def administratorinfomodify(request):
    dict = {}
    meta = {}
    dict["meta"] = meta
    try:
        if request.method == 'POST':
            reqbody = simplejson.loads(request.body)

            _requid = reqbody['uid']
            _reqtoken = reqbody['token']

            manager = reqbody['administrator']
            _id = manager['administrator_id']
            _name = manager['administrator_name']
            _password = manager['administrator_password_log']
            _address = manager['administrator_address']
            _unlockpassword = manager['administrator_password_unlock']

            updatemanager = Manager.objects.filter(mNo=_id)
            checkid = Login.objects.filter(account=_id)
            checkaddress = Login.objects.filter(address=_address)

            if tokenauth(_requid, _reqtoken):

                if len(checkid) == 1 and len(updatemanager) == 1:

                    if len(checkaddress) == 0 or (len(checkaddress) == 1 and Login.objects.get(account=_id).address == _address):
                        updatemanager.update(mName=_name, LoginPassword=_password, mAddress=_address,
                                             mUnlockPassword=_unlockpassword)
                        checkid.update(LoginPassword=_password, address=_address, unlockPassword=_unlockpassword)
                        info = "Success"

                    else:
                        info = "Address already exist"

                else:
                    info = "Manager ID dose not exist"

            else:
                info = "NotAuthorized"

            # if time.time() - time.mktime(Token.objects.get(key=_reqtoken).created.timetuple()) > AuthorizedTime:
            #     Token.objects.filter(key=_reqtoken).delete()
            #     info = "NotAuthorized"
            #
            # elif len(checkid) == 0 or len(updatemanager) != 1:
            #     info = "Manager ID dose not exist"
            #
            # elif len(checkaddress) > 0 and Login.objects.get(account=_id).address != _address:
            #     info = "Address already exist"
            #
            # else:
            #     updatemanager.update(mName=_name, LoginPassword=_password, mAddress=_address,
            #                          mUnlockPassword=_unlockpassword)
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

