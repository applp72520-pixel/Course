import os
import re
import json
import numpy as np
import pandas as pd

from scipy.sparse import hstack, csr_matrix
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import accuracy_score, precision_recall_fscore_support, classification_report
from sklearn.preprocessing import MaxAbsScaler
from sklearn.svm import LinearSVC
from sklearn.linear_model import RidgeClassifier, LogisticRegression, SGDClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.naive_bayes import MultinomialNB, ComplementNB

BASE_DIR = "."
CONCEPT_FILE = os.path.join(BASE_DIR, "clean_concept.txt")
DESCRIPTION_FILE = os.path.join(BASE_DIR, "clean_description.txt")
RELATIONSHIP_FILE = os.path.join(BASE_DIR, "clean_relationship.txt")

OUTPUT_DIR = os.path.join(BASE_DIR, "output")
os.makedirs(OUTPUT_DIR, exist_ok=True)

RANDOM_STATE = 42
MIN_CLASS_SIZE = 20

def read_txt(path):
    return pd.read_csv(path, sep="\t", dtype=str, low_memory=False).fillna("")

def extract_hierarchy(term):
    m = re.search(r"\(([^()]*)\)\s*$", str(term).strip())
    return m.group(1).strip().lower() if m else np.nan

def clean_text(text):
    text = str(text).strip().lower()
    text = re.sub(r"\s+", " ", text)
    return text

print("Loading files...")
concept_df = read_txt(CONCEPT_FILE)
description_df = read_txt(DESCRIPTION_FILE)
relationship_df = read_txt(RELATIONSHIP_FILE)

print("Original shapes:")
print("concept:", concept_df.shape)
print("description:", description_df.shape)
print("relationship:", relationship_df.shape)

# 1) 保留 active=1
concept_df = concept_df[concept_df["active"] == "1"].copy()
description_df = description_df[description_df["active"] == "1"].copy()
relationship_df = relationship_df[relationship_df["active"] == "1"].copy()

# 2) Concept 過濾
valid_concepts = set(concept_df["id"].astype(str))
description_df["conceptId"] = description_df["conceptId"].astype(str)
relationship_df["sourceId"] = relationship_df["sourceId"].astype(str)
relationship_df["destinationId"] = relationship_df["destinationId"].astype(str)

description_df = description_df[description_df["conceptId"].isin(valid_concepts)].copy()
relationship_df = relationship_df[relationship_df["sourceId"].isin(valid_concepts)].copy()

# 3) Description 處理
if "languageCode" in description_df.columns:
    description_df = description_df[description_df["languageCode"].str.lower() == "en"].copy()

if "typeId" in description_df.columns:
    description_df["desc_type"] = np.where(
        description_df["typeId"] == "900000000000003001", "FSN",
        np.where(description_df["typeId"] == "900000000000013009", "Synonym", "Other")
    )
else:
    description_df["desc_type"] = "Unknown"

description_df["hierarchy"] = description_df["term"].apply(extract_hierarchy)
description_df["clean_term"] = description_df["term"].apply(clean_text)

# 用 FSN 建立 conceptId -> hierarchy label
fsn_df = description_df[
    (description_df["desc_type"] == "FSN") &
    (description_df["hierarchy"].notna()) &
    (description_df["clean_term"] != "")
].copy()

concept_to_label = fsn_df.drop_duplicates("conceptId")[["conceptId", "hierarchy"]]
concept_to_label = concept_to_label.rename(columns={"hierarchy": "label"})

# 所有 description 都拿來當訓練樣本，但 label 由 FSN 回填
dataset = description_df.merge(concept_to_label, on="conceptId", how="inner")
dataset = dataset[(dataset["clean_term"] != "") & (dataset["label"] != "")].copy()

# 去重複
dataset = dataset.drop_duplicates(subset=["conceptId", "clean_term", "label"]).copy()

# 4) Relationship 特徵工程
rel = relationship_df.copy()

# relationship 基本統計
rel_feature_df = rel.groupby("sourceId").agg(
    rel_count=("id", "count"),
    unique_dest_count=("destinationId", pd.Series.nunique),
    unique_rel_type_count=("typeId", pd.Series.nunique),
    rel_group_count=("relationshipGroup", pd.Series.nunique),
    characteristic_type_count=("characteristicTypeId", pd.Series.nunique)
).reset_index().rename(columns={"sourceId": "conceptId"})

# IS-A 關係計數，SNOMED CT 的 typeId 116680003 常表示 is-a [file:19]
isa_df = rel[rel["typeId"] == "116680003"].copy()
isa_count_df = isa_df.groupby("sourceId").agg(
    isa_count=("id", "count"),
    isa_parent_count=("destinationId", pd.Series.nunique)
).reset_index().rename(columns={"sourceId": "conceptId"})

rel_feature_df = rel_feature_df.merge(isa_count_df, on="conceptId", how="left").fillna(0)

# 合併到資料集
dataset = dataset.merge(rel_feature_df, on="conceptId", how="left").fillna(0)

# 保留樣本數足夠的類別
label_counts = dataset["label"].value_counts()
valid_labels = label_counts[label_counts >= MIN_CLASS_SIZE].index
dataset = dataset[dataset["label"].isin(valid_labels)].copy()

print("Processed dataset shape:", dataset.shape)
print("Number of labels:", dataset["label"].nunique())

# 輸出處理後資料
dataset.to_csv(os.path.join(OUTPUT_DIR, "processed_dataset_with_rel.csv"), index=False, encoding="utf-8-sig")

label_dist = dataset["label"].value_counts().reset_index()
label_dist.columns = ["label", "count"]
label_dist.to_csv(os.path.join(OUTPUT_DIR, "label_distribution.csv"), index=False, encoding="utf-8-sig")

# 5) 切分資料
X_text = dataset["clean_term"]
X_num = dataset[[
    "rel_count",
    "unique_dest_count",
    "unique_rel_type_count",
    "rel_group_count",
    "characteristic_type_count",
    "isa_count",
    "isa_parent_count"
]].astype(float)
y = dataset["label"]

X_text_train, X_text_test, X_num_train, X_num_test, y_train, y_test = train_test_split(
    X_text, X_num, y,
    test_size=0.2,
    random_state=RANDOM_STATE,
    stratify=y
)

# 6) 文字向量化 + 數值特徵合併
tfidf = TfidfVectorizer(
    lowercase=True,
    ngram_range=(1, 2),
    min_df=3,
    max_df=0.95,
    sublinear_tf=True
)

X_train_text_vec = tfidf.fit_transform(X_text_train)
X_test_text_vec = tfidf.transform(X_text_test)

scaler = MaxAbsScaler()
X_train_num_scaled = scaler.fit_transform(X_num_train)
X_test_num_scaled = scaler.transform(X_num_test)

X_train = hstack([X_train_text_vec, csr_matrix(X_train_num_scaled)])
X_test = hstack([X_test_text_vec, csr_matrix(X_test_num_scaled)])

models = {
    "LinearSVC": LinearSVC(),
    "RidgeClassifier": RidgeClassifier(),
    "LogisticRegression": LogisticRegression(max_iter=2000),
    "SGDClassifier": SGDClassifier(random_state=RANDOM_STATE),
    "RandomForest": RandomForestClassifier(n_estimators=200, random_state=RANDOM_STATE, n_jobs=-1),
    "DecisionTree": DecisionTreeClassifier(random_state=RANDOM_STATE),
    "MultinomialNB": MultinomialNB(),
    "ComplementNB": ComplementNB()
}

results = []
reports = {}

for model_name, model in models.items():
    print(f"Training {model_name} ...")
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)

    acc = accuracy_score(y_test, y_pred)
    p_macro, r_macro, f1_macro, _ = precision_recall_fscore_support(
        y_test, y_pred, average="macro", zero_division=0
    )
    p_weighted, r_weighted, f1_weighted, _ = precision_recall_fscore_support(
        y_test, y_pred, average="weighted", zero_division=0
    )

    results.append({
        "model": model_name,
        "accuracy": acc,
        "precision_macro": p_macro,
        "recall_macro": r_macro,
        "f1_macro": f1_macro,
        "precision_weighted": p_weighted,
        "recall_weighted": r_weighted,
        "f1_weighted": f1_weighted
    })

    report_text = classification_report(y_test, y_pred, zero_division=0)
    reports[model_name] = report_text

    with open(os.path.join(OUTPUT_DIR, f"{model_name}_report.txt"), "w", encoding="utf-8") as f:
        f.write(report_text)

results_df = pd.DataFrame(results).sort_values(by="f1_macro", ascending=False)
results_df.to_csv(os.path.join(OUTPUT_DIR, "model_comparison_with_rel.csv"), index=False, encoding="utf-8-sig")

with open(os.path.join(OUTPUT_DIR, "model_reports_with_rel.json"), "w", encoding="utf-8") as f:
    json.dump(reports, f, ensure_ascii=False, indent=2)

print("\nTop models:")
print(results_df)

print("\nSaved files:")
print("- output/processed_dataset_with_rel.csv")
print("- output/label_distribution.csv")
print("- output/model_comparison_with_rel.csv")
print("- output/model_reports_with_rel.json")
for model_name in models.keys():
    print(f"- output/{model_name}_report.txt")