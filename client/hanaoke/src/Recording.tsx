import React, { useState, useEffect } from 'react'
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

export function Recording() {
    const [file, setFile] = useState([]);
    const [audioState, setAudioState] = useState(true);
    const classes = useStyles();
    return (
        <div className={classes.root}>
            <h2>マイク</h2>
        </div>

    )
}

export default Recording