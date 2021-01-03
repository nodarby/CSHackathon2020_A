import React, { useState, useEffect, useRef } from 'react'
import Button from '@material-ui/core/Button';
import Grid from "@material-ui/core/Grid"
import TextField from '@material-ui/core/TextField';
import ReactHowler from 'react-howler'
import { makeStyles, createStyles, Theme } from '@material-ui/core/styles';
import Recording from "./Recording";

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

// props の型を定義
type Props = {
    title?: string;
};

export function Home({title}: Props) {
    const classes = useStyles();
    const [bpm, setBpm] = useState(70);
    const [mute, setMute] = useState(false);
    const [recordStatus, setRecordStatus] = useState(false)
    const [file, setFile] = useState<Array<Blob>| null>([]);
    const [audioState, setAudioState] = useState(true);
    const [soundStatus, setSoundStatus] = useState(false);
    const handleChange = (event: React.ChangeEvent<HTMLInputElement>) => {
        setBpm(Number(event.target.value))
    }
    let audioRef = useRef<MediaRecorder | null>(null);


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
            setFile(chunks);
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
        setRecordStatus(true)
        if (audioRef.current) {
            audioRef.current.start();
        }
        //　録音中の画面に遷移
        setInterval(
            ()=> {
                setSoundStatus(true)
            }, 60000/bpm)
    }

    const stopRecord = () => {
        setMute(true)
        if (audioRef.current) {
            audioRef.current.stop();
        }
        //　音声データを送信


        //　返してもらった後の表示処理

        console.log("終了")
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
            <Recording/>
            <Button
                variant="contained"
                color="secondary"
                onClick={() => stopRecord()}
            >録音終了</Button>
        </div>
    )

    return (
        <Grid container alignItems="center" justify="center">
            <Grid item xs={8}>
                <h1>{title}</h1>
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
                {recordStatus ? recording : waiting}
            </Grid>
        </Grid>
    )
}

export default Home