import React, {useEffect, useRef, useState} from 'react'
import Button from '@material-ui/core/Button';
import Grid from "@material-ui/core/Grid"
import TextField from '@material-ui/core/TextField';
import ReactHowler from 'react-howler'
import {useHistory} from "react-router-dom";
import ReactAudioPlayer from "react-audio-player";
import axios from 'axios'
import ToWav from 'audiobuffer-to-wav'
import {createStyles, makeStyles, Theme} from '@material-ui/core/styles';

// 付けないとCORSで弾かれる
axios.defaults.baseURL = 'http://localhost:5000';
axios.defaults.headers.post['Content-Type'] = 'application/json;charset=utf-8';
axios.defaults.headers.post['Access-Control-Allow-Origin'] = '*';

// JavaScript の場合は makeStyles(theme => styleObject)で良い
const useStyles = makeStyles((theme: Theme) =>
    createStyles({
        root: {
            padding: theme.spacing(2),
        },
        title: {
            borderBottom: `2px solid ${theme.palette.primary.main}`
        }
    })
);

export function Home() {
    const classes = useStyles();
    const history = useHistory();
    const [bpm, setBpm] = useState(70);
    const [mute, setMute] = useState(false);
    const [mute2, setMute2] = useState(false);
    const [url, setUrl] = useState("");
    const [recordStatus, setRecordStatus] = useState("waiting")
    const [file, setFile] = useState<Blob| null>(null);
    const [audioState, setAudioState] = useState(true);
    const [soundStatus, setSoundStatus] = useState(false);
    const [sound2Status, setSound2Status] = useState(false);
    const handleChange = (event: React.ChangeEvent<HTMLInputElement>) => {
        setBpm(Number(event.target.value))
    }
    let audioRef = useRef<MediaRecorder | null>(null);
    let timer1: number
    let timer2: number

    useEffect(() => {
        // マイクへのアクセス権を取得
        //audioのみtrue
        navigator.getUserMedia(
            {
                audio: true,
                video: false,
            },
            handleSuccess,
            handleError
        );
    }, []);

    const exportWAV = (audioData: any, audio_sample_rate: number) => {
        const encodeWAV = (samples: Float32Array, sampleRate: number) => {
            const buffer = new ArrayBuffer(44 + samples.length * 2);
            const view = new DataView(buffer);

            const writeString = (view: any, offset: any, str: string) => {
                for (let i = 0; i < str.length; i++) {
                    view.setUint8(offset + i, str.charCodeAt(i));
                }
            };

            const floatTo16BitPCM = (output: any, offset: any, input: any) => {
                for (let i = 0; i < input.length; i++, offset += 2) {
                    const s = Math.max(-1, Math.min(1, input[i]));
                    output.setInt16(offset, s < 0 ? s * 0x8000 : s * 0x7fff, true);
                }
            };

            writeString(view, 0, "RIFF"); // RIFFヘッダ
            view.setUint32(4, 32 + samples.length * 2, true); // これ以降のファイルサイズ
            writeString(view, 8, "WAVE"); // WAVEヘッダ
            writeString(view, 12, "fmt "); // fmtチャンク
            view.setUint32(16, 16, true); // fmtチャンクのバイト数
            view.setUint16(20, 1, true); // フォーマットID
            view.setUint16(22, 1, true); // チャンネル数
            view.setUint32(24, sampleRate, true); // サンプリングレート
            view.setUint32(28, sampleRate * 2, true); // データ速度
            view.setUint16(32, 2, true); // ブロックサイズ
            view.setUint16(34, 16, true); // サンプルあたりのビット数
            writeString(view, 36, "data"); // dataチャンク
            view.setUint32(40, samples.length * 2, true); // 波形データのバイト数
            floatTo16BitPCM(view, 44, samples); // 波形データ

            return view;
        };

        const mergeBuffers = (audioData: any) => {
            const sl = audioData.reduce((a: number, c: any) => a + c.length, 0);
            const samples = new Float32Array(sl);
            let sampleIdx = 0;
            for (let i = 0; i < audioData.length; i++) {
                for (let j = 0; j < audioData[i].length; j++) {
                    samples[sampleIdx] = audioData[i][j];
                    sampleIdx++;
                }
            }
            return samples;
        };
        const dataview = encodeWAV(mergeBuffers(audioData), audio_sample_rate);
        return new Blob([dataview], {type: "audio/wav"});
    };

    const handleSuccess = (stream: MediaStream) => {
        // レコーディングのインスタンスを作成
        audioRef.current = new MediaRecorder(stream, {
            mimeType: "video/webm;codecs=vp9",
        });
        // 音声データを貯める場所
        let chunks: Array<Blob>= [];
        // 録音が終わった後のデータをまとめる
        audioRef.current.addEventListener("dataavailable", (ele: BlobEvent) => {
            if (ele.data.size > 0) {
                chunks.push(ele.data);
            }
            // 音声データをセット
            //const hanauta = exportWAV(chunks, 44100);
            setFile(new Blob(chunks, { 'type' : 'audio/wav' }));
            setUrl(URL.createObjectURL(new Blob(chunks, { 'type' : 'audio/wav' })))

        });
        // 録音を開始したら状態を変える
        audioRef.current.addEventListener("start", () => setAudioState(false));
        // 録音がストップしたらchunkを空にして、録音状態を更新
        audioRef.current.addEventListener("stop", () => {
            setAudioState(true);
            chunks = [];
        });
    };

    const handleError = () => {
        alert("エラーです。");
    };

    const startRecord = () => {
        setRecordStatus("recording")
        if (audioRef.current) {
            audioRef.current.start();
        }
        //　録音中の画面に遷移
        setSound2Status(true)
        timer1 = window.setInterval(
            ()=> {
                setSoundStatus(true)
            }, 60000/bpm)
        timer2 = window.setInterval(
            ()=> {
                setMute(true)
                setSound2Status(true)
            }, 60000*4/bpm)
    }

    const stopRecord = () => {
        window.clearInterval(timer1)
        window.clearInterval(timer2)
        setMute(true)
        setMute2(true)
        if (audioRef.current) {
            audioRef.current.stop();
        }
        setRecordStatus("finished")
    }

    const handleSubmit = () => {
        //　音声データを送信
        if (file){
            const fd = new FormData();
            fd.append("hanauta", file);
            fd.append("bpm", bpm.toString());
            axios.post("api/v1/post_hanaoke", fd)
                .then(res => {
                    //　返してもらった後の表示処理
                    history.push("/result")
                    console.log(res)
                })
        }
    }

    const waiting = (
        <div className={classes.root}>
            <TextField
                id="standard-basic"
                label="BPM"
                value={bpm}
                type="number"
                onChange={handleChange}
                helperText="BPMを選択してください（70~200を推奨）"
            />
            <Button
                variant="contained"
                color="primary"
                onClick={() => startRecord()}
            >録音開始</Button>
        </div>
    )

    const recording = (
        <div className={classes.root}>
            <h2>録音中</h2>
            <ReactHowler
                src="bpm_sound.mp3"
                playing={soundStatus}
                loop= {true}
                onEnd={() => {
                    // 再生完了時のendイベント
                    setSoundStatus(false)
                }}
                mute={mute}
            />
            <ReactHowler
                src="Onmtp-Ding05-3.mp3"
                playing={sound2Status}
                loop= {true}
                onEnd={() => {
                    // 再生完了時のendイベント
                    setSound2Status(false)
                    if(mute2){
                        setMute(true)
                    } else {
                        setMute(false)
                    }
                }}
                mute={mute2}
            />
            <Button
                variant="contained"
                color="secondary"
                onClick={() => stopRecord()}
            >録音終了</Button>
        </div>
    )

        //ここ直す
    const finished = (
        <div className={classes.root}>
            <h2>録音完了！</h2>
            <ReactAudioPlayer src={url} controls />
            <Button
                variant="contained"
                color="primary"
                onClick={() => handleSubmit()}
                >鼻歌をオーケストラに！</Button>
        </div>
    )

    //　画面の出し分け
    const mainContent = () => {
        switch (recordStatus){
            case "waiting":
                return(waiting)
            case "recording":
                return(recording)
            case "finished":
                return(finished)
        }
    }

    return (
        <Grid container alignItems="center" justify="center">
            <Grid item xs={8}>
                <h1>ハナオケ</h1>
                {mainContent()}
            </Grid>
        </Grid>
    )
}

export default Home