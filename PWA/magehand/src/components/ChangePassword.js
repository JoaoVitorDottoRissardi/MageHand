import React, { useState, useEffect } from 'react';
import { Container, Typography, TextField, Button, Stack } from '@mui/material';

function ChangePassword() {
  const [newPassword, setNewPassword] = useState('');

  // Fetch current user's email to reauthenticate later
  useEffect(() => {
    // const user = firebase.auth().currentUser;
    // if (user) {
    //   setNewPassword('');
    // }
  }, []);

  const updatePassword = () => {
    // const user = firebase.auth().currentUser;
    // if (user) {
    //   user
    //     .updatePassword(newPassword)
    //     .then(() => {
    //       // Password updated successfully
    //     })
    //     .catch(error => {
    //       console.error('Error updating password:', error);
    //     });
    // }
  };

  return (
    <Container maxWidth="sm">
        <Stack spacing={2} direction="column" justifyContent="center" alignItems="center">
            <Typography variant="h4">Change Password</Typography>
            <TextField
                label="New Password"
                type="password"
                variant="outlined"
                fullWidth
                value={newPassword}
                onChange={e => setNewPassword(e.target.value)}
                margin="normal"
            />
            <Button variant="contained" fullWidth onClick={updatePassword}>
                Save
            </Button>
        </Stack>
    </Container>
  );
}

export default ChangePassword;
