import numpy
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from Estimator import MondayMLModel
import pandas as pd
import pickle
import tensorflow

def main():
    x_train_time, y_train_time, x_test_time, y_test_time, x_train_difficulty, y_train_difficulty, x_test_difficulty, y_test_difficulty = load_test("/Users/ylias.2001/Desktop/HackathonTLV/Dataset.csv")
    estimator1 = MondayMLModel()
    estimator2 = MondayMLModel()
    estimator1.fit(x_train_time, y_train_time)
    estimator2.fit(x_train_difficulty, y_train_difficulty)
    pickle.dump(estimator1, open("time_model","wb"))
    pickle.dump(estimator2, open("difficulty_model","wb"))


def load_test(filename):
    df = pd.read_csv(filename)
    df = df.astype('float64')
    processing_df = pd.DataFrame()
    processing_df['assignment_num'] = numpy.max(numpy.array([k * df[f'assignment{k}'] for k in [1, 2, 3, 4, 5]]), axis=0)
    processing_df['course_num'] = numpy.max(numpy.array([k * df[f'course{k}'] for k in [1, 2, 3, 4, 5]]), axis=0)
    for i in [1,2,3,4,5]:
        processing_df[f'course_{i}'] = pd.Series(df[[f'course{i}'+f for f in ['Points', 'WeeklyHours', 'TotalAssignments', 'MandatoryAssignments']]].to_numpy().tolist())
        processing_df[f'time_course_{i}'] = pd.Series(df[[f'course{i}Time{j}' for j in [1, 2, 3, 4, 5]]].to_numpy().tolist())
        processing_df[f'difficulty_course_{i}'] = pd.Series(df[[f'course{i}Difficulty{j}' for j in [1, 2, 3, 4, 5]]].to_numpy().tolist())
    processing_df['courses'] = pd.Series(processing_df[[f'course_{i}' for i in [1,2,3,4,5]]].to_numpy().tolist())
    final_df = pd.DataFrame()
    enc = LabelEncoder()
    time_labels = []
    difficulty_labels = []
    student_percentile_time = []
    student_percentile_difficulty = []
    course = []
    for i in range(df.shape[0]):
        course.append(str(processing_df['assignment_num'][i]) + str(processing_df['course_num'][i]))

        nonzero_val_time = np.count_nonzero(np.array(processing_df['time_course_1'][i])) +\
                           np.count_nonzero(np.array(processing_df['time_course_2'][i])) +\
                           np.count_nonzero(np.array(processing_df['time_course_3'][i])) +\
                           np.count_nonzero(np.array(processing_df['time_course_4'][i])) +\
                           np.count_nonzero(np.array(processing_df['time_course_5'][i]))

        student_percentile_time.append((np.sum(np.array(processing_df['time_course_1'][i])) +\
                                                 np.sum(np.array(processing_df['time_course_2'][i])) +\
                                                 np.sum(np.array(processing_df['time_course_3'][i])) +\
                                                 np.sum(np.array(processing_df['time_course_4'][i])) +\
                                                 np.sum(np.array(processing_df['time_course_5'][i]))) / (nonzero_val_time))

        nonzero_val_difficulty = np.count_nonzero(np.array(processing_df['difficulty_course_1'][i])) +\
                           np.count_nonzero(np.array(processing_df['difficulty_course_2'][i])) +\
                           np.count_nonzero(np.array(processing_df['difficulty_course_3'][i])) +\
                           np.count_nonzero(np.array(processing_df['difficulty_course_4'][i])) +\
                           np.count_nonzero(np.array(processing_df['difficulty_course_5'][i]))

        student_percentile_difficulty.append((np.sum(np.array(processing_df['difficulty_course_1'][i])) +\
                                                 np.sum(np.array(processing_df['difficulty_course_2'][i]))  +\
                                                 np.sum(np.array(processing_df['difficulty_course_3'][i]))  +\
                                                 np.sum(np.array(processing_df['difficulty_course_4'][i]))  +\
                                                 np.sum(np.array(processing_df['difficulty_course_5'][i]))) / nonzero_val_difficulty)

        time_labels.append(float(df[f'course{int(processing_df["course_num"][i])}Time{int(processing_df["assignment_num"][i])}'][i]))

        difficulty_labels.append(df[f'course{int(processing_df["course_num"][i])}Difficulty{int(processing_df["assignment_num"][i])}'][i])

    final_df['course'] = pd.Series(course)
    final_df['course'] = enc.fit_transform(final_df['course'])
    final_df['student_percentile_time'] = pd.Series(student_percentile_time)
    final_df['student_percentile_difficulty'] = pd.Series(student_percentile_difficulty)
    final_df['student_percentile_time'] = pd.Series(numpy.argsort(final_df['student_percentile_time'].to_numpy()) / df.shape[0])
    final_df['student_percentile_difficulty'] = pd.Series(numpy.argsort(final_df['student_percentile_difficulty'].to_numpy()) / df.shape[0])
    time_labels = pd.Series(time_labels)
    difficulty_labels = pd.Series(difficulty_labels)
    x_train_time, x_test_time, y_train_time, y_test_time = train_test_split(final_df, time_labels, test_size=0.10, random_state=0)
    x_train_difficulty, x_test_difficulty, y_train_difficulty, y_test_difficulty = train_test_split(final_df, difficulty_labels, test_size=0.10, random_state=0)
    return x_train_time.to_numpy(), y_train_time.to_numpy(), x_test_time.to_numpy(),\
           y_test_time.to_numpy(), x_train_difficulty.to_numpy(), y_train_difficulty.to_numpy(),\
           x_test_difficulty.to_numpy(), y_test_difficulty.to_numpy()

def predict(X):
    x = np.array(X, dtype='float64')
    course_num = int(numpy.array([k * x[69+k] for k in [1,2,3,4,5]]).sum())
    assignment_num = int(numpy.array([k * x[69+k] for k in [1,2,3,4,5]]).sum())
    enc = LabelEncoder()
    encrypted = enc.fit_transform(enc.fit_transform(numpy.array([str(course_num) + str(assignment_num)])))[0]
    time = 0
    difficulty = 0
    norm_time = 0
    norm_difficulty = 0
    for i in [1,2,3,4,5]:
        for j in [1,2,3,4,5]:
            time_val = x[5 + (14 * (i - 1)) + (2 * (j - 1))]
            if time_val != 0:
                norm_time += 1
                time += time_val
            difficulty_val = x[4 + (14 * (i - 1)) + (2 * (j - 1))]
            if difficulty_val != 0:
                norm_difficulty += 1
                difficulty += difficulty_val
    difficulty /= norm_difficulty
    time /= norm_time
    x = numpy.array([encrypted, time, difficulty])
    difficulty_estimator = pickle.load(open("difficulty_model","rb"))
    time_estimator = pickle.load(open("time_model","rb"))
    difficulty = int(round(difficulty_estimator.predict(x.reshape(1,-1))[0]))
    time = int(round(time_estimator.predict(x.reshape(1,-1))[0] / 60))
    return difficulty, time
