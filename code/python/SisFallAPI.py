import pandas as pd
import os
import glob
import numpy as np
import matplotlib.pyplot as plt
from Trial import Trial

class DataSet:
    def __init__(self, trials = [], name = None):
        if len(trials)
        self.trials = trials
        self.name = name

    def print_all_trials(self):
        print(self.name)
        for trial in self.trials:
            trial.print_info()
            print("\n")
    # first, gather all of the relevant files
    files = {}
    dirs = !ls | grep SA

    for dir in dirs:
        print(dir)
        files[dir] = !ls {dir}

    for dir in dirs:
        for file in files[dir]:
            _fn = "%s/%s" % (dir, file)
            if _fn.split('.')[-1] == "txt":
                print(_fn)

    pd.read_csv(_fn, header = None)

def load_summary_as_df(fname):
    df = pd.read_csv(fname, sep='|', skipinitialspace=True)
    df.columns = df.columns.str.strip()
    for col in df.columns:
        if df[col].dtype.kind not in 'biufc':
            df[col] = df[col].str.strip()
    df.sort_values('ID')
    return df

def load_summaries(fpath):
    _subjt = load_summary_as_df("Subjects.txt")
    _actvt = load_summary_as_df("Activities.txt")
    return _subjt, _actvt

def load_trials(fpath, verbose=False):
    subjects, activities = load_summaries(fpath)
    trial_dict = {}
    for _s in subjects.ID:
        for _a in activity.ID:
            dpath = os.path.abspath(_s)
            fpath = os.path.join(dpath,_a)
            files = glob.glob("%s*.txt" % fpath)
            trial_dict[_s,_a] = []
            for _f in files:
                _t = os.path.split(_f)[-1].split('_')[-1].split('.')[0]
                trial_dict[_s,_a].append(_t)
            trial_dict[_s,_a].sort()
            if verbose:
                print(_s, _a, "has", len(trial_dict[_s,_a]), "trials")

    return subjects, activities, trials

def summarize_trials(trial_dict, save = False):
    total = 0
    notrial = 0
    n_trials = [[], []]
    for key in trial_dict.keys():
        _nt = len(trial_dict[key])
        total += _nt
        n_trials[0].append(_nt)
        if n_trials == 0:
            notrial += 1
    print(len(trial_dict.keys()), "entries")
    print(total, "trials")
    print(notrial, "entries without trials")

    n_trials = np.array(n_trials)
    plt.hist(n_trials[0], bins=[-0.5,0.5,1.5,2.5,3.5,4.5,5.5],
             rwidth = 0.8, align='mid')
    plt.title("Trials per subject and activity")
    plt.xlabel("number of trials")
    plt.ylabel("count")
    if save:
        plt.savefig("trial_summary.png")
    else:
        plt.show()

def fpath(sub,act,trial):
    _fn = "%s_%s_%s.txt" % (act,sub,trial)
    _fp = os.path.abspath(sub)
    _fp = os.path.join(_fp,_fn)
    return _fp

def age_subject(subject_id):
    return int(subjects[subjects.ID == subject_id].Age)

def str_activity(activity_id):
    return activity.loc[activity.ID == activity_id]['Activity'].values[0]

def plot_sensors(_subject,_activity,_tnum):
    # _subject = 'SA01'
    # _activity = 'D19'
    # _tnum = 'R01'
    _trial = Trial( fpath(_subject,_activity,_tnum),
                    age_of_subject(_subject),
                    activity_str(_activity), _tnum )
    _trial.print_info()

    trace = { 'ADXL345':  ['ax','ay','az'],
               'ITG3200':  ['rx','ry','rz'],
               'MMA8451Q': ['ax2','ay2','az2'] }

    for sensor in list(trace.keys())[:-1]:
        _trial.plot(trace[sensor], sensor)

    for sensor in list(trace.keys())[:-1]:
        _trial.hist(trace[sensor], sensor)

    _trial.get_features(trace['ITG3200'])
