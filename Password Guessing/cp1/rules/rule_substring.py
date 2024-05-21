def check_substring(pw1,pw2):
    #pw1,pw2 (string,string): a pair of input password
    #output (boolean): if pw1 and pw2 can be considered as substring of the other 
    # eg. pw1 = abc, pw2 = abcd, output true
    # eg. pw1 = abcde, pw2 = abcd, output true

    # ***********************************************************************
    # ****************************** TODO ***********************************
    # ***********************************************************************
    if pw1 in pw2 or pw2 in pw1:
        return True
    return False

def check_substring_transformation(pw1, pw2):
    #pw1,pw2 (string,string): a pair of input password
    #output (string): transformation between pw1 and pw2
    #example: pw1=123hello!!, pw2=hello, output=head\t123\ttail\t!!
    #example: pw1=hello!!, pw2=hello, output=head\t\ttail\t!!

    # ***********************************************************************
    # ****************************** TODO ***********************************
    # ***********************************************************************
    output = ''
    if pw1 in pw2:
        index = pw2.find(pw1)
        head = pw2[:index]
        tail = pw2[index + len(pw1):]
    elif pw2 in pw1:
        index = pw1.find(pw2)
        head = pw1[:index]
        tail = pw1[index + len(pw2):]
    output = f"head\t{head}\ttail\t{tail}"
    return output
    #return ''

def guess_target_as_substring(ori_pw):
    #the first transformation applied in rule_substring
    #guess the possible passwords as a substring
    #decide to only consider the substring from head or from tail
    #e.g. pw1=abc123, output = [a,ab,abc,abc1,abc12,3,23,123,c123,bc123]
    #in transformation dictionary, the transformation = 'special_trans_as_substring'

    # ***********************************************************************
    # ****************************** TODO ***********************************
    # ***********************************************************************
    output = []
    # generate substrings from the head
    for i in range(len(ori_pw)):
        output.append(ori_pw[:i+1])
    
    # generate substrings from the tail 
    # but excluding the full string t
    for i in range(1, len(ori_pw)):
        output.append(ori_pw[-i:])

    return output
    #return []

def apply_substring_transformation(ori_pw, transformation):
    #ori_pw (string): input password that needs to be transformed
    #transformation (string): transformation in string
    #output (list of string): list of passwords that after transformation
    #add head string to head, add tail string to tail
    
    # ***********************************************************************
    # ****************************** TODO ***********************************
    # ***********************************************************************
    try:
        if not ori_pw or not transformation:
            return []
        print("transformation111",transformation)
        if transformation == 'special_trans_as_substring':
            print(guess_target_as_substring(ori_pw))
            return guess_target_as_substring(ori_pw)
        output = []
        print("transformation111",transformation)
        head_tag = 'head\t'
        tail_tag = '\ttail\t'
        
        head_pos = transformation.find(head_tag)
        tail_pos = transformation.find(tail_tag)
        
        print(head_pos, tail_pos)

        if head_pos == -1 or tail_pos == -1 or head_pos >= tail_pos:
            print("Error: Transformation tags are misplaced or formatted incorrectly.")
            return []
        
        head_content = transformation[head_pos + len(head_tag):tail_pos]
        tail_content = transformation[tail_pos + len(tail_tag):]
       
        transformed_password = head_content + ori_pw + tail_content
        output.append(transformed_password)

        return output
    except Exception as e:
        print(f"An error occurred: {e}")
        return []