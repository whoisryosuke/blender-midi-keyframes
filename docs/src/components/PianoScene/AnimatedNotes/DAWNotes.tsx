import React from "react";

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

type Props = {};

const DAWNotes = (props: Props) => {
  const noteTracks = new Array(NOTE_COUNT).fill(0);
  return (
    <div className="DAWContainer">
      {noteTracks.map((_, index) => {
        return (
          <div key={index} className="DAWRow">
            <div className="DAWNote">{NOTE_MAP[index]}</div>
          </div>
        );
      })}
    </div>
  );
};

export default DAWNotes;
