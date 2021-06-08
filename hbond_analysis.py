import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from midiutil import MIDIFile

# cleaning the data and calculating continuous averages
hbond_files = ["hbonds_TYC.dat", "hbonds_TYN.dat", "hbonds_TYR.dat"]
hbond_dict = {}
hbond_file: str
for hbond_file in hbond_files:
    hbond_df = pd.read_csv(hbond_file,
                           delimiter=',',
                           header=None)
    hbond_df.columns = ['time', 'hbonds']
    newhbond_df = hbond_df[hbond_df.index % 2 != 1].copy()
    newhbond_df.loc[:, 'avg'] = newhbond_df['hbonds'].rolling(window=30).mean().shift(-29)
    hbond_dict[hbond_file[0:-4] + "_df"] = newhbond_df

# creating the constraints for mapping hydrogen bonds
conditions_dict = {}
hbondnotes_dict = {}
notes = [60, 62, 64, 65, 67, 69, 71, 72]
for dfkey, dfval in hbond_dict.items():
    conditions = []
    for segment in range(0,8):
        condition = (dfval['avg'] >= segment) & (dfval['avg'] <= segment + 1)
        conditions.append(condition)
    dfval['note'] = np.select(conditions,
                              notes,
                              default=60)
    conditions_dict[dfkey + "conditions"] = conditions
    # hbondnotes_dict[dfkey[0:-3]] = dfval['note'].tolist()

# transforming lists into MIDI data
for df_name, df_val in hbond_dict.items():

    degrees = df_val['note'].tolist()  # MIDI note numbers
    track = 0  # track numbers are zero-origin
    channel = 0
    time = 0  # In beats
    duration = 1  # In beats
    tempo = 60  # In BPM
    volume = 100  # 0-127 anything more will corrupt the file

    hbond_MIDI = MIDIFile(1)
    hbond_MIDI.addTempo(track, time, tempo)

    for i in range(1, len(degrees)):
        if degrees[i] == degrees[i - 1] and i != 1 and i != len(degrees) - 1:
            volume = 0
        else:
            volume = 100
        hbond_MIDI.addNote(track, channel, degrees[i], time + i, duration, volume)

    with open((df_name[0:10] + 'notes.mid'), 'wb') as output_file:  # writing output file
        hbond_MIDI.writeFile(output_file)

print(hbond_dict)
