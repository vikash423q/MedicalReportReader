import { Container, Grid} from '@mui/material';
import React, { useEffect, useState } from 'react';
import { useLocation } from 'react-router-dom';
import ChartArea from './ChartArea';
import SummaryContainer from './SummaryContainer';
import FileUpload from './FileUpload';


const Dashboard = (props) => {
    const location = useLocation();
    const [summary, updateSummary] = useState({count: 0, reports: []});


    const getSummary = () => {
        fetch("http://localhost:8000/report-reader/v1/user/summary",
        { method: 'GET',
          headers: {'Cookie': `id=${location.state.id}`},
          credentials: 'include'
        })
        .then(res=>res.json())
        .then((data)=>{updateSummary(()=>({count: data.count, reports: data.recent_reports}))});
    };

    useEffect(()=>getSummary(), []);

    return (
          <Container
            style={{minHeight: '100vh', minWidth: '100%', backgroundColor: 'aliceblue', flexGrow: 1, padding: 4, margin: 0}}
          >
            <Grid
                container
                direction="column"
                justifyContent="space-between"
                minHeight="100%"
            >
                <Grid item xs={6}>
                    <SummaryContainer userId={location.state.id} summary={summary}/>
                </Grid>
                <Grid item container xs={6}>
                    <Grid item container justifyContent="space-evenly" alignItems="center">
                        <Grid item lg={4} md={12}>
                            <FileUpload userId={location.state.id} getSummary={getSummary}/>
                        </Grid>
                        <Grid item lg={8} md={12}>
                            <ChartArea userId={location.state.id}/>
                        </Grid>
                    </Grid>
                </Grid>
            </Grid>


          </Container>
    );
};
 
export default Dashboard;