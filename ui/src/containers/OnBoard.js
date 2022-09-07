import '../App.css';
import Box from '@mui/material/Box';
import TextField from '@mui/material/TextField';
import { Button, Container, Grid, Typography } from '@mui/material';

import LoginContainer from './LoginContainer';
import React, { useEffect, useState } from 'react';
import SignupContainer from './SignUpContainer';
import { Link, useNavigate, useLocation } from 'react-router-dom';
import Cookies from 'universal-cookie';
import ContinueContainer from './ContinueContainer';

const cookies = new Cookies();

const OnBoardPage = (props) => {
    const navigate = useNavigate();
    const location = useLocation();

    useEffect(()=>{
        const userId = cookies.get("id");
        if(userId===null) return;
        fetch("http://localhost:8000/report-reader/v1/user/session",
                              { method: 'GET',
                                headers: {'Cookie': `id=${userId}`},
                                credentials: 'include'
                              })
                              .then(res=>res.json())
                              .then((data)=>{navigate('/continue', {state: data, replace: true});});
    }, []);

    return (
        <React.Fragment>
            <div className='App'>
            <div className='App-header'>
                <Box
                    style={{ backgroundColor: "white", padding: '2rem', borderRadius: '7px' }}
                >
                    <Grid container direction="column">
                        <Grid item xs={12} style={{ marginBottom: '1rem' }}>
                            <Typography variant='h4' color='GrayText' gutterBottom>REPORT READER</Typography>
                        </Grid>

                        <Grid item xs={12}>
                            {location.state? <ContinueContainer/>: (props.loginMode? <LoginContainer/> : <SignupContainer/>)}
                        </Grid>
                        <Grid item xs={12}>
                            <Grid container direction="row">
                                <Grid item xs={8}></Grid>
                                <Grid item xs={4}>
                                    <Button variant='text'>
                                        <Link to={props.loginMode? "/register": "/login"}>
                                            {(props.loginMode? "Signup": "Login")}
                                        </Link>
                                    </Button>
                                </Grid>
                            </Grid>
                        </Grid>
                    </Grid>
                </Box>
            </div>
            </div>
        </React.Fragment>        
    );
};

export default OnBoardPage;