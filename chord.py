from calculate_note_tick import get_notes_for_chord, get_music_info
from Dictionary import note_name_to_value, note_value_to_name, mod_note_value_to_name, note_to_chord_in_C, note_to_chord_in_Am, chord_progression_in_major, chord_progression_in_minor

import random
import logging

def get_recent_note_time(recent_note, notes):
    parts = notes[recent_note].split()
    return float(parts[1].split('=')[1])

def generate_chords_progression_from_the_melody_with_each_four_quater_notes(filename,tonality='C'):

    # 得到最大小节数
    max_keys = 0.0 # 最大小节数
    notes = get_notes_for_chord(filename)
    for i in notes:
        # print(i)
        parts = i.split()
        a = float(parts[1].split('=')[1])
        b = float(parts[2].split('=')[1])
        max_keys = (a+1/b) if max_keys<(a+1/b) else max_keys
    int_max_keys = int(max_keys)

    tempo, numerator, denominator = get_music_info(filename)
    notes_in_each_key = []
    root_notes = []
    chords = []
    max_note = len(notes) # 最大四分音符时值/节拍数量
    recent_note = 0
    recent_key = 0.0

    # 得到每个整数倍四分音符时值下的音符
    for i in range(int_max_keys):
        if(recent_note < max_note-1):
            recent_note_key_time = get_recent_note_time(recent_note, notes)
            while(i+1 >= get_recent_note_time(recent_note+1, notes)):
                recent_note += 1
                if(recent_note >= max_note-1):
                    break
            if(recent_note < max_note-1):
                notes_in_each_key.append(notes[recent_note])
                # print(f"{i+1} {notes[recent_note]}")
            else:
                break
        else:
            break

    # 得到重音音符
    for i in range(0, len(notes_in_each_key), numerator):
        root_notes.append(notes_in_each_key[i])
        # print(notes_in_each_key[i])

    # 分配和弦
    # print("info:")
    i = 0
    temp_refer_notes = []
    # 先取得和弦的根音参考
    while(i < len(root_notes)):
        # print(root_notes[i])
        parts = root_notes[i].split()
        chord_root_note = mod_note_value_to_name[(note_name_to_value[str(parts[0].split('=')[1])])%12]
        # print(f"{i} {chord_root_note}")
        temp_refer_notes.append(chord_root_note)
        i += 1
    i = 0

    tonality_list = ['C','Am']
    if tonality in tonality_list:
        pass
    else:
        logging.error("调性 '%s' 不是支持的调性", tonality)
        return

    # 这里先默认 Cmaj
    if tonality == 'C':
        while(i < len(temp_refer_notes)):
            flag = True
            random_chord_try = 'I'
            chord_progression = []
            while(flag):
                random_chord_try = note_to_chord_in_C[temp_refer_notes[i]][random.randint(0, len(note_to_chord_in_C[temp_refer_notes[i]]))-1]
                if random_chord_try in ['I', 'ii', 'V', 'vi']:
                    flag = False
            if(random_chord_try == 'I'):
                chord_progression = chord_progression_in_major[random.randint(1, 3)]
            elif(random_chord_try == 'ii'):
                chord_progression = chord_progression_in_major[4]
            elif(random_chord_try == 'V'):
                chord_progression = chord_progression_in_major[5]
            elif(random_chord_try == 'vi'):
                chord_progression = chord_progression_in_major[6]
            for j in range(0, len(chord_progression)):
                chords.append(chord_progression[j])
                i += 1
    elif tonality == 'Am':
        while(i < len(temp_refer_notes)):
            flag = True
            random_chord_try = 'I'
            chord_progression = []
            while(flag):
                random_chord_try = note_to_chord_in_Am[temp_refer_notes[i]][random.randint(0, len(note_to_chord_in_Am[temp_refer_notes[i]]))-1]
                if random_chord_try in ['i', 'ii', 'III', 'ivb']:
                    flag = False
            if(random_chord_try == 'i'):
                chord_progression = chord_progression_in_minor[random.randint(1, 5)]
            elif(random_chord_try == 'ii'):
                chord_progression = chord_progression_in_minor[random.randint(6, 7)]
            elif(random_chord_try == 'III'):
                chord_progression = chord_progression_in_minor[8]
            elif(random_chord_try == 'ivb'):
                chord_progression = chord_progression_in_minor[9]
            for j in range(0, len(chord_progression)):
                chords.append(chord_progression[j])
                i += 1
    return chords

# test_chords = generate_chords_progression_from_the_melody_with_each_four_quater_notes(tonality='Am')
# for i in test_chords:
#     print(i)