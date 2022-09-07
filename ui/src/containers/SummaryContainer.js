import { Container, Grid, Typography, Paper } from '@mui/material';
import { useEffect, useState } from 'react';
import MonitorHeartIcon from '@mui/icons-material/MonitorHeart';

const SummaryContainer = (props) => {
    const userId = props.userId;

    const reportCard = (item) => (
        <Grid key={item.report_id} item>
                    <Paper style={{backgroundColor: 'white', padding: 1, margin: '1rem'}}>
                        <Grid item container direction="column" padding={2}>
                            <Grid item>
                                <MonitorHeartIcon color='info' style={{fontSize: 32}}/>
                            </Grid>
                            <Grid item>
                                <Typography fontSize={11} color="darkgray">{item.name}</Typography>
                            </Grid>
                            <Grid item>
                                <Typography fontSize={11} color="darkgray">Lab : {item.lab}</Typography>
                            </Grid>
                            <Grid item>
                                <Typography fontSize={11} color="darkgray">Package : {item.package}</Typography>
                            </Grid>
                            <Grid item>
                                <Typography fontSize={11} color="darkgray">Date : {new Date(item.date).toDateString().slice(4)}</Typography>
                            </Grid>
                        </Grid>
                    </Paper>
                </Grid>
    );

    return (
        <Container>
        <Grid container direction="row" alignItems="center" justifyContent="space-between">
            <Grid item container alignItems="end" md={12} lg={6}>
                <Grid item><Typography color="darkgreen" fontSize={72} fontWeight={500}>{props.summary.count}</Typography></Grid>
                <Grid item><Typography fontSize={22} fontWeight={600} color="darkorange">Reports Processed</Typography></Grid>
            </Grid>
            
            {/* <Grid item container sx={{display: {xs: 'none', lg: 'inline'}}} lg={6}>
                {props.summary.reports.slice(0, 2).map((item)=>reportCard(item))}
            </Grid> */}
        </Grid>
    </Container>
    );
};
 
export default SummaryContainer;