import numpy as np

def parse_rule(rule_str):
    lhs, _ = rule_str.split("=>")
    lhs = lhs.strip()
    predicates = [p.strip() for p in lhs.split("AND")]

    def predicate_fn(row):
        result = True
        for pred in predicates:
            if pred.startswith("NOT"):
                name = pred[4:].strip()
                val = row.get(name, np.nan)
                if pd.isna(val) or val == 1:
                    result = False
            else:
                val = row.get(pred, np.nan)
                if pd.isna(val) or val != 1:
                    result = False
        return result

    return predicate_fn, predicates

def extract_predicates_from_rule(rule_str):
    lhs, _ = rule_str.split("=>")
    lhs = lhs.strip()
    predicates = [p.strip() for p in lhs.split("AND")]
    return [p.replace("NOT ", "").strip() for p in predicates]

def calculate_confidence(rule_support_series, actual_labels):
    match = (rule_support_series & (actual_labels == 1))
    total = rule_support_series.sum()
    if total == 0:
        return 0.0
    return match.sum() / total

def remove_redundant_rules(rule_list):
    seen = set()
    filtered = []
    for rule, support, confidence in rule_list:
        if rule not in seen:
            filtered.append((rule, support, confidence))
            seen.add(rule)
    return filtered