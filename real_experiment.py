#!/usr/bin/env python
# -*- coding: utf-8 -*-

# --- Import packages ---
from psychopy import locale_setup
from psychopy import prefs
from psychopy import (
    sound,
    gui,
    visual,
    core,
    data,
    event,
    logging,
    clock,
    colors,
    layout,
    parallel,
    hardware,
)
from psychopy.constants import (
    NOT_STARTED,
    STARTED,
    PLAYING,
    PAUSED,
    STOPPED,
    FINISHED,
    PRESSED,
    RELEASED,
    FOREVER,
)

import numpy as np  # whole numpy lib is available, prepend 'np.'
from numpy import (
    sin,
    cos,
    tan,
    log,
    log10,
    pi,
    average,
    sqrt,
    std,
    deg2rad,
    rad2deg,
    linspace,
    asarray,
)
from numpy.random import random, randint, normal, shuffle, choice as randchoice
import os  # handy system and path functions
import sys  # to get file system encoding
import csv
import random as rng

# sys.setdefaultencoding("utf-8")

import psychopy.iohub as io
from psychopy.hardware import keyboard

# Ensure that relative paths start from the same directory as this script
_thisDir = os.path.dirname(os.path.abspath(__file__))
os.chdir(_thisDir)
# Store info about the experiment session
psychopyVersion = "2022.2.4"
expLang = "tr"  # each participant will hear either tr or eng sentences
expName = "real_experiment"  # from the Builder filename that created this script
expInfo = {
    "participant": f"2",
    "session": "001",
    "calibration": "True",
}
# --- Show participant info dialog --
dlg = gui.DlgFromDict(dictionary=expInfo, sortKeys=False, title=expName)
if dlg.OK == False:
    core.quit()  # user pressed cancel
expInfo["date"] = data.getDateStr()  # add a simple timestamp
expInfo["expName"] = expName
expInfo["psychopyVersion"] = psychopyVersion

# We are going to load either tr or eng accordingly
if int(expInfo["participant"]) % 2 == 0:
    expLang = "eng"

# Data file name stem = absolute path + name; later add .psyexp, .csv, .log, etc
filename = (
    _thisDir
    + os.sep
    + "data/%s_%s_%s" % (expInfo["participant"], expName, expInfo["date"])
)

# An ExperimentHandler isn't essential but helps with data saving
thisExp = data.ExperimentHandler(
    name=expName,
    version="",
    extraInfo=expInfo,
    runtimeInfo=None,
    originPath="C:\\Users\\asena\\Desktop\\Asena\\real_experiment.py",
    savePickle=False,
    saveWideText=True,
    dataFileName=filename,
)
# save a log file for detail verbose info
logFile = logging.LogFile(filename + ".log", level=logging.EXP)
logging.console.setLevel(logging.WARNING)  # this outputs to the screen, not a file

endExpNow = False  # flag for 'escape' or other condition => quit the exp
frameTolerance = 0.001  # how close to onset before 'same' frame

# Start Code - component code to be run after the window creation

# --- Setup the Window ---
win = visual.Window(
    size=(1920, 1080),
    fullscr=True,
    screen=0,
    winType="pyglet",
    allowStencil=False,
    monitor="testMonitor",
    color=[-1, -1, -1],
    colorSpace="rgb",
    blendMode="avg",
    useFBO=True,
    units="height",
)

win.mouseVisible = False
# store frame rate of monitor if we can measure it
expInfo["frameRate"] = win.getActualFrameRate()
if expInfo["frameRate"] != None:
    frameDur = 1.0 / round(expInfo["frameRate"])
else:
    frameDur = 1.0 / 120.0  # could not measure, so guess
# --- Setup input devices ---
ioConfig = {}

# Setup iohub keyboard
ioConfig["Keyboard"] = dict(use_keymap="psychopy")  #

ioSession = "1"
if "session" in expInfo:
    ioSession = str(expInfo["session"])
ioServer = io.launchHubServer(window=win, **ioConfig)

# create a default keyboard (e.g. to check for escape)
defaultKeyboard = keyboard.Keyboard(backend="iohub")

# --- Initialize components for Routine "fixation_cross_routine" ---
fixation_cross_polygon = visual.ShapeStim(
    win=win,
    name="fixation_cross_polygon",
    vertices="cross",
    size=(0.3, 0.3),
    ori=0.0,
    pos=(0, 0),
    anchor="center",
    lineWidth=1.0,
    colorSpace="rgb",
    lineColor="white",
    fillColor="white",
    opacity=None,
    depth=0.0,
    interpolate=True,
)

p_port = parallel.ParallelPort(address="0x4FF8")

# Stuff added later all all here
shuf = list()
probe_words = dict()
sentences = {"eng": dict(), "tr": dict()}
emotions = ["h", "s", "n"]
speakers = ["tugce", "laura"]
sid = dict()
durations = dict()
triggers = dict()

for emo in emotions:
    for spe in speakers:
        shuf.append((emo, spe))
        sentences["tr"][(emo, spe)] = list()
        sentences["eng"][(emo, spe)] = list()

if expInfo["calibration"] == "True":
    triggers["correct"] = 255
    for lang in ["tr", "eng"]:
        for spe in speakers:
            for emo in emotions:
                triggers[(spe, emo, lang)] = 255
    triggers["show_cross"] = 255
    triggers["show_probe_word"] = 255
    triggers["false"] = 255
else:
    _idx = 1
    for lang in ["tr", "eng"]:
        for spe in speakers:
            for emo in emotions:
                triggers[(spe, emo, lang)] = _idx
                _idx += 1
    triggers["show_cross"] = 43
    triggers["show_probe_word"] = 44
    triggers["correct"] = 45
    triggers["false"] = 46

with open(
    f"C:\\Users\\asena\\Desktop\\Asena\\sentence_ids\\sentence_ids_{expLang}"
) as sentfile:
    for row in sentfile:
        pair = row.split(",", 1)
        sid[pair[0]] = pair[1].strip()

with open(f"C:\\Users\\asena\\Desktop\\Asena\\{expLang}_probe_words.csv", encoding="utf-8") as probefile:
    for idx, row in enumerate(probefile):
        pair = row.split(",", 2)
        probe_words[idx] = (pair[0].strip(), pair[1].strip())

with open("C:\\Users\\asena\\Desktop\\Asena\\selected_sentences.csv") as csvfile:
    reader = csv.DictReader(csvfile, delimiter=",")
    for row in reader:
        sentences[row["lang"]][(row["emotion"], row["speaker"])].append(row["sid"])

with open("C:\\Users\\asena\\Desktop\\Asena\\durations.csv") as csvfile:
    reader = csv.DictReader(csvfile, delimiter=",")
    for row in reader:
        durations[row["sound_file"]] = row["duration"]

for lang in sentences.values():
    for category in lang.values():
        rng.shuffle(category)

experiment_stuff = []

for i in range(180):
    if i % 6 == 0:
        rng.shuffle(shuf)
    emotion, speaker = shuf[i % 6]
    picked_id = sentences["eng"][shuf[i % 6]].pop()
    print(shuf[i % 6], end=" ")
    print(sid[picked_id])

    # Decision done
    picked_name = f"{speaker}-{expLang}-{emotion}-{picked_id}"

    s = sound.Sound(
        f"C:\\Users\\asena\\Desktop\\Asena\\amped_sound_files\\{picked_name}.wav",
        secs=durations[picked_name],
        stereo=True,
        # hamming=True,
        name=picked_name,
    )
    s.setVolume(1.0)

    probe_decision = rng.choice(("CorrectProbe", "FalseProbe"))
    probe_prompt = probe_words[int(picked_id)][0]
    prompt_correctness = True

    if probe_decision == "FalseProbe":
        probe_prompt = probe_words[int(picked_id)][1]
        prompt_correctness = False

    experiment_stuff.append(
        {
            "SoundFile": s,
            "Duration": float(durations[picked_name]),
            "Speaker": speaker,
            "Emotion": emotion,
            "ProbePrompt": probe_prompt,
            "IsCorrect": prompt_correctness,
        }
    )

# --- Initialize components for Routine "probe_word_routine" ---
probe_word = visual.TextStim(
    win=win,
    name="probe_word",
    text=f"WWWWWWWWWWWWWW",
    font="Open Sans",
    pos=(0, 0),
    height=0.05,
    wrapWidth=None,
    ori=0.0,
    color="black",
    colorSpace="rgb",
    opacity=None,
    languageStyle="LTR",
    depth=0.0,
)


# --- Initialize components for Routine "prompt_routine" ---
prompt_yes = visual.ButtonStim(
    win,
    text="Yes",
    font="Arvo",
    pos=(-0.2, -0.15),
    letterHeight=0.05,
    size=[0.25],
    borderWidth=0.0,
    fillColor="black",
    borderColor=None,
    color="white",
    colorSpace="rgb",
    opacity=None,
    bold=True,
    italic=False,
    padding=None,
    anchor="center",
    name="prompt_yes",
)
prompt_yes.buttonClock = core.Clock()
prompt_no = visual.ButtonStim(
    win,
    text="No",
    font="Arvo",
    pos=(0.2, -0.15),
    letterHeight=0.05,
    size=[0.25],
    borderWidth=0.0,
    fillColor="black",
    borderColor=None,
    color="white",
    colorSpace="rgb",
    opacity=None,
    bold=True,
    italic=False,
    padding=None,
    anchor="center",
    name="prompt_no",
)
prompt_no.buttonClock = core.Clock()

# --- Initialize components for Routine "wait_routine" ---
wait_placeholder = visual.Line(
    win=win,
    name="wait_placeholder",
    start=(-(0.0, 0.0)[0] / 2.0, 0),
    end=(+(0.0, 0.0)[0] / 2.0, 0),
    ori=0.0,
    pos=(0, 0),
    anchor="center",
    lineWidth=1.0,
    colorSpace="rgb",
    lineColor="white",
    fillColor="white",
    opacity=None,
    depth=0.0,
    interpolate=True,
)

# Create some handy timers
globalClock = core.Clock()  # to track the time since experiment started
routineTimer = (
    core.Clock()
)  # to track time remaining of each (possibly non-slip) routine

# set up handler to look after randomisation of conditions etc
trials = data.TrialHandler(
    trialList=experiment_stuff,
    dataTypes=[
        "SoundFile",
        "Duration",
        "Speaker",
        "Emotion",
        "ProbePrompt",
        "IsCorrect",
    ],
    nReps=180.0,
    method="sequential",
    extraInfo=expInfo,
    originPath=-1,
    seed=None,
    name="trials",
)

thisExp.addLoop(trials)  # add the loop to the experiment
thisTrial = trials.trialList[0]  # so we can initialise stimuli with some values
# abbreviate parameter names if possible (e.g. rgb = thisTrial.rgb)
if thisTrial != None:
    for paramName in thisTrial:
        exec("{} = thisTrial[paramName]".format(paramName))

for thisTrial in trials:
    probe_word.text = thisTrial["ProbePrompt"]

    currentLoop = trials
    # abbreviate parameter names if possible (e.g. rgb = thisTrial.rgb)
    if thisTrial != None:
        for paramName in thisTrial:
            exec("{} = thisTrial[paramName]".format(paramName))

    # --- Prepare to start Routine "fixation_cross_routine" ---
    continueRoutine = True
    routineForceEnded = False
    # update component parameters for each repeat
    # keep track of which components have finished
    fixation_cross_routineComponents = [fixation_cross_polygon, p_port]
    for thisComponent in fixation_cross_routineComponents:
        thisComponent.tStart = None
        thisComponent.tStop = None
        thisComponent.tStartRefresh = None
        thisComponent.tStopRefresh = None
        if hasattr(thisComponent, "status"):
            thisComponent.status = NOT_STARTED
    # reset timers
    t = 0
    _timeToFirstFrame = win.getFutureFlipTime(clock="now")
    frameN = -1

    # --- Run Routine "fixation_cross_routine" ---
    while continueRoutine and routineTimer.getTime() < 0.5:
        # get current time
        t = routineTimer.getTime()
        tThisFlip = win.getFutureFlipTime(clock=routineTimer)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame

        # *p_port* updates
        if p_port.status == NOT_STARTED and t >= 0.0 - frameTolerance: # TODO: trigger for initial fixation cross, adjust delay here
            p_port.frameNStart = frameN  # exact frame index
            p_port.tStart = t  # local t and not account for scr refresh
            p_port.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(p_port, "tStartRefresh")  # time at next scr refresh
            thisExp.addData("fixaton_cross_trigger.start", t)
            p_port.status = STARTED
            win.callOnFlip(p_port.setData, int(triggers["show_cross"]))
        if p_port.status == STARTED:
            # is it time to stop? (based on global clock, using actual start)
            if tThisFlipGlobal > p_port.tStartRefresh + 0.001 - frameTolerance: # 1 ms trigger
                # keep track of stop time/frame for later
                p_port.tStop = t  # not accounting for scr refresh
                p_port.frameNStop = frameN  # exact frame index
                # add timestamp to datafile
                thisExp.addData("fixaton_cross_trigger.stop", t)
                p_port.status = FINISHED
                win.callOnFlip(p_port.setData, int(0))

        # *fixation_cross_polygon* updates
        if (
            fixation_cross_polygon.status == NOT_STARTED
            and tThisFlip >= 0.0 - frameTolerance
        ):
            # keep track of start time/frame for later
            fixation_cross_polygon.frameNStart = frameN  # exact frame index
            fixation_cross_polygon.tStart = t  # local t and not account for scr refresh
            fixation_cross_polygon.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(
                fixation_cross_polygon, "tStartRefresh"
            )  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, "fixation_cross_polygon.started")
            fixation_cross_polygon.setAutoDraw(True)
        if fixation_cross_polygon.status == STARTED:
            # is it time to stop? (based on global clock, using actual start)
            if (
                tThisFlipGlobal
                > fixation_cross_polygon.tStartRefresh + 0.5 - frameTolerance
            ):
                # keep track of stop time/frame for later
                fixation_cross_polygon.tStop = t  # not accounting for scr refresh
                fixation_cross_polygon.frameNStop = frameN  # exact frame index
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, "fixation_cross_polygon.stopped")
                fixation_cross_polygon.setAutoDraw(False)

        # check for quit (typically the Esc key)
        if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
            core.quit()

        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            routineForceEnded = True
            break
        continueRoutine = (
            False  # will revert to True if at least one component still running
        )
        for thisComponent in fixation_cross_routineComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished

        # refresh the screen
        if (
            continueRoutine
        ):  # don't flip if this routine is over or we'll get a blank screen
            win.flip()

    # --- Ending Routine "fixation_cross_routine" ---
    for thisComponent in fixation_cross_routineComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    # using non-slip timing so subtract the expected duration of this Routine (unless ended on request)
    if routineForceEnded:
        routineTimer.reset()
    else:
        routineTimer.addTime(-0.500000)

    # --- Prepare to start Routine "sound_stimuli_routine" ---
    continueRoutine = True
    routineForceEnded = False

    # Hacky, I know
    sound_1 = thisTrial["SoundFile"]
    # keep track of which components have finished
    sound_stimuli_routineComponents = [
        fixation_cross_polygon,
        thisTrial["SoundFile"],
        p_port,
    ]
    for thisComponent in sound_stimuli_routineComponents:
        thisComponent.tStart = None
        thisComponent.tStop = None
        thisComponent.tStartRefresh = None
        thisComponent.tStopRefresh = None
        if hasattr(thisComponent, "status"):
            thisComponent.status = NOT_STARTED
    # reset timers
    t = 0
    _timeToFirstFrame = win.getFutureFlipTime(clock="now")
    frameN = -1

    # --- Run Routine "sound_stimuli_routine" ---
    while (
        continueRoutine and routineTimer.getTime() < thisTrial["Duration"] # TODO: fix this, the routine takes longer than the sound file duration??
    ):  # Duration here
        # get current time
        t = routineTimer.getTime()
        tThisFlip = win.getFutureFlipTime(clock=routineTimer)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame

        # *sound eeg trigger* updates
        if p_port.status == NOT_STARTED and t >= 0.11 - frameTolerance: # TODO: Sound trigger and sound *pop* delay here
            # keep track of start time/frame for later
            p_port.frameNStart = frameN  # exact frame index
            p_port.tStart = t  # local t and not account for scr refresh
            p_port.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(p_port, "tStartRefresh")  # time at next scr refresh
            # add timestamp to datafile
            thisExp.addData("sound_file_trigger.start", t)
            p_port.status = STARTED
            win.callOnFlip(p_port.setData, int(triggers[(thisTrial["Speaker"], thisTrial["Emotion"], expLang)]))
            if p_port.status == STARTED:
                # is it time to stop? (based on global clock, using actual start)
                if tThisFlipGlobal > p_port.tStartRefresh + 0.001 - frameTolerance:
                    # keep track of stop time/frame for later
                    p_port.tStop = t  # not accounting for scr refresh
                    p_port.frameNStop = frameN  # exact frame index
                    # add timestamp to datafile
                    thisExp.addData("sound_file_trigger.stop", t)
                    p_port.status = FINISHED
                    win.callOnFlip(p_port.setData, int(0))

        # *fixation_cross_polygon* updates
        if (
            fixation_cross_polygon.status == NOT_STARTED
            and tThisFlip >= 0.0 - frameTolerance
        ):
            # keep track of start time/frame for later
            fixation_cross_polygon.frameNStart = frameN  # exact frame index
            fixation_cross_polygon.tStart = t  # local t and not account for scr refresh
            fixation_cross_polygon.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(
                fixation_cross_polygon, "tStartRefresh"
            )  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, "fixation_cross_polygon.started")
            fixation_cross_polygon.setAutoDraw(True)
        if fixation_cross_polygon.status == STARTED:
            # is it time to stop? (based on global clock, using actual start)
            if (
                tThisFlipGlobal
                > fixation_cross_polygon.tStartRefresh
                + thisTrial["Duration"]
                - frameTolerance
            ):  # Duration here
                # keep track of stop time/frame for later
                fixation_cross_polygon.tStop = t  # not accounting for scr refresh
                fixation_cross_polygon.frameNStop = frameN  # exact frame index
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, "fixation_cross_polygon.stopped")
                fixation_cross_polygon.setAutoDraw(False)

        # start/stop sound_1
        if sound_1.status == NOT_STARTED and tThisFlip >= 0.0 - frameTolerance:
            # keep track of start time/frame for later
            sound_1.frameNStart = frameN  # exact frame index
            sound_1.tStart = t  # local t and not account for scr refresh
            sound_1.tStartRefresh = tThisFlipGlobal  # on global time
            # add timestamp to datafile
            thisExp.addData("sound_1.started", tThisFlipGlobal)
            sound_1.play(when=win)  # sync with win flip
        if sound_1.status == STARTED:
            # is it time to stop? (based on global clock, using actual start)
            if (
                tThisFlipGlobal
                > sound_1.tStartRefresh + thisTrial["Duration"] - frameTolerance
            ):  # Duration here
                # keep track of stop time/frame for later
                sound_1.tStop = t  # not accounting for scr refresh
                sound_1.frameNStop = frameN  # exact frame index
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, "sound_1.stopped")
                sound_1.stop()

        # check for quit (typically the Esc key)
        if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
            core.quit()

        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            routineForceEnded = True
            break
        continueRoutine = (
            False  # will revert to True if at least one component still running
        )
        for thisComponent in sound_stimuli_routineComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished

        # refresh the screen
        if (
            continueRoutine
        ):  # don't flip if this routine is over or we'll get a blank screen
            win.flip()

    # --- Ending Routine "sound_stimuli_routine" ---
    for thisComponent in sound_stimuli_routineComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    if p_port.status == STARTED:
        win.callOnFlip(p_port.setData, int(0))
    sound_1.stop()  # ensure sound has stopped at end of routine
    # using non-slip timing so subtract the expected duration of this Routine (unless ended on request)
    if routineForceEnded:
        routineTimer.reset()
    else:
        tosub = -1 * thisTrial["Duration"]
        routineTimer.addTime(tosub)  # Duration here

    ##########################################
    # Delay between sound file and probe word
    # 500 ms = 0.5 s
    ##########################################

    continueRoutine = True
    routineForceEnded = False
    # update component parameters for each repeat
    # keep track of which components have finished
    wait_routineComponents = [wait_placeholder]
    for thisComponent in wait_routineComponents:
        thisComponent.tStart = None
        thisComponent.tStop = None
        thisComponent.tStartRefresh = None
        thisComponent.tStopRefresh = None
        if hasattr(thisComponent, "status"):
            thisComponent.status = NOT_STARTED
    # reset timers
    t = 0
    _timeToFirstFrame = win.getFutureFlipTime(clock="now")
    frameN = -1

    # --- Run Routine "wait_routine" ---
    while continueRoutine and routineTimer.getTime() < 0.5:
        # get current time
        t = routineTimer.getTime()
        tThisFlip = win.getFutureFlipTime(clock=routineTimer)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame

        # *wait_placeholder* updates
        if wait_placeholder.status == NOT_STARTED and tThisFlip >= 0.0 - frameTolerance:
            # keep track of start time/frame for later
            wait_placeholder.frameNStart = frameN  # exact frame index
            wait_placeholder.tStart = t  # local t and not account for scr refresh
            wait_placeholder.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(
                wait_placeholder, "tStartRefresh"
            )  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, "wait_placeholder.started")
            wait_placeholder.setAutoDraw(True)
        if wait_placeholder.status == STARTED:
            # is it time to stop? (based on global clock, using actual start)
            if tThisFlipGlobal > wait_placeholder.tStartRefresh + 0.5 - frameTolerance:
                # keep track of stop time/frame for later
                wait_placeholder.tStop = t  # not accounting for scr refresh
                wait_placeholder.frameNStop = frameN  # exact frame index
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, "wait_placeholder.stopped")
                wait_placeholder.setAutoDraw(False)

        # check for quit (typically the Esc key)
        if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
            core.quit()

        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            routineForceEnded = True
            break
        continueRoutine = (
            False  # will revert to True if at least one component still running
        )
        for thisComponent in wait_routineComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished

        # refresh the screen
        if (
            continueRoutine
        ):  # don't flip if this routine is over or we'll get a blank screen
            win.flip()

    # --- Ending Routine "wait_routine" ---
    for thisComponent in wait_routineComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    # using non-slip timing so subtract the expected duration of this Routine (unless ended on request)
    if routineForceEnded:
        routineTimer.reset()
    else:
        routineTimer.addTime(-0.500000)
    thisExp.nextEntry()

    ################
    #  delay done  #
    ################

    # --- Prepare to start Routine "probe_word_routine" ---
    continueRoutine = True
    routineForceEnded = False
    # update component parameters for each repeat
    # keep track of which components have finished
    probe_word_routineComponents = [probe_word, p_port]
    for thisComponent in probe_word_routineComponents:
        thisComponent.tStart = None
        thisComponent.tStop = None
        thisComponent.tStartRefresh = None
        thisComponent.tStopRefresh = None
        if hasattr(thisComponent, "status"):
            thisComponent.status = NOT_STARTED
    # reset timers
    t = 0
    _timeToFirstFrame = win.getFutureFlipTime(clock="now")
    frameN = -1

    win.color = [1, 1, 1]

    # --- Run Routine "probe_word_routine" ---
    while continueRoutine and routineTimer.getTime() < 0.3:
        # get current time
        t = routineTimer.getTime()
        tThisFlip = win.getFutureFlipTime(clock=routineTimer)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame

        # *eeg trigger for probe word show* updates
        if p_port.status == NOT_STARTED and t >= 0.0 - frameTolerance: # TODO: maybe some delay here
            # keep track of start time/frame for later
            p_port.frameNStart = frameN  # exact frame index
            p_port.tStart = t  # local t and not account for scr refresh
            p_port.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(p_port, "tStartRefresh")  # time at next scr refresh
            # add timestamp to datafile
            thisExp.addData("p_port.started", t)
            p_port.status = STARTED
            win.callOnFlip(p_port.setData, int(triggers["show_probe_word"]))
        if p_port.status == STARTED:
            # is it time to stop? (based on global clock, using actual start)
            if tThisFlipGlobal > p_port.tStartRefresh + 0.001 - frameTolerance:
                # keep track of stop time/frame for later
                p_port.tStop = t  # not accounting for scr refresh
                p_port.frameNStop = frameN  # exact frame index
                # add timestamp to datafile
                thisExp.addData("p_port.stopped", t)
                p_port.status = FINISHED
                win.callOnFlip(p_port.setData, int(0))

        # *probe_word* updates
        if probe_word.status == NOT_STARTED and tThisFlip >= 0.0 - frameTolerance:
            # keep track of start time/frame for later
            probe_word.frameNStart = frameN  # exact frame index
            probe_word.tStart = t  # local t and not account for scr refresh
            probe_word.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(probe_word, "tStartRefresh")  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, "probe_word.started")
            probe_word.setAutoDraw(True)
        if probe_word.status == STARTED:
            # is it time to stop? (based on global clock, using actual start)
            if tThisFlipGlobal > probe_word.tStartRefresh + 0.300 - frameTolerance:
                # keep track of stop time/frame for later
                probe_word.tStop = t  # not accounting for scr refresh
                probe_word.frameNStop = frameN  # exact frame index
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, "probe_word.stopped")
                probe_word.setAutoDraw(False)

        # check for quit (typically the Esc key)
        if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
            core.quit()

        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            routineForceEnded = True
            break
        continueRoutine = (
            False  # will revert to True if at least one component still running
        )
        for thisComponent in probe_word_routineComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished

        # refresh the screen
        if (
            continueRoutine
        ):  # don't flip if this routine is over or we'll get a blank screen
            win.flip()

    # --- Ending Routine "probe_word_routine" ---
    for thisComponent in probe_word_routineComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    # using non-slip timing so subtract the expected duration of this Routine (unless ended on request)
    if routineForceEnded:
        routineTimer.reset()
    else:
        routineTimer.addTime(-0.300000)

    # --- Prepare to start Routine "prompt_routine" ---
    continueRoutine = True
    routineForceEnded = False
    # update component parameters for each repeat
    # keep track of which components have finished
    prompt_routineComponents = [prompt_yes, prompt_no, p_port]
    for thisComponent in prompt_routineComponents:
        thisComponent.tStart = None
        thisComponent.tStop = None
        thisComponent.tStartRefresh = None
        thisComponent.tStopRefresh = None
        if hasattr(thisComponent, "status"):
            thisComponent.status = NOT_STARTED
    # reset timers
    t = 0
    _timeToFirstFrame = win.getFutureFlipTime(clock="now")
    frameN = -1

    # Prompt answer stuff
    send_goodjob = False
    send_at_all = False

    win.color = [-1, -1, -1]

    # --- Run Routine "prompt_routine" ---
    while continueRoutine and routineTimer.getTime() < 180.0:
        # get current time
        t = routineTimer.getTime()
        tThisFlip = win.getFutureFlipTime(clock=routineTimer)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame

        # *prompt_yes* updates
        if prompt_yes.status == NOT_STARTED and tThisFlip >= 0 - frameTolerance:
            # keep track of start time/frame for later
            prompt_yes.frameNStart = frameN  # exact frame index
            prompt_yes.tStart = t  # local t and not account for scr refresh
            prompt_yes.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(prompt_yes, "tStartRefresh")  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, "prompt_yes.started")
            prompt_yes.setAutoDraw(True)
        if prompt_yes.status == STARTED:
            # is it time to stop? (based on global clock, using actual start)
            if tThisFlipGlobal > prompt_yes.tStartRefresh + 180.0 - frameTolerance:
                # keep track of stop time/frame for later
                prompt_yes.tStop = t  # not accounting for scr refresh
                prompt_yes.frameNStop = frameN  # exact frame index
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, "prompt_yes.stopped")
                prompt_yes.setAutoDraw(False)
        if prompt_yes.status == STARTED:
            # check whether prompt_yes has been pressed
            if prompt_yes.isClicked:
                if not prompt_yes.wasClicked:
                    prompt_yes.timesOn.append(
                        prompt_yes.buttonClock.getTime()
                    )  # store time of first click
                    prompt_yes.timesOff.append(
                        prompt_yes.buttonClock.getTime()
                    )  # store time clicked until
                else:
                    prompt_yes.timesOff[
                        -1
                    ] = prompt_yes.buttonClock.getTime()  # update time clicked until
                if not prompt_yes.wasClicked:
                    continueRoutine = False  # end routine when prompt_yes is clicked
                    None
                prompt_yes.wasClicked = True  # if prompt_yes is still clicked next frame, it is not a new click
            else:
                prompt_yes.wasClicked = (
                    False  # if prompt_yes is clicked next frame, it is a new click
                )
        else:
            prompt_yes.wasClicked = (
                False  # if prompt_yes is clicked next frame, it is a new click
            )

        # *prompt_no* updates
        if prompt_no.status == NOT_STARTED and tThisFlip >= 0 - frameTolerance:
            # keep track of start time/frame for later
            prompt_no.frameNStart = frameN  # exact frame index
            prompt_no.tStart = t  # local t and not account for scr refresh
            prompt_no.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(prompt_no, "tStartRefresh")  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, "prompt_no.started")
            prompt_no.setAutoDraw(True)
        if prompt_no.status == STARTED:
            # is it time to stop? (based on global clock, using actual start)
            if tThisFlipGlobal > prompt_no.tStartRefresh + 180.0 - frameTolerance:
                # keep track of stop time/frame for later
                prompt_no.tStop = t  # not accounting for scr refresh
                prompt_no.frameNStop = frameN  # exact frame index
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, "prompt_no.stopped")
                prompt_no.setAutoDraw(False)
        if prompt_no.status == STARTED:
            # check whether prompt_no has been pressed
            if prompt_no.isClicked:
                if not prompt_no.wasClicked:
                    prompt_no.timesOn.append(
                        prompt_no.buttonClock.getTime()
                    )  # store time of first click
                    prompt_no.timesOff.append(
                        prompt_no.buttonClock.getTime()
                    )  # store time clicked until
                else:
                    prompt_no.timesOff[
                        -1
                    ] = prompt_no.buttonClock.getTime()  # update time clicked until
                if not prompt_no.wasClicked:
                    continueRoutine = False  # end routine when prompt_no is clicked
                    None
                prompt_no.wasClicked = True  # if prompt_no is still clicked next frame, it is not a new click
            else:
                prompt_no.wasClicked = (
                    False  # if prompt_no is clicked next frame, it is a new click
                )
        else:
            prompt_no.wasClicked = (
                False  # if prompt_no is clicked next frame, it is a new click
            )

        if thisTrial["IsCorrect"]:
            if prompt_yes.wasClicked:
                # clicked yes, should've clicked yes, correct!
                send_goodjob = True
        else:
            if prompt_no.wasClicked:
                # clicked no, should've clicked no, correct!
                send_goodjob = True

        if prompt_yes.wasClicked or prompt_no.wasClicked:
            send_at_all = True

        # *p_port* updates
        if p_port.status == NOT_STARTED and t >= 0.0 - frameTolerance and send_at_all:
            # keep track of start time/frame for later
            p_port.frameNStart = frameN  # exact frame index
            p_port.tStart = t  # local t and not account for scr refresh
            p_port.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(p_port, "tStartRefresh")  # time at next scr refresh
            # add timestamp to datafile
            thisExp.addData("p_port.started", t)
            p_port.status = STARTED
            if send_goodjob:
                win.callOnFlip(p_port.setData, int(triggers["correct"]))
            else:
                win.callOnFlip(p_port.setData, int(triggers["false"]))
        if p_port.status == STARTED:
            # is it time to stop? (based on global clock, using actual start)
            if tThisFlipGlobal > p_port.tStartRefresh + 0.001 - frameTolerance:
                # keep track of stop time/frame for later
                p_port.tStop = t  # not accounting for scr refresh
                p_port.frameNStop = frameN  # exact frame index
                # add timestamp to datafile
                thisExp.addData("p_port.stopped", t)
                p_port.status = FINISHED
                win.callOnFlip(p_port.setData, int(0))

        # check for quit (typically the Esc key)
        if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
            core.quit()

        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            routineForceEnded = True
            break
        continueRoutine = (
            False  # will revert to True if at least one component still running
        )
        for thisComponent in prompt_routineComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished

        # refresh the screen
        if (
            continueRoutine
        ):  # don't flip if this routine is over or we'll get a blank screen
            win.flip()

    # --- Ending Routine "prompt_routine" ---
    for thisComponent in prompt_routineComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    thisExp.addData("prompt_yes.numClicks", prompt_yes.numClicks)
    if prompt_yes.numClicks:
        thisExp.addData("prompt_yes.timesOn", prompt_yes.timesOn)
        thisExp.addData("prompt_yes.timesOff", prompt_yes.timesOff)
    else:
        thisExp.addData("prompt_yes.timesOn", "")
        thisExp.addData("prompt_yes.timesOff", "")
    thisExp.addData("prompt_no.numClicks", prompt_no.numClicks)
    if prompt_no.numClicks:
        thisExp.addData("prompt_no.timesOn", prompt_no.timesOn)
        thisExp.addData("prompt_no.timesOff", prompt_no.timesOff)
    else:
        thisExp.addData("prompt_no.timesOn", "")
        thisExp.addData("prompt_no.timesOff", "")
    # using non-slip timing so subtract the expected duration of this Routine (unless ended on request)
    if routineForceEnded:
        routineTimer.reset()
    else:
        routineTimer.addTime(-180.000000)

    # --- Prepare to start Routine "wait_routine" ---
    continueRoutine = True
    routineForceEnded = False
    # update component parameters for each repeat
    # keep track of which components have finished
    wait_routineComponents = [wait_placeholder]
    for thisComponent in wait_routineComponents:
        thisComponent.tStart = None
        thisComponent.tStop = None
        thisComponent.tStartRefresh = None
        thisComponent.tStopRefresh = None
        if hasattr(thisComponent, "status"):
            thisComponent.status = NOT_STARTED
    # reset timers
    t = 0
    _timeToFirstFrame = win.getFutureFlipTime(clock="now")
    frameN = -1

    # --- Run Routine "wait_routine" ---
    while continueRoutine and routineTimer.getTime() < 1.5:
        # get current time
        t = routineTimer.getTime()
        tThisFlip = win.getFutureFlipTime(clock=routineTimer)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame

        # *wait_placeholder* updates
        if wait_placeholder.status == NOT_STARTED and tThisFlip >= 0.0 - frameTolerance:
            # keep track of start time/frame for later
            wait_placeholder.frameNStart = frameN  # exact frame index
            wait_placeholder.tStart = t  # local t and not account for scr refresh
            wait_placeholder.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(
                wait_placeholder, "tStartRefresh"
            )  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, "wait_placeholder.started")
            wait_placeholder.setAutoDraw(True)
        if wait_placeholder.status == STARTED:
            # is it time to stop? (based on global clock, using actual start)
            if tThisFlipGlobal > wait_placeholder.tStartRefresh + 1.5 - frameTolerance:
                # keep track of stop time/frame for later
                wait_placeholder.tStop = t  # not accounting for scr refresh
                wait_placeholder.frameNStop = frameN  # exact frame index
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, "wait_placeholder.stopped")
                wait_placeholder.setAutoDraw(False)

        # check for quit (typically the Esc key)
        if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
            core.quit()

        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            routineForceEnded = True
            break
        continueRoutine = (
            False  # will revert to True if at least one component still running
        )
        for thisComponent in wait_routineComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished

        # refresh the screen
        if (
            continueRoutine
        ):  # don't flip if this routine is over or we'll get a blank screen
            win.flip()

    # --- Ending Routine "wait_routine" ---
    for thisComponent in wait_routineComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    # using non-slip timing so subtract the expected duration of this Routine (unless ended on request)
    if routineForceEnded:
        routineTimer.reset()
    else:
        routineTimer.addTime(-1.500000)
    thisExp.nextEntry()

# completed the experiment

# --- End experiment ---
# Flip one final time so any remaining win.callOnFlip()
# and win.timeOnFlip() tasks get executed before quitting
win.flip()

# these shouldn't be strictly necessary (should auto-save)
thisExp.saveAsWideText(filename + ".csv", delim="auto")
thisExp.saveAsPickle(filename)
logging.flush()
thisExp.abort()  # or data files will save again on exit
win.close()
core.quit()
