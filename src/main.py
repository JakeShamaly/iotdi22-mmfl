import configparser
import argparse
import logging
import os
import warnings
import torch
from fl import FL

def read_config():
    config = configparser.ConfigParser()
    config.read('/Users/emraf/OneDrive/Documents/GitHub/iotdi22-mmfl/config/opp/dccae/A0_B0_AB30_label_AB_test_B')
    return config

config = read_config()
fl = FL(config)
fl.start()