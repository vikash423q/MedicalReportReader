import { Button, Grid, Typography } from '@mui/material';
import { useState } from 'react';
import Cookies from 'universal-cookie';
import { useNavigate, useLocation } from 'react-router-dom';
import AccountCircleIcon from '@mui/icons-material/AccountCircle';
import NavigateNextIcon from '@mui/icons-material/NavigateNext';


const cookies = new Cookies();

const ContinueContainer = (props) => {
    const navigate = useNavigate();
    const location = useLocation();

    const handleClick = () => navigate("/dashboard", {state: location.state, replace: true});

    return (
          <Grid container direction="column" component="form">
            <Grid item xs={12}>
                <AccountCircleIcon style={{fontSize:64, marginBottom: '1rem'}} color='primary'/>
            </Grid>
            <Grid item xs={12}>
                <Typography color='primary' variant='h5'>{location.state.name.toUpperCase()}</Typography>
            </Grid>
            <Grid item xs={12} marginTop='1rem'>
                <Button onClick={handleClick} style={{borderRadius: '1rem'}} size='medium' variant='contained' endIcon={<NavigateNextIcon/>}>
                    Continue
                </Button>
            </Grid>
          </Grid>
    );
};
 
export default ContinueContainer;