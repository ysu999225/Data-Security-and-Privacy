def check_reverse(pw1,pw2):
    #pw1,pw2 (string,string): a pair of input password
    #output (boolean): if pw1 and pw2 can be transformed by this category of rule
    pw1_reverse = pw1[::-1]
    if pw1_reverse == pw2:
        return True 
    return False 

def check_reverse_transformation(pw1, pw2):
    #pw1,pw2 (string,string): a pair of input password
    #output (string): transformation between pw1 and pw2
    return '' 

def apply_reverse_transformation(ori_pw, transformation):
    #ori_pw (string): input password that needs to be transformed
    #transformation (string): transformation in string, no use here
    #output (list of string): list of passwords that after transformation
    return [ori_pw[::-1]]