"""Reproduce a bounded completed-flow IoT triage study."""
import argparse
import hashlib
import io
import json
from pathlib import Path
import urllib.request
import zipfile
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.pipeline import make_pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import GroupShuffleSplit
from sklearn.metrics import confusion_matrix, average_precision_score

URL = "https://archive.ics.uci.edu/static/public/942/rt-iot2022.zip"
DIGEST = "bcaa24d62abbb1215be576d5cf9c02dfcb0bb7c4c2f5a00e03055afaa1ed109e"
FEATURES = ["proto", "service", "flow_duration", "fwd_pkts_tot", "bwd_pkts_tot"]
NORMAL = {"MQTT_Publish", "Thing_Speak", "Wipro_bulb"}

def run(output, cache):
    output = Path(output)
    if output.exists():
        raise FileExistsError(output)
    cache = Path(cache)
    if not cache.exists():
        request = urllib.request.Request(URL, headers={"User-Agent":"ML-AI-course/0.7"})
        with urllib.request.urlopen(request, timeout=60) as response:
            content = response.read(8_000_001)
        if len(content) > 8_000_000:
            raise ValueError("Archive exceeds bounded download size")
        if hashlib.sha256(content).hexdigest() != DIGEST:
            raise ValueError("Source archive changed")
        cache.parent.mkdir(parents=True, exist_ok=True)
        cache.write_bytes(content)
    content = cache.read_bytes()
    if hashlib.sha256(content).hexdigest() != DIGEST:
        raise ValueError("Source archive changed")
    with zipfile.ZipFile(io.BytesIO(content)) as archive:
        frame = pd.read_csv(archive.open("RT_IOT2022"))
    # Group identical selected inputs, including groups with conflicting labels.
    groups = pd.util.hash_pandas_object(frame[FEATURES], index=False).to_numpy()
    actual = (~frame.Attack_type.isin(NORMAL)).astype(int).to_numpy()
    trainval, test = next(GroupShuffleSplit(n_splits=1, test_size=.2, random_state=42).split(frame, actual, groups))
    fit, valid = next(GroupShuffleSplit(n_splits=1, test_size=.25, random_state=43).split(frame.iloc[trainval], actual[trainval], groups[trainval]))
    train, validation = trainval[fit], trainval[valid]
    for left, right in [(train,validation),(train,test),(validation,test)]:
        assert not set(groups[left]) & set(groups[right])
    for indices in [train,validation,test]:
        if len(np.unique(actual[indices])) != 2:
            raise ValueError("Both labels required in every partition")
    transform = ColumnTransformer([("categories",OneHotEncoder(handle_unknown="ignore"),FEATURES[:2]),("numeric",StandardScaler(),FEATURES[2:])])
    model = make_pipeline(transform, LogisticRegression(max_iter=2000, class_weight="balanced",random_state=42))
    model.fit(frame.iloc[train][FEATURES],actual[train])
    probability = model.predict_proba(frame.iloc[validation][FEATURES])[:,1]
    candidates=[]
    for threshold in [.2,.4,.6,.8]:
        tn,fp,fn,tp=confusion_matrix(actual[validation],probability>=threshold,labels=[0,1]).ravel()
        candidates.append({"threshold":threshold,"assumed_cost":int(5*fn+fp)})
    threshold=min(candidates,key=lambda row:(row["assumed_cost"],row["threshold"]))["threshold"]
    probability=model.predict_proba(frame.iloc[test][FEATURES])[:,1]
    results=[]
    for name,predicted in [("logistic",probability>=threshold),("always_review",np.ones(len(test),dtype=bool)),("never_review",np.zeros(len(test),dtype=bool))]:
        tn,fp,fn,tp=map(int,confusion_matrix(actual[test],predicted,labels=[0,1]).ravel())
        results.append({"model":name,"tp":tp,"fp":fp,"fn":fn,"tn":tn,"recall":tp/(tp+fn),"false_positive_rate":fp/(fp+tn),"alerts_per_1000":1000*(tp+fp)/len(test),"assumed_cost_per_1000":1000*(5*fn+fp)/len(test)})
    output.mkdir(parents=True)
    pd.DataFrame(results).to_csv(output/"evaluation.csv",index=False)
    pd.DataFrame(candidates).to_csv(output/"validation.csv",index=False)
    pd.DataFrame({"source_row":test,"actual":actual[test],"probability":probability,"label":frame.iloc[test].Attack_type.to_numpy()}).to_csv(output/"predictions.csv",index=False)
    frame.Attack_type.value_counts().rename_axis("label").to_csv(output/"label_counts.csv")
    summary={"source":URL,"sha256":DIGEST,"rows":len(frame),"features":FEATURES,"train":len(train),"validation":len(validation),"test":len(test),"threshold":threshold,"average_precision":float(average_precision_score(actual[test],probability)),"group_overlap":False,"decision_time":"completed flow","scope":"Retrospective within-capture exercise; device/session/time independence is unavailable.","cost_assumption":"miss=5, false alert=1; illustrative, not measured operational costs"}
    (output/"summary.json").write_text(json.dumps(summary,indent=2)+"\n", encoding="utf-8")
    print(json.dumps(summary,indent=2))

if __name__ == "__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("--output",default="runs/rt-iot-triage")
    parser.add_argument("--cache",default="runs/datasets/rt-iot2022/original.zip")
    args=parser.parse_args()
    run(args.output,args.cache)
