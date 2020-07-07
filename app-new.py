import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from sklearn.linear_model import LinearRegression 
import scipy.stats
import sys, os
from datetime import date, timedelta
sys.path.append(os.path.abspath("code/python"))
from RiskMeter import RiskMeter


def welcome():
    st.title("WobbleWatch")
    st.text("Your daily fall risk assessment.")

def load_data():
    _f = np.array([[-3,-2,-1], [4,1,1], [2,1,5], [3,5,7]])
    _f = _f.transpose()
    _c = ["Day", "Adult 1", "Adult 2", "Adult 3"]
    return pd.DataFrame(_f, columns = _c)


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

def risk_change(slope):
    text = ""
    if slope > 1:
        text = "Your risk is growing! You should [intervention]"
    elif slope < 1:
        text = "Your risk is dropping! Keep up the good work!"
    else:
        text = "Your risk is not changing much."
        if proj_risk < 3:
            text += " That's great!"
        elif proj_risk < 5:
            text += " That's okay, but you could use some improvement."
        else:
            text += " Be careful today."
    return text

def project_risk(falls, subject):
    slope, intercept, r_value, p_value, std_err = \
                scipy.stats.linregress(x=falls['Day'],y=falls[subject])

    proj_risk = intercept
    if proj_risk < 0:
        proj_risk = 0

    xt = [-3, -2, -1, 0]
    dn = falls["Day"]
    today = date.today()
    xd = []
    for i in range(len(xt)):
        _d = today + timedelta(days=xt[i])
        xd.append(_d)

    fig, ax = plt.subplots()
    ax.set_title("Stumble Summary", size=16)
    ax.bar(falls["Day"], falls[subject])
    ax.set_ylabel("Total Stumbles", size=16)
    ax.set_xlabel("Date", size=16)
    ax.set_xticks(xt)
    new_x = np.arange(xt[0], xt[-1],(xt[-1]-xt[0])/100.)
    ymax = max(proj_risk, max(falls[subject]))
    ax.set_ylim(bottom=0, top=ymax + 1)
    ax.bar(0, intercept)
    ax.plot(new_x, intercept + slope *  new_x, color='c', linestyle='-', lw = 5)
    ax.set_xticklabels(xd)

    plt.savefig("web/assets/projection.png")

    text_lines = []
    text_lines.append("Your risk level is %s" % risk_category(proj_risk))
    text_lines.append("Your most recent trend suggest %i stumbles today." % proj_risk)
    text_lines.append(risk_change(slope))
    return proj_risk, text_lines


welcome()
falls = load_data()
#subject = st.selectbox("Enter today's data (for now choose a subject)", falls.columns[1:])
subject = st.sidebar.selectbox("Enter today's data (for now choose a subject)", falls.columns[1:])

proj_risk, text_lines = project_risk(falls,subject)

val_max = 10
rm = RiskMeter(proj_risk / val_max)

st.image("web/assets/meter.png", use_column_width = True)
for line in text_lines: st.markdown("<center>" + line + "</center>", unsafe_allow_html = True)
st.image("web/assets/projection.png", use_column_width = True)
