import React, { useState, useEffect } from 'react';
import { Container, Typography, TextField, Button, Box, Stack } from '@mui/material';

function EditPaymentKeys() {
  const [paymentKey, setPaymentKey] = useState('');
  const [paymentToken, setPaymentToken] = useState('');
  const [showInstructions, setShowInstructions] = useState(false);

  // Fetch payment keys from Firebase Realtime Database when the component mounts
//   useEffect(() => {
//     // const user = firebase.auth().currentUser;
//     // if (user) {
//     //   const userId = user.uid;
//     //   // Replace 'your/database/path' with your actual database path
//     //   const dbRef = firebase.database().ref(`users/${userId}/paymentKeys`);

//     //   dbRef.once('value')
//     //     .then(snapshot => {
//     //       const data = snapshot.val();
//     //       if (data) {
//     //         setPaymentKey(data.paymentKey || '');
//     //         setPaymentToken(data.paymentToken || '');
//     //       }
//     //     })
//     //     .catch(error => {
//     //       console.error('Error fetching payment keys:', error);
//     //     });
//     // }
//   }, []);

  const toggleInstructions = () => {
    setShowInstructions(!showInstructions);
  };

  const savePaymentKeys = () => {
    // const user = firebase.auth().currentUser;
    // if (user) {
    //   const userId = user.uid;
    //   // Replace 'your/database/path' with your actual database path
    //   const dbRef = firebase.database().ref(`users/${userId}/paymentKeys`);

    //   dbRef
    //     .update({
    //       paymentKey,
    //       paymentToken,
    //     })
    //     .then(() => {
    //       // Keys saved successfully
    //     })
    //     .catch(error => {
    //       console.error('Error saving payment keys:', error);
    //     });
    // }
  };

  return (
    <Container maxWidth="sm">
        <Stack spacing={2} direction="column" justifyContent="center" alignItems="center">
            <Typography variant="h4">Edit Payment Keys</Typography>
            <TextField
                label="Payment Key"
                variant="outlined"
                fullWidth
                value={paymentKey}
                onChange={e => setPaymentKey(e.target.value)}
                margin="normal"
            />
            <TextField
                label="Payment Token"
                variant="outlined"
                fullWidth
                value={paymentToken}
                onChange={e => setPaymentToken(e.target.value)}
                margin="normal"
            />
            <Button variant="contained" fullWidth onClick={savePaymentKeys}>
                Save
            </Button>
            <Button variant="outlined"  fullWidth onClick={toggleInstructions}>
                Help
            </Button>
            {showInstructions && (
                <Box mt={2}>
                Instruction text
                </Box>
            )}
        </Stack>
    </Container>
  );
}

export default EditPaymentKeys;
