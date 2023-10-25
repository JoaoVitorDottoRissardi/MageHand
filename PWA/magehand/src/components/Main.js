import React from 'react';
import { NavLink } from 'react-router-dom';
import { Container, Typography, Button, Stack } from '@mui/material';

function Main() {
  return (
    <Container maxWidth="sm">
        <Stack spacing={2} direction="column" justifyContent="center" alignItems="center">
            <Typography variant="h4">Main Screen</Typography>
            <Button variant="contained" fullWidth component={NavLink} to="/editcandy">
                Edit Candy
            </Button>
            <Button variant="contained" fullWidth component={NavLink} to="/editpaymentkeys">
                Edit Payment Keys
            </Button>
            <Button variant="contained" fullWidth component={NavLink} to="/purchasehistory">
                Purchase History
            </Button>
            <Button variant="contained" fullWidth component={NavLink} to="/changepassword">
                Change Password
            </Button>
        </Stack>
    </Container>
  );
}

export default Main;
