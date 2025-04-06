import pandas as pd
from utils import parse_rule, extract_predicates_from_rule, calculate_confidence, remove_redundant_rules

def load_rules(filename):
    with open(filename, 'r') as f:
        return [line.strip() for line in f if line.strip()]

def compress_rules(rules, dataset, support_thresh=0.1, confidence_thresh=0.6):
    compressed = []
    for rule in rules:
        try:
            pred_fn, predicates = parse_rule(rule)
            # Check if all columns used in the rule exist in the dataset
            required_columns = set([p.replace("NOT ", "").strip() for p in predicates] + ["donor_is_old"])
            missing = required_columns - set(dataset.columns)
            if missing:
                print(f"Skipping rule '{rule}': missing columns {missing}")
                continue

            rule_support = dataset.apply(pred_fn, axis=1)
            support = rule_support.sum() / len(dataset)
            confidence = calculate_confidence(rule_support, dataset["donor_is_old"])
            if support >= support_thresh and confidence >= confidence_thresh:
                compressed.append((rule, support, confidence))
        except Exception as e:
            print(f"Error processing rule '{rule}': {e}")
    return remove_redundant_rules(compressed)

def main():
    df = pd.read_csv('dataset.tsv', sep='\t')
    rules = load_rules('rules.txt')
    compressed = compress_rules(rules, df)
    with open('compressed_rules.txt', 'w') as f:
        for rule, _, _ in compressed:
            f.write(f"{rule}\n")

if __name__ == '__main__':
    main()
