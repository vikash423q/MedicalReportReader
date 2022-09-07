import TextField from '@mui/material/TextField';
import { Button, Container, Grid, Typography } from '@mui/material';
import { useState } from 'react';
import Cookies from 'universal-cookie';
import { useNavigate } from 'react-router-dom';


const cookies = new Cookies();

const LoginContainer = (props) => {
    const navigate = useNavigate();

    const [state, setState] = useState({username: "", password: ""});
    const [error, setError] = useState(null);


    const changeUsername = (e) =>  setState({...state, username: e.target.value});
    const changePassword = (e) => setState({...state, password: e.target.value});

    const changeError = (err) => setError(err);

    const handleLogin = async () => {
      setError(null);
      const res = await fetch("http://localhost:8000/report-reader/v1/user/login",
                              { method: 'POST',
                                body: JSON.stringify(state),
                                headers: {'Content-Type': 'application/json'},
                                credentials: 'include'
                              });
      const data = await res.json();
      if(res.status>=400 & res.status<500){
        changeError(data.detail);
      }
      if(res.status===200){
        cookies.set("id", data["id"]);
        navigate('/dashboard', {state: data, replace: true});
      };
      
    };

    return (
          <Grid container direction="column" component="form">
            <Grid item xs={12}>
                <TextField
                    id="outlined-basic"
                    label="Username"
                    variant="outlined"
                    margin='dense'
                    defaultValue={state.username}
                    onChange={changeUsername}
                />
            </Grid>
            <Grid item xs={12}>
                <TextField 
                    id="filled-basic" 
                    label="Password" 
                    type="password" 
                    variant="outlined"
                    margin='dense'
                    defaultValue={state.password}
                    onChange={changePassword}
                />
            </Grid>
            <Grid item xs={12}>
                <Typography color='red' variant='caption'>{error}</Typography>
            </Grid>
            <Grid item xs={12} marginTop='1rem'>
                <Button onClick={handleLogin} variant='contained'>Login</Button>
            </Grid>
          </Grid>
    );
};
 
export default LoginContainer;