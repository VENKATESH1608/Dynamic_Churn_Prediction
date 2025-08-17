from django.shortcuts import render
from .forms import UserRegistrationForm
from django.contrib import messages
from .models import UserRegistrationModel
from .algorithms.ProcessAlgorithm import Algorithms
algo = Algorithms()


# Create your views here.
def UserRegisterActions(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            print('Data is Valid')
            form.save()
            messages.success(request, 'You have been successfully registered')
            form = UserRegistrationForm()
            return render(request, 'UserRegistrations.html', {'form': form})
        else:
            messages.success(request, 'Email or Mobile Already Existed')
            print("Invalid form")
    else:
        form = UserRegistrationForm()
    return render(request, 'UserRegistrations.html', {'form': form})


def UserLoginCheck(request):
    if request.method == "POST":
        loginid = request.POST.get('loginname')
        pswd = request.POST.get('pswd')
        print("Login ID = ", loginid, ' Password = ', pswd)
        try:
            check = UserRegistrationModel.objects.get(loginid=loginid, password=pswd)
            status = check.status
            print('Status is = ', status)
            if status == "activated":
                request.session['id'] = check.id
                request.session['loggeduser'] = check.name
                request.session['loginid'] = loginid
                request.session['email'] = check.email
                print("User id At", check.id, status)
                return render(request, 'users/UserHome.html', {})
            else:
                messages.success(request, 'Your Account has not been activated by Admin.')
                return render(request, 'UserLogin.html')
        except Exception as e:
            print('Exception is ', str(e))
            pass
        messages.success(request, 'Invalid Login id and password')
    return render(request, 'UserLogin.html', {})


def UserHome(request):
    return render(request, 'users/UserHome.html', {})

def UserTestRecordResult(request):
    if request.method == "POST":
        from django.conf import settings
        import pandas as pd
        name = request.POST.get('name')
        gender = request.POST.get('gender')
        age = request.POST.get('age')
        education = request.POST.get('education')
        experience = request.POST.get('experience')
        income = request.POST.get('income')
        partner = request.POST.get('Partner')
        tenure = request.POST.get('tenure')
        onlinesecurity = request.POST.get('OnlineSecurity')
        streamingtv = request.POST.get('StreamingTV')
        streamingmovies = request.POST.get('StreamingMovies')
        contract = request.POST.get('Contract')
        monthlycharges = request.POST.get('MonthlyCharges')
        
        path = settings.MEDIA_ROOT + "\\" + "WA_Fn-UseC_-Telco-Customer-Churn.csv"
        data = pd.read_csv(path, delimiter=',')
        data = data.drop(['customerID','SeniorCitizen','Dependents','PhoneService','MultipleLines','InternetService','OnlineBackup','DeviceProtection','TechSupport','PaperlessBilling','PaymentMethod','TotalCharges'], axis=1)
        x = data.iloc[:,0:8]
        print(x)
        y = data.iloc[:,8]
        print(y)
        x = pd.get_dummies(x)
        print(x)
    

        from sklearn.model_selection import train_test_split
        x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.25, random_state=0)
        from sklearn.preprocessing import StandardScaler
        

        sc = StandardScaler()
        x_train = sc.fit_transform(x_train)
        x_test = sc.fit_transform(x_test)
        print('qweds')
        print(x_test)
        x_train = pd.DataFrame(x_train)
        from sklearn.tree import DecisionTreeClassifier
        from sklearn.metrics import confusion_matrix
        model = DecisionTreeClassifier()
        print('x-train:',x_train)
        test_set = [partner,tenure,onlinesecurity,streamingtv,streamingmovies,contract,monthlycharges,gender,gender]
        print(y_train)
        model.fit(x_train, y_train)
        print('erdfgvcxz')
        y_pred = model.predict([test_set])
        
        #msg = ""
        #print(y_pred)
        #if data['churn']==Yes:
         #   msg=

        if y_pred==0:
            msg = "Won't stay with us."
            color = "RED"
        elif y_pred==1:
            msg='Will stay with us.'
            color = "GREEN"
        return render(request, 'users/UserChurn.html', {'msg':msg}, {'color':color})



def UserSVM(request):
    acc, recall, precc,f1 = algo.processSVM()

    return render(request, 'users/SVMResult.html',
                  {'dt_acc': acc, 'dt_recall': recall, 'dt_precc': precc, 'dt_f1':f1})

        
def UserChurn(request):
    return render(request, 'users/UserChurn.html', {})


