import React from 'react';
import LeadsPart from "./LeadsPart"
import { Grid, Container } from "@material-ui/core"
import ModelPart from "./ModelPart"
import { withTheme } from '@material-ui/core/styles';

function DiagnosisPage(props) {
    return (
        <Container style={{ padding: "100px", backgroundColor: props.theme.palette.background.default }} maxWidth="xl">
            <Grid container spacing={3}>
                <Grid item xs={6}>
                    <LeadsPart diagnosis={props.diagnosis} />
                </Grid>
                <Grid item xs={6}>
                    <ModelPart diagnosis={props.diagnosis} />
                </Grid>
            </Grid>
        </Container>

    );
}

export default withTheme(DiagnosisPage);