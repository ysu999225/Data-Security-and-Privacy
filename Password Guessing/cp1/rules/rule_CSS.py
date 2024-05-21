def All_CS(pw1, pw2):
    # find multiple common substrings between the inputs.
    # output 1. boolean: can find common substrings met the conditions specified by the threshold, min_lcs, and max_lcs
    # output 2. list: list of common strings found.
    # output 3. list: list of remaining strings for pw1.
    # output 4. list: same as above for pw2
    # example: All_CS("xyabcz", "abcxy") = (True, ['abc'], ['xy','z'], ['','xy'])
   
    threshold = 0.5
    min_lcs = 3
    max_lcs = 5

    total_length = min(len(pw1), len(pw2))
    common_length = 0
    common_list = []
    remain1, remain2 = [], []

    while True:
        css_len = 0
        common = ""
        loc_pw1, loc_pw2 = -1, -1
        
        # Iterate over the input strings to find the css_len common substring
        for idx1 in range(len(pw1)):
            inner_flag = False
            for idx2 in range(len(pw2)):
                length = 0

                # Compare characters at the current positions and increment the length if they are the same
                while (idx1 + length < len(pw1) and idx2 + length < len(pw2) and
                       pw1[idx1 + length] == pw2[idx2 + length]):
                    length += 1

                # Update the css_len common substring and its locations if a longer one is found
                if length >= min_lcs:
                    css_len = length
                    common = pw1[idx1:idx1 + length]
                    loc_pw1, loc_pw2 = idx1, idx2
                    inner_flag = True 
                    break 
            if inner_flag:
                break
                

        # If no common substring is found, break the loop
        if css_len == 0:
            remain1.append(pw1)
            remain2.append(pw2)
            break

        # Add the found common substring to the list and update the common_length
        common_list.append(common)
        common_length += css_len

        # Remove the found common substring from the input strings
        remain1.append(pw1[:loc_pw1])
        remain2.append(pw2[:loc_pw2])
        pw1 = pw1[loc_pw1 + css_len:]
        pw2 = pw2[loc_pw2 + css_len:]
    if len(common_list) == 0:
        return False, None, None, None
    max_common_len = max([len(i) for i in common_list])
    # Check if the conditions are met and return the results accordingly
    if (float(common_length) / total_length >= threshold and max_common_len >= min_lcs) or max_common_len >= max_lcs:
        return True, common_list, remain1, remain2
    else:
        return False, None, None, None

def check_CSS(pw1,pw2):
    #pw1,pw2 (string,string): a pair of input password
    #output (boolean): if pw1 and pw2 can be transformed by this category of rule
    return All_CS(pw1, pw2)[0] 

def check_CSS_transformation(pw1, pw2):
    #pw1,pw2 (string,string): a pair of input password
    #output (string): transformation between pw1 and pw2
    _, ccs_list , remain1, remain2 = All_CS(pw1, pw2)
    if len(remain1) == len(remain2):
        # should always the same, but just to check
        return '\t'.join(remain1+remain2)
    return None 

def apply_CSS_transformation(ori_pw, transformation):
    #ori_pw (string): input password that needs to be transformed
    #transformation (string): transformation in string
    #output (list of string): list of passwords that after transformation
    #some edge cases haven't handled: if remain str have overlap, 'abc', 'bcd', may need to use recursion
    transformation_split = transformation.split('\t')
    if len(transformation_split) % 2 == 1:
        return []
    remain1 = transformation_split[:len(transformation_split)//2]
    remain2 = transformation_split[(len(transformation_split)//2):]
    possible_pws = []

    forward_password = ori_pw
    forward_flag = True
    for i in range(len(remain1)):
        if remain1[i] in forward_password:
            forward_password = forward_password.replace(remain1[i], remain2[i])
        else:
            forward_flag=False
            break 
    if forward_flag:
        possible_pws.append(forward_password)

    backward_password = ori_pw
    backward_flag = True
    for i in range(len(remain2)):
        if remain2[i] in backward_password:
            backward_password = backward_password.replace(remain2[i], remain1[i])
        else:
            backward_flag=False
            break 
    if backward_flag:
        possible_pws.append(backward_password)
    return possible_pws