import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import os, sys

def onclick(event):
    global ix1
    ix1 = event.xdata
    print("x1 = %d" % ix1)
    ax1.axvline(x=ix1, color='r')
    fig.canvas.draw()
    return ix1

def onrelease(event):
    global ix2
    ix2 = event.xdata
    print("x2 = %d" % ix2)
    ax1.axvline(x=ix2,color='r')
    fig.canvas.draw()
    return ix2

def onspace(event):
    global ix3
    ix3 = event.xdata
    print("x3 = %d" % ix3)
    ax1.axvline(x=ix3, color='r')
    fig.canvas.draw()
    fig.canvas.mpl_disconnect(cid)
    return ix3

features = ["ax","ay","az","rx","ry","rz","ax2","ay2","az2"]
fname = os.path.abspath(sys.argv[1])

df = pd.read_csv(fname, names=features)

fps = 200
t = df.index.values / fps
df['t'] = t

if len(sys.argv) == 2:
    
    fig, ax1 = plt.subplots(figsize=(20,10))
    color = 'b'
    ax1.set_xlabel('time (s)')
    ax1.set_ylabel('translational acceleration', color=color)
    ax1.tick_params(axis='y', labelcolor=color)
    for feature in features[:3]:
        ax1.fill_between(t, df[feature], color=color)
    
    ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis
    color = 'c'
    ax2.set_ylabel('rotational acceleration', color=color)  # we already handled the x-label with ax1
    ax2.tick_params(axis='y', labelcolor=color)
    for feature in features[3:6]:
        ax2.plot(t, df[feature], color=color)
    
    cid = fig.canvas.mpl_connect('button_press_event', onclick)
    cid = fig.canvas.mpl_connect('button_release_event', onrelease)
    cid = fig.canvas.mpl_connect('key_press_event', onspace)

    plt.show()
    print(ix1,ix2,ix3)
    
    df['no_fall'] = (t  < ix1) | (t >= ix3)
    df['prefall'] = (t >= ix1) & (t  < ix2)
    df['falling'] = (t >= ix2) & (t  < ix3)
    
    fig = plt.figure(figsize=(20,10))
    
    plt.fill_between(df['t'].values, 0, df['no_fall'].values, label="no fall")
    plt.fill_between(df['t'].values, 0, df['prefall'].values, label="prefall")
    plt.fill_between(df['t'].values, 0, df['falling'].values, label="falling")
    plt.xlabel('time (s)')
    plt.legend()
    plt.show()

elif len(sys.argv) == 3:
    df['no_fall'] = np.ones_like(t, dtype=bool)
    df['prefall'] = np.zeros_like(t, dtype=bool)
    df['falling'] = np.zeros_like(t, dtype=bool)
    

ofname = os.path.splitext(fname)[0] + ".pkl"
print(ofname)
df.to_pickle(ofname)
