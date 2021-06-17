import React, {useState, useLayoutEffect} from 'react';
import { Typography } from '@material-ui/core';
import {Paper, Container} from "@material-ui/core"
import LeadComponent from "./LeadComponent"
import Button from '@material-ui/core/Button';
import CloudDownloadIcon from '@material-ui/icons/CloudDownload';

function LeadsPart(props) {
    const [width, setWidth] = useState( window.innerWidth > 1280 ? 700:400)
    useLayoutEffect(() => {
        function updateSize() {
          setWidth(window.innerWidth > 1280 ? 700:400)
        }
        window.addEventListener('resize', updateSize);
      }, []);
    
        const download = e => {
        fetch("/sendImage", {
            method: "GET",
            headers: {}
        })
            .then(response => {
            response.arrayBuffer().then(function(buffer) {
                const url = window.URL.createObjectURL(new Blob([buffer]));
                const link = document.createElement("a");
                link.href = url;
                link.setAttribute("download", "image.png"); //or any other extension
                document.body.appendChild(link);
                link.click();
            });
            })
            .catch(err => {
            console.log(err);
            });
        };  


      return (
        <Paper style={{borderRadius:"10px", paddingTop:"10px", paddingBottom:"10px", height:"100%"}}>
            <Typography variant="h3" align='center' style={{margin:"10px"}}>Detected leads from .mat file</Typography>
            <div style={{display: 'flex',  justifyContent:'center', alignItems:'center'}}>
                <Button variant="outlined" size="large" startIcon={<CloudDownloadIcon />} onClick={e => download(e)}>
                Download the 12 lead ECG printable</Button>
            </div>
            <Typography style={{margin:"10px"}}>
                Preview of the different leads after being filtered
            </Typography>
            <ul>
                    <li><Typography>Ctrl + Click to zoom in</Typography></li>
                    <li><Typography>Ctrl + Mayús + Click to zoom out</Typography></li>
                </ul>
            {
                props.diagnosis.leads.map((lead)=>{
                    return(
                        <Container style={{width: "100%"}} key={lead.name}>
                            <LeadComponent
                                name={lead.name}
                                signal={lead.signal}
                                width={width}
                                fs={props.diagnosis.fs}/>
                        </Container>
                        )})
                        
            }
            
        </Paper>
    );
    
}

export default LeadsPart;