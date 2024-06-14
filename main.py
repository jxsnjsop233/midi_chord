import os

from analyze_midi import analyze_midi
from write_midi import write_midi, chord_invert_to_notes
from chord import generate_chords_progression_from_the_melody_with_each_four_quater_notes
from calculate_note_tick import get_music_info, rewrite_melody_notes

emotion = 'sad' 

folder_midi_lib_path = os.path.join('midi_lib', emotion)
folder_output_midi_info_path = os.path.join('output_midi', 'info')
folder_output_midi_music_path = os.path.join('output_midi', 'music')
folder_output_notes_four_notes = os.path.join('output_notes_four_channels')

midi_file_name = "theme.mid"

analyze_midi(midi_file=f'{folder_midi_lib_path}/{midi_file_name}', output_file=f'{folder_output_midi_info_path}/{midi_file_name}_mido_info.txt')

# 取得 BPM 拍号 等音乐信息
file_name = f'{folder_output_midi_info_path}/{midi_file_name}_mido_info.txt'
tempo, numerator, denominator = get_music_info(file_name)

if emotion == 'sad' : tonality = 'Am' 
else : tonality = 'C'  # 'C' or 'Am'

chords_names = generate_chords_progression_from_the_melody_with_each_four_quater_notes(file_name,tonality=tonality)
chords_notes_value = []
for i in chords_names:
    chords_notes_value.append(chord_invert_to_notes(chord=i,tonality=tonality,pitch_level=4))

rewrited_melody_notes = rewrite_melody_notes(file_name)

output_midi_file = f'{folder_output_midi_music_path}/absolute_{midi_file_name}'

# 打开四个文件用于输出硬件编码
files = [open(f'{folder_output_notes_four_notes}/{midi_file_name}_output_{i}.txt', 'w') for i in range(4)]

write_midi(output_midi_file, rewrited_melody_notes, chords_notes_value, files, tempo=tempo)

for f in files:
    f.close()