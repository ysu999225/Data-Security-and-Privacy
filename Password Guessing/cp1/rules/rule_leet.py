import itertools

#a more complete leet_list
#leet_list = [{'4', 'a', '@', '/\\', '/-\\'}, {'b', '|3', '8', '|o'}, {'<', 'K', 'g', 'S', '9', '6', 'c', '('}, {'0', '()', '{}', 'o', '[]'}, {'!', '|', '][', '#', ')-(', '1', 'i', 'l', '}-{', '|-|', '+', 't', ']-[', 'h', '(-)', '7'}, {'5', 's', '$'}, {'+', 't'}, {'/\\/\\', 'm', '/v\\', '/|\\', '/\\\\', '|\\/|', '(\\/)', "|'|'|"}, {'\\|/', '\\|\\|', '\\^/', '//', 'w', '|/|/', '\\/\\/'}, {'|\\|', '|\\\\|', 'n', '/|/', '/\\/'}, {'u', '|_|'}, {'2', '(\\)', 'z'}, {'(,)', 'q', 'kw'}, {'v', '|/', '\\|', '\\/', '/'}, {'k', '/<', '|{', '\\<', '|<'}, {'<|', 'o|', '|)', '|>', 'd'}, {'f', 'ph', '|=', 'p#'}, {'l', '|_'}, {'j', 'y', '_|'}, {'}{', 'x', '><'}, {"'/", 'y', '`/'}, {'p', '|D', 'r', '|2'}, {'r', '|Z', '|?'}, {'e', '3'}]
leet_list = [{"@","a"},{"3","e"},{"1","i"},{"0","o"},{"$","s"},{"+","t"},{"4","a"},{"5","s"},{"|","i"},{"!","i"}]
def check_leet(pw1,pw2):
    #pw1,pw2 (string,string): a pair of input password
    #output (boolean): if pw1 and pw2 can be transformed by this category of rule
    #e.g. pw1 = abcde, pw2 = @bcd3 , output = True
    
    # ***********************************************************************
    # ****************************** TODO ***********************************
    # ***********************************************************************
    if len(pw1) != len(pw2):
        return False
    for i in range(len(pw1)):
        if pw1[i] != pw2[i]:
            flag = False
            for j in range(len(leet_list)):
                leet_pair = list(leet_list[j])
                if pw1[i] == leet_pair[0]:
                    if pw2[i] == leet_pair[1]:
                        flag = True
                        break
                elif pw1[i] == leet_pair[1]:
                    if pw2[i] == leet_pair[0]:
                        flag = True
                        break
            if flag == False:
                return False
                
    return True
    #return False

def check_leet_transformation(pw1, pw2):
    #pw1,pw2 (string,string): a pair of input password
    #output (string): transformation between pw1 and pw2
    #example: pw1=abcd3 pw2 = @bcde, transformation = 3e\ta@ because pw1->pw2:3->e and a->@ and '3e'<'a@' for the order
    #for simplicity, duplicate item is allowed. example: pw1=abcda pw2 = @bcd@, transformation = a@\ta@ 
    
    # ***********************************************************************
    # ****************************** TODO ***********************************
    # ***********************************************************************
    output = ''
    leet_pairs = []

    for i in range(len(pw1)):
        if pw1[i] != pw2[i]:
            leet_pairs.append(str(pw1[i] + pw2[i]))
    
    leet_pairs = sorted(leet_pairs)

    for i in range(len(leet_pairs)):
        if i == len(leet_pairs) - 1:
            output += leet_pairs[i]
        else:
            output += leet_pairs[i] + '\t'

    return output
    #return ''


def apply_leet_transformation(ori_pw, transformation):
    #ori_pw (string): input password that needs to be transformed
    #transformation (string): transformation in string
    #output (list of string): list of passwords that after transformation
    #only need to consider forward transformation and backward transformation combinations.
    #forward transformation: each term in transformation, can be and only be applied once on the ori_pw in forward direction (3->e,a->@)
    #backward: (e->3,@->a)
    
    # ***********************************************************************
    # ****************************** TODO ***********************************
    # ***********************************************************************
    output = []
    leet_pairs = transformation.split('\t')
    dfs_leet(ori_pw, output, 0, leet_pairs)
    return output

# def apply_leet_transformation(ori_pw, transformation):
#     #ori_pw (string): input password that needs to be transformed
#     #transformation (string): transformation in string
#     #output (list of string): list of passwords that after transformation
#     #only need to consider forward transformation and backward transformation combinations.
#     #forward transformation: each term in transformation, can be and only be applied once on the ori_pw in forward direction (3->e,a->@)
#     #backward: (e->3,@->a)
    
#     output = []
#     leet_pairs = transformation.split('\t')

#     dfs_leet(ori_pw, output, 0, leet_pairs)
    
    return output

def dfs_leet(pw, output, index, leet_pairs):
    if index == len(leet_pairs):
        output.append(pw)
        return

    original_char, transformed_char = leet_pairs[index][0],leet_pairs[index][1]
    print(f"original_char:{original_char}")
    
    print(f"transformed_char:{transformed_char}")
    
    new_pw = pw.replace(original_char, transformed_char)
    dfs_leet(new_pw, output, index + 1, leet_pairs)
    new_pw = pw.replace(transformed_char, original_char)
    dfs_leet(new_pw, output, index + 1, leet_pairs)


