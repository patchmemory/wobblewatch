import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import os, sys

features = ["ax","ay","az","rx","ry","rz","ax2","ay2","az2"]
ifname1 = os.path.abspath(sys.argv[1])
fname_split = ifname1.split('/')
base = fname_split[-3]

tname = '/'.join(fname_split[-2:])
base_enhanced = "SisFall_temporally_annotated"
ifname2 = os.path.abspath("%s/%s" % (base_enhanced, tname))

base_combined = "SisFall_labeled"
ofname = os.path.abspath("%s/%s" % (base_combined, tname))
ofname = os.path.splitext(ofname)[0] + ".pkl"

if not os.path.exists(ofname):
    
    print("file 1:", ifname1)
    print("file 2:", ifname2)
    print("ofile :", ofname)
    
    df = pd.read_csv(ifname1, names=features)
    #print(df)
    
    fps = 200
    t = df.index.values / fps
    df['t'] = t
    
    label = pd.read_csv(ifname2, names=['label'])
    #print(label)
    df['label'] = label 
    
    df = df.drop(columns = ["ax2","ay2","az2"])
    
    
    print(df)
    
    print(ofname)
    savedir = os.path.split(ofname)[0]
    if not os.path.exists(savedir):
        os.makedirs(savedir)
    
    df.to_pickle(ofname)

else:

    print("File already created.")
