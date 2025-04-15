import { useMIDIAnimationStore } from "@site/src/store/midi-animation";
import React, { useEffect, useState } from "react";
import { RhythmNote } from "./types";

const NOTE_COUNT = 12;
const NOTE_MAP = [
  "C",
  "C#",
  "D",
  "D#",
  "E",
  "F",
  "F#",
  "G",
  "G#",
  "A",
  "A#",
  "B",
];

type Props = {
  time: number;
};

const DAW_TIMELINE_LENGTH = 8;

const DAWNotes = ({ time }: Props) => {
  const [notes, setNotes] = useState<RhythmNote[]>([]);
  const noteTracks = new Array(NOTE_COUNT).fill(0);
  const { midiFile, currentTrack, playing } = useMIDIAnimationStore();

  // As time changes, spawn more notes (and delete old ones)
  useEffect(() => {
    if (!playing) return;

    const timeRangeEnd = time + DAW_TIMELINE_LENGTH;

    // Find notes within distance
    const visibleNotes = midiFile.tracks[currentTrack].notes.filter((note) => {
      const isBeforeEnd = note.time < timeRangeEnd;
      const isAfterBeginning = note.time > time;

      return isBeforeEnd && isAfterBeginning;
    });
    setNotes(visibleNotes);
  }, [playing, time]);

  return (
    <div className="AnimatedNotesContainer">
      <div className="DAWContainer">
        {noteTracks.map((_, index) => {
          const trackNotes = notes.filter(
            (note) => note.note.slice(0, -1) == NOTE_MAP[index]
          );
          return (
            <div key={index} className="DAWRow">
              {trackNotes.map((note) => {
                const screenWidth = window.innerWidth / 2 - 400;
                // We basically measure the distance from current time to when note plays
                const animatedXPosition = Math.abs(note.time - time);
                // Then we scale it up to half the size of screen
                const scaledAnimatedXPosition =
                  animatedXPosition * -screenWidth + screenWidth;

                return (
                  <div
                    className="DAWNote"
                    style={{
                      transform: `translateX(${scaledAnimatedXPosition}px)`,
                    }}
                  >
                    {note.note}
                  </div>
                );
              })}
            </div>
          );
        })}
      </div>
      <div>
        {noteTracks.map((_, index) => {
          const trackNotes = notes.filter(
            (note) => note.note.slice(0, -1) == NOTE_MAP[index]
          );
          return (
            <div key={index} className="DAWRow TimelineRow">
              {trackNotes.map((note) => {
                const delayTime = time;
                const screenWidth = window.innerWidth / 2;
                // We basically measure the distance from current time to when note plays
                const animatedXPosition = Math.abs(delayTime - note.time);
                // Then we scale it up to half the size of screen
                const scaledAnimatedXPosition =
                  animatedXPosition * -screenWidth + screenWidth;

                return (
                  <div
                    className="TimelineKeyframe"
                    style={{
                      transform: `translateX(${scaledAnimatedXPosition}px)`,
                    }}
                  ></div>
                );
              })}
            </div>
          );
        })}
      </div>
    </div>
  );
};

export default DAWNotes;
