import os
import yaml


class PassConfig:
    def __init__(self):
        self.min_length = None
        self.char_types = None
        self.min_char_types = None
        self.history = None
        self.dict_search = None
        self.login_tries = None
        self.keywords_dict = None

        self.load_params()

    def load_params(self):
        with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'pass_config.yaml'), "r") as stream:
            try:
                pass_config = yaml.safe_load(stream)
            except yaml.YAMLError as exc:
                print(exc)

            self.min_length = pass_config['min_length']
            self.char_types = pass_config['char_types']
            self.min_char_types = pass_config['min_char_types']
            self.history = pass_config['history']
            self.dict_search = pass_config['dict_search']
            self.login_tries = pass_config['login_tries']

            if self.dict_search:
                self.load_keywords_dict()

    def load_keywords_dict(self):
        with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'keywords.txt'), "r") as file:
            lines = file.readlines()
            self.keywords_dict = [line.rstrip() for line in lines]

    def count_char_types(self, user_pass):
        upper, lower, number, special = 0, 0, 0, 0
        types_counter = 0
        for i in range(len(user_pass)):
            if user_pass[i].isupper() and self.char_types['uppers']:
                upper += 1
            elif user_pass[i].islower() and self.char_types['lowers']:
                lower += 1
            elif user_pass[i].isdigit() and self.char_types['numbers']:
                number += 1
            elif self.char_types['special_chars']:
                special += 1

        if upper:
            types_counter += 1
        if lower:
            types_counter += 1
        if number:
            types_counter += 1
        if special:
            types_counter += 1

        return types_counter

    def is_in_keywords_dict(self, user_pass):
        if user_pass in self.keywords_dict:
            return True
        return False
