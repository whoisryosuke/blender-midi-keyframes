import React, { useEffect, useRef, useState } from "react";
import "./AnimatedNotes.css";
import DAWNotes from "./DAWNotes";
import { Midi } from "@tonejs/midi";
import { Instruments, MIDIFile, MIDITrack, Note, RhythmNote } from "./types";
import { useMIDIAnimationStore } from "@site/src/store/midi-animation";

type Props = {};

const AnimatedNotes = (props: Props) => {
  const [localTime, setLocalTime] = useState(0);
  const { addMidiFile } = useMIDIAnimationStore();
  const animationRef = useRef(null);

  // Load MIDI data and transfer to components
  const loadMidiFile = async () => {
    // load a midi file in the browser
    const midi = await Midi.fromUrl(
      "music/mozart-sonata-16-scales-snippet.mid"
    );
    if (!midi) return;

    const newMidiFile: MIDIFile = {
      name: midi.name,
      bpm: midi.header.tempos[0]?.bpm ?? 0,
      tracks: [],
    };

    // Process all tracks on MIDI file (track = separate instrument)
    midi.tracks.forEach((track) => {
      // No notes on an instrument? Don't save it
      if (track.notes.length == 0) return;

      // Create the new track
      const newTrack: MIDITrack = {
        instrument: track.instrument.family as Instruments,
        notes: [],
      };

      // Save notes on track
      track.notes.forEach((note) => {
        // console.log("note", note.midi, note.time, note.duration, note.name);
        const newNote: RhythmNote = {
          note: note.name as Note,
          time: note.time,
          duration: note.duration,
          velocity: note.velocity,
        };
        newTrack.notes.push(newNote);
      });

      newMidiFile.tracks.push(newTrack);
    });

    addMidiFile(newMidiFile);

    console.log("midi file", newMidiFile);
  };

  useEffect(() => {
    // Load MIDI file on initial load
    loadMidiFile();
  }, []);

  const syncTime = () => {
    const { currentAnimation } = useMIDIAnimationStore.getState();

    if (currentAnimation) {
      setLocalTime(currentAnimation.time);
    }
    animationRef.current = requestAnimationFrame(syncTime);
  };

  // Sync time
  useEffect(() => {
    animationRef.current = requestAnimationFrame(syncTime);

    return () => {
      cancelAnimationFrame(animationRef.current);
    };
  }, []);

  return (
    <div className="AnimatedNotesContainer">
      <DAWNotes time={localTime} />
      <div>{localTime}</div>
    </div>
  );
};

export default AnimatedNotes;
