import numpy as np
import pandas as pd
from tensorflow.python.keras import backend as K

def create_time_series_data(raw_data):
    number_of_race = raw_data.race_id.nunique()
    time_series_data = np.full((number_of_race, 24, raw_data.shape[1]-2), 0.0)#-float('inf')
    label = np.full((number_of_race, 24), 25)
    race_number = 0
    horse_number = 0
    for i in range(len(raw_data)):
        if i == 0:
            label[race_number][horse_number] = float(raw_data.iloc[i].order)
            time_series_data[race_number][horse_number] = raw_data.iloc[i].drop(['race_id','order'])
            horse_number += 1
            continue
        # add new race
        if raw_data.iloc[i].race_id != raw_data.iloc[i-1].race_id:
            race_number += 1
            horse_number = 0
            label[race_number][horse_number] = float(raw_data.iloc[i].order)
            time_series_data[race_number][horse_number] = raw_data.iloc[i].drop(['race_id','order'])
            horse_number += 1
        # add new horse to the same race
        else:
#             print(data.iloc[i].race_id ,race_number, horse_number)
            label[race_number][horse_number] = float(raw_data.iloc[i].order)
            time_series_data[race_number][horse_number] = raw_data.iloc[i].drop(['race_id','order'])
            horse_number += 1
    return time_series_data, label

def create_time_series_data_weekly(raw_data):
    number_of_race = raw_data.race_id.nunique()
    time_series_data = np.full((number_of_race, 24, raw_data.shape[1]-2), 0.0)#-float('inf')
    race_number = 0
    horse_number = 0
    for i in range(len(raw_data)):
        if i == 0:
            time_series_data[race_number][horse_number] = raw_data.iloc[i].drop(['race_id','order'])
            horse_number += 1
            continue
        if raw_data.iloc[i].race_id != raw_data.iloc[i-1].race_id:
            race_number += 1
            horse_number = 0
            time_series_data[race_number][horse_number] = raw_data.iloc[i].drop(['race_id','order'])
            horse_number += 1
        else:
            time_series_data[race_number][horse_number] = raw_data.iloc[i].drop(['race_id','order'])
            horse_number += 1
    return time_series_data

def smooth_label(label, factor=0.03):
    # smooth label
    label *= (1 - factor)
#     label[:,:,1:4] += (factor / 3)

    for i in range(label.shape[0]):
        for j in range(label.shape[1]):
            t = np.where(label[i][j] == 1 - factor)
            if t[0][0] != 25:
                label[i,j,max(0,t[0][0]-1):min(26,t[0][0]+2)] += (factor / 3)
    return label

def categorical_focal_loss(alpha, gamma):
    """
    Softmax version of focal loss.
    When there is a skew between different categories/labels in your data set, you can try to apply this function as a
    loss.
           m
      FL = ∑  -alpha * (1 - p_o,c)^gamma * y_o,c * log(p_o,c)
          c=1
      where m = number of classes, c = class and o = observation
    Parameters:
      alpha -- the same as weighing factor in balanced cross entropy. Alpha is used to specify the weight of different
      categories/labels, the size of the array needs to be consistent with the number of classes.
      gamma -- focusing parameter for modulating factor (1-p)
    Default value:
      gamma -- 2.0 as mentioned in the paper
      alpha -- 0.25 as mentioned in the paper
    References:
        Official paper: https://arxiv.org/pdf/1708.02002.pdf
        https://www.tensorflow.org/api_docs/python/tf/keras/backend/categorical_crossentropy
    Usage:
     model.compile(loss=[categorical_focal_loss(alpha=[[.25, .25, .25]], gamma=2)], metrics=["accuracy"], optimizer=adam)
    """

    alpha = np.array(alpha, dtype=np.float32)

    def categorical_focal_loss_fixed(y_true, y_pred):
        """
        :param y_true: A tensor of the same shape as `y_pred`
        :param y_pred: A tensor resulting from a softmax
        :return: Output tensor.
        """

        # Clip the prediction value to prevent NaN's and Inf's
        epsilon = K.epsilon()
        y_pred = K.clip(y_pred, epsilon, 1. - epsilon)

        # Calculate Cross Entropy
        cross_entropy = -y_true * K.log(y_pred)

        # Calculate Focal Loss
        loss = alpha * K.pow(1 - y_pred, gamma) * cross_entropy

        # Compute mean loss in mini_batch
        return K.mean(K.sum(loss, axis=-1))

    return categorical_focal_loss_fixed

def order_algorithm(preds):
    num_race = preds.shape[0]
    y_preds = np.full((num_race, 24), 25)
    for i in range(num_race): # iterate all race
        one_race = preds[i,:,:] # shape = (24, 26) ,so (num of horse, num of target 0-25)
        init_preds = np.argmax(one_race, axis = -1) # (24,1)
#         print(one_race)
#         print(init_preds)
        num_exist = len(init_preds)+1
        for j in reversed(range(len(init_preds))):
            if (init_preds[j] != 25):
                num_exist = j+1
                break
        exist_horse = one_race[:num_exist,:].copy()
#         print(exist_horse.shape)
#         exist_horse = np.delete(one_race, np.where(init_preds == 25)[0], 0) # shape = (num of exist horse, 26)
        for j in range(1,exist_horse.shape[0]+1): # iterate 1-num of exist horse
            one_order = np.argmax(exist_horse[:,j]) # this is a target order
            for k in range(one_race.shape[0]): # search the horse k = (0, 23)
                if np.array_equal(one_race[k], exist_horse[one_order]):
                    y_preds[i][k] = j
                    exist_horse = np.delete(exist_horse, one_order, 0)
                    exist_horse[:,j+1] += exist_horse[:,j]
                    one_race[:,j+1] += one_race[:,j]
                    break
    return y_preds