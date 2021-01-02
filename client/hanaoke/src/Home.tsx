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
    const [soundStatus, setSoundStatus] = useState(false);
    const handleChange = (event: React.ChangeEvent<HTMLInputElement>) => {
        setBpm(Number(event.target.value))
    }
    const startRecord = () => {
        setInterval(
            ()=> {
                setSoundStatus(true)
            }, 60000/bpm)
    }
    return (
        <Grid container alignItems="center" justify="center">
            <Grid item xs={8}>
                <div className={classes.root}>
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
            </Grid>
        </Grid>
    )
}

export default Home