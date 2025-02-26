import configparser
import sys
import warnings

import pandas as pd

from pymongo import MongoClient

import os

# sys.path.insert(0, ".")
from action_logging import Logger

warnings.filterwarnings("ignore")


class Preprocess:
    def __init__(self, config_path, logger=None):
        """
        Initialize Preprocess class
        :param config:
        """
        if logger is None:
            self.logger = Logger(
                log_flag=True, log_file="preprocess", log_path="../logs/"
            )
        else:
            self.logger = logger

        config = configparser.RawConfigParser()
        config.read(config_path)

        self.user_names = None
        self.color_map = {}
        self.data = None
        self.data_backup = None
        self.pd_data = None

        mongo_client = MongoClient(config["mongodb"]["connection_uri"])
        mongo_db = mongo_client[config["mongodb"]["db"]]
        self.mongo_collection = mongo_db[config["mongodb"]["collection"]]

    def load_data(self):
        """
        Reads in the array of dicts in UTF-8, parses, and formats
        Also, takes backup just to have control on things.
        :return:
        """
        self.logger.write_logger("In preprocess.py (load_data): Loading data.")

        self.data = self.mongo_collection.find({})

        # Save temporary value
        # self.data_backup = self.data.copy()

        self.logger.write_logger("In preprocess.py (load_data): Data load complete.")

    def print_sample(self, n_lines=10):
        """
        Prints sample number of lines
        :param n_lines:
        :return:
        """
        self.logger.write_logger(
            "In preprocess.py (print_sample): Printing of data (first "
            + str(n_lines)
            + " lines) starts"
        )

        print(self.data[:n_lines])

        self.logger.write_logger(
            "In preprocess.py (print_sample): Printing of data (first "
            + str(n_lines)
            + " lines) ends"
        )

    '''def add_missing_info(self, current_line, previous_line):
        """
        Add timestamp, username from previous line
        :param current_line:
        :param previous_line:
        :return:
        """
        previous_line_ts = previous_line.split("-")[0].strip()
        previous_line_name = previous_line.split("-")[1].strip().split(":")[0].strip()

        current_line = (
            previous_line_ts + " - " + previous_line_name + ": " + current_line
        )

        return current_line'''

    '''def parse_data(self, log=False):
        """
        Cleans data by adding missing information
        :return:
        """
        self.logger.write_logger(
            "In preprocess.py (clean_data): Cleaning of data starts"
        )
        # self.data = self.data_backup.copy()

        for idx, line in enumerate(self.data):
            split_part = line.split("-")

            if len(split_part) <= 1:
                if log:
                    self.logger.write_logger(f"== Before Condition 1: {self.data[idx]}")

                self.data[idx] = self.add_missing_info(
                    self.data[idx], self.data[idx - 1]
                )

                if log:
                    self.logger.write_logger(
                        f"== After Condition 1: {self.data["""idx-1]}"
                    )
                    self.logger.write_logger(f"== After Condition 1: {self.data[idx]}")

            else:
                split_part = split_part[0].strip()
                split_part = split_part.split(",")

                if len(split_part) < 2:
                    if log:
                        self.logger.write_logger(
                            f"== Before Condition 2: Current line: {self.data[idx]}, Previous line: {self.data[idx - 1]}"
                        )

                    self.data[idx] = self.add_missing_info(
                        self.data[idx], self.data[idx - 1]
                    )

                    if log:
                        self.logger.write_logger(
                            f"== After Condition 2: {self.data[idx-1]}"
                        )
                        self.logger.write_logger(
                            f"== After Condition 2: {self.data[idx]}"
                        )

                else:
                    split_part = split_part[1].strip()
                    split_part = split_part.split(" ")

                    if len(split_part) < 2:
                        if log:
                            self.logger.write_logger(
                                f"== Before Condition 3: {self.data[idx]}"
                            )

                        self.data[idx] = self.add_missing_info(
                            self.data[idx], self.data[idx - 1]
                        )

                        if log:
                            self.logger.write_logger(
                                f"== After Condition 3: {self.data[idx-1]}"
                            )
                            self.logger.write_logger(
                                f"== After Condition 3: {self.data[idx]}"
                            )

                    else:
                        split_part = split_part[1].strip()

                        if split_part.lower() != "am" and split_part.lower() != "pm":
                            if log:
                                self.logger.write_logger(
                                    f"== Before Condition 4: {self.data[idx]}"
                                )
                            self.data[idx] = self.add_missing_info(
                                self.data[idx], self.data[idx - 1]
                            )

                            if log:
                                self.logger.write_logger(
                                    f"== After Condition 4: {self.data[idx-1]}"
                                )
                                self.logger.write_logger(
                                    f"== After Condition 4: {self.data[idx]}"
                                )

                        else:
                            "No correction needed"

        self.logger.write_logger("In preprocess.py (clean_data): Cleaning of data ends")'''

    '''def drop_message(self, contains):
        """
        Drops the message if it contains the text given in parameter
        :param contains:
        :return:
        """
        self.logger.write_logger(
            "In preprocess.py (drop_message): Dropping message containing: "
            + contains
            + " starts"
        )

        self.data = [line for line in self.data if contains not in line]

        self.logger.write_logger(
            "In preprocess.py (drop_message): Dropping message containing: "
            + contains
            + " ends"
        )

        return self'''

    def prepare_df(self):
        """
        Prepares a Pandas Dataframe out of the data
        :return:
        """
        timestamps = []
        weekdays = []
        # ts_first_split = []  # stores first split of xx/xx/xx, xx:xx xx
        user_names = []
        user_ids = []
        user_avatars = []
        messages = []
        channels = []

        self.logger.write_logger(
            "In preprocess.py (prepare_df): Preparation of data frame starts"
        )

        for line in self.data:
            """timestamps.append(line.split("-")[0].strip())
            ts_first_split.append(int(line.split("-")[0].strip().split("/")[0].strip()))
            sub_line = line.split("-")[1].strip().split(":")
            user_names.append(sub_line[0].strip())
            messages.append("-".join([v.strip() for v in sub_line[1:]]))"""

            timestamps.append(pd.Timestamp(line["timestamp"]))
            weekdays.append(pd.Timestamp(line["timestamp"]).day_name())
            user_names.append(line["author"]["name"])
            user_ids.append(line["author"]["id"])
            user_avatars.append(line["author"]["avatarUrl"])
            messages.append(line["content"])
            channels.append(line["channel"]["name"])

        self.pd_data = pd.DataFrame(
            {
                "Timestamp": timestamps,
                "Weekday": weekdays,
                "User": user_names,
                "User ID": user_ids,
                "Message": messages,
                "Channel": channels,
                "User Avatar": user_avatars,
            }
        )[
            [
                "Timestamp",
                "Weekday",
                "User",
                "User ID",
                "Message",
                "Channel",
                "User Avatar",
            ]
        ]

        """if sum([1 if v > 12 else 0 for v in ts_first_split]) > 0:
            self.pd_data["timestamp"] = pd.to_datetime(
                self.pd_data["timestamp"].str.lower(), format="%d/%m/%y, %I:%M %p"
            )
        else:
            self.pd_data["timestamp"] = pd.to_datetime(
                self.pd_data["timestamp"].str.lower(), format="%m/%d/%y, %I:%M %p"
            )"""

        self.pd_data["Date"] = self.pd_data["Timestamp"].dt.strftime("%d-%b-%Y")
        # self.pd_data["weekday"] = self.pd_data["timestamp"].dt.strftime("%a")

        self.users = list(set(user_names))

        self.logger.write_logger(
            "In preprocess.py (prepare_df): Preparation of data frame ends"
        )

    def write_data(self, path="data/clean_data.csv"):
        """

        :param path:
        :return:
        """
        self.pd_data.to_csv(path, index=False)
