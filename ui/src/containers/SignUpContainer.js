import TextField from '@mui/material/TextField';
import ManIcon from '@mui/icons-material/Man';
import WomanIcon from '@mui/icons-material/Woman';
import { Button, Container, Grid, ToggleButtonGroup, ToggleButton, Typography } from '@mui/material';
import { useState } from 'react';

const SignupContainer = (props) => {

    const [sex, setSex] = useState('M');

    const changeSex = () => setSex(sex === 'F'? 'M': 'F');
    return (
          <Grid container direction="column" component="form">
            <Grid item xs={12}>
            <Grid item xs={12}>
                <TextField 
                    id="filled-basic" 
                    label="Name" 
                    variant="outlined"
                    margin='dense'
                />
            </Grid>
                <TextField
                    id="outlined-basic"
                    label="Username"
                    variant="outlined"
                    margin='dense'
                />
            </Grid>
            <Grid item xs={12}>
                <TextField 
                    id="filled-basic" 
                    label="Password" 
                    type="password" 
                    variant="outlined"
                    margin='dense'
                />
            </Grid>
            <Grid item xs={12}>
                <TextField 
                    id="filled-basic" 
                    label="Year of Birth" 
                    type="number"
                    variant="outlined"
                    margin='dense'
                />
            </Grid>
            <Grid item xs={12} style={{margin: '2rem', marginTop: '1rem'}}>
                <Grid container direction="row">
                    <Grid item xs={6}>
                        <Typography variant='button' color="GrayText">Gender</Typography>
                    </Grid>
                    <Grid item xs={6}>
                        <ToggleButtonGroup color='primary' value={sex} onChange={changeSex} size="small">
                            <ToggleButton value="M" key="M">
                                <ManIcon/>
                            </ToggleButton>,
                            <ToggleButton value="F" key="F">
                                <WomanIcon />
                            </ToggleButton>
                        </ToggleButtonGroup>
                    </Grid>
                </Grid>
                
            </Grid>
            <Grid item xs={12}>
                <Button variant='contained'>Signup</Button>
            </Grid>
          </Grid>
    );
};
 
export default SignupContainer;