#!/usr/bin/python3
# FEEL FREE TO EDIT THIS FILE FOR DEBUGGING PURPOSES,
# BUT GRADING ENVIRONMENT WILL NOT USE YOUR VERSION

import sys
from logging import debug,warning
from cp1 import cp1_1_parse_homes, cp1_2_parse_friends, cp1_3_answers
from cp2 import cp2_1_simple_inference, cp2_2_improved_inference, cp2_calc_accuracy
import logging

if __name__ == "__main__":
    if len(sys.argv) != 4 or (sys.argv[1] != "cp1" and sys.argv[1] != "cp2"):
        print("Usage: {0} <cp1|cp2> <homes.txt> <friends.txt>".format(sys.argv[0]))
        exit(1)
    User_dict = cp1_1_parse_homes(sys.argv[2])
    debug("{0} users processed.".format(len(User_dict)))
    cp1_2_parse_friends(sys.argv[3], User_dict)
    if sys.argv[1] == 'cp1':
        u_cnt, u_noloc_cnt, u_noloc_nofnds_cnt, p_b, p_u1, p_u2 = cp1_3_answers(User_dict)
        print("User_Count:{0}".format(int(u_cnt)))
        print("User_NoLocation_Count:{0}".format(int(u_noloc_cnt)))
        print("User_NoLocationNorFriends_Count:{0}".format(int(u_noloc_nofnds_cnt)))
        print("Accuracy_Baseline:{0:.2f}".format(float(p_b)))
        print("Accuracy_u1:{0:.2f}".format(float(p_u1)))
        print("Accuracy_u2:{0:.2f}".format(float(p_u2)))
    elif sys.argv[1] == 'cp2':
        User_dict_simpl_inf = cp2_1_simple_inference(User_dict)
        User_dict_imprv_inf = cp2_2_improved_inference(User_dict)
        if len(User_dict_simpl_inf) == len(User_dict):
            actual_acc_simpl = cp2_calc_accuracy(User_dict, User_dict_simpl_inf)
            print("Actual_Accuracy_Simple:{0:.2f}".format(actual_acc_simpl))
        else: warning("simple inferred dict length is not matching ground truth.")

        if len(User_dict_imprv_inf) == len(User_dict):
            actual_acc_imprv = cp2_calc_accuracy(User_dict, User_dict_imprv_inf)
            print("Actual_Accuracy_Improved:{0:.2f}".format(actual_acc_imprv))
        else: warning("improved inferred dict length is not matching ground truth.")
    else:
        print("Unrecognized option.")
        exit(1)
