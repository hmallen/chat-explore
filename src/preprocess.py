import pandas as pd
import math, os, sys, glob, re
import numpy as np
import warnings, logging, datetime
import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns

# sys.path.insert(0, ".")
from action_logging import Logger

warnings.filterwarnings('ignore')

class Preprocess:

    def __init__(self, input_file):
        """
        Initialize Preprocess class
        :param input_file:
        """
        self.file = input_file
        self.logger = Logger(log_flag = True, log_file = "preprocess", log_path = "../logs/")
        self.data = None
        self.data_backup = None
        self.pd_data = None

    def read_file(self):
        """
        Reads in the file in UTF-8 encoding and splits into lines
        Also, takes backup just to have control on things.
        :return:
        """
        f = open(self.file, 'r', encoding = "utf8")
        self.data = f.read()
        f.close()
        self.data = self.data.splitlines()

        # Save temporary value
        self.data_backup = self.data.copy()

    def print_sample(self, n_lines = 10):
        """
        Prints sample number of lines
        :param n_lines:
        :return:
        """
        print(self.data[:n_lines])

    def add_missing_info(self, current_line, previous_line):
        """
        Add timestamp, username from previous line
        :param current_line:
        :param previous_line:
        :return:
        """
        previous_line_ts = previous_line.split('-')[0].strip()
        previous_line_name = previous_line.split('-')[1].strip().split(':')[0].strip()
        current_line = previous_line_ts + " - " + previous_line_name + ": " + current_line
        return current_line

    def clean_data(self):
        """
        Cleans data by adding missing information
        :return:
        """
        self.data = self.data_backup.copy()
        for idx, line in enumerate(self.data):
            split_part = line.split('-')
            if len(split_part) == 0:
                self.logger.write_logger(f'== Before Condition 1: {self.data[idx]}')
                self.data[idx] = self.add_missing_info(self.data[idx], self.data[idx - 1])
                self.logger.write_logger(f'== After Condition 1: {self.data[idx-1]}')
                self.logger.write_logger(f'== After Condition 1: {self.data[idx]}')
            else:
                split_part = split_part[0].strip()
                split_part = split_part.split(",")
                if len(split_part) < 2:
                    self.logger.write_logger(f'== Before Condition 2: {self.data[idx]}')
                    self.data[idx] = self.add_missing_info(self.data[idx], self.data[idx - 1])
                    self.logger.write_logger(f'== After Condition 2: {self.data[idx-1]}')
                    self.logger.write_logger(f'== After Condition 2: {self.data[idx]}')
                else:
                    split_part = split_part[1].strip()
                    split_part = split_part.split(" ")
                    if len(split_part) < 2:
                        self.logger.write_logger(f'== Before Condition 3: {self.data[idx]}')
                        self.data[idx] = self.add_missing_info(self.data[idx], self.data[idx - 1])
                        self.logger.write_logger(f'== After Condition 3: {self.data[idx-1]}')
                        self.logger.write_logger(f'== After Condition 3: {self.data[idx]}')
                    else:
                        split_part = split_part[1].strip()
                        if split_part != 'am' and split_part != 'pm':
                            self.logger.write_logger(f'== Before Condition 4: {self.data[idx]}')
                            self.data[idx] = self.add_missing_info(self.data[idx], self.data[idx - 1])
                            self.logger.write_logger(f'== After Condition 4: {self.data[idx-1]}')
                            self.logger.write_logger(f'== After Condition 4: {self.data[idx]}')
                        else:
                            'No correction needed'

    def drop_message(self, contains = 'Messages to this chat and calls are now secured with end-to-end encryption'):
        """
        Drops the message if it contains the text given in parameter
        :param contains:
        :return:
        """
        self.data = [line for line in self.data if contains not in line]

    def prepare_df(self):
        """
        Prepares a Pandas Dataframe out of the data
        :return:
        """
        timestamps = []
        users = []
        messages = []
        for line in self.data:
            timestamps.append(line.split("-")[0].strip())
            sub_line = line.split("-")[1].strip().split(":")
            users.append(sub_line[0].strip())
            messages.append("-".join([v.strip() for v in sub_line[1:]]))
        self.pd_data = pd.DataFrame({'Timestamp': timestamps, 'User': users, 'Message': messages})[
            ['Timestamp', 'User', 'Message']]
        self.pd_data['Timestamp'] = pd.to_datetime(self.pd_data['Timestamp'])
        self.pd_data['Date'] = self.pd_data['Timestamp'].dt.strftime('%d-%m-%Y')
        self.pd_data['Weekday'] = self.pd_data['Timestamp'].dt.strftime('%a')

    def check_n_users(self):
        """
        Check the number of users
        if > 2 or < 2, raise Exception
        :return:
        """
        if len(np.unique(self.pd_data['User'])) != 2:
            self.logger.write_logger("You need to have 2 users in the chat. Not more, Not less !", error = True)
            sys.exit()
        else:
            self.logger.write_logger("You Chat data have 2 users.", error = False)

preprocess = Preprocess(input_file = '../data/input.txt')
preprocess.read_file()
preprocess.print_sample(10)
preprocess.clean_data()
preprocess.drop_message()
preprocess.prepare_df()
preprocess.check_n_users()
print(preprocess.pd_data.head())