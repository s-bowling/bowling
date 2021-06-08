import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from midiutil import MIDIFile

# cleaning raw data
struc_files = ["strucE_TYC.dat", "strucE_TYN.dat", "strucE_TYR.dat"]
struc_dict = {}
struc_file: str
for struc_file in struc_files:
    struc_df = pd.read_csv(struc_file,
                          delimiter=',',
                          header=None)
    struc_df.columns = ['time', 'struc']
    newstruc_df = struc_df[struc_df.index % 2 != 1].copy()  # without copy() we are only taking slice
    newstruc_df.loc[:,'avg'] = newstruc_df['struc'].rolling(window=20).mean().shift(-19)
    struc_dict[struc_file[0:-4] + "_df"] = newstruc_df

# creating conditions for transformation
conditions_dict = {}    # will contain lists instead of data frames
strucnotes_dict = {}     # name: list of notes
notes = [60, 62, 64, 65, 67, 69, 71]
for dfkey, dfval in struc_dict.items():
    conditions = []
    for segment in range(0,7):
        condition = (dfval['avg'] >= segment / 10) & (dfval['avg'] <= (segment + 1) / 10)
        conditions.append(condition)
    dfval['note'] = np.select(conditions,
                              notes,
                              default=60)
    conditions_dict[dfkey + "conditions"] = conditions
    strucnotes_dict[dfkey[0:-3]] = dfval['note'].tolist()    # separate dictionary of 3 lists

for df_name, df_val in struc_dict.items():

    degrees = df_val['note'].tolist()  # MIDI note numbers
    track = 0  # zero-origin
    channel = 0
    time = 0  # In beats
    duration = 1  # In beats
    tempo = 60  # In BPM
    volume = 100  # 0-127 anything more will corrupt the file

    struc_MIDI = MIDIFile(1)
    struc_MIDI.addTempo(track, time, tempo)

    for i in range(1, len(degrees)):
        if degrees[i] == degrees[i - 1] and i != 1 and i != len(degrees) - 1:
            volume = 0
        else:
            volume = 100
        struc_MIDI.addNote(track, channel, degrees[i], time + i, duration, volume)

    with open((df_name[0:10] + 'notes.mid'), 'wb') as output_file:  # writing output file
        struc_MIDI.writeFile(output_file)

print(struc_dict)