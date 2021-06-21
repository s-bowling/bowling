import pandas as pd
import numpy as np
import re
import os

hbond_sim_files = []


def remove_lines_fix_data(hbond_sim_file):

    hbond_df = pd.read_csv(hbond_sim_file,
                           delimiter=',',
                           header=None)
    hbond_df.columns = ['time', 'hbonds']
    newhbond_df = hbond_df[hbond_df.index % 2 != 1].copy()
    newhbond_df.loc[:, 'avg'] = newhbond_df['hbonds'].rolling(window=30).mean().shift(-29)

    # creating the constraints for mapping hydrogen bonds
    notes = [60, 62, 64, 65, 67, 69, 71, 72]
    conditions = []
    for segment in range(0,8):
        condition = (newhbond_df['avg'] >= segment) & (newhbond_df['avg'] <= segment + 1)
        conditions.append(condition)
    newhbond_df['note'] = np.select(conditions,
                              notes,
                                default=60)

    # hbondnotes_dict[dfkey[0:-3]] = dfval['note'].tolist()

    # transforming lists into MIDI data
    midiFromDataframe(newhbond_df, hbond_sim_file[0:-4] + "_df")


for file in os.listdir("/mydir"):
    pattern = re.compile("hbonds_T*.dat")
    if pattern.search(file) is not None:
        hbond_sim_files.append(file)
    remove_lines_fix_data(file)


def midiFromDataframe(dataframe, filename, track=0, channel=0, time=0, duration=1, tempo=60, active_volume=100):
    degrees = dataframe['note'].tolist()  # MIDI note numbers

    hbond_MIDI = MIDIFile(1)
    hbond_MIDI.addTempo(track, time, tempo)

    for i in range(1, len(degrees)):
        if degrees[i] == degrees[i - 1] and i != 1 and i != len(degrees) - 1:
            volume = 0
        else:
            volume = active_volume
        hbond_MIDI.addNote(track, channel, degrees[i], time + i, duration, volume)

    with open((filename + 'notes.mid'), 'wb') as output_file:
        hbond_MIDI.writeFile(output_file)
