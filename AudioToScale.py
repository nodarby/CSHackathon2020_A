import AudioToMidi 
from collections import Counter

wav_file = "./data/sample_yorukake.wav"

def ScaleJudge(note_ls):
    scale_list = {"Cmajor":["C","D","E","F","G","A","B"],"Gmajor":["C","D","E","F#","G","A","B"],"Dmajor":["C#","D","E","F#","G","A","B"],"Amajor":["C#","D","E","F#","G#","A","B"],"Emajor":["C#","D#","E","F#","G#","A","B"],"Bmajor":["C#","D#","E","F#","G#","A#","B"],"Bmajor":["C#","D#","F","F#","G#","A#","B"],"C#major":["C#","D#","F","F#","G#","A#","C"],\
                "Fmajor":["C","D","E","F","G","A","A#"],"Bbmajor":["C","D","D#","F","G","A","A#"],"Ebmajor":["C","D","D#","F","G","G#","A#"],"Abmajor":["C","C#","D#","F","G","G#","A#"],"Dbmajor":["C","C#","D#","F","F#","G#","A#"],"Gbmajor":["B","C#","D#","F","F#","G#","A#"],"Gbmajor":["B","C#","D#","E","F#","G#","A#"],}
    note_ls = Counter(note_ls)
    notecount = note_ls.most_common()
    rank = {}
    for scale in scale_list:
        scale_value = scale_list[scale]
        temp = 0
        for keyname in notecount:
            if keyname[0][:-1] in scale_value:
                temp += int(keyname[1])
        rank[scale] = temp
    optimal_scale = max(rank,key = rank.get)
    return optimal_scale


def AudioToScale(wav_file):
    return ScaleJudge(AudioToMidi.Note(wav_file))

if __name__ == "__main__":
    print(AudioToScale(wav_file))