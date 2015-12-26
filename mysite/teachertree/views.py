# Create your views here.
#-*- coding:utf-8 -*-
from teachertree.models import Person,Time
from django.template import Context
from django.shortcuts import render_to_response
def person(request):
    person_list = Person.objects.all()
    return render_to_response("personlist.html",{'person_list':person_list})


def search(request):
    person_list = Person.objects.all()
    errors = []
    tdict={}
    sdict={}
    if 'search' in request.GET:
        q = request.GET['search']
        try:
            person = Person.objects.get(Name=q)
        except Person.DoesNotExist:
            person = Person(Name=q)
            person.save()
            errors.append('此人不在库中，已添加进数据库')
            render_to_response('search_form.html',{'person_list':person_list,'errors':errors})
        else:
            teacher = person.Teacher.all()
            for i in range(len(teacher)):
                S1 = person.Date.all()
                for j in range(len(S1)):
                    if S1[j].Tors ==teacher[i]:
                        tdict[teacher[i].Name]=S1[j].Day       
            student = person.Student.all()
            for i in range(len(student)):
                S2 = person.Date.all()
                for j in range(len(S2)):
                    if S2[j].Tors ==student[i]:
                        sdict[student[i].Name]=S2[j].Day
            return render_to_response('search_results.html',{'person':person,'tdict':tdict,'sdict':sdict,
            'errors': errors,'query':q})
    return render_to_response('search_form.html',{'person_list':person_list,'errors':errors})

    
def addteacher(request,perid):
    errors=[]
    tdict={}
    sdict={}
    person =Person.objects.get(id=perid)
    if request.GET and request.GET['Name'] and request.GET['Date']:
        GET = request.GET
        new_person=Person(
            Name = GET['Name'],
            )
        tmp = list(Person.objects.filter(Name=GET['Name']))
        if tmp == [] :
            new_person.save()
        elif person.Name==GET['Name']:
            errors.append('不能添加自己为老师')
            return render_to_response('formteacher.html',{'errors':errors})
        else:
            new_person=Person.objects.get(Name=GET['Name'])
        person.Teacher.add(new_person)
#        new_person.Teacher.remove(person)
        new_date = Time(
                   Tors=new_person,
                   Day=GET['Date'],
                   )
        new_date.save()
        person.Date.add(new_date)
        new_date0 =Time(
                   Tors=person,
                   Day=GET['Date'],
                   )
        new_date0.save()
        new_person.Student.add(person)
        new_person.Date.add(new_date0)
        
        teacher = person.Teacher.all()
        for i in range(len(teacher)):
            S1 = person.Date.all()
            for j in range(len(S1)):
                if S1[j].Tors ==teacher[i]:
                    tdict[teacher[i].Name]=S1[j].Day       
        student = person.Student.all()
        for i in range(len(student)):
            S2 = person.Date.all()
            for j in range(len(S2)):
                if S2[j].Tors ==student[i]:
                    sdict[student[i].Name]=S2[j].Day
        return render_to_response('search_results.html',{'person':person,'tdict':tdict,
        'sdict':sdict,'query':person.Name})
    return render_to_response('formteacher.html',{'errors':errors})
    
def addstudent(request,perid):
    errors=[]
    tdict={}
    sdict={}
    person=Person.objects.get(id=perid)
    if request.GET and request.GET['Name']:
        GET = request.GET
        new_person=Person(
            Name = GET['Name'],
            )
        tmp = list(Person.objects.filter(Name=GET['Name']))
        if tmp == [] :
            new_person.save()
        elif person.Name==GET['Name']:
            errors.append('不能添加自己为学生')
            return render_to_response('formstudent.html',{'errors':errors})
        else:
            new_person=Person.objects.get(Name=GET['Name'])
        person.Student.add(new_person)
        new_date = Time(
                   Tors=new_person,
                   Day=GET['Date'],
                   )
        new_date.save()
        person.Date.add(new_date)
        new_date0 = Time(
                   Tors=person,
                   Day=GET['Date'],
                   )
        new_date0.save()
        new_person.Teacher.add(person)
        new_person.Date.add(new_date0)
        
        teacher = person.Teacher.all()
        for i in range(len(teacher)):
            S1 = person.Date.all()
            for j in range(len(S1)):
                if S1[j].Tors ==teacher[i]:
                    tdict[teacher[i].Name]=S1[j].Day       
        student = person.Student.all()
        for i in range(len(student)):
            S2 = person.Date.all()
            for j in range(len(S2)):
                if S2[j].Tors ==student[i]:
                    sdict[student[i].Name]=S2[j].Day
        return render_to_response('search_results.html',{'person':person,'tdict':tdict,
        'sdict':sdict,'query':person.Name})
    return render_to_response('formstudent.html',{'errors':errors})
    
    

    
    
def deleteteacher(request,personid,name):
    nm=Person.objects.get(id=personid)
    teacher = nm.Teacher.all()
    for i in range(len(teacher)):
        if teacher[i].Name==name:
            te=teacher[i]
            nm.Teacher.remove(te)
            break
    te.Student.remove(nm)
    date = nm.Date.all()
    for i in range(len(date)):
        if date[i].Tors == te:
            date[i].delete()
    date0 = te.Date.all()
    for i in range(len(date0)):
        if date0[i].Tors == nm:
            date0[i].delete()
    return render_to_response("delete.html")
    
    
def deletestudent(request,personid,name):
    nm=Person.objects.get(id=personid)
    student = nm.Student.all()
    for i in range(len(student)):
        if student[i].Name==name:
            st=student[i]
            nm.Student.remove(st)
            break
    nm.Teacher.remove(st)
    date = nm.Date.all()
    for i in range(len(date)):
        if date[i].Tors == st:
            date[i].delete()
    date0 = st.Date.all()
    for i in range(len(date0)):
        if date0[i].Tors == nm:
            date0[i].delete()
    return render_to_response("delete.html")
