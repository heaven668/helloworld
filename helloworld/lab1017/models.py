# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Course(models.Model):
    cNo = models.IntegerField(primary_key=True)
    cName = models.CharField(max_length=40)
    cCredit = models.IntegerField()
    cNature = models.CharField(max_length=10)
    cNumber = models.IntegerField()
    cMajor = models.CharField(max_length=1000)
    cGrade = models.CharField(max_length=20)
    cTerm = models.CharField(max_length=40)
    cComposition = models.CharField(max_length=5000, default="期末:100%")
    cIntroduction = models.CharField(max_length=5000, null=True, blank=True)


class CourseMaterial(models.Model):
    cNo = models.ForeignKey('Course', on_delete=models.CASCADE)
    cMaterialsHash = models.CharField(max_length=100)
    cMaterialsName = models.CharField(max_length=1000)
    cMaterialsType = models.CharField(max_length=10)
    cMaterialsSize = models.CharField(max_length=10)
    cMaterialsTime = models.DateField(auto_now=True)


class Student(models.Model):
    sNo = models.IntegerField(primary_key=True)
    sName = models.CharField(max_length=40)
    sGender = models.CharField(max_length=10)
    sClass = models.IntegerField()
    sMajor = models.CharField(max_length=40)
    sSchool = models.CharField(max_length=40)
    sGrade = models.CharField(max_length=10)
    LoginPassword = models.CharField(max_length=20)
    sAddress = models.CharField(max_length=42, unique=True, null=True, blank=True)
    sUnlockPassword = models.CharField(max_length=20, null=True, blank=True)
    sTelephone = models.IntegerField(null=True, blank=True)
    sEmail = models.CharField(max_length=5000, null=True, blank=True)


class StudentCourse(models.Model):
    cNo = models.ForeignKey('Course', on_delete=models.CASCADE)
    sNo = models.ForeignKey('Student', on_delete=models.CASCADE)
    status = models.CharField(max_length=10)


class Teacher(models.Model):
    tNo = models.IntegerField(primary_key=True)
    tName = models.CharField(max_length=40)
    tSchool = models.CharField(max_length=40)
    LoginPassword = models.CharField(max_length=20)
    tAddress = models.CharField(max_length=42, unique=True, null=True, blank=True)
    tUnlockPassword = models.CharField(max_length=20, null=True, blank=True)
    tTelephone = models.CharField(max_length=11, null=True, blank=True)
    tEmail = models.CharField(max_length=5000, null=True, blank=True)


class Manager(models.Model):
    mNo = models.IntegerField(primary_key=True)
    mName = models.CharField(max_length=40)
    LoginPassword = models.CharField(max_length=20)
    mAddress = models.CharField(max_length=42, unique=True, null=True, blank=True)
    mUnlockPassword = models.CharField(max_length=20, null=True, blank=True)
    mTelephone = models.CharField(max_length=11, null=True, blank=True)
    mEmail = models.CharField(max_length=5000, null=True, blank=True)


class Question(models.Model):
    qNo = models.IntegerField(primary_key=True)
    cNo = models.ForeignKey('Course', on_delete=models.CASCADE)
    qQuestion = models.CharField(max_length=5000)
    qOption = models.CharField(max_length=5000)
    qAnswer = models.CharField(max_length=10)


class TeacherCourse(models.Model):
    cNo = models.ForeignKey('Course', on_delete=models.CASCADE)
    tNo = models.ForeignKey('Teacher', on_delete=models.CASCADE)
    sClass = models.CharField(max_length=256, null=True, blank=True)


class TeacherCourseApply(models.Model):
    cNo = models.ForeignKey('Course', on_delete=models.CASCADE)
    tNo = models.ForeignKey('Teacher', on_delete=models.CASCADE)
    status = models.CharField(max_length=10)


class TeacherNewCourseApply(models.Model):
    ncacNo = models.IntegerField(primary_key=True)
    ncacName = models.CharField(max_length=40)
    ncacCredit = models.IntegerField()
    ncacNature = models.CharField(max_length=10)
    ncacNumber = models.IntegerField()
    ncacMajor = models.CharField(max_length=1000)
    ncacGrade = models.CharField(max_length=20)
    ncacTerm = models.CharField(max_length=40)
    ncacComposition = models.CharField(max_length=5000, default="期末:100%")
    ncacIntroduction = models.CharField(max_length=5000, null=True, blank=True)
    ncatNo = models.ForeignKey('Teacher', on_delete=models.CASCADE)
    ncaStatus = models.CharField(max_length=10)


class Login(User):
    uid = models.CharField(unique=True, max_length=40)
    account = models.IntegerField(primary_key=True)
    accountType = models.CharField(max_length=13)
    LoginPassword = models.CharField(max_length=20)
    address = models.CharField(max_length=42, unique=True, null=True, blank=True)
    unlockPassword = models.CharField(max_length=20, null=True, blank=True)


class ContractStudentInfo(models.Model):
    txid = models.CharField(unique=True, max_length=100)
    times = models.IntegerField()
    sNo = models.IntegerField()
    sName = models.CharField(max_length=40)
    sClass = models.IntegerField()


class ContractManagerInfo(models.Model):
    txid = models.CharField(unique=True, max_length=100)
    times = models.IntegerField()
    mNo = models.IntegerField()


class ContractTeacherInfo(models.Model):
    txid = models.CharField(unique=True, max_length=100)
    times = models.IntegerField()
    tNo = models.IntegerField()
    tName = models.CharField(max_length=40)


class ContractCourseInfo(models.Model):
    txid = models.CharField(unique=True, max_length=100)
    times = models.IntegerField()
    cNo = models.IntegerField()
    cName = models.CharField(max_length=40)
    cCredit = models.IntegerField()
    cNature = models.CharField(max_length=10)
    cGrade = models.CharField(max_length=20)
    cTerm = models.CharField(max_length=40)
    cComposition = models.CharField(max_length=5000)


class ContractTeacherCourseInfo(models.Model):
    txid = models.CharField(unique=True, max_length=100)
    times = models.IntegerField()
    cNo = models.IntegerField()
    tNo = models.IntegerField()


class ContractAddress(models.Model):
    txid = models.CharField(unique=True, max_length=100)
    times = models.IntegerField()
    accountType = models.IntegerField()
    account = models.IntegerField()
    address = models.CharField(max_length=42, unique=True)


class ContractMark(models.Model):
    txid = models.CharField(unique=True, max_length=100)
    times = models.IntegerField()
    tNo = models.IntegerField()
    cNo = models.IntegerField()
    sNo = models.IntegerField()
    mark = models.CharField(max_length=100)


class ContractSelectCourse(models.Model):
    txid = models.CharField(unique=True, max_length=100)
    times = models.IntegerField()
    cNo = models.IntegerField()
    sNo = models.IntegerField()
    timestamp = models.CharField(max_length=40)
