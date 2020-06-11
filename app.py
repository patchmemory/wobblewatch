import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import scipy.stats

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
    if slope > 1:
        st.text("Your risk is growing! You should [intervention]")
    elif slope < 1: 
        st.text("Your risk is dropping! Keep up the good work!")
    else:
        st.text("Your risk is not changing much...")
        if proj_risk < 3:
            st.text("... and that's great!")
        elif proj_risk < 5:
            st.text("... and that's okay, but you could use some improvement.")
        else:
            st.text("... but you should work to bring it down.")

def project_risk(falls, subject, show=False):
    slope, intercept, r_value, p_value, std_err = \
                scipy.stats.linregress(x=falls['Day'],y=falls[subject])
    if show:
        plt.title("Risk as pre-fall events")
        ax = sns.regplot(x = falls["Day"], y = falls[subject],scatter_kws={'s':231})
        plt.ylabel("Pre-fall events")
        plt.xlabel("Day")
        plt.ylim(bottom=0)
        plt.xticks([-3,-2,-1,0])
        xlims = ax.get_xlim()
        new_x = np.arange(xlims[0], xlims[1],(xlims[1]-xlims[0])/100.)
        ax.plot(new_x, intercept + slope *  new_x, color='c', linestyle='-', lw = 5)
        st.pyplot()
    proj_risk = intercept
    if proj_risk < 0:
        proj_risk = 0

    st.text("Your risk level is %s" % risk_category(proj_risk))
    st.text("Your most recent trend suggest %i stumbles today." % proj_risk)
    risk_change(slope)


welcome()
falls = load_data()
subject = st.selectbox("Enter today's data (for now choose a subject)", falls.columns[1:])
_s = st.checkbox("Show prediction plot", key=None)
project_risk(falls,subject,show=_s)

