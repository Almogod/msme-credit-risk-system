import joblib
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from xgboost import XGBRegressor

from features.feature_store import load_and_process

def train():
    df = load_and_process("data/processed/train.csv")

    target = "credit_limit"
    X = df.drop(columns=[target])
    y = df[target]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    model = XGBRegressor(n_estimators=100)

    model.fit(X_train, y_train)

    preds = model.predict(X_test)
    rmse = mean_squared_error(y_test, preds, squared=False)

    print("RMSE:", rmse)

    joblib.dump(model, "models/trained/credit_model.pkl")

if __name__ == "__main__":
    train()
