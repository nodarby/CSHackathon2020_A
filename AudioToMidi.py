from scipy.io import wavfile
import pyworld as pw
import numpy as np
import matplotlib.pyplot as plt
from statistics import mode
from collections import Counter
import mido
from mido import Message, MidiFile, MidiTrack, MetaMessage
from collections import OrderedDict
#!python3.7

wav_file = "./data/sample_yorukake.wav"

freqlist = {0:"N", 8.175798915643707:"C0", 8.661957218027252:"C#0", 9.177023997418988:"D0", 9.722718241315029:"D#0", 10.300861153527183:"E0", 10.913382232281373:"F0", 11.562325709738575:"F#0", 12.249857374429663:"G0", 12.978271799373287:"G#0", 13.75:"A0", 14.567617547440307:"A#0", 15.433853164253883:"B0", 16.351597831287414:"C1", 17.323914436054505:"C#1", 18.354047994837977:"D1", 19.445436482630058:"D#1", 20.601722307054366:"E1", 21.826764464562746:"F1", 23.12465141947715:"F#1", 24.499714748859326:"G1", 25.956543598746574:"G#1", 27.5:"A1", 29.13523509488062:"A#1", 30.86770632850775:"B1", 32.70319566257483:"C2", 34.64782887210901:"C#2", 36.70809598967594:"D2", 38.890872965260115:"D#2", 41.20344461410875:"E2", 43.653528929125486:"F2", 46.2493028389543:"F#2", 48.999429497718666:"G2", 51.91308719749314:"G#2", 55.0:"A2", 58.27047018976124:"A#2", 61.7354126570155:"B2", 65.40639132514966:"C3", 69.29565774421802:"C#3", 73.41619197935188:"D3", 77.78174593052023:"D#3", 82.4068892282175:"E3", 87.30705785825097:"F3", 92.4986056779086:"F#3", 97.99885899543733:"G3", 103.82617439498628:"G#3", 110.0:"A3", 116.54094037952248:"A#3", 123.47082531403103:"B3", 130.8127826502993:"C4", 138.59131548843604:"C#4", 146.8323839587038:"D4", 155.56349186104046:"D#4", 164.81377845643496:"E4", 174.61411571650194:"F4", 184.9972113558172:"F#4", 195.99771799087463:"G4", 207.65234878997256:"G#4", 220.0:"A4", 233.08188075904496:"A#4", 246.94165062806206:"B4", 261.6255653005986:"C5", 277.1826309768721:"C#5", 293.6647679174076:"D5", 311.1269837220809:"D#5", 329.6275569128699:"E5", 349.2282314330039:"F5", 369.9944227116344:"F#5", 391.99543598174927:"G5", 415.3046975799451:"G#5", 440.0:"A5", 466.1637615180899:"A#5", 493.8833012561241:"B5", 523.2511306011972:"C6", 554.3652619537442:"C#6", 587.3295358348151:"D6", 622.2539674441618:"D#6", 659.2551138257398:"E6", 698.4564628660078:"F6", 739.9888454232688:"F#6", 783.9908719634985:"G6", 830.6093951598903:"G#6", 880.0:"A6", 932.3275230361799:"A#6", 987.7666025122483:"B6", 1046.5022612023945:"C7", 1108.7305239074883:"C#7", 1174.6590716696303:"D7", 1244.5079348883237:"D#7", 1318.5102276514797:"E7", 1396.9129257320155:"F7", 1479.9776908465376:"F#7", 1567.981743926997:"G7", 1661.2187903197805:"G#7", 1760.0:"A7", 1864.6550460723597:"A#7", 1975.533205024496:"B7", 2093.004522404789:"C8", 2217.4610478149766:"C#8", 2349.31814333926:"D8", 2489.0158697766474:"D#8", 2637.02045530296:"E8", 2793.825851464031:"F8", 2959.955381693075:"F#8", 3135.9634878539946:"G8", 3322.437580639561:"G#8", 3520.0:"A8", 3729.3100921447194:"A#8", 3951.066410048992:"B8", 4186.009044809578:"C9", 4434.922095629953:"C#9", 4698.63628667852:"D9", 4978.031739553295:"D#9", 5274.04091060592:"E9", 5587.651702928062:"F9", 5919.91076338615:"F#9", 6271.926975707989:"G9", 6644.875161279122:"G#9", 7040.0:"A9", 7458.620184289437:"A#9", 7902.132820097988:"B9", 8372.018089619156:"C10", 8869.844191259906:"C#10", 9397.272573357044:"D10", 9956.06347910659:"D#10", 10548.081821211836:"E10", 11175.303405856126:"F10", 11839.8215267723:"F#10", 12543.853951415975:"G10"}
bpm = 130
SAMPLING_RATE = int(50*120/bpm)


def PitchAnalyze(wav_file):
    # fs : sampling frequency, 音楽業界では44,100Hz
    # data : arrayの音声データが入る 
    fs, data = wavfile.read(wav_file)

    # floatでないとworldは扱えない
    data = data.astype(np.float)

    _f0, _time = pw.dio(data, fs)    # 基本周波数の抽出
    f0 = pw.stonemask(data, _f0, _time, fs)  # 基本周波数の修正

    return(f0)

def getNearestValue(num):
    
    # リスト要素と対象値の差分を計算し最小値のインデックスを取得
    sound_freq = list(freqlist.keys())
    idx = np.abs(np.asarray(sound_freq) - num).argmin()
    return sound_freq[idx]


def NoteName(f0):
    tune = []
    j = 1
    temp_ls = []
    note_ls = []
    #各データを最も周波数の近い音名に変換
    for i in range(len(f0)):
        now_freq = f0[i]
        now_notename = freqlist[getNearestValue(now_freq)]
        temp_ls.append(now_notename)

        #SAMPLING_RATE内の最頻値を採用
        #周波数平均から求めるとポルタメント部分の影響でずれるので最頻値がよさそう
        if i == SAMPLING_RATE * j:
            counter = Counter(temp_ls)
            note_ls.append(counter.most_common()[0][0])
            j += 1
            temp_ls = []
    
    return note_ls

def Note(wav_file):
    note_ls = NoteName(PitchAnalyze(wav_file))
    print(note_ls)
    return note_ls


def NotoToMidi(note_ls,bpm):
    mid = MidiFile()
    track = MidiTrack()
    mid.tracks.append(track)
    track.append(MetaMessage("set_tempo",tempo = mido.bpm2tempo(bpm)))
    time = 0
    basetime = 240
    flag = 0
    for note in range(len(note_ls)):
        #休符の場合
        if note_ls[note] == "N":
            if flag == 1:
                #前のノートを入力
                track.append(Message("note_on", note = note_num, velocity=127, time = 0))
                track.append(Message("note_off", note = note_num,time = notetime))

            track.append(Message("note_off", note = 1,time = basetime))
            flag = 0

        #前のノートと同じなら繋げる
        elif note != 0 and note_ls[note] == note_ls[note - 1]:
            notetime += basetime
        
        else:
            #前のノートを止める
            if flag == 1:
                track.append(Message("note_on", note = note_num, velocity=127, time = 0))
                track.append(Message("note_off", note = note_num,time = notetime))

            #現在のmidiのノートナンバーを求める
            note_num_dic = {"C":0,"C#":1,"D":2,"D#":3,"E":4,"F":5,"F#":6,"G":7,"G#":8,"A":9,"A#":10,"B":11}
            temp = note_ls[note]
            note_num = note_num_dic[temp[:-1]] + int(temp[-1])*12
            notetime = basetime 
            flag = 1
    


    mid.save("new_song.mid")

def AudioToMidi(wav_file):
    NotoToMidi(Note(wav_file),120)

if __name__ == "__main__":
    AudioToMidi(wav_file)