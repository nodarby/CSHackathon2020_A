from pydub import AudioSegment

def mixing(sound1,sound2):
    sound1 = AudioSegment.from_file(sound1)
    sound2 = AudioSegment.from_file(sound2)

    output = sound1.overlay(sound2, position=0)

    # save the result
    output.export("mixed_sounds.wav", format="wav")


if __name__ == "__main__":
    
    wav_file = "./data/ashita_miku.wav"
    mixing(wav_file,"instruments.wav")
    print("completed")