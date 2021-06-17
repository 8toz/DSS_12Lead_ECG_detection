import React, {useState, useEffect} from 'react';
import {Line} from "@nivo/line"
import {ExpansionPanel, ExpansionPanelDetails, ExpansionPanelSummary, Typography} from "@material-ui/core"
import ExpandMoreIcon from '@material-ui/icons/ExpandMore';
import { makeStyles } from '@material-ui/core/styles';
import { withTheme } from '@material-ui/core/styles';

const useStyles = makeStyles((theme) => ({
    root: {
      width: '100%',
      marginBottom: "10px"
    },
    heading: {
      fontSize: theme.typography.pxToRem(15),
      fontWeight: theme.typography.fontWeightRegular,
    },
    details: {
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
    },
    scrollable:{
        overflowX:"auto", 
        whiteSpace:"nowrap"
    }
  }));

function LeadComponent(props) {
    const classes = useStyles();
    const clickHandler = (point,event) =>{
        event.stopPropagation();
        if(event.ctrlKey){
            if(event.shiftKey) setWidth(width/2)
            else setWidth(width*2)
        }
    }

    const [width, setWidth] = useState(props.width + 30)
    useEffect(() => {
        setWidth(props.width + 30)
    }, [props.width])
    return (
        <ExpansionPanel className={classes.root}>
            <ExpansionPanelSummary
                expandIcon={<ExpandMoreIcon />}
                aria-controls="panel1a-content"
                id="panel1a-header">
                    <Typography className={classes.heading}>{props.name}</Typography>
            </ExpansionPanelSummary>
            <ExpansionPanelDetails>
                <div className={classes.details}>
                    <div className={classes.scrollable} style={{width: props.width}}>
                        <Line
                            height={400}
                            animate
                            theme={props.theme.nivo}
                            width={width}
                            data={[{"id":props.name, 
                                    "color": "hsl(0, 100%, 50%)", 
                                    "data": props.signal.map((value,index)=>{
                                                                return {"x":index/props.fs, "y":value}})}]}
                            enablePoints={false}
                            margin={{ top: 60, right: 80, bottom: 60, left: 80 }}
                            xScale={{ type: 'linear' }}
                            yScale={{ type: 'linear', min: 'auto', max: 'auto', stacked: true, reverse: false }}
                            colors={["#ff5c5c"]}
                            axisBottom={{
                                tickValues:5,
                            }}
                            axisLeft={null}
                            onClick={clickHandler}
                            useMesh />
                    </div>
                    <Typography><i>Time in seconds</i></Typography>
                </div>
            </ExpansionPanelDetails>
        </ExpansionPanel>
    );
}

export default withTheme(LeadComponent);