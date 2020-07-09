import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from sklearn.linear_model import LinearRegression 
import scipy.stats
import sys, os
import pickle
from datetime import date, timedelta
sys.path.append(os.path.abspath("code/python"))
from RiskMeter import RiskMeter


def welcome():
    st.title("WobbleWatch")
    st.text("Your daily fall risk assessment.")

def disclaim():
    st.markdown("Subjects are examples from the PhysioNet Long-Term Movement Monitoring Database. This data-set contains 3-day long data, and the dates shown above do not reflect the actual date of data collected but are just projected back from today to make this example more realistic.")

def load_data():
    fname = os.path.abspath("data/physionet_results_by_name.pik")
    with open(fname, 'rb') as handle:
        d = pickle.load(handle)
    return d


def risk_category(risk):
    if risk < 1:
        return "Very Low!"
    elif risk < 3:
        return "Low."
    elif risk < 5:
        return "Medium."
    elif risk < 10:
        return "High."
    else:
        return "Very High!"

def risk_change(slope, proj_stumbles):
    text = ""
    if slope > 0.5:
        text = "Your risk is growing! You should [intervention]"
    elif slope < -0.5:
        text = "Your risk is dropping! Keep up the good work!"
    else:
        text = "Your risk is not changing much."
        if proj_stumbles < 3:
            text += " That's great!"
        elif proj_stumbles < 5:
            text += " That's okay, but you could use some improvement."
        else:
            text += " Be careful today."
    return text

def project_risk(falls, subject):
    slope, intercept, r_value, p_value, std_err = \
                scipy.stats.linregress(x=falls[:,0],y=falls[:,1])

    proj_stumbles = intercept
    if proj_stumbles < 0:
        proj_stumbles = 0

    xt = [-3, -2, -1, 0]
    today = date.today()
    xd = []
    for i in range(len(xt)):
        _d = today + timedelta(days=xt[i])
        xd.append(_d)

    fig, ax = plt.subplots()
    ax.set_title("Stumble Summary", size=16)
    ax.bar(falls[:,0], falls[:,1])
    ax.set_ylabel("Total Stumbles", size=16)
    ax.set_xlabel("Date", size=16)
    ax.set_xticks(xt)
    new_x = np.arange(xt[0], xt[-1],(xt[-1]-xt[0])/100.)
    ymax = max(proj_stumbles, max(falls[:,1]))
    ax.set_ylim(bottom=0, top=ymax + 1)
    ax.bar(0, intercept)
    ax.plot(new_x, intercept + slope *  new_x, color='c', linestyle='-', lw = 5)
    ax.set_xticklabels(xd)

    plt.savefig("web/assets/projection.png")

    text_lines = []
    text_lines.append("Your risk level is %s" % risk_category(proj_stumbles))
    text_lines.append("Your most recent trend suggests %i stumbles today." % proj_stumbles)
    text_lines.append(risk_change(slope, proj_stumbles))
    return proj_stumbles, text_lines


def relative_risk(subject, results, thresh):
    N = { 'F': [], 'C': []}
    for _r in results:
        if _r[0] == 'C':
            N['C'].append(len(results[_r][:,2][results[_r][:,2] > thresh]))
        elif _r[0] == 'F':
            N['F'].append(len(results[_r][:,2][results[_r][:,2] > thresh]))
    ARF = np.mean(N['F'])
    ARC = np.mean(N['C']) 
    RR = ARC/ARF
    return ARF, ARC, RR

def n_stumbles_day(subject, results, thresh, day):
    mask1 = results[subject][:,2] > thresh
    mask2 = results[subject][:,0] > 24*(day-1)
    mask3 = results[subject][:,0] < 24*day
    mask = mask1 & mask2 & mask3
    return len(results[subject][mask])

def individual_stumbles(subject, results, thresh, ARF):
    days = [1,2,3]
    stumbles = []
    for day in days:
        _ns = n_stumbles_day(subject, results, thresh, day)
        stumbles.append([-day, _ns])
    return np.array(stumbles)

welcome()
results = load_data()
names = list(results.keys())
subject = st.sidebar.selectbox("Choose a subject (F's are known fallers)", names[::-1])
thresh = st.sidebar.slider("Threshold", min_value=0.5, max_value=0.8, value=0.8)

ARF, ARC, RR = relative_risk(subject, results, thresh)
st.sidebar.text("Relative Risk = %5.3f" % RR)

stumbles = individual_stumbles(subject, results, thresh, ARF)
proj_stumbles, text_lines = project_risk(stumbles,subject)
tune = 5 # adhoc tuning parameter for sensitivity of RiskMeter
rm = RiskMeter(proj_stumbles/ ARF*tune)

st.image("web/assets/meter.png", use_column_width = True)
for line in text_lines: st.markdown("<center>" + line + "</center>", unsafe_allow_html = True)
st.image("web/assets/projection.png", use_column_width = True)
disclaim()
