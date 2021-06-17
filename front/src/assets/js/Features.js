import React from 'react';
import { makeStyles } from '@material-ui/core/styles';
import Accordion from '@material-ui/core/Accordion';
import AccordionSummary from '@material-ui/core/AccordionSummary';
import AccordionDetails from '@material-ui/core/AccordionDetails';
import Typography from '@material-ui/core/Typography';
import ExpandMoreIcon from '@material-ui/icons/ExpandMore';



export const Features = ({features}) => {
    return (

        <div className={features.root}>
            <h2 align='center'>
                Average BPM {features.average_bpm}
            </h2>
      <Accordion>
        <AccordionSummary
          expandIcon={<ExpandMoreIcon />}
          aria-controls="panel1a-content"
          id="panel1a-header"
        >
          <Typography className={features.heading}><b>RR interval: </b>{features.average_RR_distance} ms</Typography>
        </AccordionSummary>
        <AccordionDetails>
          <Typography>
            {features.RR_distance}
          </Typography>
        </AccordionDetails>
      </Accordion>
      <Accordion>
        <AccordionSummary
          expandIcon={<ExpandMoreIcon />}
          aria-controls="panel2a-content"
          id="panel2a-header"
        >
          <Typography className={features.heading}><b>PR interval: </b>{features.average_PR_distance} ms</Typography>
        </AccordionSummary>
        <AccordionDetails>
          <Typography>
            {features.PR_distance}
          </Typography>
        </AccordionDetails>
      </Accordion>

      <Accordion disabled>
        <AccordionSummary
          expandIcon={<ExpandMoreIcon />}
          aria-controls="panel3a-content"
          id="panel3a-header"
        >
          <Typography className={features.heading}><b>QRS Complex</b></Typography>
        </AccordionSummary>
      </Accordion>

      <Accordion disabled>
        <AccordionSummary
          expandIcon={<ExpandMoreIcon />}
          aria-controls="panel3a-content"
          id="panel3a-header"
        >
          <Typography className={features.heading}><b>ST segment</b></Typography>
        </AccordionSummary>
      </Accordion>
    
    

      <Accordion>
        <AccordionSummary
          expandIcon={<ExpandMoreIcon />}
          aria-controls="panel2a-content"
          id="panel2a-header"
        >
          <Typography className={features.heading}><b>RT interval: </b>{features.average_RT_distance} ms</Typography>
        </AccordionSummary>
        <AccordionDetails>
          <Typography>
            {features.RT_distance}
          </Typography>
        </AccordionDetails>
      </Accordion>


      <Accordion>
        <AccordionSummary
          expandIcon={<ExpandMoreIcon />}
          aria-controls="panel2a-content"
          id="panel2a-header"
        >
          <Typography className={features.heading}><b>PP interval: </b>{features.average_PP_distance} ms</Typography>
        </AccordionSummary>
        <AccordionDetails>
          <Typography>
            {features.PP_distance}
          </Typography>
        </AccordionDetails>
      </Accordion>

      <Accordion>
        <AccordionSummary
          expandIcon={<ExpandMoreIcon />}
          aria-controls="panel2a-content"
          id="panel2a-header"
        >
          <Typography className={features.heading}><b>TT interval: </b>{features.average_TT_distance} ms</Typography>
        </AccordionSummary>
        <AccordionDetails>
          <Typography>
            {features.TT_distance}
          </Typography>
        </AccordionDetails>
      </Accordion>


    </div>
        
    
    )
}
