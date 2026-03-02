import joblib
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score
from xgboost import XGBClassifier

from features.feature_store import load_and_process

def train():
    df = load_and_process("data/processed/train.csv")

    target = "default"
    X = df.drop(columns=[target])
    y = df[target]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    model = XGBClassifier(n_estimators=100, max_depth=5)

    model.fit(X_train, y_train)

    preds = model.predict_proba(X_test)[:, 1]
    auc = roc_auc_score(y_test, preds)

    print("ROC-AUC:", auc)

    joblib.dump(model, "models/trained/pd_model.pkl")

if __name__ == "__main__":
    train()
