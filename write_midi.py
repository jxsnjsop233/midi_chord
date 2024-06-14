from mido import Message, MidiFile, MidiTrack, MetaMessage
import mido

from Dictionary import chord_in_C, chord_in_Am, mod_note_name_to_value, note_name_to_value

class CurrentTime:
    totalTime = 0

    def TimeAdd(addedTime=0):
        CurrentTime.totalTime += addedTime
        return CurrentTime.totalTime

def chord_invert_to_notes(chord='I', tonality='C', pitch_level=5): # 将和弦名转化为特定阶数下和弦音符的note_value值的list返回
    chord_note_value_min = pitch_level*12-6
    chord_note_value_max = (pitch_level+1)*12+6
    chord_note_name = []
    chord_note_value = []
    fixed_chord_note_value = [] # 修正后带有转位音符的和弦list

    # 调性
    if tonality == 'C':
        chord_note_name = chord_in_C[chord]
    if tonality == 'Am':
        chord_note_name = chord_in_Am[chord]

    for note_name in chord_note_name:
        note_value = mod_note_name_to_value[note_name] + 12*pitch_level
        chord_note_value.append(note_value)

    # 添加转位
    if len(chord_note_value) == 3:
        if chord_note_value[2] - 12 > chord_note_value_min:
            fixed_chord_note_value.append(chord_note_value[1] - 12)
        elif chord_note_value[2] - 12 < chord_note_value_min:
            fixed_chord_note_value.append(chord_note_value[2] - 12)
        for i in chord_note_value:
            fixed_chord_note_value.append(i)
        if chord_note_value[1] + 12 < chord_note_value_max:
            fixed_chord_note_value.append(chord_note_value[1] + 12)
        elif chord_note_value[0] + 12 < chord_note_value_max:
            fixed_chord_note_value.append(chord_note_value[0] + 12)
    else: 
        fixed_chord_note_value = chord_note_value
        fixed_chord_note_value[2] -= 12

    # 如果修正后有五个以上音符，删除第三个音符直至只剩下四个
    while len(fixed_chord_note_value) >= 5:
        del fixed_chord_note_value[2]

    if fixed_chord_note_value[2]-fixed_chord_note_value[1] == 1 or fixed_chord_note_value[2]-fixed_chord_note_value[1] == 2:
        fixed_chord_note_value[2] -= 12
        
    return fixed_chord_note_value
        

def init_midi(track, tempo=500000, numerator=4, denominator=4, key='C'):
    
    meta_time_signature = MetaMessage('time_signature', numerator=numerator, denominator=denominator)
    meta_tempo = MetaMessage('set_tempo', tempo = int(tempo), time=0)
    meta_tone = MetaMessage('key_signature', key=key)
    track.append(meta_time_signature)
    track.append(meta_tempo)
    track.append(meta_tone)

def play_note(note_name, start_tick, end_tick, track, velocity=100, delay=0, channel=0):
    length = end_tick - start_tick
    meta_time = 96
    track.append(Message('note_on', note=note_name_to_value[note_name], velocity=velocity, time=(round(delay) if round(delay) > 0 else 0), channel=channel))
    track.append(Message('note_off', note=note_name_to_value[note_name], velocity=velocity, time=(round(length) if round(length) > 0 else 0), channel=channel))

from mido import Message

def play_chord(chord_notes_value, track, files,keys=1.0, velocity=50, delay=0, channel=0, numerator=4, tempo=500000):
    meta_time = 96
    key_time = int(numerator * 480 * keys)  # keys 是和弦持续的小节数
    real_time = int(numerator * tempo/1000 * keys)
    chord_notes_value = sorted(chord_notes_value)
    
    for i in chord_notes_value:
        velocity += 10
        track.append(Message('note_on', note=i, velocity=velocity, time=0, channel=channel))
    total_key_time = key_time
    total_real_time = real_time
    
    
    for i in range(4):
        if i < len(chord_notes_value):
            track.append(Message('note_off', note=chord_notes_value[i], velocity=velocity, time=(total_key_time if total_key_time > 0 else 0), channel=channel))
            files[i].write(f"note={chord_notes_value[i]} time={CurrentTime.TimeAdd(total_real_time)}\n")
            total_key_time -= total_key_time
            total_real_time -= total_real_time


def write_midi(output_midi_file, rewrited_melody_notes, chords_notes_value, tracks_files, tempo=500000):
    mid = MidiFile()
    track_melody = MidiTrack()
    mid.tracks.append(track_melody)
    track_chord = MidiTrack()
    mid.tracks.append(track_chord)
    meta_time = 96.0

    init_midi(track_melody,tempo=tempo)

    chord_ticks = 0
    last_note = ['C5', 0, 0]
    for note in rewrited_melody_notes: # note 格式为 [音符, 起始tick, 终止tick]
        play_note(note[0], note[1], note[2], track_melody, channel=0, delay=note[1]-last_note[2])
        last_note = note

    # track_chord.append(Message('program_change',channel=0,program=33,time=0))
    for chord_notes_value in chords_notes_value:
        chord_ticks += 4 * 480
        play_chord(chord_notes_value, track_chord, files=tracks_files, keys=1.0, channel=1, numerator=4, tempo=tempo)

    mid.save(output_midi_file)

    print(f"midi has been saved to {output_midi_file} successfully")