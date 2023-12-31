# worker_evaluator.py
from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot
import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import time
import math


class WorkerEvaluator(QObject):
    first_delay_reached = pyqtSignal()
    evaluation_result = pyqtSignal(bool, dict, dict, dict, list, float)

    @pyqtSlot()
    def first_delay(self):
        # slow down to adapt to UI
        time.sleep(0.2)
        self.remove_png_files()
        self.first_delay_reached.emit()

    @pyqtSlot()
    def remove_png_files(self):
        for step_number in range(1, 5):
            for gesture_index in range(1, 5):
                fig_name = f'records/count_plot_step_{step_number}_gesture_{gesture_index}.png'
                # removing png file
                if os.path.exists(fig_name):
                    os.remove(fig_name)
                else:
                    print("png file does not exist")

    @pyqtSlot()
    def remove_csv_file(self, csv_name):
        # removing png file
        if os.path.exists(csv_name):
            os.remove(csv_name)
        else:
            print("csv file does not exist")

    @pyqtSlot()
    def evaluate(self, archive_file_name, evaluation_flag):
        success_flag = False
        success_flag_dict = {'step_1': False, 'step_2': False, 'step_3': False, 'step_4': False}
        difference_dict = {'step_1': [None, None, None, None], 'step_2': [None, None, None, None], 'step_3': [None, None, None, None], 'step_4': [None, None, None, None]}
        step_score_dict = {'step_1': 0, 'step_2': 0, 'step_3': 0, 'step_4': 0}
        score_dict = {'step_1': [0, 0, 0, 0], 'step_2': [0, 0, 0, 0], 'step_3': [0, 0, 0, 0], 'step_4': [0, 0, 0, 0]}
        step_score_sorted_list = [[0, 0, 0, 0],[0, 0, 0, 0],[0, 0, 0, 0],[0, 0, 0, 0]]
        overall_score_percentage = 0
        # True to be good match, False for not as good
        if evaluation_flag:
            if archive_file_name:
                print('archive_file_name is: ', archive_file_name)
                # load data to process
                column_names = ['role', 'timestamp', 'step', 'sensor_type', 'recognized_gesture']
                df_newbie = pd.read_csv(archive_file_name, header=None, names=column_names)
                # df_newbie = pd.read_csv('ui/resources/record_newbie.csv', header=None, names=column_names)
                df_newbie = df_newbie.dropna()
                if df_newbie.shape[0] == 0:
                    print('no data collected')
                    success_flag = False
                else:
                    df_expert = pd.read_csv('ui/resources/record_expert.csv', header=None, names=column_names)
                    df_expert = df_expert.dropna()
                    # filter data frame for each step
                    df_expert_step_1 = df_expert[df_expert['step'] == 'step_1']
                    df_expert_step_2 = df_expert[df_expert['step'] == 'step_2']
                    df_expert_step_3 = df_expert[df_expert['step'] == 'step_3']
                    df_expert_step_4 = df_expert[df_expert['step'] == 'step_4']
                    df_newbie_step_1 = df_newbie[df_newbie['step'] == 'step_1']
                    df_newbie_step_2 = df_newbie[df_newbie['step'] == 'step_2']
                    df_newbie_step_3 = df_newbie[df_newbie['step'] == 'step_3']
                    df_newbie_step_4 = df_newbie[df_newbie['step'] == 'step_4']
                    # perform the same data processing on each step dataset
                    success_flag_dict['step_1'], difference_dict['step_1'], score_dict['step_1'], step_score_dict['step_1'] = self.process_data_frame(df_expert_step_1, df_newbie_step_1, 1)
                    success_flag_dict['step_2'], difference_dict['step_2'], score_dict['step_2'], step_score_dict['step_2'] = self.process_data_frame(df_expert_step_2, df_newbie_step_2, 2)
                    success_flag_dict['step_3'], difference_dict['step_3'], score_dict['step_3'], step_score_dict['step_3'] = self.process_data_frame(df_expert_step_3, df_newbie_step_3, 3)
                    success_flag_dict['step_4'], difference_dict['step_4'], score_dict['step_4'], step_score_dict['step_4'] = self.process_data_frame(df_expert_step_4, df_newbie_step_4, 4)
                    # aggregate success_flag from each step
                    success_flag = success_flag_dict['step_1'] or success_flag_dict['step_2'] or success_flag_dict['step_3'] or success_flag_dict['step_4']
                    # use step_score_dict to find out the ranking
                    step_score_sorted_list = sorted(step_score_dict.items(), key=lambda x: x[1], reverse=True)
                    step_score_percentage = [0, 0, 0, 0]
                    for index in range(4):
                        step_score_percentage[index] = sum(score_dict[f'step_{index+1}']) / 4
                    overall_score_percentage = sum(step_score_percentage) / 4
                    print('overall_score_percentage: ', overall_score_percentage)
            else:
                print('archive_file_name is none')
                success_flag = False
        self.evaluation_result.emit(success_flag, difference_dict, score_dict, step_score_dict, step_score_sorted_list, overall_score_percentage)

    @pyqtSlot()
    # process data frame for each step
    def process_data_frame(self, data_frame_expert_step, data_frame_newbie_step, step_number):
        success_flag = False
        score_array = [0, 0, 0, 0]
        step_score = 0
        df_position = None
        df_expert_position_amount = [0, 0, 0, 0]
        df_newbie_position_amount = [0, 0, 0, 0]
        amount_difference = [None, None, None, None]
        try:
            # filter position and motion
            df_expert_position = data_frame_expert_step[data_frame_expert_step['sensor_type'] == 'position']
            df_newbie_position = data_frame_newbie_step[data_frame_newbie_step['sensor_type'] == 'position']
            df_position = df_expert_position.append(df_newbie_position)
        except ValueError:
            print(ValueError)
            print('reaching point - error encountered filtering position and motion')
            success_flag = False
        # check df_position
        for gesture_index in range(1, 5):
            # filter gesture x
            df_newbie_gesture_x = df_newbie_position[df_newbie_position['recognized_gesture'] == gesture_index]
            df_expert_gesture_x = df_expert_position[df_expert_position['recognized_gesture'] == gesture_index]
            df_position_gesture_x = df_position[df_position['recognized_gesture'] == gesture_index]
            try:
                # define data
                df_newbie_position_amount[gesture_index-1] = df_newbie_gesture_x.shape[0]
                df_expert_position_amount[gesture_index-1] = df_expert_gesture_x.shape[0]
            except ValueError:
                print(ValueError)
                print(f'reaching point - error encountered finding position amount: {gesture_index}')
                success_flag = False
            # define Seaborn color palette to use
            sns.set(style='whitegrid', palette='muted', font_scale=1)
            # creating image - gesture x - change plot size
            # plt.figure(figsize=(12, 4.8)).gca().yaxis.get_major_locator().set_params(integer=True)
            plt.figure(figsize=(12, 4.8))
            # count plot
            # plt.title('How many times did you perform each gesture?')
            # plt.title('How many times does an expert perform each gesture?')
            sns_count_plot = sns.countplot(y='role', data=df_position_gesture_x, order=['expert', 'newbie'])
            strFile = f'records/count_plot_step_{step_number}_gesture_{gesture_index}.png'
            if os.path.isfile(strFile):
                os.remove(strFile)
            sns_count_plot.figure.savefig(strFile)

        if df_newbie_position_amount == [0, 0, 0, 0]:
            # -1 represents no gesture performed
            amount_difference = [-1, -1, -1, -1]
            success_flag = False
        else:
            # calculation of differences in 4 gestures in one step
            for index in range(4):
                if df_newbie_position_amount[index] is None:
                    df_newbie_position_amount[index] = 0
                if df_expert_position_amount[index] is None:
                    df_expert_position_amount[index] = 0
                amount_difference[index] = abs(df_newbie_position_amount[index] - df_expert_position_amount[index])
                # calculation of score_array for each gesture
                score_array[index] = self.get_score(df_newbie_position_amount[index], df_expert_position_amount[index])
            # calculation of score in each step
            step_score = sum(score_array) / len(score_array)
            success_flag = True
            print('score_array, step_score: ', score_array, step_score)
        return success_flag, amount_difference, score_array, step_score
    
    def get_score(self, newbie_count, expert_count):
        if expert_count == 0:
            score = math.exp(-newbie_count)
        else:
            score = (newbie_count/expert_count) if (newbie_count<=expert_count) else (math.exp((2/expert_count)*(expert_count-newbie_count)))
        return score