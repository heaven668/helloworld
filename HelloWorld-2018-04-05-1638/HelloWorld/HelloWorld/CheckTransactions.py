# -*- coding: utf-8 -*-

import json
import time
import simplejson
import math
import random

from threading import Timer

from web3 import Web3, HTTPProvider
from web3.contract import ConciseContract

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
from lab1017.models import ContractManagerInfo
from lab1017.models import ContractTeacherInfo
from lab1017.models import ContractCourseInfo
from lab1017.models import ContractTeacherCourseInfo
from lab1017.models import ContractAddress
from lab1017.models import ContractMark
from lab1017.models import ContractSelectCourse

from HelloWorld.Common import tokenauth
from HelloWorld.Common import contract_abi
from HelloWorld.Common import contract_address
from HelloWorld.Common import super_manager_address


def checkall(request):
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
                # info = checkstudentinfo(_requid)
                # poll(_requid)
                # info = checkcourseinfo(_requid)
                # info = checkstudentinfo(_requid)
                # info = checkcourseinfo(_requid)
                # info = checkteacherinfo(_requid)
                # checkaddress(_requid)
                # checkstudentinfo(_requid)
                # checkmanagerinfo(_requid)
                # checkteacherinfo(_requid)
                checkcourseinfo(_requid)
                # checkmark(_requid)
                # checkselectcourse(_requid)
                info = "Success"
            else:
                info = "NotAuthorized"
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


def checkaddress(_uid):
    try:
        w3 = Web3(HTTPProvider("http://localhost:8545"))
        contract_instance = w3.eth.contract(contract_abi, contract_address, ContractFactoryClass=ConciseContract)
        tx_list = ContractAddress.objects.filter()
        # info = ""
        if len(tx_list) > 0:

            for tx in tx_list:
                tx_success = contract_instance.getTxTag(tx.txid, call={'from': super_manager_address})
                # info = "test"
                if tx_success:
                    ContractAddress.objects.filter(txid=tx.txid).delete()
                    # info = "Success"
                else:
                    r = str(math.floor(random.random() * 10**10))
                    r.zfill(10)
                    new_txid = '%s%s%s' % (_uid, str(int(time.time())), str(r))
                    # new_txid = _uid + str(int(time.time()))
                    tx_hash = contract_instance.addAccount(new_txid, int(tx.accountType), int(tx.account), tx.address,
                                                           transact={'from': super_manager_address, 'gas': 400000})
                    ContractAddress.objects.filter(txid=tx.txid).update(txid=new_txid, times=tx.times+1)
                    # info = "Resending" + str(tx_hash)
            # info = ""
        else:
            # info = "No tx"
            pass

        info = "Success"

    except:
        import sys
        info = "%s || %s" % (sys.exc_info()[0], sys.exc_info()[1])
        # info = "Syntax error Or parameter error."

    return info


def checkstudentinfo(_uid):
    try:
        w3 = Web3(HTTPProvider("http://localhost:8545"))
        contract_instance = w3.eth.contract(contract_abi, contract_address, ContractFactoryClass=ConciseContract)
        tx_list = ContractStudentInfo.objects.filter()
        # info = ""
        if len(tx_list) > 0:

            for tx in tx_list:

                # info = tx.sName

                tx_success = contract_instance.getTxTag(tx.txid, call={'from': super_manager_address})
                info = "test"
                if tx_success:
                    ContractStudentInfo.objects.filter(txid=tx.txid).delete()
                    info = "Success"
                else:
                    r = str(math.floor(random.random() * 10**10))
                    r.zfill(10)
                    new_txid = '%s%s%s' % (_uid, str(int(time.time())), str(r))
                    # new_txid = _uid + str(int(time.time()))
                    tx_hash = contract_instance.addStuInfo(new_txid, tx.sNo, tx.sClass,
                                                           transact={'from': super_manager_address, 'gas': 400000})
                    # tx_hash = contract_instance.addStuInfo(new_txid, tx.sNo, u'u738b', tx.sClass,
                    #                                        transact={'from': super_manager_address, 'gas': 400000})
                    ContractStudentInfo.objects.filter(txid=tx.txid).update(txid=new_txid, times=tx.times+1)
                    info = "Resending"
                    info = tx.sName.encode('latin-1', 'ignore')
                    # + str(tx_hash)

            # info = ""
        else:
            info = "No tx"
            # info = u'\u738b'
            pass

        info = "Success"

    except:
        import sys
        info = "%s || %s" % (sys.exc_info()[0], sys.exc_info()[1])
        # info = "Syntax error Or parameter error."

    return info


def checkmanagerinfo(_uid):
    try:
        w3 = Web3(HTTPProvider("http://localhost:8545"))
        contract_instance = w3.eth.contract(contract_abi, contract_address, ContractFactoryClass=ConciseContract)
        tx_list = ContractManagerInfo.objects.filter()
        # info = ""
        if len(tx_list) > 0:

            for tx in tx_list:
                tx_success = contract_instance.getTxTag(tx.txid, call={'from': super_manager_address})
                # info = "test"
                if tx_success:
                    ContractManagerInfo.objects.filter(txid=tx.txid).delete()
                    # info = "Success"
                else:
                    r = str(math.floor(random.random() * 10 ** 10))
                    r.zfill(10)
                    new_txid = '%s%s%s' % (_uid, str(int(time.time())), str(r))
                    # new_txid = _uid + str(int(time.time()))
                    tx_hash = contract_instance.addManagerInfo(new_txid, tx.mNo,
                                                               transact={'from': super_manager_address, 'gas': 400000})
                    ContractManagerInfo.objects.filter(txid=tx.txid).update(txid=new_txid, times=tx.times+1)
                    # info = "Resending" + str(tx_hash)
            # info = ""
        else:
            # info = "No tx"
            pass

        info = "Success"

    except:
        import sys
        info = "%s || %s" % (sys.exc_info()[0], sys.exc_info()[1])
        # info = "Syntax error Or parameter error."

    return info


def checkteacherinfo(_uid):
    try:
        w3 = Web3(HTTPProvider("http://localhost:8545"))
        contract_instance = w3.eth.contract(contract_abi, contract_address, ContractFactoryClass=ConciseContract)
        tx_list = ContractTeacherInfo.objects.filter()
        # info = ""
        if len(tx_list) > 0:

            for tx in tx_list:
                # info = str(tx.tName)

                tx_success = contract_instance.getTxTag(tx.txid, call={'from': super_manager_address})
                # info = "test"
                if tx_success:
                    ContractTeacherInfo.objects.filter(txid=tx.txid).delete()
                    # info = "Success"
                else:
                    r = str(math.floor(random.random() * 10 ** 10))
                    r.zfill(10)
                    new_txid = '%s%s%s' % (_uid, str(int(time.time())), str(r))
                    # new_txid = _uid + str(int(time.time()))
                    tx_hash = contract_instance.addTchInfo(new_txid, tx.tNo,
                                                           transact={'from': super_manager_address, 'gas': 400000})
                    ContractTeacherInfo.objects.filter(txid=tx.txid).update(txid=new_txid, times=tx.times+1)
                    # info = "Resending" + str(tx_hash)

            # info = ""
        else:
            info = "No tx"
            pass

        info = "Success"

    except:
        import sys
        info = "%s || %s" % (sys.exc_info()[0], sys.exc_info()[1])
        # info = "Syntax error Or parameter error."

    return info


def checkcourseinfo(_uid):
    try:
        w3 = Web3(HTTPProvider("http://localhost:8545"))
        contract_instance = w3.eth.contract(contract_abi, contract_address, ContractFactoryClass=ConciseContract)
        tx_list = ContractCourseInfo.objects.filter()
        # info = ""
        if len(tx_list) > 0:
            info = "test"
            for tx in tx_list:
                tx_success = contract_instance.getTxTag(tx.txid, call={'from': super_manager_address})

                if tx_success:
                    ContractCourseInfo.objects.filter(txid=tx.txid).delete()
                    ContractTeacherCourseInfo.objects.filter(txid=tx.txid).delete()
                    info = "Success"
                else:
                    r = str(math.floor(random.random() * 10 ** 10))
                    r.zfill(10)
                    new_txid = '%s%s%s' % (_uid, str(int(time.time())), str(r))
                    # new_txid = _uid + str(int(time.time()))
                    _term, _composition, _nature = formatcourseinfo(tx.cGrade, tx.cTerm, tx.cComposition, tx.cNature)
                    teacher_id = ContractTeacherCourseInfo.objects.get(txid=tx.txid).tNo

                    tx_hash = contract_instance.addCourseInfo(new_txid, tx.cNo, _nature, _term, tx.cCredit,
                                                              _composition, teacher_id,
                                                              transact={'from': super_manager_address, 'gas': 400000})
                    ContractCourseInfo.objects.filter(txid=tx.txid).update(txid=new_txid, times=tx.times+1)
                    ContractTeacherCourseInfo.objects.filter(txid=tx.txid).update(txid=new_txid, times=tx.times + 1)
                    info = "Resending" + str(tx_hash)
            # info = ""
        else:
            info = "No tx"
            pass

        # info = "Success"

    except:
        import sys
        info = "%s || %s" % (sys.exc_info()[0], sys.exc_info()[1])
        # info = "Syntax error Or parameter error."

    return info


def checkmark(_uid):
    try:
        w3 = Web3(HTTPProvider("http://localhost:8545"))
        contract_instance = w3.eth.contract(contract_abi, contract_address, ContractFactoryClass=ConciseContract)
        tx_list = ContractMark.objects.filter()
        # info = ""
        if len(tx_list) > 0:

            for tx in tx_list:
                tx_success = contract_instance.getTxTag(tx.txid, call={'from': super_manager_address})
                # info = "test"
                if tx_success:
                    ContractMark.objects.filter(txid=tx.txid).delete()
                    # info = "Success"
                else:
                    r = str(math.floor(random.random() * 10 ** 10))
                    r.zfill(10)
                    new_txid = '%s%s%s' % (_uid, str(int(time.time())), str(r))
                    # new_txid = _uid + str(int(time.time()))
                    _mark = formatmark(tx.mark)
                    tx_hash = contract_instance.setStuMark(new_txid, tx.tNo, tx.cNo, tx.sNo, _mark,
                                                           transact={'from': super_manager_address, 'gas': 400000})
                    ContractMark.objects.filter(txid=tx.txid).update(txid=new_txid, times=tx.times+1)
                    # info = "Resending" + str(tx_hash)
            # info = ""
        else:
            # info = "No tx"
            pass

        info = "Success"

    except:
        import sys
        info = "%s || %s" % (sys.exc_info()[0], sys.exc_info()[1])
        # info = "Syntax error Or parameter error."

    return info


def checkselectcourse(_uid):
    try:
        w3 = Web3(HTTPProvider("http://localhost:8545"))
        contract_instance = w3.eth.contract(contract_abi, contract_address, ContractFactoryClass=ConciseContract)
        tx_list = ContractSelectCourse.objects.filter()
        # info = ""
        if len(tx_list) > 0:

            for tx in tx_list:
                tx_success = contract_instance.getTxTag(tx.txid, call={'from': super_manager_address})
                # info = "test"
                if tx_success:
                    ContractSelectCourse.objects.filter(txid=tx.txid).delete()
                    # info = "Success"
                else:
                    r = str(math.floor(random.random() * 10 ** 10))
                    r.zfill(10)
                    new_txid = '%s%s%s' % (_uid, str(int(time.time())), str(r))
                    # new_txid = _uid + str(int(time.time()))
                    tx_hash = contract_instance.stuChooseCourse(new_txid, tx.cNo, tx.sNo, int(tx.timestamp),
                                                                transact={'from': super_manager_address, 'gas': 400000})
                    ContractSelectCourse.objects.filter(txid=tx.txid).update(txid=new_txid, times=tx.times+1)
                    # info = "Resending" + str(tx_hash)
            # info = ""
        else:
            # info = "No tx"
            pass

        info = "Success"

    except:
        import sys
        info = "%s || %s" % (sys.exc_info()[0], sys.exc_info()[1])
        # info = "Syntax error Or parameter error."

    return info


def formatcourseinfo(_grade, _term, _composition, _nature):
    d_grade = {'大一': '001', '大二': '002', '大三': '003', '大四': '004', '研究生': '011', '博士': '101'}
    d_term = {'上学期': '0', '下学期': '1'}
    try:
        format_term = int(d_grade[_grade] + d_term[_term])
        format_composition = [int(_composition)]
        if _nature == "必修":
            format_nature = True
        else:
            format_nature = False
        return format_term, format_composition, format_nature

    except:
        pass


def formatmark(_mark):
    format_mark = [int(_mark)]
    return format_mark


def poll(_uid):
    checkaddress(_uid)
    checkstudentinfo(_uid)
    checkmanagerinfo(_uid)
    checkteacherinfo(_uid)
    checkcourseinfo(_uid)
    checkmark(_uid)
    checkselectcourse(_uid)

    # t = Timer(300, poll(_uid))
    # t.start()


# contract_abi, contract_address, super_manager_address REQUIRED
# 2018/03/25    Tsai

# function checkcourseinfo need to be reviewed
# function checkmark _mark need to be assigned
# 2018/03/31    Tsai

# function formatmark need to be modified
