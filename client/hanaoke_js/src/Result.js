import React, { useState, useEffect, useRef } from 'react'
import Grid from "@material-ui/core/Grid"
import { makeStyles, createStyles, Theme } from '@material-ui/core/styles';
import Button from "@material-ui/core/Button";
import { useHistory } from "react-router-dom";
import ReactAudioPlayer from "react-audio-player";

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

export function Result(props) {
    const classes = useStyles();
    const history = useHistory();
    return (
        <Grid container alignItems="center" justify="center">
            <Grid item xs={8}>
                <div className="root">
                <h1>"結果画面"</h1>
                    <ReactAudioPlayer src={props.location.state.url} controls />
                    <Button
                        variant="contained"
                        color="primary"
                        onClick={()=>history.push("/")}
                    >トップ画面に戻る</Button>
                </div>
            </Grid>
        </Grid>
    )
}

export default Result