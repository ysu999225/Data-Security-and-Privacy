import itertools

def check_capt(pw1,pw2):
    #pw1,pw2 (string,string): a pair of input password
    #output (boolean): if pw1 and pw2 can be transformed by this category of rule
    #e.g. pw1 = abcdE, pw2= abCde, output =True
    
    # ***********************************************************************
    # ****************************** TODO ***********************************
    # ***********************************************************************
    if len(pw1) != len(pw2):
        return False
    
    pw1_lower = pw1.lower()
    p2_lower = pw2.lower()

    if pw1_lower == p2_lower:
        return True

    return False 

def check_capt_transformation(pw1, pw2):
    #pw1,pw2 (string,string): a pair of input password
    #output (string): transformation between pw1 and pw2
    #consider if head char is capt transformed, if tail char is capt transformed, and # of chars that has been capt transformed in total
    #example pw1 = abcde, pw2 = AbcDe, transformation = head\t2 (head char is capt transformed, in total 2 chars are capt transformed)
    #example pw1 = abcdE, pw2 = AbcDe, transformation = head\ttail\t3 (head char and tail chars are capt transformed, in total 3 chars are capt transformed)
    #example pw1 = abcde, pw2 = abcDe, transformation = 1 (in total 1 chars are capt transformed)

    # ***********************************************************************
    # ****************************** TODO ***********************************
    # ***********************************************************************
    output = ''
    if pw1[0] != pw2[0]:
        output += 'head\t'
    if pw1[-1] != pw2[-1]:
        output += 'tail\t'
    
    count = 0
    for i in range(len(pw1)):
        if pw1[i] != pw2[i]:
            count += 1
    
    output += str(count)

    return output
    #return ''

def apply_capt_transformation(ori_pw, transformation):
    #ori_pw (string): input password that needs to be transformed
    #transformation (string): transformation in string
    #output (list of string): list of passwords that after transformation (all possiblities)
    #ori_pw = "abcde", transformation = "head\t2", output = [ABcde, AbCde, AbcDe]
    
    # ***********************************************************************
    # ****************************** TODO ***********************************
    # ***********************************************************************
    try:
        if not ori_pw:  
            return []
        output = []
        potential_pw = ori_pw  
        count = int(transformation.split('\t')[-1])  
        if 'head' in transformation:
            count -= 1  
            potential_pw = (ori_pw[0].upper() if ori_pw[0].islower() else ori_pw[0].lower()) + ori_pw[1:]
        if 'tail' in transformation:
            count -= 1  
            potential_pw = potential_pw[:-1] + (potential_pw[-1].upper() if potential_pw[-1].islower() else potential_pw[-1].lower())

        
        dfs_change(potential_pw, count, output, 1)
        return output
    except Exception as e:
        print(f"An error occurred in apply_capt_transformation: {e}")
        return []  

def dfs_change(pw, count, output, pos):
    try:
        if count == 0:
            output.append(pw)
            return
        for i in range(pos, len(pw)): 
            if pw[i].islower() or pw[i].isupper():  
                new_char = pw[i].upper() if pw[i].islower() else pw[i].lower()
                dfs_change(pw[:i] + new_char + pw[i+1:], count - 1, output, i + 1)
    except Exception as e:
        print(f"An error occurred in dfs_change: {e}")


