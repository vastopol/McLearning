#!/usr/bin/python3

# Feature Selection Algorithm
# give data file as commandline argument
# data file is matrix of floating point
#--------------------------------------

# Modules
import sys
import random
import math
import numpy as np
import copy
import time
#--------------------------------------

def main(argv,choice):
    arr = np.loadtxt(argv)
    classes = arr[:,0]
    classes = classes.reshape((len(classes),1)) # make into 1 column of N rows
    features = arr[:,1:]
    print("This data set has " + str(len(features[0])) + " features, and " + str(len(features)) + " instances")
    print("Normalizing")
    normy = normalizer(features)
    print("Running nearest neighbor with all " + str(len(features[0])) + " features, using 'leave one out' evaluation")
    accuracy = leave_one_out(normy,classes)
    print("Got an accuracy of " + str(accuracy) + "%")
    print("Beginning search")
    if choice == 1:
        st = time.clock()
        forward_selection(normy,classes)
        fn = time.clock()
        print("runtime: ",fn-st,"sec")
    elif choice == 2:
        st = time.clock()
        backward_elimination(normy,classes) # normalized data seems not to work right
        fn = time.clock()
        print("runtime: ",fn-st,"sec")
    else:
        st = time.clock()
        special_search(normy,classes)
        fn = time.clock()
        print("runtime: ",fn-st,"sec")
#--------------------------------------

def forward_selection(data,classes):
    numrow = np.shape(data)[0]
    numcol = np.shape(data)[1]
    curr_features = []
    best_accuracy = 0.0
    best_features = []
    for i in range(numcol):
        print("On the " + str(i+1) + " level of search tree")
        feature_to_add = -1
        most_accuracy = 0.0
        for j in range(numcol):
            if j not in curr_features:
                print("Considering adding the " + str(j+1) + " feature")
                new_data = np.zeros((numrow,1)) # dummy column of zeros
                for k in curr_features:
                    new_data = np.c_[new_data,data[:,k]] # add features in current set
                new_data = np.c_[new_data,data[:,j]]     # add new feature to consider
                new_data = np.delete(new_data,0,axis=1)  # remove dummy column by delete first item of each row
                curr_accuracy = leave_one_out(new_data,classes)
                print("accuracy of: ", curr_accuracy, "%")
                if curr_accuracy > most_accuracy:
                    most_accuracy = curr_accuracy
                    feature_to_add = j
        curr_features.append(feature_to_add)
        if most_accuracy > best_accuracy: # track the overall best
            best_accuracy = most_accuracy
            best_features = copy.deepcopy(curr_features)
        print("On level " + str(i+1) + " added feature " + str(feature_to_add+1) + " to the current set")
        print("current set: ", [x+1 for x in curr_features], "current accuracy: ", most_accuracy, "%")
    print("best set: ", [x+1 for x in best_features], "best accuracy: ", best_accuracy, "%")
#--------------------------------------

def backward_elimination(data,classes):
    numrow = np.shape(data)[0]
    numcol = np.shape(data)[1]
    curr_features = [x for x in range(numcol)]   # start with all
    best_accuracy = leave_one_out(data,classes)  # start with initial accuracy
    best_features = [x for x in range(numcol)]   # start with all
    for i in range(numcol):
        print("On the " + str(i+1) + " level of search tree")
        feature_to_remove = -1
        most_accuracy = 0.0
        for j in range(numcol):
            if j in curr_features:
                print("Considering removing the " + str(j+1) + " feature")
                new_data = np.zeros((numrow,1)) # dummy column of zeros
                for k in curr_features:
                    if k == j:
                        continue # skip this feature
                    new_data = np.c_[new_data,data[:,k]] # add features in current set
                new_data = np.delete(new_data,0,axis=1)  # remove dummy column by delete first item of each row
                curr_accuracy = leave_one_out(new_data,classes)
                print("accuracy of: ", curr_accuracy, "%")
                if curr_accuracy >= most_accuracy:
                    most_accuracy = curr_accuracy
                    feature_to_remove = j
        curr_features = [x for x in curr_features if x != feature_to_remove] # remove the feature from current set
        if most_accuracy >= best_accuracy: # track the overall best
            best_accuracy = most_accuracy
            best_features = copy.deepcopy(curr_features)
        print("On level " + str(i+1) + " removed feature " + str(feature_to_remove+1) + " from the current set")
        print("current set: ", [x+1 for x in curr_features], "current accuracy: ", most_accuracy, "%")
    print("best set: ", [x+1 for x in best_features], "best accuracy: ", best_accuracy, "%")
#--------------------------------------

def special_search(data,classes):
    numrow = np.shape(data)[0]
    numcol = np.shape(data)[1]
    curr_features = []
    best_accuracy = 0.0
    best_features = []
    num_wrong = math.inf # keep track of amt was wrong
    for i in range(numcol):
        print("On the " + str(i+1) + " level of search tree")
        feature_to_add = -1
        most_accuracy = -1
        for j in range(numcol):
            if j not in curr_features:
                print("Considering adding the " + str(j+1) + " feature")
                new_data = np.zeros((numrow,1)) # dummy column of zeros
                for k in curr_features:
                    new_data = np.c_[new_data,data[:,k]] # add features in current set
                new_data = np.c_[new_data,data[:,j]]     # add new feature to consider
                new_data = np.delete(new_data,0,axis=1)  # remove dummy column by delete first item of each row
                crap = leave_one_out2(new_data,classes,num_wrong)
                curr_accuracy = crap[0]
                num_wrong = crap[1]
                print("accuracy of: ", curr_accuracy, "%")
                if curr_accuracy > most_accuracy:
                    most_accuracy = curr_accuracy
                    feature_to_add = j
        if most_accuracy != -1:
            curr_features.append(feature_to_add)
            if most_accuracy > best_accuracy: # track the overall best
                best_accuracy = most_accuracy
                best_features = copy.deepcopy(curr_features)
        else:
            print("no feature to add")
            continue
        print("On level " + str(i+1) + " added feature " + str(feature_to_add+1) + " to the current set")
        print("current set: ", [x+1 for x in curr_features], "current accuracy: ", most_accuracy, "%")
    print("best set: ", [x+1 for x in best_features], "best accuracy: ", best_accuracy, "%")
#--------------------------------------

# leave one out validation for the special search
def leave_one_out2(data,classes,num_wrong):
    rows = np.shape(data)[0]
    proper = 0
    nogo = 0
    for i in range(rows):
        if nogo >= num_wrong:
            return [-1,num_wrong]
        pnt_to_test = data[i,:]
        actual_class = classes[i,:]
        mod_data = np.delete(data,i,0)
        mod_classes = np.delete(classes,i,0)
        this_class = nearest_neighbor(pnt_to_test,mod_data,mod_classes)
        # print('class_guess: ',this_class,'actual_class: ',actual_class)
        if this_class == actual_class:
            proper += 1
        else:
            nogo += 1
            # print('correct_classify: ',proper)
    akk = float(proper) / float(rows)
    return [akk,nogo]
    # return random.random() #FIXME!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#--------------------------------------

# leave one out for forward and backward
def leave_one_out(data,classes):
    rows = np.shape(data)[0]
    proper = 0
    for i in range(rows):
        pnt_to_test = data[i,:]
        actual_class = classes[i,:]
        mod_data = np.delete(data,i,0)
        mod_classes = np.delete(classes,i,0)
        this_class = nearest_neighbor(pnt_to_test,mod_data,mod_classes)
        # print('class_guess: ',this_class,'actual_class: ',actual_class)
        if this_class == actual_class:
            proper += 1
            # print('correct_classify: ',proper)
    return float(proper) / float(rows)
    # return random.random() #FIXME!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#--------------------------------------

def nearest_neighbor(point,group,classes): # point is a single row, group is a collection of rows
    least_dist = math.inf
    best_neigh = -1
    for i in range(len(group)):
        curr_dist = distance(point,group[i])
        # print('least_dist: ',least_dist,'curr_dist: ',curr_dist)
        if curr_dist < least_dist:
            # print("new dist: ",curr_dist,"new neigh: ", classes[i])
            least_dist = curr_dist
            best_neigh = i
    return classes[best_neigh,:]
#--------------------------------------

# euclidian distance for n dimensions
def distance(p1,p2):
    tot = 0.0
    for i in range(len(p1)):
        tot += pow((p2[i]-p1[i]),2)
    return math.sqrt(tot)
#--------------------------------------

def normalizer(x):
    y = (x - x.mean()) / x.std()
    return y
#--------------------------------------

def printer(x):
    for z in x:
        print(z)
#--------------------------------------

# run main function after all other functions are declared
if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Error: missing data file")
        sys.exit(1)
    print("Choose which algorithm to run")
    print("1. Forward Selection")
    print("2. Backward Elimination")
    print("3. Special Algorithm")
    try:
        choice = int(input())
    except:
        print("input error, now using forward selection")
        choice = 1
    if choice < 1 or choice > 3:
        print("input error, now using forward selection")
        choice = 1
    main(sys.argv[1],choice)
