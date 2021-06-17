import React from 'react';
import { Typography } from "@material-ui/core"
import { ResponsiveBar } from '@nivo/bar'
import disseases from "../../assets/js/disseases"
import { withTheme } from '@material-ui/core/styles';

const colors = ["hsl(305, 70%, 50%)", "hsl(128, 70%, 50%)", "hsl(78, 70%, 50%)", "hsl(82, 70%, 50%)", "hsl(116, 70%, 50%)", "hsl(64, 70%, 50%)", "hsl(0, 70%, 50%)", "hsl(154, 70%, 50%)", "hsl(196, 70%, 50%)"]
const tooltip = (info) => {
    return (
        <div style={{ display: "flex", flexDirection: "row", alignItems: "center" }}>
            <svg width="16" height="16" style={{ marginRight: 4 }} xmlns="https://www.w3.org/2000/svg">
                <rect width="16" height="16" style={{ fill: info["color"] }} />
            </svg>
            <Typography>{disseases[info["indexValue"]]} - <b> {info["value"]} %</b></Typography>
        </div>
    )
}
function ProbabilitiesComponent(props) {
    return (
        <div style={{ display: "flex", flexDirection: "column", width: "auto", alignItems: "center" }}>
            <div style={{ height: "50vh", width: "100%" }}>
                <ResponsiveBar
                    theme={props.theme.nivo}
                    data={props.diagnosis.classes.map((c, i) => {
                        var color = c + "Color"
                        var result = { "class": c }
                        result[c] = (props.diagnosis.score[i] * 100).toFixed(2) / 1
                        result[color] = colors[i]
                        return result
                    }).filter((c, i) => props.diagnosis.score[i] > 0)}
                    keys={props.diagnosis.classes.filter((c, i) => props.diagnosis.score[i] > 0)}
                    margin={{ top: 50, right: 130, bottom: 50, left: 60 }}
                    layout="horizontal"
                    colors={{ scheme: "pastel1" }}
                    enableLabel={false}
                    maxValue={100}
                    tooltip={tooltip}
                    indexBy={"class"} />
            </div>
            <Typography style={{ textAlign: "center" }}><i>Detection probability of a specific waver pattern</i></Typography>
        </div>
    );
}

export default withTheme(ProbabilitiesComponent);