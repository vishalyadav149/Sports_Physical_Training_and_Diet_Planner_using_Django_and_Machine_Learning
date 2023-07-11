from pyexpat.errors import messages
from django.shortcuts import render ,HttpResponse
import os
from foodrec.settings import BASE_DIR
from recommender.functions import Weight_Gain ,Weight_Loss,Healthy
from recommender.models import Food
import pandas as pd


def index(request):
    if request.method=="POST":
      
        age=int(request.POST.get("age"))
        weight=int(request.POST.get("weight"))
        height=int(request.POST.get("height"))
        bodyfat=float(request.POST.get("bodyfat"))
        goal=request.POST.get("goal")
        activity=float(request.POST.get("activity"))
        gender=request.POST.get("gender")
        

        leanfactor=0.0
        if(gender=="m"):
            if(10<=bodyfat<=14):
                leanfactor=1
            elif(15<=bodyfat<=20):
                leanfactor=0.95
            elif(21<=bodyfat<=28):
                leanfactor=0.90
            else:
                leanfactor=0.85    
        else:
            if(14<=bodyfat<=18):
                leanfactor=1
            elif(19<=bodyfat<=28):
                leanfactor=0.95
            elif(29<=bodyfat<=38):
                leanfactor=0.90
            else:
                leanfactor=0.85            


        maintaincalories=int(weight*24*leanfactor*activity)
        
        caloriesreq=0
        finaldata=[]
        bmi=0
        bmiinfo=""
        if(goal=="weight gain"):
            print("wg")
            finaldata=Weight_Gain(age,weight,height)
            bmi=int(finaldata[len(finaldata)-2])
            bmiinfo=finaldata[len(finaldata)-1]
            caloriesreq=maintaincalories+300
        if(goal=="weight loss"):
            print("wl")
            finaldata=Weight_Loss(age,weight,height)
            bmi=int(finaldata[len(finaldata)-2])
            bmiinfo=finaldata[len(finaldata)-1]
            caloriesreq=maintaincalories-300
        
        if(goal=="healthy"):
            print("h")
            finaldata=Healthy(age,weight,height)
            bmi=int(finaldata[len(finaldata)-2])
            bmiinfo=finaldata[len(finaldata)-1]
            caloriesreq=maintaincalories
  
        breakfastdata=Food.objects.all().filter(bf=1).filter(name__in=finaldata)
        lunchdata=Food.objects.all().filter(lu=1).filter(name__in=finaldata)
        dinnerdata=Food.objects.all().filter(di=1).filter(name__in=finaldata)


       
        context={ 
            "breakfast":breakfastdata,
            "lunch":lunchdata,
            "dinner":dinnerdata,
            "bmi":bmi,
            "bmiinfo":bmiinfo,
            "caloriesreq":caloriesreq
        }

        return render(request,"diet.html",context)


    return render(request,"index.html")


def bodymass(request):
    return render(request,"bodymass.html")   

def home(request):
    return render(request,"home.html")        

def diet(request):
    return render(request,"diet.html")                

def sports(request):
    from django.shortcuts import render
    from django.http import HttpResponse
    import pandas as pd
    from sklearn.tree import DecisionTreeClassifier
    from sklearn.model_selection import train_test_split
    import joblib

    # load the trained machine learning model
    model = joblib.load('model.pkl')

    if request.method == 'POST':
        BMI = request.POST['BMI']
        Gender = request.POST['Gender']
        Sports = request.POST['Sports']
        recommendation = model.predict([[BMI,Gender, Sports]])
        return render(request, 'sports.html', {'recommendation': recommendation})
    else:
        return render(request, 'sports.html')
 
