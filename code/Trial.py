import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import sys

class Trial:
    def __init__(self, fname, age, action, trial_id,
                 fps = 200,
                 features = ["ax","ay","az",
                             "rx","ry","rz",
                             "ax2","ay2","az2"]):
        self.fname = fname
        self.df = pd.read_csv(fname, header=None)
        self.df.columns = features
        self.fps = fps
        self.age = age
        self.action = action
        self.id = trial_id

        self.fall = False
        if action[0] == 'F':
            self.fall = True

    def print_info(self):
        print("  Trial Info")
        print("         age:", self.age)
        print("      action:", self.action)
        print("          ID:", self.id)
        print("         fps:", self.fps)
        print("       steps:", len(self.df))
        print("     time(s):", len(self.df)/self.fps)
        print("        file:", self.fname)
        #print("    features:", list(self.df.columns))
        print("\n")

    def plot(self, cols, title = None):
        for col in cols:
            plt.plot(self.df.index/self.fps, self.df[col],
                     label = col)
            plt.xlabel("time (sec)")
            plt.ylabel("signal")
            plt.legend()
            plt.title(title)
        plt.show()
        plt.clf()

    def hist(self, cols, title = None):
        for col in cols:
            plt.hist(self.df[col], bins = 40,
                     alpha = 0.5, label = col)
            plt.xlabel("signal")
            plt.ylabel("freq.")
            plt.legend()
            plt.title(title)
        plt.show()
        plt.clf()

    def get_features(self,cols):
        return self.df[cols].values, int(self.fall)
