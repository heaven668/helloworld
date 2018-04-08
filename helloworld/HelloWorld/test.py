# -*- coding: utf-8 -*-

import json
import time
import simplejson

import web3
import xlrd

from django.conf import settings

from django.http import HttpResponse
from django.http import HttpResponseForbidden
from django.http import HttpResponseBadRequest
from django.http import JsonResponse
from rest_framework.authtoken.models import Token

from web3 import Web3, HTTPProvider, TestRPCProvider
from web3.admin import Admin
from solc import compile_source, wrapper, compile_files
from web3.contract import ConciseContract
from web3.utils import filters
from web3 import eth

from lab1017.models import Course
from lab1017.models import Student
from lab1017.models import Teacher
from lab1017.models import Manager
from lab1017.models import TeacherCourse
from lab1017.models import Question
from lab1017.models import Login

from HelloWorld.Common import AuthorizedTime
from HelloWorld.Common import compiled_sol

contract_source_code = '''
pragma solidity ^0.4.4;

contract Metacoin {
	mapping (address => uint) balances;

	event Transfer(address indexed _from, address indexed _to, uint256 _value);

	function MetaCoin() {
		balances[tx.origin] = 10000;
	}

	function sendCoin(address receiver, uint amount) returns(bool sufficient) {
		if (balances[msg.sender] < amount) return false;
		balances[msg.sender] -= amount;
		balances[receiver] += amount;
		Transfer(msg.sender, receiver, amount);
		return true;
	}

	function getBalance(address addr) returns(uint) {
		return balances[addr];
	}
}
'''


def get_balance(request):
    dict = {}
    data = {}
    meta = {}
    dict["meta"] = meta
    dict["data"] = data

    w3 = Web3(HTTPProvider("http://localhost:8545"))


    # try:
    # compiled_sol = compile_source(contract_source_code)  # Compiled source code
    # compiled_sol = compile_files(["MetaCoin.sol"],output_values=['abi'])
    # contract_interface = compiled_sol['MetaCoin.sol:Metacoin']
    #
    metacoin_abi = [{'constant': False, 'inputs': [{'name': 'receiver', 'type': 'address'}, {'name': 'amount', 'type': 'uint256'}], 'name': 'sendCoin', 'outputs': [{'name': 'sufficient', 'type': 'bool'}], 'payable': False, 'stateMutability': 'nonpayable', 'type': 'function'}, {'constant': False, 'inputs': [], 'name': 'MetaCoin', 'outputs': [], 'payable': False, 'stateMutability': 'nonpayable', 'type': 'function'}, {'constant': True, 'inputs': [{'name': 'addr', 'type': 'address'}], 'name': 'getBalance', 'outputs': [{'name': '', 'type': 'uint256'}], 'payable': False, 'stateMutability': 'view', 'type': 'function'}, {'anonymous': False, 'inputs': [{'indexed': True, 'name': '_from', 'type': 'address'}, {'indexed': True, 'name': '_to', 'type': 'address'}, {'indexed': False, 'name': '_value', 'type': 'uint256'}], 'name': 'Transfer', 'type': 'event'}]

    # try:
    metacoin_instance = w3.eth.contract(metacoin_abi, "0x016ed8e1ece5a5962584143e87ccf20f5a0d048a",
                                        ContractFactoryClass=ConciseContract)
    # try:
    b = metacoin_instance.getBalance("0xc5af40009043617a2042634aa0e88eae350334ff",
                                     call={'from': "0xc5af40009043617a2042634aa0e88eae350334ff"})

    # data['balance'] = w3.eth.accounts[0]
    data['old_balance'] = b

    tx = metacoin_instance.sendCoin("0x2483144f5c99e7185aa47ceb3ecad347dfc3f668", 200,
                                    transact={'from': "0xc5af40009043617a2042634aa0e88eae350334ff", 'gas': 410000})
    data['tx'] = tx
    transaction_filter = eth.TransactionFilter(tx)

    b_new = metacoin_instance.getBalance("0x2483144f5c99e7185aa47ceb3ecad347dfc3f668",
                                         call={'from': "0x2483144f5c99e7185aa47ceb3ecad347dfc3f668"})
    data['new_balance'] = b_new

    info = "Success"
    # data['balance'] = w3.isConnected()
    # data['balance'] = wrapper.get_solc_binary_path()
    # except:
    #     import sys
    #     info = "%s || %s" % (sys.exc_info()[0], sys.exc_info()[1])
    #     # info = "Syntax Error Or Parameter Error"
    #     # dict['message'] = info
    #     meta['code'] = "400"
    #     meta['message'] = info
    #     jsonr = simplejson.dumps(dict)
    #     res = HttpResponseBadRequest(jsonr)
    #     res.__setitem__('Access-Control-Allow-Origin', '*')
    #     return res

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


def exceltest(request):
    dict = {}
    meta = {}
    data = {}
    dict["meta"] = meta
    dict["data"] = data
    try:
        if request.method == "POST":
            user = request.POST.get('user')
            file = request.FILES["testfile"]
            filename = '%s%s' % (settings.MEDIA_ROOT, file.name)
            # with open(filename, 'wb') as f:
            #     for _file in file.chunks():
            #         f.write(_file)

            file_data = xlrd.open_workbook(filename)
            table = file_data.sheets()[0]
            nrows = table.nrows
            ncols = table.ncols
            data['user'] = user
            data['nrows'] = nrows
            data['ncols'] = ncols
            data['cell(1, 0)'] = table.cell(1, 0).value
            info = "Success"
        else:
            info = "Failed"
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
