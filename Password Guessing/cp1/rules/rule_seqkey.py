
def walk_checker(graph, password, length=4, strict=False, repeat=True):
    # Check if substring of password is a walk in graph with at least "length" length.
    # Check if password length matches the specified length (if strict=True)
    if strict and len(password) != length:
        return False
    # Initialize variables
    result = False
    path = password[0]
    return_path = password[0]
    max_path_len = 1
    # Traverse the graph and build the traversal path
    for i in range(len(password)-1):
        current = password[i]
        next_ = password[i+1]
        # Check if next character is a valid adjacent vertex
        if current not in graph.keys():
            graph[current] = {}
        if next_ in graph[current].values() and (next_.lower() != current.lower() if not repeat else True):
            path += next_
        else:
            if len(path) > max_path_len:
                max_path_len = len(path)
                return_path = path
            path = next_
    if len(path) > max_path_len:
        max_path_len = len(path)
        return_path = path
        # Check if the traversal path meets the minimum length requirement
    if max_path_len >= length:
        result = True
    # Return the traversal path (if it meets the minimum length requirement) or False
    return return_path if result else False


def check_seqkey(pw1,pw2, graph):
    #pw1,pw2 (string,string): a pair of input password
    #output (boolean): if pw1 and pw2 can be transformed by this category of rule
    pw1_walk = walk_checker(graph, pw1, length=max(0.5*len(pw1), 3))
    pw2_walk = walk_checker(graph, pw2, length=max(0.5*len(pw2), 3))
    if pw1_walk and pw2_walk:
        return True
    return False

def check_seqkey_transformation(pw1, pw2, graph):
    #pw1,pw2 (string,string): a pair of input password
    #output (string): transformation between pw1 and pw2
    pw1_walk = walk_checker(graph, pw1, length=max(0.5*len(pw1), 3))
    pw2_walk = walk_checker(graph, pw2, length=max(0.5*len(pw2), 3))
    return '\t'.join([pw1_walk, pw2_walk])

def apply_seqkey_transformation(ori_pw, transformation, graph):
    #ori_pw (string): input password that needs to be transformed
    #transformation (string): transformation in string (different from above, commonest walk str)
    #output (list of string): list of passwords that after transformation
    ori_walk = walk_checker(graph, ori_pw)
    if ori_walk:
        return [ori_pw.replace(ori_walk,transformation)] 
    return []
