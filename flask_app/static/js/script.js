const pianoKeys = document.querySelectorAll('.piano-keys .key');

keysCheckbox = document.querySelector('.keys-checkbox input');
// Convert the NodeList to an Array for easier manipulation
const pianoKeysArray = Array.from(pianoKeys);


// Select the oscillator type dropdown and initialize the current oscillator type
const oscillatorTypeSelect = document.getElementById('oscillator-type');
let currentOscillatorType = 'sine';

// Initialize a Map to keep track of active notes and an array to store available synthesizers
const activeNotes = new Map();
const availableSynths = [];

// Setting the maximum number of simultaneous notes to 8
let maxPolyphony = 8;

// Define the mapping of notes to their corresponding frequencies
const notes = {
    'q': -9,
    '2': -8,
    'w': -7,
    '3': -6,
    'e': -5,
    'r': -4,
    '5': -3,
    't': -2,
    '6': -1,
    'y': 0,
    '7': 1,
    'u': 2,
    'c': 3,
    'f': 4,
    'v': 5,
    'g': 6,
    'b': 7,
    'n': 8,
    'j': 9,
    'm': 10,
    'k': 11,
    ',': 12,
    'l': 13,
    '.': 14,
    '/': 15
};

// Function to create a new synthesizer and add it to the availableSynths array
function createSynth() {
    const synth = new Tone.Synth().toDestination();
    // Get the volume slider element
    const volumeSlider = document.getElementById('volume-slider');
    // Set the initial volume of the synth based on the value of the volume slider
    synth.volume.value = Tone.gainToDb(volumeSlider.value);

    availableSynths.push(synth);
}
// Function to get the next available synthesizer from the availableSynths array
function getNextAvailableSynth() {
    if (availableSynths.length === 0) {
        createSynth();
    }
    return availableSynths.pop();
}

// Function to play a sound when a valid note is pressed
function playSound(note) {
    // Check if the note is a valid key in the 'notes' object
    const validNotes = Object.keys(notes);
    if (!validNotes.includes(note)) {
        // If the note is not a valid key in the 'notes' object, does nothing
        return;
    }
    // If the note is not already playing, trigger its attack using a synthesizer
    if (!activeNotes.has(note)) {
        const synth = getNextAvailableSynth();
        const frequency = getFrequency(note);
        synth.set({
            oscillator: {
                type: currentOscillatorType
            }
        }).triggerAttack(frequency);
        activeNotes.set(note, synth);
    }
    // Find the corresponding piano key in the DOM and add the 'active' class
    const clicked = pianoKeysArray.find(key => key.getAttribute('data-note') === note);
    if (clicked) {
        clicked.classList.add('active'); //Add the 'active' class to the piano key, making it visually active
    }
}
// Function to stop playing a sound when a note is released
function stopSound(note) {
    // Check if the note is currently active (being played)
    if (activeNotes.has(note)) {
        const synth = activeNotes.get(note);
        synth.triggerRelease(); // Release the note on the synthesizer to stop the sound
        activeNotes.delete(note); // Remove the note from the activeNotes map
        availableSynths.push(synth); // Add the synthesizer back to the availableSynths array for reuse
    }
    // Find the corresponding piano key in the DOM and remove the 'active' class
    const clicked = pianoKeysArray.find(key => key.getAttribute('data-note') === note);
    if (clicked) {
        clicked.classList.remove('active'); // Remove the 'active' class from the piano key, making it visually inactive
    }
}

// Function to calculate the frequency of a given note
function getFrequency(note) {
    const A3Frequency = 220;
    return A3Frequency * Math.pow(2, notes[note] / 12);
}

// Helper function to check if the pressed key corresponds to a valid note
function isValidNoteKey(key) {
    const validNoteKeys = Object.keys(getFrequency());
    return validNoteKeys.includes(key);
}
// Add event listeners to each piano key to handle mouse interactions
// Loop through each piano key and add event listeners to handle mouse interactions
pianoKeys.forEach(key => {
    key.addEventListener('mousedown', () => {
        const note = key.getAttribute('data-note');
        if (!Tone.context.state.startsWith('running')) {
            // Start audio context when user interacts with the piano keys
            // This is necessary to ensure audio playback works as browsers often require user interaction to start audio
            Tone.context.resume().then(() => {
                createSynth(); // Create a new synthesizer if one is not available
                playSound(note); // Play the note using the synthesizer
            });
        } else {
             // If the audio context is already running, play the note directly without resuming the context
            playSound(note);
        }
    });
    // When the mouse is released (mouse up event) from the piano key, get its associated note and stop playing the sound
    key.addEventListener('mouseup', () => {
        const note = key.getAttribute('data-note');
        stopSound(note);
    });

    // When the mouse leaves the area of the piano key (mouse leave event), get its associated note
    // and if the note is currently active (playing), stop playing the sound
    key.addEventListener('mouseleave', () => {
        const note = key.getAttribute('data-note');
        if (activeNotes.has(note)) {
            stopSound(note);
        }
    });
});
// Add an event listener to the oscillator type dropdown to change the current oscillator type
oscillatorTypeSelect.addEventListener('change', event => {
    currentOscillatorType = event.target.value;
});

// Get the valid note keys for use in the pressedKey event handler
const validNoteKeys = Object.keys(getFrequency());

// Function to handle keyboard interactions when a key is pressed down
const pressedKey = (e) => {
    if (e.target.tagName.toLowerCase() !== 'input' && e.target.tagName.toLowerCase() !== 'select') {
        const note = e.key;
        if (!Tone.context.state.startsWith('running')) {
            // Start audio context when user interacts with the piano keys
            Tone.context.resume().then(() => {
                createSynth();
                playSound(note);
            });
        } else {
            if (!activeNotes.has(note) && activeNotes.size < maxPolyphony) {
                playSound(note);
            }
        }
    }
}

// Add event listeners for keyboard interactions
document.addEventListener('keydown', pressedKey);
document.addEventListener('keyup', (e) => {
    const note = e.key;
    stopSound(note);
});

// Function to start the audio context when the user interacts with the piano keys or clicks the "Start Audio" button
function startAudioContext() {
    // Start audio context when the user interacts with the piano keys or clicks the "Start Audio" button
    Tone.start();
}

const showHideKeys = () =>{
    pianoKeys.forEach(key => key.classList.toggle("hide"));
}

// Add an event listener for the "Start Audio" button click to start the audio context
document.getElementById('start-audio').addEventListener('click', () => {
    // Start audio context when user clicks the "Start Audio" button
    startAudioContext();
});


keysCheckbox.addEventListener('click',showHideKeys);

//add an event listener to the volume slider to update the volume of the synthesizer when the slider value changes
const volumeSlider = document.getElementById('volume-slider');

volumeSlider.addEventListener('input', () => {
    const volumeValue = parseFloat(volumeSlider.value);
    // Check if the volume value is valid (between 0 and 1)
    if (!isNaN(volumeValue) && volumeValue >= 0 && volumeValue <= 1) {
        // Set the volume of all available synths
        availableSynths.forEach(synth => {
            synth.volume.value = Tone.gainToDb(volumeValue); // Convert linear gain to dB
        });
    }
});