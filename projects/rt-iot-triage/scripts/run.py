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
MISS_COST, FALSE_ALERT_COST = 5, 1
THRESHOLDS = [round(value, 2) for value in np.arange(.05, .96, .05)]
CONSTANT_POLICIES = ["always_review", "never_review"]

def load_frame(cache):
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
        return pd.read_csv(archive.open("RT_IOT2022"))

def score(actual, predicted, policy, threshold=None):
    tn,fp,fn,tp=map(int,confusion_matrix(actual,predicted,labels=[0,1]).ravel())
    cost=MISS_COST*fn+FALSE_ALERT_COST*fp
    return {"policy":policy,"threshold":threshold,"tp":tp,"fp":fp,"fn":fn,"tn":tn,
            "recall":tp/(tp+fn) if tp+fn else None,"false_positive_rate":fp/(fp+tn) if fp+tn else None,
            "alerts_per_1000":1000*(tp+fp)/len(actual),"assumed_cost":cost,"assumed_cost_per_1000":1000*cost/len(actual)}

def constant_decisions(policy, size):
    return np.full(size, policy == "always_review")

def choose(rows):
    # Lowest assumed cost; ties prefer fewer alerts (less analyst workload), then the name.
    return min(rows, key=lambda row:(row["assumed_cost"],row["alerts_per_1000"],row["policy"],row["threshold"] or 0))

def study(frame):
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
    # Validation alone fixes the logistic threshold and the recommended policy.
    # The constant policies compete, because high attack prevalence can make reviewing everything cheaper.
    probability = model.predict_proba(frame.iloc[validation][FEATURES])[:,1]
    logistic_rows=[score(actual[validation],probability>=threshold,"logistic",threshold) for threshold in THRESHOLDS]
    constant_rows=[score(actual[validation],constant_decisions(name,len(validation)),name) for name in CONSTANT_POLICIES]
    logistic=choose(logistic_rows)
    selected=choose([logistic,*constant_rows])
    # Final evaluation of the frozen choices; test labels never revise them.
    probability=model.predict_proba(frame.iloc[test][FEATURES])[:,1]
    evaluation=[score(actual[test],probability>=logistic["threshold"],"logistic",logistic["threshold"]),
                *[score(actual[test],constant_decisions(name,len(test)),name) for name in CONSTANT_POLICIES]]
    for row in evaluation:
        row["validation_selected"]=row["policy"]==selected["policy"]
    test_cost={row["policy"]:row["assumed_cost_per_1000"] for row in evaluation}
    summary={"source":URL,"sha256":DIGEST,"rows":len(frame),"features":FEATURES,"train":len(train),"validation":len(validation),"test":len(test),
             "attack_prevalence":{name:float(actual[indices].mean()) for name,indices in [("train",train),("validation",validation),("test",test)]},
             "threshold":logistic["threshold"],"threshold_candidates":THRESHOLDS,"threshold_at_grid_edge":logistic["threshold"] in (THRESHOLDS[0],THRESHOLDS[-1]),
             "validation_selected_policy":selected["policy"],
             "test_assumed_cost_per_1000":test_cost,
             "logistic_cheaper_than_always_review_on_test":test_cost["logistic"]<test_cost["always_review"],
             "average_precision":float(average_precision_score(actual[test],probability)),"group_overlap":False,"decision_time":"completed flow",
             "scope":"Retrospective within-capture exercise; device/session/time independence is unavailable.",
             "cost_assumption":f"miss={MISS_COST}, false alert={FALSE_ALERT_COST}; illustrative, not measured operational costs"}
    predictions=pd.DataFrame({"source_row":test,"actual":actual[test],"probability":probability,"logistic_review":probability>=logistic["threshold"],
                              "label":frame.iloc[test].Attack_type.to_numpy()})
    return {"summary":summary,"validation":pd.DataFrame(logistic_rows+constant_rows),"evaluation":pd.DataFrame(evaluation),"predictions":predictions}

def run(output, cache):
    output = Path(output)
    if output.exists():
        raise FileExistsError(output)
    frame = load_frame(cache)
    result = study(frame)
    output.mkdir(parents=True)
    result["evaluation"].to_csv(output/"evaluation.csv",index=False)
    result["validation"].to_csv(output/"validation.csv",index=False)
    result["predictions"].to_csv(output/"predictions.csv",index=False)
    frame.Attack_type.value_counts().rename_axis("label").to_csv(output/"label_counts.csv")
    (output/"summary.json").write_text(json.dumps(result["summary"],indent=2)+"\n", encoding="utf-8")
    print(json.dumps(result["summary"],indent=2))
    return result

if __name__ == "__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("--output",default="runs/rt-iot-triage")
    parser.add_argument("--cache",default="runs/datasets/rt-iot2022/original.zip")
    args=parser.parse_args()
    run(args.output,args.cache)
