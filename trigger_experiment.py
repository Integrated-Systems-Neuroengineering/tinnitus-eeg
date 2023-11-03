from psychopy import visual, event, core, data, gui
from pylsl import StreamInfo, StreamOutlet

info = StreamInfo("TinnitusOnsetData", "Markers", 1,
                  channel_format='int32', source_id='uniqueid12345')
outlet = StreamOutlet(info)
win = visual.Window([2560, 1440], fullscr=True)

rest_fixation = visual.TextStim(win, "Rest")
tinnitus_onset = visual.TextStim(win, "Onset tinnitus")

time_info = {'pre_stimulus_rest': 10, 'tinnitus_onset_time': 5}

keys = event.waitKeys(keyList=["space"])
if (keys[0] == 'space') is True:
    trails = data.TrialHandler(trialList=[], nReps=5)
    for thisTrial in trails:

        rest_fixation.draw()
        win.flip()
        outlet.push_sample(x=[0])
        core.wait(time_info['pre_stimulus_rest'])

        tinnitus_onset.draw()
        win.flip()
        outlet.push_sample(x=[1])
        core.wait(time_info['tinnitus_onset_time'])