#-*- coding:utf-8 -*-
from django.shortcuts import render,render_to_response
from django.http import HttpResponse,HttpResponseRedirect
from django.template import RequestContext
from django import forms
from teachertree.models import Person,Teacher,Student

from django.contrib.auth.models import User
from django.contrib import auth
import json
import random
from datetime import *

class PersonForm(forms.Form):
    name = forms.CharField(label='姓名:',max_length=100)
    age = forms.IntegerField(label='年龄:')
    sex = forms.ChoiceField(label = '性别:',widget=forms.Select(),choices=([('男','男'),('女','女'),]),initial=2,)
    
class PersForm(forms.Form):

    email = forms.EmailField(label='电子邮件:')
    identity_card = forms.CharField(label='身份证号:',max_length=18)

    password = forms.CharField(label='密码:',widget=forms.PasswordInput())
    password2 = forms.CharField(label='再次输入密码:',widget=forms.PasswordInput())


    def clean_identity_card(self):
        identity_card = self.cleaned_data['identity_card']
        if len(identity_card) != 18:
            raise forms.ValidationError(u"identity_card invalid")
        else:
            try:
                Person.objects.get(identity_card=identity_card)
            except Person.DoesNotExist:
                return identity_card
            else:
                raise forms.ValidationError(u"identity_card has registered")
        
    def clean_password(self):
        password = self.cleaned_data['password']
        if len(password) <= 5:
            raise forms.ValidationError(u"password insecure")
        return password
        
    def clean_email(self):
        email = self.cleaned_data['email']
        try:
            Person.objects.get(email=email)
        except Person.DoesNotExist:
            return email
        else:
            raise forms.ValidationError("email already existed")
       
    def clean(self):
        cleaned_data = super(PersForm, self).clean()
        password = cleaned_data.get('password', '')
        password2 = cleaned_data.get('password2', '')

        if password != password2:
            raise forms.ValidationError(u"passwords not match")
        return cleaned_data


class UserForm(forms.Form): 
    username = forms.CharField(label='邮箱:',max_length=100)
    password = forms.CharField(label='密码:',widget=forms.PasswordInput())


def CreUser(request):
    if request.method =='POST':
        Se = PersForm(request.POST)
        Pe = PersonForm(request.POST)
        if Se.is_valid():
            P0 = Person(
                name = request.POST['name'],
                age = request.POST['age'],
                sex = request.POST['sex'],
                school = request.POST['school'],
                email = request.POST['email'],
                identity_card = request.POST['identity_card'],
                province = request.POST['province']
            )
            P0.save()
            user = User.objects.create_user(
                username = request.POST['email'],
                password = request.POST['password'])
            user.save()
            return render_to_response('registersuc.html')
        else:
            return render_to_response('register.html',{'Pe':Pe,'Se':Se},
                                      context_instance=RequestContext(request))
    else:
        Pe = PersonForm()
        Se = PersForm()
        return render_to_response('register.html',{'Pe':Pe,'Se':Se},
                                  context_instance=RequestContext(request))
            

#登陆
def login(req):
    errors = []
    if req.method == 'POST':
        if True:
            #获取表单用户密码
            username = req.POST['username']
            password = req.POST['password']
            #获取的表单数据与数据库进行比较
            user = auth.authenticate(username=username, password=password)
            if user is not None:
                #比较成功，跳转index
                auth.login(req, user)
                person = Person.objects.get(email=username)
                req.session['member_id'] = person.id
                return HttpResponseRedirect('/index/')
            else:
                #比较失败，还在login
                errors.append('用户名密码匹配错误，请重新输入')
#                return HttpResponseRedirect('/login/')
                return render_to_response('login1.html',{'errors':errors},
                                          context_instance=RequestContext(req))
    return render_to_response('login1.html',context_instance=RequestContext(req))

#登陆成功
def index(req):
    pid = req.session['member_id']
    person = Person.objects.get(id=pid)
    username = person.name
    return render_to_response('index.html' ,{'username':username})

#退出
def logout(req):
    try:
        del req.session['member_id']
        auth.logout(req)
    except KeyError:
        pass
    return HttpResponseRedirect('/login/')


def query(request):
    pid = request.session['member_id']
    person = Person.objects.get(id= pid)
    personname = []
    personname.append(person.name)
    personname.append(person.id)
    teachers = Teacher.objects.filter(pid = person.id)
    students = Student.objects.filter(pid = person.id)
    teacherlist=[]
    studentlist=[]
    if list(teachers) != []:
        for teacher in teachers:
            dicttmp={}
            name=Person.objects.get(id=teacher.tid).name
            dicttmp['pid']=teacher.pid.id
            dicttmp['tid']=teacher.tid
            dicttmp['name']=name
            dicttmp['date0']=str(teacher.date0)
            dicttmp['date1']=str(teacher.date1)
            teacherlist.append(dicttmp)
    if list(students) != []:
        for student in students:
            dicttmp1={}
            name=Person.objects.get(id=student.sid).name
            dicttmp1['pid']=student.pid.id
            dicttmp1['sid']=student.sid
            dicttmp1['name']=name
            dicttmp1['date0']=str(student.date0)
            dicttmp1['date1']=str(student.date1)
            studentlist.append(dicttmp1)
    if teacherlist == [] and studentlist == []:
        return render_to_response("searchresult.html")
    else:
        return render(request,'searchresult.html',{'person':json.dumps(personname),'teachers':json.dumps(teacherlist),'students':json.dumps(studentlist)})
    
    
def query2(request):
    pid = request.GET['idtemp']
    pid = int(pid)
    person = Person.objects.get(id= pid)
    teachers = Teacher.objects.filter(pid = person.id)
    students = Student.objects.filter(pid = person.id)
    ret=[[],[]]
    teacherlist=[]
    for teacher in teachers:
        dicttmp={}
        name=Person.objects.get(id=teacher.tid).name
        dicttmp['pid']=teacher.pid.id
        dicttmp['tid']=teacher.tid
        dicttmp['name']=name
        dicttmp['date0']=str(teacher.date0)
        dicttmp['date1']=str(teacher.date1)
        teacherlist.append(dicttmp)
    ret[0]=teacherlist
    studentlist=[]
    for student in students:
        dicttmp1={}
        name=Person.objects.get(id=student.sid).name
        dicttmp1['pid']=student.pid.id
        dicttmp1['sid']=student.sid
        dicttmp1['name']=name
        dicttmp1['date0']=str(student.date0)
        dicttmp1['date1']=str(student.date1)
        studentlist.append(dicttmp1)
    ret[1]=studentlist
    return HttpResponse(json.dumps(ret),content_type='application/json')
    
def queryothers(request,idtmp):
    person = Person.objects.get(id=idtmp)
    personname = []
    personname.append(person.name)
    personname.append(person.id)
    teachers = Teacher.objects.filter(pid = person.id)
    students = Student.objects.filter(pid = person.id)
    teacherlist=[]
    studentlist=[]
    if list(teachers) != []:
        for teacher in teachers:
            dicttmp={}
            name=Person.objects.get(id=teacher.tid).name
            dicttmp['pid']=teacher.pid.id
            dicttmp['tid']=teacher.tid
            dicttmp['name']=name
            dicttmp['date0']=str(teacher.date0)
            dicttmp['date1']=str(teacher.date1)
            teacherlist.append(dicttmp)
    if list(students) != []:
        for student in students:
            dicttmp1={}
            name=Person.objects.get(id=student.sid).name
            dicttmp1['pid']=student.pid.id
            dicttmp1['sid']=student.sid
            dicttmp1['name']=name
            dicttmp1['date0']=str(student.date0)
            dicttmp1['date1']=str(student.date1)
            studentlist.append(dicttmp1)
    if teacherlist == [] and studentlist == []:
        return render_to_response("others.html")
    else:
        return render(request,'others.html',{'name':person,'person':json.dumps(personname),'teachers':json.dumps(teacherlist),'students':json.dumps(studentlist)})
    
  
def searchteacher(request):
    search = False
    if 'name' in request.POST:
        pid = request.session['member_id']
        name = request.POST['name']
        person = Person.objects.filter(name = name)
        teachers = person.exclude(id=pid)
        search = True
        return render_to_response('searchteacher.html',{'search':search,'teachers':teachers},
                                  context_instance=RequestContext(request))
    return render_to_response('searchteacher.html',{'search':search},
                              context_instance=RequestContext(request))
    
def buildteacher(request,tid):
    teacher = Person.objects.get(id = tid)
    if 'date0' in request.POST:
        pid = request.session['member_id']
        person = Person.objects.get(id=pid)
        date0 = request.POST['date0']
        date1 = request.POST['date1']
        teacher = Person.objects.get(id = tid)
        T0 = Teacher(pid=person,tid=tid ,date0=date0,date1=date1)
        T0.save()
        S0 = Student(pid=teacher,sid=pid,date0=date0,date1=date1)
        S0.save()
        return render_to_response('addtesuccess.html')
    return render_to_response('buildteacher.html',{'teacher':teacher},
                              context_instance=RequestContext(request))
    
def searchstudent(request):
    search = False
    if 'name' in request.POST:
        pid = request.session['member_id']
        name = request.POST['name']
        person = Person.objects.filter(name = name)
        students = person.exclude(id=pid)
        search = True
        return render_to_response('searchstudent.html',{'search':search,'students':students},
                                  context_instance=RequestContext(request))
    return render_to_response('searchstudent.html',{'search':search},
                              context_instance=RequestContext(request))

def buildstudent(request,sid):
    student = Person.objects.get(id = sid)
    if 'date0' in request.POST:
        pid = request.session['member_id']
        person = Person.objects.get(id=pid)
        date0 = request.POST['date0']
        date1 = request.POST['date1']
        student = Person.objects.get(id = sid)
        S0 = Student(pid=person,sid=sid ,date0=date0,date1=date1)
        S0.save()
        T0 = Teacher(pid=student,tid=pid,date0=date0,date1=date1)
        T0.save()
        return render_to_response('addstsuccess.html')
    return render_to_response('buildstudent.html',{'student':student},
                              context_instance=RequestContext(request))

def searchperson(request):
    search = False
    if 'name' in request.POST:
        pid = request.session['member_id']
        name = request.POST['name']
        person = Person.objects.filter(name = name)
        people = person.exclude(id=pid)
        search = True
        return render_to_response('searchperson.html',{'search':search,'people':people},
                                  context_instance=RequestContext(request))
    return render_to_response('searchperson.html',{'search':search},
                              context_instance=RequestContext(request))

#id2是id1的老师
def is_teacher(id1,id2):
    person = Person.objects.get(id = id1)
    teachers = Teacher.objects.filter(pid=person)
    for teacher in teachers:
        if teacher.tid == id2:
            return True
    return False

#id2是id1的学生
def is_student(id1,id2):
    person = Person.objects.get(id = id1)
    students = Student.objects.filter(pid=person)
    for student in students:
        if student.sid == id2:
            return True
    return False
    
#师兄弟
def is_fellow_apprentice(id1,id2):
    person = Person.objects.get(id = id1)
    teachers = Teacher.objects.filter(pid=person)
    for teacher in teachers:
        tea = Person.objects.get(id = teacher.tid)
        students = Student.objects.filter(pid=tea)
        for student in students:
            if student.sid == id2:
                return True
    return False 

def iterate_search_teacher(id1,id2,count,index,prt,flag,a):
    flag[(int(id1)-1)]=1
    person = Person.objects.get(id = id1)
    teachers = Teacher.objects.filter(pid=person)
    persons = Person.objects.all()
    lp= len(persons)
    if len(teachers) == 0 or count == 10 :
        flag = [0]*lp
    else:
        a[count] = 0
        while a[count]<len(teachers):
            index[count]=teachers[a[count]].tid
            if flag[(teachers[a[count]].tid-1)]==1:
                flag[(teachers[a[count]].tid-1)]=0
            elif teachers[a[count]].tid==id2:
                prt.append(index[0:(count+1)])
            else:
                flag[(teachers[a[count]].tid-1)]=1
                iterate_search_teacher(teachers[a[count]].tid,id2,count+1,index,prt,flag,a)
            a[count] += 1
            
def iterate_search_student(id1,id2,count,index,prt,flag,a):
    flag[(int(id1)-1)]=1
    person = Person.objects.get(id = id1)
    students = Student.objects.filter(pid=person)
    persons = Person.objects.all()
    lp= len(persons)
    if len(students) == 0 or count == 10:
        flag = [0]*lp
    else:
        a[count] = 0
        while a[count]<len(students):
            index[count]=students[a[count]].sid
            if students[a[count]].sid == id1:
                flag[(students[a[count]].sid-1)]=1
            if flag[(students[a[count]].sid-1)]==1:
                flag[(students[a[count]].sid-1)]=0
            elif students[a[count]].sid==id2:
                prt.append(index[0:(count+1)])
            #自己在环路里不访问
            else:
                flag[(students[a[count]].sid-1)]=1
                iterate_search_student(students[a[count]].sid,id2,count+1,index,prt,flag,a)
            a[count] += 1

                
def update(request):
    errors = []
    pid = request.session['member_id']
    person = Person.objects.get(id = pid)
    if 'name' in request.POST:
        try:
            int(request.POST['age'])
        except ValueError:
            errors.append('请输入正确的年龄')
            return render_to_response('update.html',{'errors':errors,'person':person},
                              context_instance=RequestContext(request))
        else:
            if int(request.POST['age'])<1 or int(request.POST['age'])>150:
                errors.append('请输入正确的年龄')
                return render_to_response('update.html',{'errors':errors,'person':person},
                              context_instance=RequestContext(request))
            else:
                person.name = request.POST['name']
                person.age = request.POST['age']
                person.sex = request.POST['sex']
                person.country = request.POST['country']
                person.school = request.POST['school']
                person.province = request.POST['province']
                person.save()
                return render_to_response('updatesuccess.html')
    return render_to_response('update.html',{'errors':errors,'person':person},
                              context_instance=RequestContext(request))
def deletedetail(request):
    pid = request.session['member_id']
    person = Person.objects.get(id = pid)
    tea=[]
    stu=[]
    teachers = Teacher.objects.filter(pid = person)
    for teacher in teachers:
        per = Person.objects.get(id=teacher.tid)
        tea.append(per)
    students = Student.objects.filter(pid = person)
    for student in students:
        per = Person.objects.get(id=student.sid)
        stu.append(per)
    return render_to_response('delete.html',{'tea':tea,'stu':stu})
    
def deleteteacher(request,id1):
    pid = request.session['member_id']
    person = Person.objects.get(id = pid)
    per0 = Person.objects.get(id=id1)
    teacher = Teacher.objects.get(pid=person,tid=id1)
    teacher.delete()
    student = Student.objects.get(pid=per0,sid=pid)
    student.delete()
    return render_to_response('deletesuccess.html')

def deletestudent(request,id1):
    pid = request.session['member_id']
    person = Person.objects.get(id = pid)
    per0 = Person.objects.get(id=id1)
    student = Student.objects.get(pid=person,sid=id1)
    student.delete()
    teacher = Teacher.objects.get(pid=per0,tid=pid)
    teacher.delete()
    return render_to_response('deletesuccess.html')
    
def se_re(request):
    search = False
    if 'name' in request.POST:
        pid = request.session['member_id']
        name = request.POST['name']
        person = Person.objects.filter(name = name)
        persons = person.exclude(id=pid)
        search = True
        return render_to_response('searchre.html',{'search':search,'persons':persons},
                                  context_instance=RequestContext(request))
    return render_to_response('searchre.html',{'search':search},
                              context_instance=RequestContext(request))

                
def search_relation(request,id2):
    index=[0,0,0,0,0,0,0,0,0,0]
    a = [0,0,0,0,0,0,0,0,0,0]
    prt=[]
    sear = False
    pid = request.session['member_id']
    relation = []
    count = 0
    tea=[]
    stu=[]
    if is_teacher(id2,pid):
        sear = True
        relation.append('他是您的学生之一')
#        return render_to_response('searchre.html',{'sear':sear,'relation':relation},
#                              context_instance=RequestContext(request))
    if is_student(id2,pid):
        sear = True
        relation.append('他是您的老师之一')
#        return render_to_response('searchre.html',{'sear':sear,'relation':relation},
#                              context_instance=RequestContext(request))
#        return render_to_response('searchre.html',{'sear':sear,'relation':relation},
#                              context_instance=RequestContext(request))

    if sear == False:
        sear = True
        if is_fellow_apprentice(id2,pid):
            relation.append('你们拥有共同的老师')
        persons = Person.objects.all()
        lp= len(persons)
        flag = [0]*lp
        
        flag1 = 0
        flag2 = 0
        iterate_search_student(id2,pid,count,index,prt,flag,a)
        
        if len(prt) != 0:
            for prin in prt:
                teacher=[]
                per = Person.objects.get(id = id2)
                teacher.append(per)
                for i in range(len(prin)):
                    person = Person.objects.get(id = prin[i])
                    teacher.append(person)
                rela = '他是你'+str(len(prin))+'代之前的老师'
                teacher.append(rela)
                teacher.reverse()
                tea.append(teacher)
#            return render_to_response('searchre.html',{'sear':sear,'relation':relation,'prt':prt},
#                                      context_instance=RequestContext(request))
        else:
            flag1 = 1
        prt =[]
        index =[0,0,0,0,0,0,0,0,0,0]
        flag = [0]*lp
        iterate_search_teacher(id2,pid,count,index,prt,flag,a)
        if len(prt) != 0:
            for prin in prt:
                student = []
                per = Person.objects.get(id = id2)
                student.append(per)
                for i in range(len(prin)):
                    person = Person.objects.get(id = prin[i])
                    student.append(person)
                rela = '他是你'+str(len(prin))+'代之后的学生'
                student.append(rela)
                student.reverse()
                stu.append(student)
        else:
            flag2 = 1
        if flag1 == 1 and flag2 == 1:
            if is_schoolfellow(id2,pid):
                relation.append('你们是校友关系')
            else:
                relation.append('你们之间没有关系')     
    return render_to_response('searchre.html',{'sear':sear,'relation':relation,'tea':tea,'stu':stu},
                              context_instance=RequestContext(request))
        
def is_schoolfellow(id1,id2):
    person1 = Person.objects.get(id = id1)
    person2 = Person.objects.get(id = id2)
    if person1.school == person2.school:
        return True
    return False          

def search_schoolfellow(request):
    errors=[]
    pid = request.session['member_id']
    person = Person.objects.get(id = pid)
    school = person.school
    queryset = Person.objects.filter(school = school).exclude(id=pid)
    queryset2 = []
    if len(queryset) == 0:
        errors.append('本系统中暂时没有您的校友')
        return render_to_response('search_schoolfellow.html',{'errors':errors,'queryset':queryset,'queryset2':queryset2},
                              context_instance=RequestContext(request))
    elif len(queryset) <= 5:
        return render_to_response('search_schoolfellow.html',{'queryset':queryset,'queryset2':queryset2},
                              context_instance=RequestContext(request))
    else:
        index=[]
        count =0
        while (count <5):
            ind = random.randint(0,len(queryset)-1)
            if ind not in index:
                index.append(ind)
                count +=1
        for i in range(5):
            queryset2.append(queryset[index[i]])
        return render_to_response('search_schoolfellow.html',{'queryset2':queryset2},
                              context_instance=RequestContext(request))


def search_date(request):
    search = False
    if 'date0' in request.POST:
        dt0 = request.POST['date0']
        dt1 = request.POST['date1']
        pid = request.session['member_id']
        person = Person.objects.get(id = pid)
        tea_queryset=[]
        stu_queryset=[]
        teacher = Teacher.objects.filter(pid=person)
        student = Student.objects.filter(pid=person)
        dt00 = dt0.split('-')
        dt11 = dt1.split('-')
        dat0 = date(int(dt00[0]),int(dt00[1]),int(dt00[2]))
        dat1 = date(int(dt11[0]),int(dt11[1]),int(dt11[2]))
        for tea in teacher:
            if tea.date0<=dat0 and tea.date1>=dat1:
                Tea = Person.objects.get(id = tea.tid)
                tea_queryset.append(Tea)
        for stu in student:
            if stu.date0<=dat0 and stu.date1>=dat1:
                Stu = Person.objects.get(id = stu.sid)
                stu_queryset.append(Stu)
        search = True
        return render_to_response('search_date.html',{'search':search,'tea_queryset':tea_queryset,
                                'stu_queryset':stu_queryset},context_instance=RequestContext(request))
    return render_to_response('search_date.html',{'search':search},
                                  context_instance=RequestContext(request))
#@login_required  