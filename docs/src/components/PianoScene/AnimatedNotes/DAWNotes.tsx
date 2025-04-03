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

const DAW_TIMELINE_LENGTH = 4;

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
    <div className="DAWContainer">
      {noteTracks.map((_, index) => {
        const trackNotes = notes.filter(
          (note) => note.note.slice(0, -1) == NOTE_MAP[index]
        );
        return (
          <div key={index} className="DAWRow">
            {trackNotes.map((note) => (
              <div
                className="DAWNote"
                style={{
                  transform: `translateX(${
                    (Math.abs(note.time - time) * -window.innerWidth) / 2 +
                    window.innerWidth / 2
                  }px)`,
                }}
              >
                {note.note}
              </div>
            ))}
          </div>
        );
      })}
    </div>
  );
};

export default DAWNotes;
