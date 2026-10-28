"""Staged real UCI website-phishing case. No live website access or model pickle."""
import argparse
import json
from pathlib import Path
import numpy as np
import pandas as pd
from scipy.io import arff
from sklearn.dummy import DummyClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import GroupShuffleSplit
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.tree import DecisionTreeClassifier
from .continuation_data import fetch_source, new_run, publish_report, write_json, binary_metrics


def prepare(output):
    directory = new_run(output)
    folder = fetch_source("phishing")
    records,_ = arff.loadarff(folder/"Training Dataset.arff")
    frame = pd.DataFrame(records).astype(int)
    if frame.shape != (11055,31) or set(frame.Result.unique()) != {-1,1}:
        raise ValueError("Unexpected phishing source shape or labels.")
    features = [name for name in frame if name != "Result"]
    if not np.isin(frame[features].to_numpy(),[-1,0,1]).all():
        raise ValueError("Unexpected encoded feature domain.")
    frame["record_id"] = np.arange(len(frame))
    frame["label"] = (frame.Result == -1).astype(int)
    frame["profile_id"] = pd.util.hash_pandas_object(frame[features],index=False).astype(str)
    conflicts = frame.groupby("profile_id").label.nunique()
    ambiguous = set(conflicts[conflicts > 1].index)
    frame = frame.loc[~frame.profile_id.isin(ambiguous)].copy()
    train_idx,remaining = next(GroupShuffleSplit(n_splits=1,test_size=.4,random_state=42).split(frame,groups=frame.profile_id))
    val_local,test_local = next(GroupShuffleSplit(n_splits=1,test_size=.5,random_state=43).split(frame.iloc[remaining],groups=frame.iloc[remaining].profile_id))
    parts={"train":frame.iloc[train_idx],"validation":frame.iloc[remaining[val_local]],"test":frame.iloc[remaining[test_local]]}
    for name,part in parts.items():
        if part.label.nunique() != 2: raise ValueError("Each split needs both labels.")
        part[features+["record_id","profile_id","label"]].to_csv(directory/(name+".csv"),index=False)
    write_json(directory/"protocol.json",{"source":"UCI Phishing Websites, DOI:10.24432/C51W2X","raw_rows":11055,
        "ambiguous_profiles_removed":len(ambiguous),"rows_after_exclusions":len(frame),"features":features,
        "positive_label":"original Result=-1 (phishing)","split_rows":{k:len(v) for k,v in parts.items()},
        "selection":"validation balanced accuracy, threshold fixed 0.5, alphabetical tie-break",
        "boundary":"Identical encoded profiles grouped; actual domain/campaign/time independence is unknown."})
    return directory


def train(output):
    directory=Path(output)
    if (directory/"trained.json").exists(): raise ValueError("Training already completed; use a fresh study.")
    protocol=json.loads((directory/"protocol.json").read_text(encoding="utf-8"));features=protocol["features"]
    training=pd.read_csv(directory/"train.csv")
    models={"dummy":DummyClassifier(strategy="prior"),
        "logistic":make_pipeline(StandardScaler(),LogisticRegression(max_iter=1000,random_state=42)),
        "tree":DecisionTreeClassifier(max_depth=6,min_samples_leaf=10,random_state=42),
        "forest":RandomForestClassifier(n_estimators=50,max_depth=8,min_samples_leaf=5,random_state=42,n_jobs=1)}
    for name,model in models.items():
        model.fit(training[features],training.label)
        # Frozen inference on inputs only. Test labels never enter fitting or selection.
        for part in ["validation","test"]:
            inputs=pd.read_csv(directory/(part+".csv"),usecols=features+["record_id"])
            probability=model.predict_proba(inputs[features])[:,1]
            pd.DataFrame({"record_id":inputs.record_id,"model":name,"probability":probability,
                          "predicted":(probability >= .5).astype(int)}).to_csv(directory/(part+"_"+name+".csv"),index=False)
    write_json(directory/"trained.json",{"models":sorted(models),"threshold":.5,"parameters_frozen":True})


def validate(output):
    directory=Path(output)
    if (directory/"selection.json").exists(): raise ValueError("Selection already frozen.")
    actual=pd.read_csv(directory/"validation.csv").set_index("record_id").label
    models=json.loads((directory/"trained.json").read_text(encoding="utf-8"))["models"]
    scores=[]
    for name in models:
        prediction=pd.read_csv(directory/("validation_"+name+".csv")).set_index("record_id")
        scores.append({"model":name,**binary_metrics(actual.loc[prediction.index],prediction.predicted)})
    scores.sort(key=lambda row:(-row["balanced_accuracy"],row["model"]))
    pd.DataFrame(scores).to_csv(directory/"validation_scores.csv",index=False)
    write_json(directory/"selection.json",scores[0])


def evaluate(output):
    directory=Path(output)
    if (directory/"evaluation.json").exists(): raise ValueError("Final evaluation already completed.")
    chosen=json.loads((directory/"selection.json").read_text(encoding="utf-8"))["model"]
    actual=pd.read_csv(directory/"test.csv").set_index("record_id").label
    scores=[]
    for name in sorted({chosen,"dummy"}):
        prediction=pd.read_csv(directory/("test_"+name+".csv")).set_index("record_id")
        scores.append({"model":name,**binary_metrics(actual.loc[prediction.index],prediction.predicted)})
    write_json(directory/"evaluation.json",{"chosen":chosen,"test_scores":scores})


def report(output):
    directory=Path(output)
    protocol=json.loads((directory/"protocol.json").read_text(encoding="utf-8"))
    result=json.loads((directory/"evaluation.json").read_text(encoding="utf-8"))
    return publish_report(directory,"IT case: historical website phishing",{**protocol,**result},
        {"validation_scores":pd.read_csv(directory/"validation_scores.csv"),"test_scores":pd.DataFrame(result["test_scores"])},
        ["Encoded historical URL/host/content attributes are not raw network packets or live reputation data.",
         "Original Result=-1 means phishing; +1 means legitimate. Encoded attributes are categories, not measured continuous quantities.",
         "The split groups identical feature profiles and removes contradictory labels. It cannot establish domain/campaign/time independence.",
         "No URLs are visited. Historical benchmark performance does not establish current detection quality or justify blocking websites.",
         "Technical protocol guards are not access controls. Once public final results are viewed, further selection needs new evaluation planning."])


def main(argv=None):
    parser=argparse.ArgumentParser();parser.add_argument("stage",choices=["prepare","train","validate","evaluate","report","all"])
    parser.add_argument("--output",required=True);args=parser.parse_args(argv)
    stages=[prepare,train,validate,evaluate,report] if args.stage == "all" else [globals()[args.stage]]
    for stage in stages: stage(args.output)

if __name__ == "__main__": main()
