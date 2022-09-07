import { Container, Grid, Typography, Snackbar, Button} from '@mui/material';
import React, { useEffect, useState } from 'react';
import CloseIcon from '@mui/icons-material/Close';
import IconButton from '@mui/material/IconButton';
import FileUploadIcon from '@mui/icons-material/FileUpload';

import Dialog from '@mui/material/Dialog';
import DialogActions from '@mui/material/DialogActions';
import DialogContent from '@mui/material/DialogContent';
import DialogContentText from '@mui/material/DialogContentText';
import DialogTitle from '@mui/material/DialogTitle';

const FileUpload = (props) => {
    const userId = props.userId;

    const [selectedFile, selectFile] = useState({file: null, userId: userId, validate_user: true, validate_report: true});
    const [userValidOpen, setUserValidOpen] = useState(false);
    const [reportValidOpen, setReportValidOpen] = useState(false);
    const [error, setError] = useState('');
    const [snack, handleSnack] = useState({open: false, message: ''});

    const hiddenFileInput = React.useRef(null);
  
    const handleClick = event => {
        hiddenFileInput.current.click();
    };

    const tryUpload = () => {
        var data = new FormData();
        data.append('file', selectedFile.file);
        data.append('user_id', selectedFile.userId);
        data.append('validate_user', selectedFile.validate_user);
        data.append('validate_report', selectedFile.validate_report);
        fetch("http://localhost:8000/report-reader/v1/report/index",
        { method: 'POST',
          headers: {'Cookie': `id=${userId}`},
          body: data,
          credentials: 'include'
        })
        .then(response=>{
            if(response.status===420){
                setUserValidOpen(true);
            } else if(response.status===421){
                setReportValidOpen(true);
            }
            if(!response.ok) {return response.json().then(body=>{throw new Error(body.detail);})}
            else return response.json();
        })
        .then((body)=>{
            handleSnack(()=>({open: true, message: 'Upload successful!'}));
            selectFile(state=>({...state, file: null, validate_user: true, validate_report: true}));
            props.getSummary();
        })
        .catch((err)=>{
            handleSnack(()=>({open: true, message: err.message}));
            setError('Error: ' + err.message);
        });
        setUserValidOpen(false);
        setReportValidOpen(false);
    }

    const handleUpload = (e) => {
        if(!e.target.value.toLowerCase().endsWith('.pdf')){
            handleSnack(()=>({open: true, message: 'Invalid File Type! Only PDF supported.'}));
            return;
        }
        selectFile(state=>({...state, file: e.target.files[0]}));
    };

    const action = (
        <React.Fragment>
          <IconButton
            size="small"
            aria-label="close"
            color="inherit"
            onClick={()=>handleSnack({open: false, message: ''})}
          >
            <CloseIcon fontSize="small" />
          </IconButton>
        </React.Fragment>
      );

    useEffect(()=>{
        if(selectedFile.file!==null){
            tryUpload();
        }
    }, [selectedFile]);

    return (
        <Container>
        <Grid container direction="column" alignItems='center' justifyContent='space-between'>
            <IconButton onClick={handleClick} style={{padding: '3rem', backgroundColor: 'white', marginBottom: '1rem'}}>
                <FileUploadIcon style={{fontSize: 48}}/>
            </IconButton>
            <input type="file" ref={hiddenFileInput} onChange={handleUpload} style={{display:'none'}}/> 
            <Typography color="darkgray" variant='h5'>UPLOAD REPORT</Typography>
        </Grid>
        <Snackbar
        open={snack.open}
        autoHideDuration={5000}
        // onClose={handleClose}
        message={snack.message}
        action={action}
        />
        <Dialog
        open={userValidOpen}
        onClose={()=>selectFile(state=>({...state, file: null, validate_user: true, validate_report: true}))}
      >
        <DialogTitle id="alert-dialog">
          {"User Validation Failed"}
        </DialogTitle>
        <DialogContent>
          <DialogContentText id="alert-dialog-description">
            {error}
          </DialogContentText>
        </DialogContent>
        <DialogActions>
          <Button onClick={()=>setUserValidOpen(false)} autoFocus>Cancel</Button>
          <Button onClick={()=>selectFile(state=>({...state, validate_user: false}))}>
            Still Me. Upload?
          </Button>
        </DialogActions>
      </Dialog>
      <Dialog
        open={reportValidOpen}
        onClose={()=>selectFile(state=>({...state, file: null, validate_user: true, validate_report: true}))}
      >
        <DialogTitle id="alert-dialog">
          {"Report Validation Failed"}
        </DialogTitle>
        <DialogContent>
          <DialogContentText id="alert-dialog-description">
            {error}
          </DialogContentText>
        </DialogContent>
        <DialogActions>
          <Button onClick={()=>setReportValidOpen(false)} autoFocus>Cancel</Button>
          <Button onClick={()=>selectFile(state=>({...state, validate_report: false}))}>
            It's Fine. Upload?
          </Button>
        </DialogActions>
      </Dialog>
    </Container>
    );
};
 
export default FileUpload;