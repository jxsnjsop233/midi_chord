import mido

def analyze_midi(midi_file, output_file):

    # midi_file = "melodyglm_1.mid"
    # output_file = "mido_info.txt"

    with open(output_file, 'w', encoding='utf-8') as f:
        mid = mido.MidiFile(midi_file)
        for i, track in enumerate(mid.tracks):
            f.write('Track {}: {}\n'.format(i, track.name))
            for msg in track:
                f.write(str(msg) + '\n')