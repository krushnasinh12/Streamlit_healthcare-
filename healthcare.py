import pandas as pd
# Load patient data from Excel
data= pd.read_excel("C:/Users/krush/OneDrive/Documents/learning python/healthcare/hospital_data.xlsx",sheet_name='patients')
print(data.head())

data.columns = data.columns.str.strip()

from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report

le = LabelEncoder()

data["Gender"] = le.fit_transform(data["Gender"])
data["diagnosis name"] = le.fit_transform(data["diagnosis name"])

X = data[["Age","Gender","diagnosis name","Length of Stay","TreatmentCost"]]
y = data["Risk score"]

X_train, X_test, y_train, y_test = train_test_split(
X, y, test_size=0.2, random_state=42
)

model = RandomForestClassifier(n_estimators=100)
model.fit(X_train, y_train)

y_pred = model.predict(X_test)

pred = model.predict(X_test)

accuracy = accuracy_score(y_test, pred)
print("Model Accuracy:", accuracy)

print(confusion_matrix(y_test, y_pred))

# Classification Report
print(classification_report(y_test, y_pred))

