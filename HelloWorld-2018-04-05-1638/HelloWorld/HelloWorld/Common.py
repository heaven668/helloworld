# -*- coding: utf-8 -*-

# contract_abi, contract_address, super_manager_address REQUIRED
# 2018/03/25    Tsai

import json
import time
import simplejson
import math
import random

from web3 import Web3, HTTPProvider
from web3.contract import ConciseContract
from web3 import eth

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
from lab1017.models import ContractStudentInfo
from lab1017.models import ContractAddress

AuthorizedTime = 60*60

compiled_sol = ""

amount = 10000000000000000000

# contract_abi = [{"constant":True,"inputs":[{"name":"_Txid","type":"string"}],"name":"getTxTag","outputs":[{"name":"","type":"bool"}],"payable":False,"stateMutability":"view","type":"function"},{"constant":True,"inputs":[],"name":"get_StudentList","outputs":[{"name":"","type":"uint256[]"}],"payable":False,"stateMutability":"view","type":"function"},{"constant":True,"inputs":[],"name":"course_tmp","outputs":[{"name":"CourseID","type":"uint256"},{"name":"CourseName","type":"string"},{"name":"Compulsory","type":"bool"},{"name":"Term","type":"uint256"},{"name":"Credit","type":"uint256"}],"payable":False,"stateMutability":"view","type":"function"},{"constant":True,"inputs":[],"name":"manager_tmp","outputs":[{"name":"ManagerID","type":"uint256"},{"name":"ManagerAddr","type":"address"}],"payable":False,"stateMutability":"view","type":"function"},{"constant":True,"inputs":[],"name":"get_TeacherList","outputs":[{"name":"","type":"uint256[]"}],"payable":False,"stateMutability":"view","type":"function"},{"constant":True,"inputs":[{"name":"_CourseID","type":"uint256"}],"name":"courseIDExist","outputs":[{"name":"","type":"bool"}],"payable":False,"stateMutability":"view","type":"function"},{"constant":True,"inputs":[{"name":"_ManagerAddr","type":"address"}],"name":"managerAddrExist","outputs":[{"name":"","type":"bool"}],"payable":False,"stateMutability":"view","type":"function"},{"constant":True,"inputs":[],"name":"get_ManagerList","outputs":[{"name":"","type":"uint256[]"}],"payable":False,"stateMutability":"view","type":"function"},{"constant":True,"inputs":[{"name":"_CourseID","type":"uint256"}],"name":"getStuMarksByCourseAll","outputs":[{"name":"","type":"uint256[]"},{"name":"","type":"uint256[]"}],"payable":False,"stateMutability":"view","type":"function"},{"constant":True,"inputs":[{"name":"_ManagerID","type":"uint256"}],"name":"managerIDExist","outputs":[{"name":"","type":"bool"}],"payable":False,"stateMutability":"view","type":"function"},{"constant":True,"inputs":[],"name":"get_safeNumberForOwner","outputs":[{"name":"","type":"uint8"}],"payable":False,"stateMutability":"view","type":"function"},{"constant":True,"inputs":[{"name":"_StudentID","type":"uint256"}],"name":"len_sCourseIDs","outputs":[{"name":"","type":"uint256"}],"payable":False,"stateMutability":"view","type":"function"},{"constant":False,"inputs":[{"name":"_Txid","type":"string"},{"name":"_TeacherID","type":"uint256"},{"name":"_TeacherName","type":"string"}],"name":"addTchInfo","outputs":[{"name":"","type":"bool"}],"payable":False,"stateMutability":"nonpayable","type":"function"},{"constant":True,"inputs":[],"name":"stu_tmp","outputs":[{"name":"StudentID","type":"uint256"},{"name":"StudentName","type":"string"},{"name":"StudentClass","type":"uint256"},{"name":"StudentAddr","type":"address"}],"payable":False,"stateMutability":"view","type":"function"},{"constant":True,"inputs":[{"name":"_StudentAddr","type":"address"}],"name":"studentAddrExist","outputs":[{"name":"","type":"bool"}],"payable":False,"stateMutability":"view","type":"function"},{"constant":False,"inputs":[{"name":"_Txid","type":"string"},{"name":"_CourseID","type":"uint256"},{"name":"_CourseName","type":"string"},{"name":"_Compulsory","type":"bool"},{"name":"_Term","type":"uint256"},{"name":"_Credit","type":"uint256"},{"name":"_Percentage","type":"uint256[]"},{"name":"_TeacherID","type":"uint256"}],"name":"addCourseInfo","outputs":[{"name":"","type":"bool"}],"payable":False,"stateMutability":"nonpayable","type":"function"},{"constant":True,"inputs":[],"name":"tch_tmp","outputs":[{"name":"TeacherID","type":"uint256"},{"name":"TeacherName","type":"string"},{"name":"TeacherAddr","type":"address"}],"payable":False,"stateMutability":"view","type":"function"},{"constant":True,"inputs":[{"name":"_TeacherID","type":"uint256"}],"name":"teacherIDExist","outputs":[{"name":"","type":"bool"}],"payable":False,"stateMutability":"view","type":"function"},{"constant":False,"inputs":[{"name":"_newOwner","type":"address"}],"name":"transferOwnerShip","outputs":[{"name":"","type":"bool"}],"payable":False,"stateMutability":"nonpayable","type":"function"},{"constant":False,"inputs":[{"name":"_SuperUser","type":"address"}],"name":"setSuperUser","outputs":[{"name":"","type":"bool"}],"payable":False,"stateMutability":"nonpayable","type":"function"},{"constant":False,"inputs":[{"name":"_Txid","type":"string"},{"name":"_CourseID","type":"uint256"},{"name":"_StudentID","type":"uint256"},{"name":"_requestTime","type":"uint256"}],"name":"stuChooseCourse","outputs":[{"name":"","type":"bool"}],"payable":False,"stateMutability":"nonpayable","type":"function"},{"constant":False,"inputs":[{"name":"_Txid","type":"string"},{"name":"_TeacherID","type":"uint256"},{"name":"_CourseID","type":"uint256"},{"name":"_StudentID","type":"uint256"},{"name":"_Marks","type":"uint256[]"}],"name":"setStuMark","outputs":[{"name":"boolValue","type":"bool"},{"name":"mark","type":"uint256"}],"payable":False,"stateMutability":"nonpayable","type":"function"},{"constant":True,"inputs":[{"name":"_StudentID","type":"uint256"}],"name":"studentIDExist","outputs":[{"name":"","type":"bool"}],"payable":False,"stateMutability":"view","type":"function"},{"constant":True,"inputs":[],"name":"getEnableTxTag","outputs":[{"name":"","type":"bool"}],"payable":False,"stateMutability":"view","type":"function"},{"constant":True,"inputs":[],"name":"Owner","outputs":[{"name":"","type":"address"}],"payable":False,"stateMutability":"view","type":"function"},{"constant":False,"inputs":[{"name":"_Txid","type":"string"},{"name":"_ManagerID","type":"uint256"}],"name":"addManagerInfo","outputs":[{"name":"","type":"bool"}],"payable":False,"stateMutability":"nonpayable","type":"function"},{"constant":True,"inputs":[{"name":"_StudentID","type":"uint256"},{"name":"_CourseID","type":"uint256"}],"name":"getStuMark","outputs":[{"name":"","type":"uint256"}],"payable":False,"stateMutability":"view","type":"function"},{"constant":True,"inputs":[],"name":"SuperUser","outputs":[{"name":"","type":"address"}],"payable":False,"stateMutability":"view","type":"function"},{"constant":True,"inputs":[],"name":"get_CourseList","outputs":[{"name":"","type":"uint256[]"}],"payable":False,"stateMutability":"view","type":"function"},{"constant":False,"inputs":[{"name":"_Txid","type":"string"},{"name":"_Identity","type":"uint256"},{"name":"_ID","type":"uint256"},{"name":"_Addr","type":"address"}],"name":"addAccount","outputs":[{"name":"","type":"bool"}],"payable":False,"stateMutability":"nonpayable","type":"function"},{"constant":True,"inputs":[{"name":"_CourseID","type":"uint256"}],"name":"len_cStuIDs","outputs":[{"name":"","type":"uint256"}],"payable":False,"stateMutability":"view","type":"function"},{"constant":False,"inputs":[{"name":"value","type":"bool"}],"name":"setEnableTxTag","outputs":[],"payable":False,"stateMutability":"nonpayable","type":"function"},{"constant":False,"inputs":[{"name":"_Txid","type":"string"},{"name":"_StudentID","type":"uint256"},{"name":"_StudentName","type":"string"},{"name":"_StudentClass","type":"uint256"}],"name":"addStuInfo","outputs":[{"name":"","type":"bool"}],"payable":False,"stateMutability":"nonpayable","type":"function"},{"constant":True,"inputs":[{"name":"_CourseID","type":"uint256"},{"name":"_StudentID","type":"uint256"}],"name":"getStuMarksByCourse","outputs":[{"name":"","type":"uint256"}],"payable":False,"stateMutability":"view","type":"function"},{"inputs":[],"payable":False,"stateMutability":"nonpayable","type":"constructor"},{"anonymous":False,"inputs":[{"indexed":False,"name":"newSuperUser","type":"address"}],"name":"SetSuperUser","type":"event"},{"anonymous":False,"inputs":[{"indexed":False,"name":"newOwner","type":"address"}],"name":"TransferOwnerShip","type":"event"},{"anonymous":False,"inputs":[{"indexed":True,"name":"txid","type":"string"},{"indexed":True,"name":"Success","type":"bool"},{"indexed":True,"name":"Operator","type":"address"}],"name":"TxMined","type":"event"}]

contract_abi = [{"constant":False,"inputs":[{"name":"_Txid","type":"string"},{"name":"_StudentID","type":"uint256"},{"name":"_StudentClass","type":"uint256"}],"name":"addStuInfo","outputs":[{"name":"","type":"bool"}],"payable":False,"stateMutability":"nonpayable","type":"function"},{"constant":True,"inputs":[{"name":"_Txid","type":"string"}],"name":"getTxTag","outputs":[{"name":"","type":"bool"}],"payable":False,"stateMutability":"view","type":"function"},{"constant":True,"inputs":[],"name":"get_StudentList","outputs":[{"name":"","type":"uint256[]"}],"payable":False,"stateMutability":"view","type":"function"},{"constant":True,"inputs":[],"name":"course_tmp","outputs":[{"name":"CourseID","type":"uint256"},{"name":"CourseName","type":"string"},{"name":"Compulsory","type":"bool"},{"name":"Term","type":"uint256"},{"name":"Credit","type":"uint256"}],"payable":False,"stateMutability":"view","type":"function"},{"constant":True,"inputs":[],"name":"manager_tmp","outputs":[{"name":"ManagerID","type":"uint256"},{"name":"ManagerAddr","type":"address"}],"payable":False,"stateMutability":"view","type":"function"},{"constant":True,"inputs":[],"name":"get_TeacherList","outputs":[{"name":"","type":"uint256[]"}],"payable":False,"stateMutability":"view","type":"function"},{"constant":True,"inputs":[{"name":"_CourseID","type":"uint256"}],"name":"courseIDExist","outputs":[{"name":"","type":"bool"}],"payable":False,"stateMutability":"view","type":"function"},{"constant":True,"inputs":[{"name":"_ManagerAddr","type":"address"}],"name":"managerAddrExist","outputs":[{"name":"","type":"bool"}],"payable":False,"stateMutability":"view","type":"function"},{"constant":True,"inputs":[],"name":"get_ManagerList","outputs":[{"name":"","type":"uint256[]"}],"payable":False,"stateMutability":"view","type":"function"},{"constant":True,"inputs":[{"name":"_CourseID","type":"uint256"}],"name":"getStuMarksByCourseAll","outputs":[{"name":"","type":"uint256[]"},{"name":"","type":"uint256[]"}],"payable":False,"stateMutability":"view","type":"function"},{"constant":True,"inputs":[{"name":"_ManagerID","type":"uint256"}],"name":"managerIDExist","outputs":[{"name":"","type":"bool"}],"payable":False,"stateMutability":"view","type":"function"},{"constant":True,"inputs":[],"name":"get_safeNumberForOwner","outputs":[{"name":"","type":"uint8"}],"payable":False,"stateMutability":"view","type":"function"},{"constant":True,"inputs":[{"name":"_StudentID","type":"uint256"}],"name":"len_sCourseIDs","outputs":[{"name":"","type":"uint256"}],"payable":False,"stateMutability":"view","type":"function"},{"constant":True,"inputs":[],"name":"stu_tmp","outputs":[{"name":"StudentID","type":"uint256"},{"name":"StudentName","type":"string"},{"name":"StudentClass","type":"uint256"},{"name":"StudentAddr","type":"address"}],"payable":False,"stateMutability":"view","type":"function"},{"constant":False,"inputs":[{"name":"_LogContract","type":"address"}],"name":"setLogAddress","outputs":[{"name":"","type":"bool"}],"payable":False,"stateMutability":"nonpayable","type":"function"},{"constant":True,"inputs":[{"name":"_StudentAddr","type":"address"}],"name":"studentAddrExist","outputs":[{"name":"","type":"bool"}],"payable":False,"stateMutability":"view","type":"function"},{"constant":True,"inputs":[],"name":"tch_tmp","outputs":[{"name":"TeacherID","type":"uint256"},{"name":"TeacherName","type":"string"},{"name":"TeacherAddr","type":"address"}],"payable":False,"stateMutability":"view","type":"function"},{"constant":True,"inputs":[{"name":"_TeacherID","type":"uint256"}],"name":"teacherIDExist","outputs":[{"name":"","type":"bool"}],"payable":False,"stateMutability":"view","type":"function"},{"constant":False,"inputs":[{"name":"_newOwner","type":"address"}],"name":"transferOwnerShip","outputs":[{"name":"","type":"bool"}],"payable":False,"stateMutability":"nonpayable","type":"function"},{"constant":False,"inputs":[{"name":"_SuperUser","type":"address"}],"name":"setSuperUser","outputs":[{"name":"","type":"bool"}],"payable":False,"stateMutability":"nonpayable","type":"function"},{"constant":False,"inputs":[{"name":"_Txid","type":"string"},{"name":"_CourseID","type":"uint256"},{"name":"_StudentID","type":"uint256"},{"name":"_requestTime","type":"uint256"}],"name":"stuChooseCourse","outputs":[{"name":"","type":"bool"}],"payable":False,"stateMutability":"nonpayable","type":"function"},{"constant":False,"inputs":[{"name":"_Txid","type":"string"},{"name":"_TeacherID","type":"uint256"},{"name":"_CourseID","type":"uint256"},{"name":"_StudentID","type":"uint256"},{"name":"_Marks","type":"uint256[]"}],"name":"setStuMark","outputs":[{"name":"boolValue","type":"bool"},{"name":"mark","type":"uint256"}],"payable":False,"stateMutability":"nonpayable","type":"function"},{"constant":False,"inputs":[{"name":"_Txid","type":"string"},{"name":"_TeacherID","type":"uint256"}],"name":"addTchInfo","outputs":[{"name":"","type":"bool"}],"payable":False,"stateMutability":"nonpayable","type":"function"},{"constant":True,"inputs":[{"name":"_StudentID","type":"uint256"}],"name":"studentIDExist","outputs":[{"name":"","type":"bool"}],"payable":False,"stateMutability":"view","type":"function"},{"constant":True,"inputs":[],"name":"getEnableTxTag","outputs":[{"name":"","type":"bool"}],"payable":False,"stateMutability":"view","type":"function"},{"constant":True,"inputs":[],"name":"Owner","outputs":[{"name":"","type":"address"}],"payable":False,"stateMutability":"view","type":"function"},{"constant":False,"inputs":[{"name":"_Txid","type":"string"},{"name":"_ManagerID","type":"uint256"}],"name":"addManagerInfo","outputs":[{"name":"","type":"bool"}],"payable":False,"stateMutability":"nonpayable","type":"function"},{"constant":True,"inputs":[{"name":"_StudentID","type":"uint256"},{"name":"_CourseID","type":"uint256"}],"name":"getStuMark","outputs":[{"name":"","type":"uint256"}],"payable":False,"stateMutability":"view","type":"function"},{"constant":True,"inputs":[],"name":"SuperUser","outputs":[{"name":"","type":"address"}],"payable":False,"stateMutability":"view","type":"function"},{"constant":False,"inputs":[{"name":"_Txid","type":"string"},{"name":"_CourseID","type":"uint256"},{"name":"_Compulsory","type":"bool"},{"name":"_Term","type":"uint256"},{"name":"_Credit","type":"uint256"},{"name":"_Percentage","type":"uint256[]"},{"name":"_TeacherID","type":"uint256"}],"name":"addCourseInfo","outputs":[{"name":"","type":"bool"}],"payable":False,"stateMutability":"nonpayable","type":"function"},{"constant":True,"inputs":[],"name":"get_CourseList","outputs":[{"name":"","type":"uint256[]"}],"payable":False,"stateMutability":"view","type":"function"},{"constant":False,"inputs":[{"name":"_Txid","type":"string"},{"name":"_Identity","type":"uint256"},{"name":"_ID","type":"uint256"},{"name":"_Addr","type":"address"}],"name":"addAccount","outputs":[{"name":"","type":"bool"}],"payable":False,"stateMutability":"nonpayable","type":"function"},{"constant":True,"inputs":[{"name":"_CourseID","type":"uint256"}],"name":"len_cStuIDs","outputs":[{"name":"","type":"uint256"}],"payable":False,"stateMutability":"view","type":"function"},{"constant":False,"inputs":[{"name":"value","type":"bool"}],"name":"setEnableTxTag","outputs":[],"payable":False,"stateMutability":"nonpayable","type":"function"},{"constant":True,"inputs":[],"name":"LogContract","outputs":[{"name":"","type":"address"}],"payable":False,"stateMutability":"view","type":"function"},{"constant":True,"inputs":[{"name":"_CourseID","type":"uint256"},{"name":"_StudentID","type":"uint256"}],"name":"getStuMarksByCourse","outputs":[{"name":"","type":"uint256"}],"payable":False,"stateMutability":"view","type":"function"},{"inputs":[],"payable":False,"stateMutability":"nonpayable","type":"constructor"},{"anonymous":False,"inputs":[{"indexed":False,"name":"newSuperUser","type":"address"}],"name":"SetSuperUser","type":"event"},{"anonymous":False,"inputs":[{"indexed":False,"name":"newOwner","type":"address"}],"name":"TransferOwnerShip","type":"event"},{"anonymous":False,"inputs":[{"indexed":False,"name":"newLogContract","type":"address"}],"name":"SetLogAddress","type":"event"},{"anonymous":False,"inputs":[{"indexed":True,"name":"txid","type":"string"},{"indexed":True,"name":"Success","type":"bool"},{"indexed":True,"name":"Operator","type":"address"}],"name":"TxMined","type":"event"}]

# contract_address = "0x97c5d8f515f967d247552fc73cd19840bd58edcd"
#  本地链地址

contract_address = "0x94a82b0f4db0d63b488f3f9458c24c9f0ac71ba8"
# 服务器链地址

super_manager_address = "0xb36943d9ee7d3a2f82460bec0cd149427d54150f"
# 本地超级管理员

# super_manager_address = "0x608f28d66a51d7d1b9851fca91b913543138a055"
# 服务器超级管理员


def login(request):
    dict = {}
    meta = {}
    data = {}
    _blockchain = {}
    dict["meta"] = meta
    dict["data"] = data
    try:
        if request.method == 'POST':
            req = simplejson.loads(request.body)
            user = req['user']
            _account = user['account']
            _password = user['password']
            if _account == "" or _password == "":
                info = "Syntax Error Or Parameter Error"
                # return HttpResponseForbidden(info)
            elif len(Login.objects.filter(account=_account)) == 1:
                check = Login.objects.get(account=_account)
                if check.LoginPassword == _password:
                    _accounttype = check.accountType
                    data['type'] = _accounttype
                    data['uid'] = check.uid
                    if len(Token.objects.filter(user_id=check.account)) == 1:
                        Token.objects.filter(user_id=check.account).delete()
                    newtoken = Token.objects.create(user=check)
                    data['token'] = newtoken.key

                    if check.address is None and check.unlockPassword is None:
                    # if str(check.address) == "" and str(check.unlockPassword) == "":
                        data['address_exist'] = "0"
                        # info = "Success"
                        if _accounttype == "student":
                            if len(Student.objects.filter(sNo=_account)) == 1:
                                data['name'] = Student.objects.get(sNo=_account).sName
                                info = "Success"
                            else:
                                data['name'] = ""
                                info = "Account does not exist"
                        elif _accounttype == "teacher":
                            if len(Teacher.objects.filter(tNo=_account)) == 1:
                                data['name'] = Teacher.objects.get(tNo=_account).tName
                                info = "Success"
                            else:
                                data['name'] = ""
                                info = "Account does not exist"
                        elif _accounttype == "administrator":
                            if len(Manager.objects.filter(mNo=_account)) == 1:
                                data['name'] = Manager.objects.get(mNo=_account).mName
                                info = "Success"
                            else:
                                data['name'] = ""
                                info = "Account does not exist"
                        else:
                            info = "Wrong type. Please notify the administrator."
                        # data['name'] = _name
                    else:
                        if _accounttype == "student":
                            if len(Student.objects.filter(sNo=_account)) == 1:
                                data['name'] = Student.objects.get(sNo=_account).sName
                                info = "Success"
                            else:
                                data['name'] = ""
                                info = "Account does not exist"
                        elif _accounttype == "teacher":
                            if len(Teacher.objects.filter(tNo=_account)) == 1:
                                data['name'] = Teacher.objects.get(tNo=_account).tName
                                info = "Success"
                            else:
                                data['name'] = ""
                                info = "Account does not exist"
                        elif _accounttype == "administrator":
                            if len(Manager.objects.filter(mNo=_account)) == 1:
                                data['name'] = Manager.objects.get(mNo=_account).mName
                                info = "Success"
                            else:
                                data['name'] = ""
                                info = "Account does not exist"
                        else:
                            info = "Wrong type. Please notify the administrator."
                        data['address_exist'] = "1"
                        _blockchain['address'] = check.address
                        _blockchain['password_unlock'] = check.unlockPassword
                    data['blockchain'] = _blockchain

                else:
                    info = "Wrong password."
            else:
                info = "Account does not exist"
        else:
            info = "Wrong request method."
    except:
        import sys
        info = "%s || %s" % (sys.exc_info()[0], sys.exc_info()[1])
        # info = "Syntax error Or parameter error."
        meta['message'] = info
        meta['code'] = "400"
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


def addresspasswordsent(request):
    dict = {}
    meta = {}
    data = {}
    # _blockchain = {}
    dict["meta"] = meta
    dict["data"] = data
    try:
        w3 = Web3(HTTPProvider("http://localhost:8545"))
        contract_instance = w3.eth.contract(contract_abi, contract_address, ContractFactoryClass=ConciseContract)
        if request.method == 'POST':
            req = simplejson.loads(request.body)
            _uid = req['uid']
            # _timestamp = req['timestamp']
            _blockchain = req['block_chain']
            _address = _blockchain['address']
            _password = _blockchain['password_unlock']
            super_manager_uid = Login.objects.get(account=3).uid

            r = str(math.floor(random.random() * 10 ** 10))
            r.zfill(10)
            _txid = '%s%s%s' % (super_manager_uid, str(int(time.time())), str(r))

            # _txid = super_manager_uid + _timestamp

            if _uid == "" or _address == "" or _password == "":
                info = "Syntax Error Or Parameter Error"
            elif len(Login.objects.filter(uid=_uid)) == 1:
                check = Login.objects.get(uid=_uid)
                if check.address is None and check.unlockPassword is None:
                    Login.objects.filter(uid=_uid).update(address=_address, unlockPassword=_password)
                    data['type'] = check.accountType
                    _accounttype = check.accountType
                    _account = check.account
                    if _accounttype == "student":
                        if len(Student.objects.filter(sNo=_account)) == 1:
                            Student.objects.filter(sNo=_account).update(sAddress=_address, sUnlockPassword=_password)
                            contract_instance.addAccount(_txid, 0, _account, _address,
                                                         transact={'from': super_manager_address, 'gas': 400000})
                            w3.eth.sendTransaction({'from': super_manager_address, 'to': _address, 'value': amount,
                                                    'gas': 400000})
                            new_tx = ContractAddress(txid=_txid, times=0, accountType=0, account=_account,
                                                     address=_address)
                            new_tx.save()
                            info = "Success"
                        else:
                            info = "Account does not exist"
                    elif _accounttype == "teacher":
                        if len(Teacher.objects.filter(tNo=_account)) == 1:
                            Teacher.objects.filter(tNo=_account).update(tAddress=_address, tUnlockPassword=_password)
                            contract_instance.addAccount(_txid, 1, _account, _address,
                                                         transact={'from': super_manager_address, 'gas': 400000})
                            new_tx = ContractAddress(txid=_txid, times=0, accountType=1, account=_account,
                                                     address=_address)
                            new_tx.save()
                            info = "Success"
                        else:
                            info = "Account does not exist"
                    elif _accounttype == "administrator":
                        if len(Manager.objects.filter(mNo=_account)) == 1:
                            Manager.objects.filter(mNo=_account).update(mAddress=_address, mUnlockPassword=_password)
                            contract_instance.addAccount(_txid, 2, _account, _address,
                                                         transact={'from': super_manager_address, 'gas': 400000})
                            new_tx = ContractAddress(txid=_txid, times=0, accountType=2, account=_account,
                                                     address=_address)
                            new_tx.save()
                            info = "Success"
                        else:
                            info = "Account does not exist"
                    else:
                        info = "Wrong type. Please notify the administrator."
                else:
                    info = "Address and password already exist"
            else:
                info = "ID not exist"
        else:
            info = "Wrong request method."
    except:
        import sys
        info = "%s || %s" % (sys.exc_info()[0], sys.exc_info()[1])
        # info = "Syntax error Or parameter error."
        meta['message'] = info
        meta['code'] = "400"
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


def addresspasswordquery(request):
    dict = {}
    meta = {}
    data = {}
    # _blockchain = {}
    dict["meta"] = meta
    dict["data"] = data
    try:
        if request.method == 'POST':
            req = simplejson.loads(request.body)
            _uid = req['uid']
            # _token = req['token']
            if _uid == "":
                info = "Syntax Error Or Parameter Error"
            elif len(Login.objects.filter(uid=_uid)) == 1:
                data['address'] = Login.objects.get(uid=_uid).address
                data['unlock_password'] = Login.objects.get(uid=_uid).unlockPassword
                info = "Success"
            else:
                info = "Account not exist"
        else:
            info = "Wrong request method"
    except:
        import sys
        info = "%s || %s" % (sys.exc_info()[0], sys.exc_info()[1])
        # info = "Syntax error Or parameter error."
        meta['message'] = info
        meta['code'] = "400"
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


# def checktoken(uid, token):


def supermanager(request):
    dict = {}
    meta = {}
    dict["meta"] = meta
    try:
        if request.method == "POST":
            reqbody = simplejson.loads(request.body)

            _user = reqbody['user']
            _password = reqbody['password']

            _mid = 3
            _mpassword = "123456"
            _mname = "SuperManager"
            _uid = str(_mid) + str(int(time.time()))

            if _user == "lab1017" and _password == r"d.,.53bff4":
                if len(Manager.objects.filter(mNo=_mid)) > 0 or len(Login.objects.filter(account=_mid)) > 0:
                    info = "The manager already exists"
                else:
                    newmanager = Manager(mNo=_mid, mName=_mname, LoginPassword=_mpassword)
                    newmanager.save()

                    _type = "administrator"
                    # newlogin = Login(uid=_uid, account=_mid, accountType=_type, LoginPassword=_mpassword)
                    newlogin = Login(uid=_uid, account=_mid, accountType=_type, LoginPassword=_mpassword,
                                     id=_mid, password=_mpassword, is_superuser=0, username=_mid, first_name="blank",
                                     last_name="blank", email="null@null.com", is_staff=0, is_active=0,
                                     date_joined=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
                    newlogin.save()

                    info = "Success"
            else:
                info = "Wrong user or password"

        else:
            info = "Wrong request method."
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


def auth(request):
    dict = {}
    meta = {}
    dict["meta"] = meta
    try:
        if request.method == 'POST':
            reqbody = simplejson.loads(request.body)
            req_user = reqbody['user']
            _requid = req_user['uid']
            _reqtoken = req_user['token']
            _reqtype = reqbody['interface']

            if len(Token.objects.filter(key=_reqtoken)) != 1 or len(Login.objects.filter(uid=_requid)) != 1 or Token.objects.get(key=_reqtoken).user_id != Login.objects.get(uid=_requid).account or _reqtype != Login.objects.get(uid=_requid).accountType:
                info = "NotAuthorized"

            elif time.time() - time.mktime(Token.objects.get(key=_reqtoken).created.timetuple()) > AuthorizedTime:
                Token.objects.filter(key=_reqtoken).delete()
                info = "NotAuthorized"

            else:
                info = "Success"
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


def tokenauth(_requid, _reqtoken):
    if len(Token.objects.filter(key=_reqtoken)) == 1 and len(Login.objects.filter(uid=_requid)) == 1 and Token.objects.get(key=_reqtoken).user_id == Login.objects.get(uid=_requid).account and len(Token.objects.filter(key=_reqtoken, user_id=Login.objects.get(uid=_requid).account)) == 1:
        if time.time() - time.mktime(Token.objects.get(key=_reqtoken).created.timetuple()) <= AuthorizedTime:
            return True
        else:
            Token.objects.filter(key=_reqtoken, user_id=Login.objects.get(uid=_requid).account).delete()
            return False
    else:
        return False

