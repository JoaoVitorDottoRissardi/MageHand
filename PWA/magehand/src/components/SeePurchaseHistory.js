import React, { useState, useEffect } from 'react';
import { Container, Typography, Box, Paper } from '@mui/material';

function SeePurchaseHistory() {
  const [purchaseHistory, setPurchaseHistory] = useState([]);

  useEffect(() => {
    // const user = firebase.auth().currentUser;

    // if (user) {
    //   const userId = user.uid;
    //   // Replace 'your/database/path' with the actual path to your purchase history data
    //   const dbRef = firebase.database().ref(`users/${userId}/purchaseHistory`);

    //   dbRef.on('value', snapshot => {
    //     const data = snapshot.val();
    //     if (data) {
    //       // Convert the data into an array for sorting
    //       const purchaseArray = Object.values(data);

    //       // Sort the purchases by timestamp (most recent first)
    //       purchaseArray.sort((a, b) => b.timestamp - a.timestamp);

    //       setPurchaseHistory(purchaseArray);
    //     }
    //   });
    // }
  }, []);

  return (
    <Container maxWidth="sm">
      <Typography variant="h4">Purchase History</Typography>
      {purchaseHistory.map((purchase, index) => (
        <Paper key={index} elevation={3} style={{ padding: '1rem', margin: '1rem 0' }}>
          <Typography variant="h6">Purchase Date: {new Date(purchase.timestamp).toLocaleString()}</Typography>
          <Typography>Quantity of Candies: {purchase.quantity}</Typography>
          <Typography>Price Paid: ${purchase.price}</Typography>
          <Typography>Purchase Status: {purchase.status}</Typography>
        </Paper>
      ))}
    </Container>
  );
}

export default SeePurchaseHistory;
