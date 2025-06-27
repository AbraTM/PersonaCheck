import pandas as pd
import matplotlib.pyplot as plot
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import classification_report
import joblib
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = (BASE_DIR.parent / "data" / "personality_dataset.csv").resolve()
MODEL_PATH = (BASE_DIR.parent / "models" / "personality_classifier_model.pkl").resolve()

# Pre Processing the data
def pre_process(data_frame):
    data_frame.dropna(inplace = True)
    data_frame.reset_index(drop = True, inplace = True)

    # Encoding text based features
    # Label Encoding for data that takes binary values
    """
    -> Encoding for Stage_fear Feature Column
        'Does have stage fear' -> 1
        'Doesn't have stage fear' -> 0

    -> Encoding for Drained_after_socializing Feature Column
        'Is drained after socializing' -> 1
        'Is not drained after socializing' -> 0

    -> Encoding for Personality Feature Column
        'Extroverted' -> 0
        'Introverted' -> 1

    """
    new_df = pd.get_dummies(data_frame[["Stage_fear", "Drained_after_socializing", "Personality"]], dtype='int')
    encoded_df = pd.concat([data_frame, new_df], axis=1)
    encoded_df.drop(columns=["Stage_fear", "Drained_after_socializing", "Personality", "Stage_fear_No", "Drained_after_socializing_No", "Personality_Extrovert"], inplace=True)
    encoded_df.rename(columns={"Stage_fear_Yes" : "Stage_fear", "Drained_after_socializing_Yes": "Drained_after_socializing", "Personality_Introvert" : "Personality"}, inplace=True)
    return encoded_df


""" Other Approaches to encode binary data """
# Using Pandas methods to label encode data that takes binary values
# new_df_sf = pd.get_dummies(df["Stage_fear"], dtype='int')
# new_df_sf.columns = ["Stage_fear_no", "Stage_fear_yes"]
# new_df_dfa = pd.get_dummies(df["Drained_after_socializing"], dtype='int')
# new_df_dfa.columns = ["Drained_after_socializing_no", "Drained_after_socializing_yes"]
# new_df_p = pd.get_dummies(df["Personality"], dtype='int')
# encoded_df = pd.concat([df, new_df_sf, new_df_dfa, new_df_p], axis=1)
# encoded_df.drop(columns=["Stage_fear", "Drained_after_socializing", "Personality", "Stage_fear_no", "Drained_after_socializing_no", "Extrovert"], inplace=True)
# encoded_df.rename(columns={"Stage_fear_yes" : "Stage_fear", "Drained_after_socializing_yes": "Drained_after_socializing", "Introvert" : "Personality"}, inplace=True)
# encoded_df.head(10)

# Using sklearn to label encode
# Create a new label encoder for each feature column because using the same encoder can result in unexpected values
# from sklearn.preprocessing import LabelEncoder
# lbe = LabelEncoder()
# df["Stage_fear"] = lbe.fit_transform(df["Stage_fear"])
# lbe = LabelEncoder()
# df["Drained_after_socializing"] = lbe.fit_transform(df["Drained_after_socializing"])
# lbe = LabelEncoder()
# df["Personality"] = lbe.fit_transform(df["Personality"])
# df.head(10)

def train_model(X_train, y_train):
    # Fitting the data
    gnb = GaussianNB()
    gnb.fit(X_train, y_train)
    return gnb

def evaluate_model(model, X_train, X_test, y_train, y_test ):
    y_pred = model.predict(X_test)
    report = classification_report(y_test, y_pred)
    train_data_score = model.score(X_train, y_train)
    test_data_score = model.score(X_test, y_test)
    print(report)
    print(f"\nTrain Data Score: {train_data_score: .2%}")
    print(f"Test Data Score: {test_data_score: .2%}")

def main():
    """Data Set from KAGGLE"""
    # Raw Data
    raw_df = pd.read_csv(DATA_PATH)
    print("RAW DATA Sample : ")
    print(raw_df.head(10))

    df = pre_process(raw_df)

    # Input data / Features
    X = df.drop(["Personality"], axis=1)
    y = df["Personality"]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=10)

    # Training the model
    model = train_model(X_train, y_train)
    
    # Evaluating the model
    evaluate_model(model, X_train, X_test, y_train, y_test)

    # Saving the model
    joblib.dump(model, MODEL_PATH)
    print("Model saved to '../models/personality_classifier_model.pkl'")

if __name__ == "__main__":
    main()