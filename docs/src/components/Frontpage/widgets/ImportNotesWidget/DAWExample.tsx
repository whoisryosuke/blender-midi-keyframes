import React from "react";
import "./DAWExample.css";

const SAMPLES_NOTE = [
  {
    note: "C",
    time: 0.5,
    duration: 1,
  },
  {
    note: "D",
    time: 0.5,
    duration: 1,
  },
  {
    note: "E",
    time: 0.5,
    duration: 1,
  },
  {
    note: "C",
    time: 4.5,
    duration: 1,
  },
  {
    note: "F",
    time: 4.5,
    duration: 1,
  },
  {
    note: "C",
    time: 8.5,
    duration: 1,
  },

  // D# Sequence 1
  {
    note: "D#",
    time: 3.5,
    duration: 0.5,
  },
  {
    note: "D#",
    time: 5.5,
    duration: 0.5,
  },
  {
    note: "D#",
    time: 7.5,
    duration: 0.5,
  },

  // D# Sequence 2
  {
    note: "D#",
    time: 10.5,
    duration: 0.5,
  },
  {
    note: "D#",
    time: 12.5,
    duration: 0.5,
  },
  {
    note: "D#",
    time: 14.5,
    duration: 0.5,
  },
];

const NOTES = [
  "spacer",
  "C",
  "C#",
  "D",
  "D#",
  "E",
  "F",
  // 'F#',
  // 'G',
  // 'G#',
  // 'A',
  // 'A',
  // 'B',
];
const NUM_COLS = 10;

type Props = {};

const DAWExample = (props: Props) => {
  return (
    <div className="DAWExample">
      <div className="PianoKeyColumn">
        {NOTES.map((note) => (
          <div
            className={
              note === "spacer"
                ? "header"
                : note.includes("#")
                ? "black"
                : "white"
            }
          >
            {note !== "spacer" ? `${note}4` : ""}
          </div>
        ))}
      </div>

      {/* Generate columns for each DAW "block" for each note */}
      {new Array(NUM_COLS).fill(0).map((_, index) => (
        <div className="BlockColumn">
          {NOTES.map((note, index) => (
            <div
              className={
                note === "spacer"
                  ? "header"
                  : index % 2 == 0
                  ? "daw-row alt"
                  : "daw-row"
              }
            ></div>
          ))}
        </div>
      ))}

      <div className="SampleNotes">
        {SAMPLES_NOTE.map((note) => (
          <div
            className="DAWNote"
            style={{
              minWidth: 112 * note.duration,
              top: NOTES.findIndex((notes) => notes == note.note) * 40,
              left: 200 + note.time * 40,
            }}
          >
            {note.note}4
          </div>
        ))}
      </div>
    </div>
  );
};

export default DAWExample;
