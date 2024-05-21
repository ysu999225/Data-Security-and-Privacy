import numpy as np
import json
import sys
import random
from tqdm import tqdm

# please don't modify this line otherwise you will get different results
random.seed(100)

# ---------------------------------------------------------------------------------------- Load module ----------------------------------------------------------------------------------------
sys.path.append('../cp1')
sys.path.append("../cp1/rules")

try:
    from model import NBClassifier
    from rule_capt import *
    from rule_CSS import *
    from rule_identical import *
    from rule_leet import *
    from rule_reverse import *
    from rule_substring import *
    from rule_seqkey import *
    from rules_process import *


except Exception as e:
    print(f"Error: {e}")
    print("Cannot load rule modules correctly, please ensure you have followed the code framework")
    sys.exit(1)


# guess rules for this MP, each guess rule will contain many transformations given in transformation matrix
guess_classes = ['identical', 'leet', 'reverse',
                 'substring', 'seqkey', 'capt', 'CSS']

# idx of each guess rule in guess_classes, they will be the output of naive bayes classifier
guess_class_index = {'identical': 0, 'leet': 1, 'reverse': 2,'substring': 3, 'seqkey': 4, 'capt': 5, 'CSS': 6}

# the functions to apply the transformation rules, which are imported from cp1/rules
guess_functions = {'identical': apply_identical_transformation,
                   'leet': apply_leet_transformation,
                   'reverse': apply_reverse_transformation,
                   'substring': apply_substring_transformation,
                   'seqkey': apply_seqkey_transformation,
                   'capt': apply_capt_transformation,
                   'CSS': apply_CSS_transformation}


# ---------------------------------------------------------------------------------------- Helper Funcs ----------------------------------------------------------------------------------------


# vectorize the password, turn the string into a dim-18 vector
# the vector is used as features for naive bayes classifier
# input: password(string), password is the raw string password
# output: vector(np.array with shape (1,18)), a dim-18 vector as the input of naive bayes classifier
def vectorize(password):
    
    vector = []

    # ***********************************************************************
    # ****************************** TODO ***********************************
    # ***********************************************************************

    # we extract 18 features from the password
    # they are used as features for naive bayes classifier
    # we have implemented feature 11 for you, please implement the rest of them
    # REMEMBER: the order of features should be exactly the same as the order of them in return vector
    #           each element should be an integer!

    # 1. password length
    f1 = len(password)

    # 2. number of lowercase letters
    f2 = 0
    for c in password:
        if c.islower():
            f2 += 1
    

    # 3. number of uppercase letters
    f3 = 0
    for c in password:
        if c.isupper():
            f3 += 1
   

    # 4. number of digits
    f4 = 0
    for c in password:
        if c.isdigit():
            f4 += 1
   

    # 5. number of special characters (not a-z, A-Z, 0-9)
    f5 = len(password) - f2 - f3 - f4

   

    # 6. letter-only password? (1 for yes, 0 for no)
    f6 = 1
    if f4 > 0 or f5 > 0:
        f6 = 0
    

    # 7. digit-only password? (1 for yes, 0 for no)
    f7 = 1
    if f2 > 0 or f3 > 0 or f5 > 0:
        f7 = 0
    

    # 8. number of repeated character (Put each character into lower case. For each pair of characters next to each other, if they are the same, count 1. e.g. 'aabb' has 2 repeated characters.)
    rep_char = []
    for c in password:
        if c not in rep_char and password.count(c) > 1:
            rep_char.append(c)
    f8 = len(rep_char)

    # 9. max number of consec. letters
    f9 = 0
    count = 0
    for c in password:
        if c.isalpha():
            count += 1
            f9 = max(f9, count)
        else:
            count = 0

    # 10. max number of consec. digits
    f10 = 0
    count = 0
    for c in password:
        if c.isdigit():
            count += 1
            f10 = max(f10, count)
        else:
            count = 0

    # 11. max number of sequential keys (we have implemented this for you, just skip)
    f11 = walk_checker(seq_graph,password)
    if f11 == False :
        f11 = ""
    f11 = len(f11)
   

    # 12. Englishword-only password? (this should be exactly the same as feature 6 in this MP)
    f12 = f6

    # 13. number of consec. digits (head)
    f13 = 0
    for c in password:
        if c.isdigit():
            f13 += 1
        else:
            break

    # 14. number of consec. digits (tail)
    f14 = 0
    for c in password[::-1]:
        if c.isdigit():
            f14 += 1
        else:
            break

    # 15. number of consec. letters (head)
    f15 = 0
    for c in password:
        if c.isalpha():
            f15 += 1
        else:
            break


    # 16. number of consec. letters (tail)
    f16 = 0
    for c in password[::-1]:
        if c.isalpha():
            f16 += 1
        else:
            break


    # 17. number of consec. special characters (head)
    f17 = 0
    for c in password:
        if c.isalnum():
            break
        else:
            f17 += 1

    # 18. number of consec. special characters (tail)
    f18 = 0
    for c in password[::-1]:
        if c.isalnum():
            break
        else:
            f18 += 1
            
    vector.append(f1)
    vector.append(f2)
    vector.append(f3)
    vector.append(f4)
    vector.append(f5)
    vector.append(f6)
    vector.append(f7)
    vector.append(f8)
    vector.append(f9)
    vector.append(f10)
    vector.append(f11)
    vector.append(f12)
    vector.append(f13)
    vector.append(f14)
    vector.append(f15)
    vector.append(f16)
    vector.append(f17)
    vector.append(f18)
    return np.array(vector)



# guess the password sequentially in the priority of class given by bayes estimation
# guess all transformations from one class at a time then switch to next lower-prioritized class
# input: password(string), the first element in each test pairs (the given password for you to guess the second element in each pair)
# output: guess(string), the output of generator, which is the guessed password, you need to compared with the second element in each pair to verity correctness
# REMEMBER: please use python generator here, because we use next() to get the guess from your generator
def sequential_guessor(password):

    # class_order is the priority of those classes
    class_probs = model.predict_proba(vectorize(password).reshape(1,-1))[0]
    class_order = np.argsort(class_probs)[::-1]

    # ***********************************************************************
    # ****************************** TODO ***********************************
    # ***********************************************************************

    # sequential guessing (high rank class has absolute priority to guess)
    # iterate over all transformations in that class
    # higher (from naive bayes estimation) class's transformation has absolute priority over lower ones
    # Example:
    # if the class_order is [4,2,1,3,5,6,0]
    # the guess order will be:
    # 4[0],4[1],4[2],4[3]... -> 2[0],2[1],2[2]...->...->0[0],0[1],0[2]...
    # here [#] means the [#]th transformation in that class
    # Mapping class indices to transformation functions
    transformation_functions = {
        0: apply_identical_transformation,
        1: apply_leet_transformation,
        2: apply_reverse_transformation,
        3: apply_substring_transformation,
        4: lambda pwd, trans: apply_seqkey_transformation(pwd, trans, seq_graph),  # Handle the special case with a lambda
        5: apply_capt_transformation,
        6: apply_CSS_transformation
    }
        # Iterate over each class in the order of their probability
    for class_idx in class_order:
        transformation_list = transformation_mat[guess_classes[class_idx]]
        func = transformation_functions[class_idx]  # Retrieve the appropriate transformation function

        # Apply the transformation function to each transformation in the list
        for transformation in transformation_list:
            output = func(password, transformation)

            # Yield each transformed output
            for o in output:
                yield o
    
    # for class_idx in class_order:
    #     transaformation_list = transformation_mat[guess_classes[class_idx]]
    #     for transformation in transaformation_list:
    #         output = []
    #         if class_idx == 0:
    #             output = apply_identical_transformation(password, transformation)
    #         elif class_idx == 1:
    #             output = apply_leet_transformation(password, transformation)
    #         elif class_idx == 2:
    #             output = apply_reverse_transformation(password, transformation)
    #         elif class_idx == 3:
    #             output = apply_substring_transformation(password, transformation)
    #         elif class_idx == 4:
    #             output = apply_seqkey_transformation(password, transformation, seq_graph)
    #         elif class_idx == 5:
    #             output = apply_capt_transformation(password, transformation)
    #         elif class_idx == 6:
    #             output = apply_CSS_transformation(password, transformation)
    #         for o in output:
    #             guess = o
    #             yield guess

    #yield None

    #guess = None

    #yield guess



# guess the password rotationally in the priority of class given by bayes estimation
# guess one transformation from one class at a time then switch to next lower-prioritized class
# when reach to the last class (the lowest priority class), switch back to the highest priority class
def rotational_guessor(password):
    class_probs = model.predict_proba(vectorize(password).reshape(1,-1))[0]
    class_order = np.argsort(class_probs)[::-1]

    class_idx = 0  # the idx of current guessing class
    trans_idxs = [-1 for _ in range(len(transformation_mat))]  # the idx of current guessing transformation of each class
    trans_idxs_limit = [len(transformation_mat[i]) for i in guess_classes]  # the number of transformations in each class
    alive = len(trans_idxs_limit)  # the number of classes that still have transformation to try
    alive_list = [1 for _ in range(len(transformation_mat))]  # the alive status of each class

    # guess at most guess_limit times
    # we guess one transformation from one class at a time then switch to next class
    while alive > 0:
        
        # the idx of current guessing transformation of current guessing class
        trans_idxs[class_order[class_idx]] += 1
        trans_idx = trans_idxs[class_order[class_idx]]

        # if the class has no more transformation to try, report dead and skip
        if trans_idxs_limit[class_order[class_idx]] <= trans_idx and alive_list[class_order[class_idx]] == 1:
            alive -= 1
            alive_list[class_order[class_idx]] = 0
            class_idx = (class_idx + 1) % len(transformation_mat)
            continue

        # if the class has no more transformation to try and have reported, skip
        elif trans_idxs_limit[class_order[class_idx]] <= trans_idx:
            class_idx = (class_idx + 1) % len(transformation_mat)
            continue
 
        else:
            cur_func = guess_functions[guess_classes[class_order[class_idx]]]
            if cur_func == apply_seqkey_transformation:
                cur_guesses = cur_func(password, transformation_mat[guess_classes[class_order[class_idx]]][trans_idx],seq_graph)
            else:
                cur_guesses = cur_func(password, transformation_mat[guess_classes[class_order[class_idx]]][trans_idx])


            # iterate over all guesses from that transformation
            for guess in cur_guesses:
                yield guess

            # switch to next class
            class_idx = (class_idx + 1) % len(transformation_mat)
            continue
  


# input: path(string), the file path to the json file you generated (using function generate_test_data in rule_process.py)
# output: ret_pairs(list of pairs). 1st element in each pair is the given password, 2nd element is what you need to guess
def loading_test_data(path):

    with open(path, "r") as file:
        dataset_rule_list = json.load(file)

    pass_word_dict = {}
    ret_pairs = []
    for pair in dataset_rule_list:
        pass1,pass2 = pair[0]
        ret_pairs.append([pass1,pass2])
    
    return ret_pairs


# in this function we will vectorize each training password and label each training password with a guess class.
# vectorizing procedure: for each password we call vectorize function to get a feature vector (dim-18)
# labeling procedure: for each password, we get all pairs where the first element is the password, then we label the password with the most frequent guess class in the pairs
# input: path(string), the file path to the json file you generated (using function generate_train_data in rule_process.py)
# output: trainx(np.array with shape (# of samples, # of features)), trainy(np.array with shape (1, # of samples)), they are for training of Naive Bayes
def loading_train_data(path):

    with open(path, "r") as file:
        dataset_rule_list = json.load(file)

    pass_word_dict = {}

    for pair in dataset_rule_list:
        pass1,pass2 = pair[0]
        passtype = pair[1][0]
        if pass1 not in pass_word_dict:
            pass_word_dict[pass1] = np.array([0 for i in range(len(guess_classes))])
            pass_word_dict[pass1][guess_class_index[passtype]] += 1
        else:
            pass_word_dict[pass1][guess_class_index[passtype]] += 1
        
        if pass2 not in pass_word_dict:
            pass_word_dict[pass2] = np.array([0 for i in range(len(guess_classes))])
            pass_word_dict[pass2][guess_class_index[passtype]] += 1
        else:
            pass_word_dict[pass2][guess_class_index[passtype]] += 1


    for key in pass_word_dict:
        v = pass_word_dict[key]
        indices = np.where(v == np.max(v))[0]
        if len(indices) > 1:
            # random select one
            pass_word_dict[key] = indices[np.random.randint(len(indices))]
        else:
            pass_word_dict[key] = indices[0]

    
    print("total num of training passwords: ",len(pass_word_dict))
    train_x = np.zeros((len(pass_word_dict), 18))
    train_y = np.zeros(len(pass_word_dict))
    
    for i,key in enumerate(pass_word_dict):
        train_x[i] = vectorize(key)
        train_y[i] = pass_word_dict[key]

    return train_x,train_y



if __name__ == "__main__":

    # ----------------------------------------------------------------------------------------- Load data -----------------------------------------------------------------------------------------
    try:
        # we load the transformation matrix here
        # transformation matrix is a dict(string,list of string)
        # the key is the guess class as listed in variable guess_classes
        # the value is a list of transformations(string) in that class
        # you need to apply transfomation (via apply_xxx_transformation functions) to a given password (the 1st element in pair) to guess the targeted password (the 2nd element in pair)
        print("loading transformation matrix...")
        mat_path = r"../dataset/processed_data/rule_transformation_in_order.json"
        with open(mat_path, 'r') as f:
            transformation_mat = json.load(f)
            
        
        # this is for the seqkey class, we extract the necessary information and form a graph to accelerate the procedure
        graph_path=r"../dataset/raw_data/qwerty_graph.txt"
        seq_graph = eval(open(graph_path).read())

        
        
        # load the training data
        # the procedure is as follows:
        # 1.generate json pairs (stored in train_json_path) using function generate_train_data in rule_process.py (stored in train_raw_path), each pair is a list of two strings, the 1st element is the given password, the 2nd element is the targeted password
        # 2.load the json file using function loading_train_data in pipeline.py, this function will vectorize each string password into a dim-18 numerical vector
        print("-----------------------------------------")
        print("loading training data...")
        train_raw_path = r"../dataset/raw_data/train.txt"
        train_json_path = r'../dataset/processed_data/train_pairs.json'
        generate_train_data(train_raw_path,graph_path,train_json_path)
        train_x,train_y = loading_train_data(train_json_path)


        
        # load the testing data
        # the procedure is almost the same as load training data
        print("-----------------------------------------")
        print("loading testing data...")
        test_raw_path = r"../dataset/raw_data/test.txt"
        test_json_path = r'../dataset/processed_data/test_pairs.json'
        generate_test_data(test_raw_path,graph_path, test_json_path,filter=False)
        test_pair_no_filter = loading_test_data( test_json_path)

        #------------------------DONT MODIFY THIS--------------------------
        testing_ratio = 0.05
        final_test_pairs = random.sample(test_pair_no_filter, int(len(test_pair_no_filter)*testing_ratio))
        print("total num of testing passwords: ",len(final_test_pairs))
        #------------------------------------------------------------------
        
    except Exception as e:
        print("-----------------------------------------")
        print(f"Error: {e}")
        print("Error in loading data (training, testing and transformation matrix)")
        sys.exit(1)

    # ------------------------------------------------------------------------------------------- Training -------------------------------------------------------------------------------------------
 
    # initialize the naive bayes classifier
    model = NBClassifier()

    try:
        print("-----------------------------------------")
        print("training...")
        model.train(train_x, train_y)

    except Exception as e:
        print("-----------------------------------------")
        print(f"Error: {e}")
        print("the format of training file is not correct")
        sys.exit(1)


    # --------------------------------------------------------------------------------------- Guessing Password ---------------------------------------------------------------------------------------

    try:
        print("-----------------------------------------")
        print("Start guessing...")
        success = 0   # number of success guesses

        #------------------------DONT MODIFY THIS--------------------------
        guess_limit = 1000  # number of guesses allowed for each password
        #------------------------------------------------------------------

        # iterate all test pairs
        # we try to predict pair[1] by pair[0] based on naive bayes model
        for pair in tqdm(final_test_pairs):
            found = 0
            # pair[0] is the given password, using this to guess pair[1]
            seq_guessor = sequential_guessor(pair[0])
            rot_guessor = rotational_guessor(pair[0])

            for _ in range(guess_limit):
                try:
                    cur_guess = next(seq_guessor)
                    if cur_guess == pair[1]:
                        success += 1
                        found = 1
                        break
                except StopIteration:
                    break

            # if sequential guessing fails, we try rotational guessing (1000 guesses allowed)
            if not found:
                for _ in range(guess_limit):
                    try:
                        cur_guess = next(rot_guessor)
                        if cur_guess == pair[1]:
                            success += 1
                            found = 1
                            break
                    except StopIteration:
                        break


    except Exception as e:
        print("-----------------------------------------")
        print(f"Error: {e}")
        print("error in guessing procedure, please check the format of transformation matrix and apply-rule functions")
        sys.exit(1)

    
    # Success rate, the portion of pairs you successfully guess the second element given the first
    print("***************************************")
    print("Success rate: {}".format(success / len(final_test_pairs)))
    print("***************************************")
