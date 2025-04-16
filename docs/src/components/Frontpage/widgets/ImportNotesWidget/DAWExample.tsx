import React from "react";
import "./DAWExample.css";

const SAMPLES_NOTE = [
  {
    note: "C",
    time: 0.5,
  },
  {
    note: "D",
    time: 0.5,
  },
  {
    note: "C",
    time: 1,
  },
  {
    note: "C",
    time: 1.5,
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
const NUM_COLS = 8;

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
    </div>
  );
};

export default DAWExample;
