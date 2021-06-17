import React from 'react';
import { ResponsiveHeatMap } from '@nivo/heatmap'
import { Typography } from '@material-ui/core';
import { withTheme } from '@material-ui/core/styles';
const tooltip = (info) =>{
    return(
        <div style={{display:"flex", flexDirection:"row", alignItems:"center"}}>
            <svg width="16" height="16" style={{marginRight:4}} xmlns="https://www.w3.org/2000/svg">
                <rect width="16" height="16" style={{fill: info["color"]}}/>
            </svg>
            <Typography>{info["yKey"]} - {info["xKey"]} - <b> {info["value"]} %</b></Typography>
        </div>
    )
}

function ConfusionMatrixComponent(props) {
    return (
        <div style={{display:"flex", flexDirection:"column", width:"auto", alignItems:"center"}}>
            <div style={{height:"50vh", width:"100%"}}>
                <ResponsiveHeatMap
                    theme={props.theme.nivo}
                    data={props.diagnosis.heatmap}
                    keys={props.diagnosis.classes}
                    indexBy="class"
                    margin={{ bottom: 60}}
                    forceSquare={true}
                    axisBottom={{ orient: 'top', tickSize: 5, tickPadding: 5, tickRotation: -90, legend: '', legendOffset: 36 }}
                    axisRight={null}
                    axisTop={null}
                    axisLeft={{
                        orient: 'left',
                        tickSize: 5,
                        tickPadding: 5,
                        tickRotation: 0,
                    }}
                    cellOpacity={1}
                    minValue={0}
                    maxValue={100}
                    cellBorderColor={{ from: 'color', modifiers: [ [ 'darker', 0.4 ] ] }}
                    labelTextColor={{ from: 'color', modifiers: [ [ 'darker', 1.8 ] ] }}
                    defs={[
                        {
                            id: 'lines',
                            type: 'patternLines',
                            background: 'inherit',
                            color: 'rgba(0, 0, 0, 0.1)',
                            rotation: -45,
                            lineWidth: 4,
                            spacing: 7
                        }
                    ]}
                    fill={[ { id: 'lines' } ]}
                    animate={true}
                    motionStiffness={80}
                    motionDamping={9}
                    hoverTarget="cell"
                    tooltip={tooltip}
                    cellHoverOthersOpacity={0.25}
                />
            </div>
            <Typography style={{textAlign:"center"}}><i>Enfermedad diagnosticada vs enfermedad real del paciente</i></Typography>
        </div>
    );
}

export default withTheme(ConfusionMatrixComponent);