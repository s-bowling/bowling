import numpy as np
import pandas as pd
from midiutil import MIDIFile
import matplotlib.pyplot as plt

# cleaning raw data
rgyr_files = ["rgyr_TYC.dat", "rgyr_TYN.dat", "rgyr_TYR.dat"]
rgyr_dict = {}
rgyr_file: str
for rgyr_file in rgyr_files:
    rgyr_df = pd.read_csv(rgyr_file,
                          delimiter=',',
                          header=None)
    rgyr_df.columns = ['time', 'rgyr']
    newrgyr_df = rgyr_df[rgyr_df.index % 2 != 1].copy()  # without copy() we are only taking slice
    newrgyr_df.loc[:,'avg'] = newrgyr_df['rgyr'].rolling(window=20).mean().shift(-19)
    rgyr_dict[rgyr_file[0:-4] + "_df"] = newrgyr_df

# creating conditions for transformation
conditions_dict = {}    # will contain lists instead of data frames
rgyrnotes_dict = {}     # name: list of notes
notes = [60, 62, 64, 65, 67, 69]
for dfkey, dfval in rgyr_dict.items():
    conditions = []
    for segment in range(0,6):
        condition = (dfval['avg'] >= segment + 8) & (dfval['avg'] <= segment + 9)
        conditions.append(condition)
    dfval['note'] = np.select(conditions,
                              notes,
                              default=60)
    conditions_dict[dfkey + "conditions"] = conditions
    rgyrnotes_dict[dfkey[0:-3]] = dfval['note'].tolist()

for df_name, df_val in rgyr_dict.items():

    degrees = df_val['note'].tolist()  # MIDI note numbers
    track = 0  # track numbers are zero-origin
    channel = 0
    time = 0  # In beats
    duration = 1  # In beats
    tempo = 60  # In BPM
    volume = 100  # 0-127 anything more will corrupt the file

    rgyr_MIDI = MIDIFile(1)
    rgyr_MIDI.addTempo(track, time, tempo)

    for i in range(1, len(degrees)):
        if degrees[i] == degrees[i - 1] and i != 1 and i != len(degrees)-1:
            volume = 0
        else:
            volume = 100
        rgyr_MIDI.addNote(track, channel, degrees[i], time + i, duration, volume)

    with open((df_name[0:8] + 'notes.mid'), 'wb') as output_file:
        rgyr_MIDI.writeFile(output_file)
