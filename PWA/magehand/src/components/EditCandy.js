import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { Container, Typography, Paper, TextField, Stack, Snackbar, Alert, Button } from '@mui/material';
import {app, authErrorCodes} from '../firebase/config'
import { getAuth } from "firebase/auth";
import { getDatabase, ref, onValue, get, child, update} from "firebase/database";
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
  
function EditCandy() {

  const navigate = useNavigate();
  const auth = getAuth(app);
  const dbRef = ref(getDatabase(app));

  const[candy1, setCandy1] = useState({
    name: 'Candy 1',
    price: 0,
    photo: null,
    base64Image: null, 
  })
  
  const[candy2, setCandy2] = useState({
    name: 'Candy 2',
    price: 0,
    photo: null,
    base64Image: null,
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
  const [updateSuccessful, setUpdateSuccessful] = useState(true);

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
      setUpdateSuccessful(false);
      setOpen(true);
      setSnackbarMessage('Error: login timeout. Redirecting to login page!');
      setLoginTimeout(true);
      return;
    }
    
    const uid = auth.currentUser.uid;
      
    get(child(dbRef, uid + '/candyInformation')).then( (snapshot) => {
      if(snapshot.exists()){
        console.log(snapshot.val());
        setCandy1({name: snapshot.val().Candy1.Name, price: snapshot.val().Candy1.Price, photo: atob(snapshot.val().Candy1.Image)});
        // setCandy2({name: snapshot.val().Candy2.Name, price: snapshot.val().Candy2.Price, photo: atob(snapshot.val().Candy2.Image)});

        // setCandy1({name: snapshot.val().Candy1.Name, price: snapshot.val().Candy1.Price});
        setCandy2({name: snapshot.val().Candy2.Name, price: snapshot.val().Candy2.Price});
      }
      else {
        console.log("No data available");
      }
    }).catch((error) => {
      console.error(error);
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
      console.log(file)
      if(file && file.type.startsWith('image/')){
        const reader = new FileReader();
        reader.onloadend = () => {
          const base64String = reader.result
            .replace('data:', '')
            .replace(/^.+,/, '');
          setCandy1({...candy1, photo : file, base64Image : base64String});
        };
        reader.readAsDataURL(file);
      }
      else{
        setSnackbarMessage('Error: you can only select image files!');
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
      if(file && file.type.startsWith('image/')){
          setCandy2({...candy2, photo : file});
      }
      else{
        setSnackbarMessage('Error: you can only select image files!');
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
      setUpdateSuccessful(false);
      setOpen(true);
      setSnackbarMessage('Error: login timeout. Redirecting to login page!');
      setLoginTimeout(true);
      return;
    }
    
    const uid = auth.currentUser.uid;
    
    const newCandy1 = {
      Name: candy1.name,
      Price: candy1.price,
      Image: candy1.base64Image,
    };

    const newCandy2 = {
      Name: candy2.name,
      Price: candy2.price,
    };

    const updates = {};
    updates['/' + uid + '/candyInformation/Candy1'] = newCandy1;
    updates['/' + uid + '/candyInformation/Candy2'] = newCandy2;

    update(dbRef, updates).then( (update) => {
      console.log(update);
      setUpdateSuccessful(true);
      setOpen(true);
      setSnackbarMessage('Update successful!');
    }).catch((error) => {
      console.error(error);
      setUpdateSuccessful(false);
      setOpen(true);
      setSnackbarMessage(error);
    })

    setEditingCandy1(false);
    setEditingCandy2(false); 
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
          <Typography variant="h4" style={{fontFamily: 'AbrilFatface'}}>Edit Candies 🍬</Typography>
            <Paper 
              elevation={15}
              fullWidth
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
                  onChange={e => setCandy1({...candy1, name: e.target.value})}
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
                  onChange={e => setCandy1({...candy1, price: e.target.value})}
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
                  src={candy1.photo ? URL.createObjectURL(candy1.photo) : process.env.PUBLIC_URL + '/candyImages/Undefined.png'}
                  alt={candy1.name}
                  onClick={handleImageUpload1}
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
                <Typography variant="h7" sx={{fontFamily: 'PlaypenSans'}} style={{marginTop: '2.25%'}} >👈 Candy image</Typography>
              </Stack>
            </Paper>
            <Paper 
              elevation={15}
              fullWidth
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
                  onChange={e => setCandy2({...candy2, name: e.target.value})}
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
                  onChange={e => setCandy2({...candy2, price: e.target.value})}
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
                  src={candy2.photo ? URL.createObjectURL(candy2.photo) : process.env.PUBLIC_URL + '/candyImages/Undefined.png'}
                  alt={candy2.name}
                  onClick={handleImageUpload2}
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
                <Typography variant="h7" sx={{fontFamily: 'PlaypenSans'}} style={{marginTop: '2.25%'}} >⬅️ Candy image</Typography>
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
        </Stack>
        <Snackbar open={open} autoHideDuration={6000} onClose={handleClose}>
        <Alert onClose={handleClose} severity={updateSuccessful ? 'success' : "error"} sx={{ width: '100%' }}>
          {snackbarMessage}
        </Alert>
      </Snackbar>
    </Container>
  );
}

export default EditCandy;
