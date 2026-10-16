import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from xgboost import XGBClassifier
from sklearn.metrics import accuracy_score, classification_report

print("1. Loading dataset...")
df = pd.read_csv('clinvar_conflicting.csv', low_memory=False)

# Select key features matching ClinVar dataset
target = 'CLASS'
features = ['CHROMOSOME', 'POS', 'REF', 'ALT', 'AF_ESP', 'AF_EXAC', 'AF_TGP']

# Fill missing values
for col in ['AF_ESP', 'AF_EXAC', 'AF_TGP']:
    if col in df.columns:
        df[col] = df[col].fillna(0)

# Encode categorical text into numbers
le = LabelEncoder()
for col in ['CHROMOSOME', 'REF', 'ALT']:
    if col in df.columns:
        df[col] = le.fit_transform(df[col].astype(str))

# Filter clean data
df_clean = df.dropna(subset=[target] + [f for f in features if f in df.columns])

X = df_clean[[f for f in features if f in df.columns]]
y = df_clean[target]

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

print("2. Training XGBoost AI Model...")
model = XGBClassifier(n_estimators=100, learning_rate=0.05, max_depth=5, random_state=42)
model.fit(X_train, y_train)

# Output evaluation
predictions = model.predict(X_test)
print("\n--- Model Results ---")
print("Accuracy:", accuracy_score(y_test, predictions))
print("\nClassification Report:\n", classification_report(y_test, predictions))