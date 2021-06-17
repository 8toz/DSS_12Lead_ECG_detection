import React, {useEffect, useState} from 'react';
import ProbabilitiesComponent from "./ProbabilitiesComponent"
import { Typography } from '@material-ui/core';
import { Paper } from "@material-ui/core"
import disseases from "../../assets/js/disseases"
import {Features} from "../../assets/js/Features"

function ModelPart(props) {
    
    const [features, setFeatures] = useState([]);

    useEffect(()=>{
        fetch('/getFeatures').then(response => response.json().then(data =>{
            setFeatures(data);
        }))
    },[]);

    console.log(features)

    return (
        <Paper style={{ borderRadius: "10px", paddingTop: "10px", paddingBottom: "10px", height: "100%" }}>
            <Typography variant="h3" align='center' style={{ margin: "10px" }}>Model's prediction</Typography>
            <Typography style={{ margin: "10px" }}>
                The model predicts that there is a high chance of having a <b>{props.diagnosis.classes
                    .map((val) => disseases[val])
                    .filter((c, i) => props.diagnosis.labels[i] === 1)
                    .reduce((acc = "", val) => (acc + val + " y "))}</b>
            </Typography>
            <ProbabilitiesComponent diagnosis={props.diagnosis} />
            <Typography style={{ margin: "10px" }}>
                Here you can explore some ECG features extracted from Lead II of the uploaded file
            </Typography>
           
            <Features features = {features}/>
            
        </Paper>
    );
}

export default ModelPart;