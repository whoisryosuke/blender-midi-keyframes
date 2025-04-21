import React, { useRef } from "react";
import "./DAWExample.css";
import { motion } from "motion/react";

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
  const containerRef = useRef(null);
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

      <motion.div
        className="SampleNotes"
        initial={{ opacity: 0 }}
        whileInView={{ opacity: 1 }}
        transition={{}}
      >
        {SAMPLES_NOTE.map((note, index) => (
          <motion.div
            className="DAWNote"
            style={{
              minWidth: 112 * note.duration,
              // top: NOTES.findIndex((notes) => notes == note.note) * 40,
              // left: 200 + note.time * 40,
            }}
            initial={{
              opacity: 0,
              y: NOTES.findIndex((notes) => notes == note.note) * 40,
              x: 0,
            }}
            animate={{
              opacity: [0, 1],
              x: [200 + note.time * 40 - 50, 200 + note.time * 40],
            }}
            // viewport={{ once: true, amount: 1, root: containerRef }}
            transition={{
              duration: 1.5,
              delay: index * 0.1,
            }}
          >
            {note.note}4
          </motion.div>
        ))}
      </motion.div>
    </div>
  );
};

export default DAWExample;
