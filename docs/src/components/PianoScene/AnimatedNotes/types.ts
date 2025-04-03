export type WhiteNotes = "C" | "D" | "E" | "F" | "G" | "A" | "B";
export type BlackNotes = "C#" | "D#" | "F#" | "G#" | "A#";
export type BaseNote = WhiteNotes | BlackNotes;
export type Octaves = "1" | "2" | "3" | "4" | "5" | "6" | "7";
export type Note = `${BaseNote}${Octaves}`;

// MIDI TYPES

// This is technically "family" - and the instrument has a "name"
// e.g. family = guitar, name = Acoustic Guitar
// Later might be interesting to save name to see if we can match to more exact sample
export type Instruments =
  | "pipe"
  | "reed"
  | "organ"
  | "guitar"
  | "ensemble"
  | "strings"
  | "drums"
  | "strings";

export type RhythmNote = {
  note: Note;
  time: number;
  duration: number;
  velocity: number;
};

export type MIDITrack = {
  instrument: Instruments;
  notes: RhythmNote[];
};

export type MIDIFile = {
  name: string;
  bpm: number; // Assume constant now - but ideally allow for an array for changes mid-song
  duration: number;
  tracks: MIDITrack[];
};
