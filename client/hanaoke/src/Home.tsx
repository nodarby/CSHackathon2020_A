import React, { useState, useEffect } from 'react'
import Button from '@material-ui/core/Button';
import Grid from "@material-ui/core/Grid"
import TextField from '@material-ui/core/TextField';
import ReactHowler from 'react-howler'
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

// props の型を定義
type Props = {
    title?: string;
};

export function Home({title}: Props) {
    const classes = useStyles();
    const [bpm, setBpm] = useState(70);
    const [recordStatus, setRecordStatus] = useState(false)
    const [soundStatus, setSoundStatus] = useState(false);
    const handleChange = (event: React.ChangeEvent<HTMLInputElement>) => {
        setBpm(Number(event.target.value))
    }
    const startRecord = () => {
        setRecordStatus(true)
        //　録音中の画面に遷移
        setInterval(
            ()=> {
                setSoundStatus(true)
            }, 60000/bpm)
    }

    const stopRecord = () => {
        setSoundStatus(false)
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
                />
                {recordStatus ? recording : waiting}
            </Grid>
        </Grid>
    )
}



export default Home