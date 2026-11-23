"""Local teaching interface using actual public-data inference."""
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
import streamlit as st
from practical_ml_ai.classical import classification_bundle
from practical_ml_ai.deployment import checked_predict

st.set_page_config(page_title="Practical ML: local inference")
st.title("Practical ML: local inference")
st.write("A local teaching service, not a certification or production guarantee.")
mode = st.radio("Choose the workflow", ["Classifier", "Local LLM triage"])


@st.cache_resource
def fitted_bundle():
    return classification_bundle()


if mode == "Classifier":
    bundle = fitted_bundle()
    source_row = bundle["split"]["test"].iloc[0]
    st.write("Defaults are one actual held-out UCI record. The label is not an input.")
    with st.form("chemistry"):
        record = {feature: st.number_input(feature, min_value=0.0, max_value=1000000.0,
                   value=float(source_row[feature]), key=feature) for feature in bundle["features"]}
        submitted = st.form_submit_button("Predict")
    if submitted:
        try:
            result = checked_predict(bundle, record)
            st.metric("Estimated probability of the classroom higher-rated label", f"{result['probability']:.3f}")
            st.metric("Predicted label at the validation-selected threshold", str(result["predicted"]))
            st.write("Model:", result["model"], "Threshold:", result["threshold"])
            if result["outside_training_range"]:
                st.warning("Outside training range: " + ", ".join(result["outside_training_range"]))
            st.write("This probability has not been established as calibrated confidence.")
        except ValueError as error:
            st.error(str(error))
else:
    from practical_ml_ai.continuation_data import sms_splits
    from practical_ml_ai.language import local_model, generate_label, redact_contacts
    st.write("First use downloads a public model; inference stays local. Do not enter secrets.")
    source = sms_splits()[0]["test"].iloc[0]
    with st.form("message"):
        message = st.text_area("Message to classify", value=redact_contacts(source.text), max_chars=1000)
        submitted = st.form_submit_button("Run local triage")
    if submitted:
        model, tokenizer, revision = local_model()
        label, response, seconds = generate_label(model, tokenizer, message)
        if label is None:
            st.error("Invalid output schema: the result was rejected.")
        else:
            st.success("Predicted label: " + ("spam" if label else "ham"))
        st.write("Model revision:", revision)
        st.write("Generation seconds:", round(seconds, 3))
        st.write("Model response (untrusted text):", response)
st.caption("UCI data retain CC BY 4.0 attribution. The CLI/text route provides the same inference workflow; consult the course accessibility guide for interface test scope.")
