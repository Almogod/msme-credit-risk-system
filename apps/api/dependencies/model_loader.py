import joblib

class ModelLoader:
    def __init__(self):
        self.pd_model = joblib.load("models/trained/pd_model.pkl")
        self.approval_model = joblib.load("models/trained/approval_model.pkl")
        self.credit_model = joblib.load("models/trained/credit_model.pkl")

model_loader = ModelLoader()
