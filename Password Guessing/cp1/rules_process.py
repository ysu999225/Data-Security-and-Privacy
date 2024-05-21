import sys
import json
import itertools

sys.path.append("./rules")

# Import necessary modules
try:
    from rule_capt import *
    from rule_CSS import *
    from rule_identical import *
    from rule_leet import *
    from rule_reverse import *
    from rule_substring import *
    from rule_seqkey import *
except Exception as e:
    print(f"Error: {e}")
    print("Cannot load rule modules correctly, please ensure you have followed the code framework")
    sys.exit(1)

def transformation_stat(processed_data_file, output_file):
    # Input the preprocessed dataset
    # Statistically record the frequency of transformations for each rule respectively
    # You will save a dictionary in a json file in the end
    # keys() = rules (in string)
    # values() = list of transformations (sorted by their frequency)
    # two special case: 
    # 1. seqkey, the transformation recorded in the value list will be the walk founded, input transformation= "qwert\t1q2w3e", this transformation count as 1 time for "qwert" and 1 time for "1q2w3e"
    # 2. substring, to handle if the guessing pw is a substring of input pw, add a special character at the very front of substring transformation list to trigger guess_target_as_substring().
    rules = ['identical', 'substring', 'capt', 'leet', 'reverse', 'seqkey', 'CSS']
    rule_stat = {}
    for r in rules:
        rule_stat[r] = {}
    with open(processed_data_file, 'r') as f:
        preprocess_data = json.load(f)
        for item in preprocess_data:
            cur_rule = item[1][0]
            cur_trans = item[1][1]
            if cur_rule not in rules:
                continue
            if cur_rule == 'seqkey':
                # Special handle for seqkey transformation: frequency of appeared seq strings
                for seq in cur_trans.split('\t'):
                    if seq in rule_stat[cur_rule].keys():
                        rule_stat[cur_rule][cur_trans] += 1
                    else:
                        rule_stat[cur_rule][cur_trans] = 1
                continue
            if cur_trans in rule_stat[cur_rule].keys():
                rule_stat[cur_rule][cur_trans] += 1
            else:
                rule_stat[cur_rule][cur_trans] = 1

    rule_transformation_in_order = {}
    for r in rules:
        rule_transformation_in_order[r] = sorted(rule_stat[r].keys(), key=lambda x: rule_stat[r][x], reverse=True)
    
    # Special handle for 'special_trans_as_substring' transformation
    rule_transformation_in_order['substring'] = ['special_trans_as_substring'] + rule_transformation_in_order['substring']
    
    # Save the rule transformations in order in a JSON file
    with open(output_file, "w") as file:
        json.dump(rule_transformation_in_order, file)
    print(f'{output_file} has been saved!')
    return True


def get_all_pairs(pw_list):
    # Generate all possible unique pairs from a list of passwords
    # Input a list of passwords, ['abc', 'ab', 'bc']
    # Output all pairs, [('abc', 'ab'), ('abc', 'bc'), ('ab', 'bc')]
    pairs = list(itertools.combinations(pw_list, 2))
    return pairs

def get_all_pairs_symmetric(pw_list):
    # Generate all possible unique pairs and their symmetric counterparts
    # Input a list of passwords, ['abc', 'ab', 'bc']
    # Output all pairs in two ways, [('abc', 'ab'), ('abc', 'bc'), ('ab', 'bc'), ('ab', 'abc'), ('bc', 'abc'), ('bc', 'ab')]
    pairs = list(itertools.combinations(pw_list, 2))
    pairs += [(pair[1], pair[0]) for pair in pairs]
    return pairs

def generate_train_data(path, graph_path, output_file):
    # Generate training data by processing the input dataset (from path)
    # graph_path is used for the seqkey rule
    # Save the processed data in the output_file
    # In the end, Json will save a list, each element of the list is [[pair],[rule the pair belongs to, transformation between pair[0] and pair[1]]]
    input_dataset = path
    dataset_rule_list = []
    rule_seqkey_graph = eval(open(graph_path).read())
    
    # Read input data file
    with open(input_dataset, 'r', errors='ignore') as f:
        all_pairs = []
        for line in f:
            split_line = line.strip().split('\t')
            cur_pairs = get_all_pairs(split_line[1:])
            all_pairs += cur_pairs

    identical = 0
    no_rule = 0
    
    # Check and apply rules on the password pairs
    for pair in all_pairs:
        # Check and apply identical rule
        if check_identical(pair[0], pair[1]):
            transformation = check_identical_transformation(pair[0], pair[1])
            dataset_rule_list.append([pair, ['identical', transformation]])
            identical += 1
        # Check and apply substring rule
        elif check_substring(pair[0], pair[1]):
            transformation = check_substring_transformation(pair[0], pair[1])
            dataset_rule_list.append([pair, ['substring', transformation]])
        # Check and apply capitalization rule
        elif check_capt(pair[0], pair[1]):
            transformation = check_capt_transformation(pair[0], pair[1])
            dataset_rule_list.append([pair, ['capt', transformation]])
        # Check and apply leet rule
        elif check_leet(pair[0], pair[1]):
            transformation = check_leet_transformation(pair[0], pair[1])
            dataset_rule_list.append([pair, ['leet', transformation]])
        # Check and apply reverse rule
        elif check_reverse(pair[0], pair[1]):
            transformation = check_reverse_transformation(pair[0], pair[1])
            dataset_rule_list.append([pair, ['reverse', transformation]])
        # Check and apply sequential key rule
        elif check_seqkey(pair[0], pair[1], rule_seqkey_graph):
            transformation = check_seqkey_transformation(pair[0], pair[1], rule_seqkey_graph)
            dataset_rule_list.append([pair, ['seqkey', transformation]])
        # Check and apply CSS rule
        elif check_CSS(pair[0], pair[1]):
            transformation = check_CSS_transformation(pair[0], pair[1])
            dataset_rule_list.append([pair, ['CSS', transformation]])
        else:
            no_rule += 1
            continue

    # Report rule ratios
    total = len(all_pairs)
    print("Identical ratio: {}".format(identical/total))
    print("No rule ratio: {}".format(no_rule/total))
    print("Other rules ratio: {}".format((total-no_rule-identical)/total))

    # Save the processed data-rule list in a JSON file
    with open(output_file, "w") as file:
        json.dump(dataset_rule_list, file)
    print(f'{output_file} has been saved!')
    return output_file


def generate_test_data(path, graph_path, output_file, filter=False):
    # Generate test data by processing the input dataset (from path)
    # graph_path is used for the seqkey rule
    # Save the processed data in the output_file
    # In the end, Json will save a list, each element of the list is [[pair],["nan", "nan"]]
    # If filter == True: it will filter out all identical and no_rule pairs like the setting in the paper
    # If filter == False: it will keep all pairs
    input_dataset = path
    dataset_rule_list = []
    rule_seqkey_graph = eval(open(graph_path).read())
    
    # Read input data file
    with open(input_dataset, 'r', errors='ignore') as f:
        all_pairs = []
        for line in f:
            split_line = line.strip().split('\t')
            cur_pairs = get_all_pairs_symmetric(split_line[1:])
            all_pairs += cur_pairs

    identical = 0
    no_rule = 0
    
    # Check and apply rules on the password pairs
    for pair in all_pairs:
        if not filter:
            dataset_rule_list.append([pair, ["nan", "nan"]])
            continue

        # Check and apply identical rule
        if check_identical(pair[0], pair[1]):
            identical += 1
        # Check and apply other rules
        elif any([
            check_substring(pair[0], pair[1]),
            check_capt(pair[0], pair[1]),
            check_leet(pair[0], pair[1]),
            check_reverse(pair[0], pair[1]),
            check_seqkey(pair[0], pair[1], rule_seqkey_graph),
            check_CSS(pair[0], pair[1]),
        ]):
            dataset_rule_list.append([pair, ["nan", "nan"]])
        else:
            no_rule += 1

    # Report rule ratios
    total = len(all_pairs)
    if filter:
        print("Identical ratio: {}".format(identical/total))
        print("No rule ratio: {}".format(no_rule/total))
        print("Other rules ratio: {}".format((total-no_rule-identical)/total))

    # Save the processed data-rule list in a JSON file
    with open(output_file, "w") as file:
        json.dump(dataset_rule_list, file)
    print(f'{output_file} has been saved!')
    return output_file
