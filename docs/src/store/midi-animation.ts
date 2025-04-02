import { create } from "zustand";
import { devtools } from "zustand/middleware";
import { MIDIFile } from "../components/PianoScene/AnimatedNotes/types";
import { AnimationAction } from "three";
// import type {} from "@redux-devtools/extension"; // required for devtools typing

export interface MIDIAnimationStore {
  // Is game playing?
  playing: boolean;
  setPlaying: (playing: boolean) => void;
  paused: boolean;
  setPaused: (paused: boolean) => void;

  // Current playback time for piano roll
  startTime: number;
  elapsedTime: number;
  setStartTime: (startTime: number) => void;
  setElapsedTime: (elapsedTime: number) => void;
  incrementElapsedTime: (elapsedTime: number) => void;

  currentAnimation: AnimationAction;
  setCurrentAnimation: (currentAnimation: AnimationAction) => void;

  // Tracks
  currentTrack: number;
  setCurrentTrack: (currentTrack: number) => void;
  midiFile: MIDIFile;
  addMidiFile: (midiFile: MIDIFile) => void;
}

export const useMIDIAnimationStore = create<MIDIAnimationStore>()(
  devtools((set) => ({
    playing: false,
    setPlaying: (playing) =>
      set(() => ({
        playing,
      })),
    paused: false,
    setPaused: (paused) =>
      set(() => ({
        paused,
      })),

    startTime: 0,
    elapsedTime: 0,
    setStartTime: (startTime) =>
      set(() => ({
        startTime,
      })),
    setElapsedTime: (elapsedTime) =>
      set(() => ({
        elapsedTime,
      })),
    incrementElapsedTime: (elapsedTime) =>
      set((prevState) => ({
        elapsedTime: prevState.elapsedTime + elapsedTime,
      })),

    currentAnimation: null,
    setCurrentAnimation: (currentAnimation) =>
      set(() => ({
        currentAnimation,
      })),

    currentTrack: 0,
    setCurrentTrack: (currentTrack) =>
      set(() => ({
        currentTrack,
      })),
    midiFile: {
      name: "",
      bpm: 0,
      tracks: [],
    },
    addMidiFile: (midiFile) =>
      set((state) => ({
        midiFile: midiFile,
      })),
    // removeTrack: (index) =>
    //   set((state) => ({
    //     tracks: state.tracks.filter((_, trackIndex) => trackIndex === index),
    //   })),
  }))
);
