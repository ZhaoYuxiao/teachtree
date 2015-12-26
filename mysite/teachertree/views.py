#-*- coding:utf-8 -*-
from django.shortcuts import render,render_to_response
from django.http import HttpResponse,HttpResponseRedirect
from django.template import RequestContext
from django import forms
from django.contrib.auth.decorators import login_required
import os 
from teachertree.models import Person,Teacher,Student
from django.template import Context
from django.contrib.auth.models import User
from django.contrib import auth

class PersonForm(forms.Form):
    name = forms.CharField(label='姓名:',max_length=100)
    age = forms.IntegerField(label='年龄:')
    sex = forms.CharField(label='性别:',max_length=100)
    country = forms.CharField(label='国籍:',max_length=100,required=False)
    school = forms.CharField(label='毕业院校:',max_length=100,required=False)
    email = forms.EmailField(label='电子邮件:')
    identity_card = forms.CharField(label='身份证号:',max_length=18)
    province = forms.CharField(label='省份:',max_length=100,required=False)
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
            person = Person.objects.get(email=email)
        except Person.DoesNotExist:
            return email
        else:
            raise forms.ValidationError("email already existed")
       
    def clean(self):
        cleaned_data = super(PersonForm, self).clean()
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
        Pe = PersonForm(request.POST)
        if Pe.is_valid():
            pe = Pe.cleaned_data
            Name = pe['name']
            identity_card = pe['identity_card']
            P0 = Person(
                name = Name,
                age = pe['age'],
                sex = pe['sex'],
                country = pe['country'],
                school = pe['school'],
                province = pe['province'],
                email = pe['email'],
                identity_card = identity_card
            )
            P0.save()
            user = User.objects.create_user(
                username = pe['email'],
                password = pe['password'])
            user.save()
            return render_to_response('registersuc.html')

        else:
            return render_to_response('register.html',{'Pe':Pe},
                                      context_instance=RequestContext(request))
    else:
        Pe = PersonForm()
        return render_to_response('register.html',{'Pe':Pe},
                                  context_instance=RequestContext(request))
            

#登陆
def login(req):
    errors = []
    if req.method == 'POST':
        uf = UserForm(req.POST)
        if uf.is_valid():
            #获取表单用户密码
            username = uf.cleaned_data['username']
            password = uf.cleaned_data['password']
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
                return render_to_response('login.html',{'uf':uf,'errors':errors},
                                          context_instance=RequestContext(req))
    else:
        uf = UserForm()
    return render_to_response('login.html',{'uf':uf},context_instance=RequestContext(req))

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
    teachers = Teacher.objects.filter(pid = person.id)
    students = Student.objects.filter(pid = person.id)
    return render_to_response('.html',{'teachers':teachers,'students':students})
    
def query2(request):
    pid = request.GET['id']
    person = Person.objects.get(id= pid)
    teachers = Teacher.objects.filter(pid = person.id)
    students = Student.objects.filter(pid = person.id)
    return render_to_response('.html',{'teachers':teachers,'students':students})
   
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
    if is_fellow_apprentice(id2,pid):
        sear = True
        relation.append('你们拥有共同的老师')
#        return render_to_response('searchre.html',{'sear':sear,'relation':relation},
#                              context_instance=RequestContext(request))

    if sear == False:
        persons = Person.objects.all()
        lp= len(persons)
        flag = [0]*lp
        sear = True
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
            relation.append('你们之间没有关系')
            
    return render_to_response('searchre.html',{'sear':sear,'relation':relation,'tea':tea,'stu':stu},
                              context_instance=RequestContext(request))
        
            

#@login_required  
