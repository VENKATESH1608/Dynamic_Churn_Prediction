from django.conf import settings
import pandas as pd
from sklearn.metrics import confusion_matrix,accuracy_score,precision_score,recall_score,roc_auc_score,f1_score
class Algorithms:
    path = settings.MEDIA_ROOT + "\\" + "WA_Fn-UseC_-Telco-Customer-Churn.csv"
    data = pd.read_csv(path, delimiter=',')

    data = data.drop(['customerID','SeniorCitizen','Dependents','PhoneService','MultipleLines','InternetService','OnlineBackup','DeviceProtection','TechSupport','PaperlessBilling','PaymentMethod','TotalCharges'], axis=1)
    x = data.iloc[:,0:8]
    y = data.iloc[:,8]
    x = pd.get_dummies(x)

    from sklearn.model_selection import train_test_split
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.25, random_state=0)
    from sklearn.preprocessing import StandardScaler

    sc = StandardScaler()
    x_train = sc.fit_transform(x_train)
    x_test = sc.fit_transform(x_test)

    x_train = pd.DataFrame(x_train)
    x_train.head()


    def processSVM(self):
        from sklearn.svm import SVC
        from sklearn.metrics import confusion_matrix
        
        model = SVC()
        model.fit(self.x_train, self.y_train)
        y_pred = model.predict(self.x_test)
        print("Training Accuracy :", model.score(self.x_train, self.y_train))
        print("Testing Accuaracy :", model.score(self.x_test,self. y_test))
        cm = confusion_matrix(self.y_test, y_pred)
        dt_acc = accuracy_score(self.y_test, y_pred)
        dt_precc = precision_score(self.y_test, y_pred, pos_label = 1)
        dt_recall = recall_score(self.y_test, y_pred,pos_label = 1)
        dt_f1 = f1_score(self.y_test, y_pred ,pos_label = 1)
        #dt_auc = roc_auc_score(self.y_test, y_pred, average=None)
        

        # k fold cross validatio
        from sklearn.model_selection import cross_val_score
        cvs = cross_val_score(estimator=model, X=self.x_train, y=self.y_train, cv=10)
        print(cvs)

        return dt_acc,dt_recall,dt_precc,dt_f1
