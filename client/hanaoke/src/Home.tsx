import React, { useState, useEffect, useRef } from 'react'
import Button from '@material-ui/core/Button';
import Grid from "@material-ui/core/Grid"
import TextField from '@material-ui/core/TextField';
import ReactHowler from 'react-howler'
import { useHistory } from "react-router-dom";
import { makeStyles, createStyles, Theme } from '@material-ui/core/styles';

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
    const [recordStatus, setRecordStatus] = useState("waiting")
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
                console.log("ためた")
                chunks.push(ele.data);
                console.log(chunks)
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
        setRecordStatus("recording")
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
        setRecordStatus("finished")
    }

    const handleSubmit = () => {
        //　音声データを送信


        //　返してもらった後の表示処理
        history.push("/result")
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
            <Button
                variant="contained"
                color="secondary"
                onClick={() => stopRecord()}
            >録音終了</Button>
        </div>
    )

    const finished = (
        <div className={classes.root}>
            <h2>録音完了！</h2>
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
                {mainContent()}
            </Grid>
        </Grid>
    )
}

export default Home