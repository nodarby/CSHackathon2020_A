import React, {useEffect, useRef, useState} from 'react'
import Button from '@material-ui/core/Button';
import Grid from "@material-ui/core/Grid"
import TextField from '@material-ui/core/TextField';
import MenuItem from '@material-ui/core/MenuItem';
import ReactHowler from 'react-howler'
import {useHistory} from "react-router-dom";
import ReactAudioPlayer from "react-audio-player";
import axios from 'axios'
import Recorder from 'recorderjs'
import MyRecorder from "./MyRecorder";
import {createStyles, makeStyles, Theme} from '@material-ui/core/styles';

// 付けないとCORSで弾かれる
axios.defaults.baseURL = 'http://localhost:5000';
axios.defaults.headers.post['Content-Type'] = 'application/json;charset=utf-8';
axios.defaults.headers.post['Access-Control-Allow-Origin'] = '*';

// JavaScript の場合は makeStyles(theme => styleObject)で良い
const useStyles = makeStyles((theme) =>
    createStyles({
        root: {
            padding: theme.spacing(2),
        },
        title: {
            borderBottom: `2px solid ${theme.palette.primary.main}`
        }
    })
);

let recorder

const currencies = [
    {
        value: 60,
        label: '60',
    },
    {
        value: 75,
        label: '75',
    },
    {
        value: 80,
        label: '80',
    },
    {
        value: 100,
        label: '100',
    },
    {
        value: 120,
        label: '120',
    },
    {
        value: 125,
        label: '125',
    },
    {
        value: 150,
        label: '150',
    },
    {
        value: 200,
        label: '200',
    },
];

export function Home() {
    const classes = useStyles();
    const history = useHistory();
    const [bpm, setBpm] = useState(70);
    const [mute, setMute] = useState(false);
    const [mute2, setMute2] = useState(false);
    const [url, setUrl] = useState("");
    const [recordStatus, setRecordStatus] = useState("waiting")
    const [file, setFile] = useState(null);
    const [fd, setFd] = useState(null);
    const [audioState, setAudioState] = useState(true);
    const [soundStatus, setSoundStatus] = useState(false);
    const [sound2Status, setSound2Status] = useState(false);
    const handleChange = (event) => {
        setBpm(Number(event.target.value))
    }
    let timer1
    let timer2

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

    const handleSuccess = (stream) => {
        let audio_context = new AudioContext()
        let input = audio_context.createMediaStreamSource(stream)
        recorder = new MyRecorder(input,{numChannels:1})
    };

    const handleError = () => {
        alert("エラーです。");
    };

    const startRecord = () => {
        setRecordStatus("recording")
        recorder.record()
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
        recorder.stop()
        recorder.exportWAV((blob) => {
            setUrl(URL.createObjectURL(blob))
            let formData = new FormData()
            formData.append('hanauta', blob)
            formData.append('bpm', bpm.toString())
            setFd(formData)
        })
        window.clearInterval(timer1)
        window.clearInterval(timer2)
        setMute(true)
        setMute2(true)
        setRecordStatus("finished")
    }

    const handleSubmit = () => {
        //　音声データを送信
        axios.post("api/v1/post_hanaoke", fd,{
            responseType: 'blob',
        })
            .then(res => {
                //　返してもらった後の表示処理
                let blob = new Blob([res.data], {type:"audio/wav"});
                history.push({ pathname: '/result', state: { url:URL.createObjectURL(blob) }})
            })
    }

    const waiting = (
        <div className={classes.root}>
            <TextField
                id="standard-basic"
                label="BPM"
                value={bpm}
                type="number"
                select
                onChange={handleChange}
                helperText="BPMを選択してください（70~200を推奨）"
            >{currencies.map((option) => (
                <MenuItem key={option.value} value={option.value}>
                    {option.label}
                </MenuItem>
            ))}</TextField>
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