import json 
from rules_process import *


# generate training data in the train_data_save_file
raw_train_file= r'../dataset/raw_data/sanity_check_cases.txt'
# can use sanity_check_cases.txt to get a quick check
seqkey_graph_file = r'../dataset/raw_data/qwerty_graph.txt'
train_data_save_file = r'../dataset/processed_data/sanity_check_pairs.json'
processed_train_file_path = generate_train_data(raw_train_file,seqkey_graph_file,train_data_save_file)

# use training data to learn the transformation order for each rule
learned_transformation_save_file = r'../dataset/processed_data/sanity_check_transformations.json'
transformation_stat(processed_train_file_path, learned_transformation_save_file)
