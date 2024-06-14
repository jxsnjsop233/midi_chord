from Dictionary import note_value_to_name, note_name_to_value, channel_value_to_name

def parse_midi_text(filename):
    notes = []
    notes_bool_list = [False] * 128
    notes_start_tick_list = [0] * 128
    with open(filename, 'r') as file:
        current_tick = 0
        for line in file:
            if 'note_on' in line or 'note_off' in line:
                parts = line.split()
                pitch_info = parts[2]
                pitch = int(pitch_info.split('=')[1])
                velocity_info = parts[3]
                velocity = int(velocity_info.split('=')[1])
                time_info = parts[4]
                tick = int(time_info.split('=')[1])
                current_tick += tick
                if velocity > 0 and 'note_on' in line:
                    notes_bool_list[pitch] = True
                    notes_start_tick_list[pitch] = current_tick
                else:
                    notes_bool_list[pitch] = False
                    notes.append((pitch, notes_start_tick_list[pitch], current_tick))

            # if 'note_on' in line or 'note_off' in line:
            #     parts = line.split()
            #     time_info = parts[4]
            #     tick = int(time_info.split('=')[1])
            #     if tick > 0:
            #         pitch_info = parts[2]
            #         pitch = int(pitch_info.split('=')[1])
            #         notes.append((pitch, current_tick, current_tick + tick))
            #     current_tick += tick

    return notes
    


def search_meta_info(filename):
    channel_value = 0
    tempo = 500000
    numerator = 4
    denominator = 4
    with open(filename, 'r') as file:
        for line in file:
            if 'tempo' in line:
                parts = line.split()
                tempo_str = parts[1].split('=')[1]
                tempo = int(tempo_str.split(',')[0])
            if 'numerator' in line:
                parts = line.split()
                numerator_str = parts[1].split('=')[1]
                numerator = int(numerator_str.split(',')[0])
            if 'denominator' in line:
                parts = line.split()
                denominator_str = parts[2].split('=')[1]
                denominator = int(denominator_str.split(',')[0])
    return tempo, numerator, denominator

def note_duration(tick_a, tick_b):
    # 辗转相除法求最大公约数
    def gcd(x, y):
        while y:
            x, y = y, x % y
        return x

    gcd_value = gcd(tick_a, tick_b)
    tick_a /= gcd_value
    tick_b /= gcd_value
    return "{}/{} 小节, {}分音符".format(int(tick_a), int(tick_b), (4.0*float(tick_b))/float(tick_a))

# print(f"乐器 = {channel_value_to_name[channel_value]}")
def get_music_info(filename): # 返回值: tempo, numerator, denominator
    return search_meta_info(filename)

def get_notes_for_chord(filename):
    meta_time = 96.0
    notes = parse_midi_text(filename)
    notes_for_chord = []
    for i, (pitch, start_tick, end_tick) in enumerate(notes, start=1):
        notes_for_chord.append(f"pitch={note_value_to_name[pitch]} note_time={1+start_tick/meta_time} note_time_name={4.0*meta_time/float(end_tick-start_tick)}")
        # print(f"音符 {i}: 音调 = {note_value_to_name[pitch]} 起始 tick = {start_tick}, 结束 tick = {end_tick}, 小节 = {1 + start_tick/480}, 时值 = {note_duration(end_tick-start_tick, 480)}")
    return notes_for_chord

# 提取旋律的 音符 起始tick 结束tick 并重新格式化输出  
def rewrite_melody_notes(filename):
    notes = parse_midi_text(filename)
    notes_for_chord = []
    for i, (pitch, start_tick, end_tick) in enumerate(notes, start=1):
        notes_for_chord.append([note_value_to_name[pitch], start_tick/96*480, end_tick/96*480])
    return notes_for_chord

# notes_ = rewrite_melody_notes()
# get_music_info()

# for i in notes_:
#     print(i)