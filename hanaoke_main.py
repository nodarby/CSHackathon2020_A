from scipy.io import wavfile
import pyworld as pw
import numpy as np
import matplotlib.pyplot as plt
from statistics import mode
from collections import Counter,OrderedDict
import mido
from mido import Message, MidiFile, MidiTrack, MetaMessage
import pretty_midi
from midi2audio import FluidSynth
<<<<<<< HEAD
import random 

=======
import mixing
import soundfile
#!python3.7
>>>>>>> 結合（）


class Hanaoke():
    freqlist = {0:"N", 8.175798915643707:"C0", 8.661957218027252:"C#0", 9.177023997418988:"D0", 9.722718241315029:"D#0", 10.300861153527183:"E0", 10.913382232281373:"F0", 11.562325709738575:"F#0", 12.249857374429663:"G0", 12.978271799373287:"G#0", 13.75:"A0", 14.567617547440307:"A#0", 15.433853164253883:"B0", 16.351597831287414:"C1", 17.323914436054505:"C#1", 18.354047994837977:"D1", 19.445436482630058:"D#1", 20.601722307054366:"E1", 21.826764464562746:"F1", 23.12465141947715:"F#1", 24.499714748859326:"G1", 25.956543598746574:"G#1", 27.5:"A1", 29.13523509488062:"A#1", 30.86770632850775:"B1", 32.70319566257483:"C2", 34.64782887210901:"C#2", 36.70809598967594:"D2", 38.890872965260115:"D#2", 41.20344461410875:"E2", 43.653528929125486:"F2", 46.2493028389543:"F#2", 48.999429497718666:"G2", 51.91308719749314:"G#2", 55.0:"A2", 58.27047018976124:"A#2", 61.7354126570155:"B2", 65.40639132514966:"C3", 69.29565774421802:"C#3", 73.41619197935188:"D3", 77.78174593052023:"D#3", 82.4068892282175:"E3", 87.30705785825097:"F3", 92.4986056779086:"F#3", 97.99885899543733:"G3", 103.82617439498628:"G#3", 110.0:"A3", 116.54094037952248:"A#3", 123.47082531403103:"B3", 130.8127826502993:"C4", 138.59131548843604:"C#4", 146.8323839587038:"D4", 155.56349186104046:"D#4", 164.81377845643496:"E4", 174.61411571650194:"F4", 184.9972113558172:"F#4", 195.99771799087463:"G4", 207.65234878997256:"G#4", 220.0:"A4", 233.08188075904496:"A#4", 246.94165062806206:"B4", 261.6255653005986:"C5", 277.1826309768721:"C#5", 293.6647679174076:"D5", 311.1269837220809:"D#5", 329.6275569128699:"E5", 349.2282314330039:"F5", 369.9944227116344:"F#5", 391.99543598174927:"G5", 415.3046975799451:"G#5", 440.0:"A5", 466.1637615180899:"A#5", 493.8833012561241:"B5", 523.2511306011972:"C6", 554.3652619537442:"C#6", 587.3295358348151:"D6", 622.2539674441618:"D#6", 659.2551138257398:"E6", 698.4564628660078:"F6", 739.9888454232688:"F#6", 783.9908719634985:"G6", 830.6093951598903:"G#6", 880.0:"A6", 932.3275230361799:"A#6", 987.7666025122483:"B6", 1046.5022612023945:"C7", 1108.7305239074883:"C#7", 1174.6590716696303:"D7", 1244.5079348883237:"D#7", 1318.5102276514797:"E7", 1396.9129257320155:"F7", 1479.9776908465376:"F#7", 1567.981743926997:"G7", 1661.2187903197805:"G#7", 1760.0:"A7", 1864.6550460723597:"A#7", 1975.533205024496:"B7", 2093.004522404789:"C8", 2217.4610478149766:"C#8", 2349.31814333926:"D8", 2489.0158697766474:"D#8", 2637.02045530296:"E8", 2793.825851464031:"F8", 2959.955381693075:"F#8", 3135.9634878539946:"G8", 3322.437580639561:"G#8", 3520.0:"A8", 3729.3100921447194:"A#8", 3951.066410048992:"B8", 4186.009044809578:"C9", 4434.922095629953:"C#9", 4698.63628667852:"D9", 4978.031739553295:"D#9", 5274.04091060592:"E9", 5587.651702928062:"F9", 5919.91076338615:"F#9", 6271.926975707989:"G9", 6644.875161279122:"G#9", 7040.0:"A9", 7458.620184289437:"A#9", 7902.132820097988:"B9", 8372.018089619156:"C10", 8869.844191259906:"C#10", 9397.272573357044:"D10", 9956.06347910659:"D#10", 10548.081821211836:"E10", 11175.303405856126:"F10", 11839.8215267723:"F#10", 12543.853951415975:"G10"}
    scale_list = {"Cmajor":["C","D","E","F","G","A","B"],"Gmajor":["G","A","B","C","D","E","F#"],"Dmajor":["D","E","F#","G","A","B","C#"],"Amajor":["A","B","C#","D","E","F#","G#"],"Emajor":["E","F#","G#","A","B","C#","D#"],"Bmajor":["B","C#","D#","E","F#","G#","A#"],\
    "Fmajor":["F","G","A","A#","C","D","E"],"A#major":["A#","C","D","D#","F","G","A"],"D#major":["D#","F","G","G#","A#","C","D"],"G#major":["G#","A#","C","C#","D#","F","G"],"C#major":["C#","D#","F","F#","G#","A#","C"],"Gbmajor":["F#","G#","A#","B","C#","D#","F"]}
    note_num_dic = {"C":0,"C#":1,"D":2,"D#":3,"E":4,"F":5,"F#":6,"G":7,"G#":8,"A":9,"A#":10,"B":11}
    
    
    def __init__(self, wav_file, bpm): 
        self.bpm = bpm
        self.rug = 0
        self.sampling_rate = int(50*120/bpm)
        self.wav_file = wav_file
        self.Note()
        self.ScaleJudge()
        self.CodeJudge()
        self.MakeMidi()
        #self.MidiToWav()

    def PitchAnalyze(self):
        
        # fs : sampling frequency, 音楽業界では44,100Hz
        # data : arrayの音声データが入る 
        fs, data = wavfile.read(self.wav_file)
        
        # floatでないとworldは扱えない
        data = data.astype(np.float)
        _f0, _time = pw.dio(data, fs)    # 基本周波数の抽出
        f0 = pw.stonemask(data, _f0, _time, fs)  # 基本周波数の修正
        self.f0 = f0
        return(f0)

    def getNearestValue(self,num):
        
        # リスト要素と対象値の差分を計算し最小値のインデックスを取得
        sound_freq = list(Hanaoke.freqlist.keys())
        idx = np.abs(np.asarray(sound_freq) - num).argmin()
        return sound_freq[idx]


    def NoteName(self):
        
        tune = []
        j = 1
        temp_ls = []
        note_ls = []
        f0 = self.f0

        #各データを最も周波数の近い音名に変換
        for i in range(len(f0)):
            now_freq = f0[i]
            now_notename = Hanaoke.freqlist[self.getNearestValue(now_freq)]
            temp_ls.append(now_notename)

            #SAMPLING_RATE内の最頻値を採用
            #周波数平均から求めるとポルタメント部分の影響でずれるので最頻値がよさそう
            if i == self.sampling_rate * j - 1:
                counter = Counter(temp_ls)
                note_ls.append(counter.most_common()[0][0])
                j += 1
                temp_ls = []
        
        self.note_ls = note_ls
        return note_ls

    def Note(self):
        self.PitchAnalyze()
        self.NoteName()
        return self.note_ls


    def NotoToMidi(self):
        mid = MidiFile()
        track = MidiTrack()
        mid.tracks.append(track)
        track.append(MetaMessage("set_tempo",tempo = mido.bpm2tempo(bpm)))
        time = 0
        basetime = 240
        flag = 0
        note_ls = self.note_ls
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
                temp = note_ls[note]
                note_num = self.NoteNumber(temp)
                notetime = basetime 
                flag = 1
        
        mid.save("new_song.mid")


    def ScaleJudge(self):
        note_ls = self.note_ls
        scale_list = self.scale_list
        note_ls = Counter(note_ls)
        notecount = note_ls.most_common()
        rank = {}

        for scale in scale_list:
            scale_value = scale_list[scale]
            temp = 0
            for keyname in notecount:
                #スケールに含まれる音ならカウント、そうでなければマイナス
                if keyname[0][:-1] in scale_value:
                    temp += int(keyname[1])
                elif keyname[0] != "N":
                    temp -= int(keyname[1])
            rank[scale] = temp
        self.scalerank = rank
        optimal_scale = max(rank,key = rank.get)

        self.optimal_scale = optimal_scale
        self.scale = self.scale_list[self.optimal_scale]
        self.DefineCode()


    def DefineCode(self):
        scale = self.scale
        self.code1 = [scale[0],scale[2],scale[4]]
        self.code4 =  [scale[3],scale[5],scale[0]]
        self.code5 = [scale[4],scale[6],scale[1]]

    def CodeJudge(self):
        rug = self.rug
        note_ls = self.note_ls
        scale = self.scale

        code1 = self.code1
        code4 =  self.code4
        code5 = self.code5
        
        #note4つ(2拍)をとってきて含まれている音の数でコード判定
        #1,4,5のどれか
        code_ls = []
        j = 0
        points = {"code1":0,"code4":0,"code5":0}
        for i in range(rug,len(note_ls)):
            note = note_ls[i][:-1]
            j += 1
            #ポイント決定ここから

            #通常のポイント
            if note in code1:
                points["code1"] += 2
            if note in code4:
                points["code4"] += 2
            if note in code5:
                points["code5"] += 2
            
            #小節頭の音にはボーナス
            if j == 1:
                if note in code1:
                    points["code1"] += 1
                if note in code4:
                    points["code4"] += 1
                if note in code5:
                    points["code5"] += 1

            #小節最後の音は1点
            if j == 4:
                if note in code1:
                    points["code1"] -= 1
                if note in code4:
                    points["code4"] -= 1
                if note in code5:
                    points["code5"] -= 1

            #ポイント決定ここまで


            if j == 4:
                counter = Counter(points)
                points = sorted(points.items(), key=lambda x:x[1],reverse=True)
                if points[0][1] == 0:
                    code = "N"
                else:
                    #1位同率で片方([1])がcode1のとき)
                    if points[0][1] == points[1][1] and points[0][0] == "code1":
                        #次が休符ならcode1
                        if (len(note_ls) > i+1 and note_ls[i+1] =="N")or i==3:
                            code = "code1"
                        #直前がcode1ならcode4かcode5
                        elif code == "code1":
                            code = points[1][0]
                        #直前がcode4ならcode1かcode5
                        elif code == "code4":
                            if points[1][0] == "code5":
                                code = "code5"
                            else:
                                code = "code1"
                        #直前がcode5ならcode1
                        elif code == "code5":
                            code = "code1"
                        #よくわからんかったらcode1
                        else:
                            code = "code1"

                    else:
                        code = points[0][0]                   
                code_ls.append(code)
                j = 0
               
                points = {"code1":0,"code4":0,"code5":0}

        else:       
            counter = Counter(points)
            points = sorted(points.items(), key=lambda x:x[1],reverse=True)
            if points[0][1] == 0:
                code = "N"
            else:
                code = points[0][0]  
            code_ls.append(code)
  
        self.code_ls = code_ls

    #任意の音名+オクターブ数のノートナンバーを返す
    def NoteNumber(self,notename):
        note_num = self.note_num_dic[notename[:-1]] + int(notename[-1])*12
        return note_num


    #コードの音名をノートナンバーに変換する.オクターブ数4
    def CodeNumber(self,code):
        code_num_ls = []
        for i in code:
            notename = "".join([i,"5"])
            code_num_ls.append(self.NoteNumber(notename))
        return code_num_ls



    def CodeToPiano(self):
        bpm = self.bpm
        code_ls = self.code_ls
        beat = 60/bpm

        self.code1_num = self.CodeNumber(self.code1)
        self.code4_num = self.CodeNumber(self.code4)
        self.code5_num = self.CodeNumber(self.code5)

        inst_pm_num = pretty_midi.instrument_name_to_program("Acoustic Grand Piano")
        track = pretty_midi.Instrument(program=inst_pm_num)
        
        
        now = self.rug
        #本体    
        for i in range(len(code_ls)):
            code = code_ls[i]

            #休符の時
            if code == "N":
                
                #直前にコードが存在すれば2拍ならす
                #codenumは直前のものが残る
                beforecode = code_ls[i-1]
                if beforecode in ["code1","code4","code5"]:
                    for j in range(3):
                        note = pretty_midi.Note(velocity = 100,pitch = codenum[j],start=now,end=now+beat*2)
                        track.notes.append(note)
                    now += beat*2

                #休符にする場合
                else:
                    now += beat* 2

            #コードが存在するとき
            else:
                if code == "code1":
                    codenum = self.code1_num
                elif code == "code4":
                    codenum = self.code4_num
                elif code == "code5":
                    codenum = self.code5_num
                
                #三種の音×2回
                for i in range(2):
                    for j in range(3):
                        note = pretty_midi.Note(velocity = 100,pitch = codenum[j],start=now,end=now+beat)
                        track.notes.append(note)
                    now += beat

        return track


    def CodeToBass(self):
        bpm = self.bpm
        code_ls = self.code_ls
        beat = 60/bpm


        inst_pm_num = pretty_midi.instrument_name_to_program("Electric Bass (finger)")
        track = pretty_midi.Instrument(program=inst_pm_num)
        
        now = 0
        def Octave(note):
            if note in ["C","C#","D","D#","E","F"]:
                return 3
            else:
                return 2

        root1 = self.note_num_dic[self.code1[0]] + 12*Octave(self.code1[0])
        root4 = self.note_num_dic[self.code4[0]] + 12*Octave(self.code4[0])
        root5 = self.note_num_dic[self.code5[0]] + 12*Octave(self.code5[0])   
        
        now = self.rug

        for i in range(len(code_ls)):
            code = code_ls[i]
            
            #休符の時
            if code == "N":
                
                #直前にコードが存在すれば1拍ならす
                beforecode = code_ls[i-1]
                if beforecode in ["code1","code4","code5"]:
                    note = pretty_midi.Note(velocity = 100,pitch = root, start=now, end=now+beat*2)
                    track.notes.append(note)
                    now += beat*2

                #休符にする場合
                else:
                    now += beat*2
                    
            #コードが存在するとき
            else:
                if code == "code1":
                    root = root1
                elif code == "code4":
                    root = root4
                elif code == "code5":
                    root = root5
                
                for i in range(4):
                    note = pretty_midi.Note(velocity = 100,pitch = root, start=now, end=now+beat/2)
                    track.notes.append(note)
                    now += beat/2
                   
        return track


    def CodeToCello(self):
        bpm = self.bpm
        code_ls = self.code_ls
        beat = 60/bpm


        inst_pm_num = pretty_midi.instrument_name_to_program("Cello")
        track = pretty_midi.Instrument(program=inst_pm_num)
        
        now = 0
        def Octave(note):
            if note in ["C","C#","D","D#","E","F"]:
                return 5
            else:
                return 4

        root1 = self.note_num_dic[self.code1[0]] + 12*Octave(self.code1[0])
        root4 = self.note_num_dic[self.code4[0]] + 12*Octave(self.code4[0])
        root5 = self.note_num_dic[self.code5[0]] + 12*Octave(self.code5[0])   
        
        now = self.rug

        for i in range(len(code_ls)):
            code = code_ls[i]
            
            #休符の時
            if code == "N":
                
                #直前にコードが存在すれば1拍ならす
                beforecode = code_ls[i-1]
                if beforecode in ["code1","code4","code5"]:
                    note = pretty_midi.Note(velocity = 50,pitch = root, start=now, end=now+beat*2)
                    track.notes.append(note)

                #休符にする場合
                else:
                    pass
                    
            #コードが存在するとき
            else:
                if code == "code1":
                    root = root1
                elif code == "code4":
                    root = root4
                elif code == "code5":
                    root = root5
                
               
                note = pretty_midi.Note(velocity = 50,pitch = root, start=now, end=now+beat*2)
                track.notes.append(note)
            now += beat*2
                   
        return track

        
    def CodeToStrings(self):
        bpm = self.bpm
        code_ls = self.code_ls
        beat = 60/bpm

        self.code1_num = self.CodeNumber(self.code1)
        self.code4_num = self.CodeNumber(self.code4)
        self.code5_num = self.CodeNumber(self.code5)

        inst_pm_num = pretty_midi.instrument_name_to_program("Violin")
        vntrack = pretty_midi.Instrument(program=inst_pm_num)
        inst_pm_num = pretty_midi.instrument_name_to_program("Viola")
        vlatrack = pretty_midi.Instrument(program=inst_pm_num)
        
        now = self.rug
        #本体    
        for i in range(len(code_ls)):
            code = code_ls[i]

            #休符の時
            if code == "N":
                
                #直前にコードが存在すれば2拍ならす
                #codenumは直前のものが残っているので使う
                beforecode = code_ls[i-1]
                if beforecode in ["code1","code4","code5"]:
                    numrange = [0,1,2]

                    num = random.sample(numrange,2)
                    vn_note = pretty_midi.Note(velocity = 50,pitch = vnpitch,start=now,end=now+beat*2)                
                    vlapitch = codenum[num[1]] + 12
                    if vlapitch > vnpitch:
                        vlapitch -= 12
                    vla_note = pretty_midi.Note(velocity = 50,pitch = vlapitch,start=now,end=now+beat*2)
                    vntrack.notes.append(vn_note)
                    vlatrack.notes.append(vla_note)

                #休符にする場合
                else:
                    pass

            #コードが存在するとき
            else:
                if code == "code1":
                    codenum = self.code1_num
                elif code == "code4":
                    codenum = self.code4_num
                elif code == "code5":
                    codenum = self.code5_num
                
                #3音から任意の1つを2拍
                
                #バイオリンとビオラの重複は禁止
                #バイオリンよりビオラが高かったら1オク下げる
                numrange = [0,1,2]
                num = random.sample(numrange,2)

                vnpitch = codenum[num[0]]+12
                vn_note = pretty_midi.Note(velocity = 50,pitch = vnpitch,start=now,end=now+beat*2)
                
                 
                vlapitch = codenum[num[1]] + 12
                if vlapitch > vnpitch:
                    vlapitch -= 12
                vla_note = pretty_midi.Note(velocity = 50,pitch = vlapitch,start=now,end=now+beat*2)
                vntrack.notes.append(vn_note)
                vlatrack.notes.append(vla_note)

            now += beat*2

        return [vntrack,vlatrack]



    
       
    def CodeToDrum(self):
        bpm = self.bpm
        code_ls = self.code_ls
        beat = 60/bpm


        
        track = pretty_midi.Instrument(program=35,is_drum = True)
        
        now = self.rug

        for i in range(len(code_ls)):
            code = code_ls[i]
            
            #休符の時
            if code == "N":
                
                #直前にコードが存在すればクラッシュ
                beforecode = code_ls[i-1]
                if beforecode in ["code1","code4","code5"]: 
                    note = pretty_midi.Note(velocity = 100,pitch = 49, start=now, end=now+beat/2)
                    track.notes.append(note)                   
                
                #次のコードの頭でクラッシュ
                if i+1 < len(code_ls) and code_ls[i+1] in ["code1","code4","code5"]:
                        note = pretty_midi.Note(velocity = 100,pitch = 49, start=now+beat*2, end=now+beat*2)
                        track.notes.append(note) 
                        clash_interval = 1
                
                #拍数を進める
                now += beat*2
                    
                    
            #コードが存在するとき
            else:
                
                if clash_interval == 8:
                    note = pretty_midi.Note(velocity = 100,pitch = 49, start=now+beat*2, end=now+beat*2)
                    track.notes.append(note)
                    clash_interval = 1
                else: 
                    clash_interval += 1
                note = pretty_midi.Note(velocity = 120,pitch = 35, start=now, end=now+beat/2)
                track.notes.append(note)
                note = pretty_midi.Note(velocity = 120,pitch = 38, start=now+beat, end=now+(3*beat/2))
                track.notes.append(note)
                for i in range(4):
                    note = pretty_midi.Note(velocity = 100,pitch = 42, start=now, end=now+beat)
                    track.notes.append(note)
                    now += beat/2        
        return track
    

    def MidiToWav(self):
        # fluidsynthでwavに変換
        audio_data = self.midifile.fluidsynth() 

        # wavファイル書き出し
        soundfile.write("instruments.wav", audio_data, 44100, subtype='PCM_16')

        mixing.mixing(self.wav_file, "instruments.wav")
        pass

    
    def ShowNote(self):
        return self.note_ls


    def ShowRank(self):
        return self.scalerank


    def ShowScale(self):
        return self.optimal_scale

    def ShowCode(self):
        return self.code_ls


    def MakeMidi(self):
        mid = pretty_midi.PrettyMIDI()
        mid.instruments.append(self.CodeToPiano())
        mid.instruments.append(self.CodeToBass())
        strings = self.CodeToStrings()
        mid.instruments.append(strings[0])
        mid.instruments.append(strings[1])
        mid.instruments.append(self.CodeToCello())

        
        while len(mid.instruments) < 9:
            empty_track = pretty_midi.Instrument(program=0)
            mid.instruments.append(empty_track)
        mid.instruments.append(self.CodeToDrum())


        self.instruments = mid
        mid.write('instruments.mid')
        


if __name__ == "__main__":
<<<<<<< HEAD

=======
>>>>>>> 44d89a54e506d91144ea94fab6e1ce38e59f5ebc
    wav_file = "./data/ashita_miku.wav"
    bpm = 120
    hanaoke = Hanaoke(wav_file,bpm)  
    print("completed")
