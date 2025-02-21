import numpy as np

import resonance.run
import resonance.pipe
import resonance.cross
import resonance.db
from process import *


def interleave_blocks(blocks):
    return sorted(blocks, key=lambda x: x.TS[0])


def artificial_eeg(sampling_rate, seconds, freq):
    si = resonance.si.Channels(1, sampling_rate)
    data = [
        resonance.db.Channels(
            si,
            time*1e9,
            np.sin(np.linspace(time, time+1, num=sampling_rate)*2*np.pi*freq)
        )
        for time in np.arange(0, seconds)
    ]
    return si, data


eeg_si, eeg_blocks = artificial_eeg(500, 8, 4.3)
events_si = resonance.si.Event()
events_blocks = [
    resonance.db.Event(events_si, 1.1e9, '1'),
    resonance.db.Event(events_si, 5.4e9, '2'),
    resonance.db.Event(events_si, 5.6e9, '1'),
    resonance.db.Event(events_si, 6.4e9, '3')
]

si = [eeg_si, events_si]
data = interleave_blocks(eeg_blocks + events_blocks)

proc = online_processing_4
# r1 = resonance.run.offline(si, data, proc)
# print(r1)
r2 = resonance.run.online(si, data, proc, return_blocks=False)
print(r2)