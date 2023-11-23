import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { Container, Typography, Paper, TextField, Stack, Snackbar, Alert, Button } from '@mui/material';
import {app, storageErrorCodes} from '../firebase/config'
import { getAuth } from "firebase/auth";
import { getDatabase, ref as databaseRef, get, child, update} from "firebase/database";
import { getStorage, uploadBytes, ref as storageRef, getDownloadURL } from 'firebase/storage'; 
import InputAdornment from '@mui/material/InputAdornment';
import EditIcon from '@mui/icons-material/Edit';
import Fab from '@mui/material/Fab';
import Avatar from '@mui/material/Avatar';
import IconButton from '@mui/material/IconButton';
import CheckIcon from '@mui/icons-material/Check';
import CloudUploadIcon from '@mui/icons-material/CloudUpload';
import ArrowBackIcon from '@mui/icons-material/ArrowBack';
import CircularProgress from '@mui/material/CircularProgress';
import { yellow } from '@mui/material/colors';
import '../assets/CustomFonts.css';

function addDecimalPlaces(number) {
  const parts = number.split('.');
  if (parts.length === 1) {
    return number + '.00';
  } else if (parts[1].length === 1) {
    return number + '0';
  } else {
    return number;
  }
}

function EditCandy() {

  const navigate = useNavigate();
  const auth = getAuth(app);
  const dbRef = databaseRef(getDatabase(app));

  const[candy1, setCandy1] = useState({
    name: '',
    price: 0,
    url: null,
    file: null,
  })
  
  const[candy2, setCandy2] = useState({
    name: '',
    price: 0,
    url: null,
    file: null,
  })

  const [editingCandy1, setEditingCandy1] = useState(false);
  const [editingCandy2, setEditingCandy2] = useState(false);

  const [editingImage1, setEditingImage1] = useState(false);
  const [editingImage2, setEditingImage2] = useState(false);

  const fabYellowStyle = {
    color: 'common.white',
    bgcolor: yellow[600],
    '&:hover': {
      bgcolor: yellow[700],
    },
  };

  const [open, setOpen] = useState(false);
  const [snackbarMessage, setSnackbarMessage] = useState('');
  const [loginTimeout, setLoginTimeout] = useState(false);
  const [alertSeverity, setalertSeverity] = useState('');

  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (loginTimeout) {
      const timeout = setTimeout(() => {
        navigate('/'); 
      }, 5000); 
      return () => clearTimeout(timeout); 
    }
  }, [loginTimeout, navigate]);

  useEffect(() => {

    if(auth.currentUser === null){
      setalertSeverity('error');
      setOpen(true);
      setSnackbarMessage('Error: login timeout. Redirecting to login page!');
      setLoginTimeout(true);
      return;
    }
    
    const uid = auth.currentUser.uid;

    const stRef1 = storageRef(getStorage(app), uid + '/Candy1.jpg');
    const stRef2 = storageRef(getStorage(app), uid + '/Candy2.jpg');
      
    get(child(dbRef, uid + '/candyInformation')).then( (snapshot) => {
      if(snapshot.exists()){
        getDownloadURL(stRef1).then((url) => {
          setCandy1({ ...candy1, name: snapshot.val().Candy1.Name, price: snapshot.val().Candy1.Price, url : url});
        }).catch((error) => {
          setSnackbarMessage(storageErrorCodes[error.code]);
          setCandy1({...candy1, name: snapshot.val().Candy1.Name, price: snapshot.val().Candy1.Price});
          setalertSeverity('warning');
          setOpen(true);
        })
        getDownloadURL(stRef2).then((url2) => {
          setCandy2({...candy2, name: snapshot.val().Candy2.Name, price: snapshot.val().Candy2.Price, url : url2});
        }).catch((error) => {
          setCandy2({...candy2, name: snapshot.val().Candy2.Name, price: snapshot.val().Candy2.Price});
          setSnackbarMessage(storageErrorCodes[error.code]);
          setalertSeverity('warning');
          setOpen(true);
        })
      }
      else {
        setSnackbarMessage("No data available");
        setalertSeverity('error');
        setOpen(true);
        return;
      }
    }).catch((error) => {
      setSnackbarMessage(error.code);
      setalertSeverity('error');
      setOpen(true);
      return;
    }).finally(() => {
      setLoading(false);
    })
  }, []);

  const handleClose = (event, reason) => {
    if (reason === 'clickaway') {
      return;
    }
    setOpen(false);
  };

  const handleImageUpload1 = () => {
    const fileInput = document.createElement('input');
    fileInput.type = 'file';
    fileInput.accept = 'image/*';
    fileInput.onchange = (e) => {
      const file = e.target.files[0];
      if(file && (file.type.startsWith('image/png') || file.type.startsWith('image/jpg') || file.type.startsWith('image/jpeg'))){
        setCandy1({...candy1, file: file, url : URL.createObjectURL(file)});
      }
      else{
        setSnackbarMessage('Error: you can only select png, jpg or jpeg files!');
        setalertSeverity('error');
        setOpen(true);
      }
    };
    fileInput.click();
  };

  const handleImageUpload2 = () => {
    const fileInput = document.createElement('input');
    fileInput.type = 'file';
    fileInput.accept = 'image/*';
    fileInput.onchange = (e) => {
      const file = e.target.files[0];
      if(file && (file.type.startsWith('image/png') || file.type.startsWith('image/jpg') || file.type.startsWith('image/jpeg'))){
        setCandy2({...candy2, file: file, url : URL.createObjectURL(file)});
      }
      else{
        setSnackbarMessage('Error: you can only select image files!');
        setalertSeverity('error');
        setOpen(true);
      }
    };
    fileInput.click();
  };

  const handleEditCandy1 = () => {
    setEditingCandy1(!editingCandy1);
    setEditingImage1(!editingImage1);
  };

  const handleEditCandy2 = () => {
    setEditingCandy2(!editingCandy2);
    setEditingImage2(!editingImage2);
  };

  const handleSaveCandies = () => {
    
    if(auth.currentUser === null){
      setSnackbarMessage('Error: login timeout. Redirecting to login page!');
      setalertSeverity('error');
      setLoginTimeout(true);
      setOpen(true);
      return;
    }

    setEditingCandy1(false);
    setEditingCandy2(false);
    setEditingImage1(false);
    setEditingImage2(false); 
    
    const uid = auth.currentUser.uid;

    if (!(/^\$?(([1-9](\d*|\d{0,2}(,\d{3})*))|0)(\.\d{1,2})?$/.test(candy1.price))){
      setSnackbarMessage('Error: invalid format for Candy 1 Price!');
      setalertSeverity('error');
      setOpen(true);
      return;
    }

    if (!(/^\$?(([1-9](\d*|\d{0,2}(,\d{3})*))|0)(\.\d{1,2})?$/.test(candy2.price))){
      setSnackbarMessage('Error: invalid format for Candy 2 Price!');
      setalertSeverity('error');
      setOpen(true);
      return;
    }

    if (candy1.price == 0.0 || candy2.price == 0.0){
      setSnackbarMessage('Error: candy price cannot be zero!');
      setalertSeverity('error');
      setOpen(true);
      return;
    }

    const stRef1 = storageRef(getStorage(app), uid + '/Candy1.jpg');
    const stRef2 = storageRef(getStorage(app), uid + '/Candy2.jpg');
    
    setCandy1({...candy1, price: addDecimalPlaces(candy1.price)})
    setCandy2({...candy2, price: addDecimalPlaces(candy2.price)})

    const newCandy1 = {
      Name: candy1.name,
      Price: addDecimalPlaces(candy1.price),
    };

    const newCandy2 = {
      Name: candy2.name,
      Price: addDecimalPlaces(candy2.price),
    };

    const updates = {};
    updates['/' + uid + '/candyInformation/Candy1/Name'] = newCandy1.Name;
    updates['/' + uid + '/candyInformation/Candy1/Price'] = newCandy1.Price;
    updates['/' + uid + '/candyInformation/Candy2/Name'] = newCandy2.Name;
    updates['/' + uid + '/candyInformation/Candy2/Price'] = newCandy2.Price;


    update(dbRef, updates).then( (update) => {
      setalertSeverity('success');
      setOpen(true);
      setSnackbarMessage('Candies updated successfully!');
      if(candy1.file !== null){
        uploadBytes(stRef1, candy1.file).then((snapshot) => { 
        }).catch((error) => {
          setSnackbarMessage(error.code);
          setalertSeverity('error');
          setOpen(true);
        })
      }
      if(candy2.file !== null){
        uploadBytes(stRef2, candy2.file).then((snapshot) => {
        }).catch((error) => {
          setSnackbarMessage(error.code);
          setalertSeverity('error');
          setOpen(true);
        }) 
      }
    }).catch((error) => {
      setSnackbarMessage(error.code);
      setalertSeverity('error');
      setOpen(true);
    })
  };

  return (
    <Container maxWidth="xs" style={{padding: '20px'}}>
        <Stack
            spacing={2}
            direction="column"
            justifyContent="center"
            alignItems="center"
            height="100vh" 
            display="flex" 
            flexDirection="column" 
        >
          <Typography variant="h4" style={{fontFamily: 'AbrilFatface'}}>
            Edit Candies&nbsp; 
            <img
              src="/assets/windows-11-emojis/candy_1f36c.png"
              alt="🍬"
              style={{ width: '1.4em', height: '1.4em', verticalAlign: 'top' }}
            />
          </Typography>
            {!loading && <>
              <Paper 
                elevation={15}
                style={{borderRadius: '10px', backgroundColor: '#469Fd17f', padding: '5%'}}
              >
                <Stack
                  spacing={2}
                  direction="row"
                  marginBottom='5%'
                  justifyContent="space-between"
                >
                  <Typography variant="h5" sx={{fontFamily: 'PlaypenSans'}}><u>Candy #1</u></Typography>
                  <Fab color="primary" aria-label="edit" size='small' onClick={handleEditCandy1}>
                    <EditIcon style={{ color: editingCandy1 ? 'black' : 'white' }} />
                  </Fab>
                </Stack>
                <Stack
                  spacing={2}
                  direction="row"
                >
                  <Typography variant="h7" sx={{fontFamily: 'PlaypenSans'}} style={{marginTop: '0.75%'}} >Candy name:</Typography>
                  <TextField
                    variant='standard'
                    value={candy1.name}
                    sx={{width: '62.5%', margin: '0px'}}
                    onChange={(e) => {
                      if (e.target.value.length <= 15) {
                        setCandy1({ ...candy1, name: e.target.value });
                      }
                    }}
                    disabled={!editingCandy1}
                  />
                </Stack>
                <Stack
                  spacing={2}
                  direction="row"
                >
                  <Typography variant="h7" sx={{fontFamily: 'PlaypenSans'}} style={{marginTop: '0.75%'}} >Candy price/mL:</Typography>
                  <TextField
                    variant='standard'
                    value={candy1.price}
                    type='number'
                    sx={{width: '55%', margin: '0px'}}
                    onChange={(e) => {
                      const inputValue = e.target.value;
                      if (/^\$?(([1-9](\d*|\d{0,2}(,\d{3})*))|0)(\.\d{1,2})?$/.test(inputValue) || inputValue === "") {
                        setCandy1({ ...candy1, price: inputValue });
                      }
                    }}
                    disabled={!editingCandy1}
                    InputProps={{
                      startAdornment: <InputAdornment position="start">R$</InputAdornment>
                    }}
                  />
                </Stack>
                <Stack
                  spacing={2}
                  direction="row"
                  marginTop="5%"
                  position="relative"
                >
                  <Avatar
                    src={candy1.url ? candy1.url : process.env.PUBLIC_URL + '/candyImages/Undefined.png'}
                    alt={candy1.name}
                  />
                  {editingImage1 && (
                    <IconButton
                      style={{
                        position: 'absolute',
                        top: 0,
                        right: 0,
                        backgroundColor: 'white',
                        borderRadius: '50%',
                      }}
                      onClick={handleImageUpload1}
                    >
                      <CloudUploadIcon />
                    </IconButton>
                  )}
                  <Typography variant="h7" sx={{fontFamily: 'PlaypenSans'}} style={{marginTop: '2.25%'}} >
                    <img
                      src="/assets/windows-11-emojis/backhand-index-pointing-left_1f448.png"
                      alt="👈"
                      style={{ width: '1.4em', height: '1.4em', verticalAlign: 'top' }}
                    />
                    &nbsp;Candy image
                  </Typography>
                </Stack>
              </Paper>
              <Paper 
                elevation={15}
                style={{borderRadius: '10px', backgroundColor: '#CFCF007f', padding: '5%'}}
              >
                <Stack
                  spacing={2}
                  direction="row"
                  marginBottom='5%'
                  justifyContent="space-between"
                >
                  <Typography variant="h5" sx={{fontFamily: 'PlaypenSans'}}><u>Candy #2</u></Typography>
                  <Fab color="primary" aria-label="edit" size='small' onClick={handleEditCandy2} sx={fabYellowStyle}>
                    <EditIcon style={{ color: editingCandy2 ? 'black' : 'white' }} />
                  </Fab>
                </Stack>
                <Stack
                  spacing={2}
                  direction="row"
                >
                  <Typography variant="h7" sx={{fontFamily: 'PlaypenSans'}} style={{marginTop: '0.75%'}} >Candy name:</Typography>
                  <TextField
                    variant='standard'
                    value={candy2.name}
                    sx={{width: '62.5%', margin: '0px'}}
                    onChange={(e) => {
                      if (e.target.value.length <= 15) {
                        setCandy2({ ...candy2, name: e.target.value });
                      }
                    }}
                    disabled={!editingCandy2}
                  />
                </Stack>
                <Stack
                  spacing={2}
                  direction="row"
                >
                  <Typography variant="h7" sx={{fontFamily: 'PlaypenSans'}} style={{marginTop: '0.75%'}} >Candy price/mL:</Typography>
                  <TextField
                    variant='standard'
                    value={candy2.price}
                    type='number'
                    sx={{width: '55%', margin: '0px'}}
                    onChange={(e) => {
                      const inputValue = e.target.value;
                      if (/^\$?(([1-9](\d*|\d{0,2}(,\d{3})*))|0)(\.\d{1,2})?$/.test(inputValue) || inputValue === "") {
                        setCandy2({ ...candy2, price: inputValue });
                      }
                    }}
                    disabled={!editingCandy2}
                    InputProps={{
                      startAdornment: <InputAdornment position="start">R$</InputAdornment>
                    }}
                  />
                </Stack>
                <Stack
                  spacing={2}
                  direction="row"
                  marginTop="5%"
                  position="relative"
                >
                  <Avatar
                    src={candy2.url ? candy2.url : process.env.PUBLIC_URL + '/candyImages/Undefined.png'}
                    alt={candy2.name}
                  />
                  {editingImage2 && (
                    <IconButton
                      style={{
                        position: 'absolute',
                        top: 0,
                        right: 0,
                        backgroundColor: 'white',
                        borderRadius: '50%',
                      }}
                      onClick={handleImageUpload2}
                    >
                      <CloudUploadIcon />
                    </IconButton>
                  )}
                  <Typography variant="h7" sx={{fontFamily: 'PlaypenSans'}} style={{marginTop: '2.25%'}} >
                    <img
                      src="/assets/windows-11-emojis/left-arrow_2b05-fe0f.png"
                      alt="⬅️"
                      style={{ width: '1.4em', height: '1.4em', verticalAlign: 'top' }}
                    />
                    &nbsp;Candy image
                  </Typography>
                </Stack>
              </Paper>
              <Button 
                variant="contained"
                fullWidth 
                onClick={handleSaveCandies}
                sx={{fontFamily: 'PlaypenSans'}}  
                endIcon={<CheckIcon />}
              >
                  Save
              </Button>
              <Button 
                variant="contained"
                fullWidth 
                onClick={() => navigate('/main') }
                sx={{fontFamily: 'PlaypenSans'}}  
                endIcon={<ArrowBackIcon />}
              >
                  Back
              </Button>
              {loginTimeout && <CircularProgress />}
            </>}
            {loading && <CircularProgress />}
        </Stack>
        <Snackbar open={open} autoHideDuration={6000} onClose={handleClose}>
        <Alert onClose={handleClose} severity={alertSeverity === 'success' ? 'success' : 'error'} sx={{ width: '100%' }}>
          {snackbarMessage}
        </Alert>
      </Snackbar>
    </Container>
  );
}

export default EditCandy;
