import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from midiutil import MIDIFile

# cleaning raw data
end2end_files = ["end2end_dist_TYC.dat", "end2end_dist_TYN.dat", "end2end_dist_TYR.dat"]
end2end_dict = {}
end2end_file: str
for end2end_file in end2end_files:
    end2end_df = pd.read_csv(end2end_file,
                          delimiter=',',
                          header=None)
    end2end_df.columns = ['time', 'dist']
    newend2end_df = end2end_df[end2end_df.index % 2 != 1].copy()  # without copy() we are only taking slice
    newend2end_df.loc[:,'avg'] = newend2end_df['dist'].rolling(window=20).mean().shift(-19)
    end2end_dict[end2end_file[0:-4] + "_df"] = newend2end_df

# creating conditions for transformation
conditions_dict = {}    # will contain lists instead of data frames
end2endnotes_dict = {}     # name: list of notes
notes = [60, 62, 64, 65, 67, 69]
for dfkey, dfval in end2end_dict.items():
    conditions = []
    for segment in range(0,6):
        condition = (dfval['avg'] >= (segment * 5) + 5) & (dfval['avg'] <= (segment * 5) + 10)
        conditions.append(condition)
    dfval['note'] = np.select(conditions,
                              notes,
                              default=60)
    conditions_dict[dfkey + "conditions"] = conditions
    end2endnotes_dict[dfkey[0:-3]] = dfval['note'].tolist()    # separate dictionary of 3 lists

for df_name, df_val in end2end_dict.items():

    degrees = df_val['note'].tolist()  # MIDI note numbers
    track = 0  # track numbers are zero-origin
    channel = 0
    time = 0  # In beats
    duration = 1  # In beats
    tempo = 60  # In BPM
    volume = 100  # 0-127 anything more will corrupt the file

    end2end_MIDI = MIDIFile(1)
    end2end_MIDI.addTempo(track, time, tempo)

    for i in range(1, len(degrees)):
        if degrees[i] == degrees[i - 1] and i != 1 and i != len(degrees) - 1:
            volume = 0
        else:
            volume = 100
        end2end_MIDI.addNote(track, channel, degrees[i], time + i, duration, volume)

    with open((df_name[0:16] + 'notes.mid'), 'wb') as output_file:  # writing output file
        end2end_MIDI.writeFile(output_file)

print(end2end_dict)