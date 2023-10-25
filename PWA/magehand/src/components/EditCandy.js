import React, { useState } from 'react';
import { Container, Typography, Grid, Paper, Button, IconButton, TextField, Stack } from '@mui/material';
import EditIcon from '@mui/icons-material/Edit';

function EditCandy() {
  const [candies, setCandies] = useState([
    {
      id: 1,
      name: 'Candy 1',
      price: 1.99,
      photo: 'candy1.jpg',
    },
    {
      id: 2,
      name: 'Candy 2',
      price: 2.49,
      photo: 'candy2.jpg',
    },
    // Add more candies as needed
  ]);

  const [editingCandy, setEditingCandy] = useState(null);

  const handleEditCandy = (candy) => {
    setEditingCandy(candy);
  };

  const handleSaveCandy = (candy) => {
    // Implement logic to save edited candy details
    // Update the candies array with the new details
    setEditingCandy(null); // Clear the editing state
  };

  return (
    <Container maxWidth="lg">
        <Stack spacing={2} direction="column" justifyContent="center" alignItems="center">
            <Typography variant="h4">Edit Candy</Typography>
            <Grid container spacing={2}>
                {candies.map((candy) => (
                <Grid item xs={12} sm={6} md={4} key={candy.id}>
                    <Paper elevation={3}>
                    <img src={candy.photo} alt={candy.name} />
                    {editingCandy === candy ? (
                        <div>
                        <TextField
                            label="Candy Name"
                            value={candy.name}
                            fullWidth
                            // Add onChange handler to update the candy name
                        />
                        <TextField
                            label="Candy Price"
                            type="number"
                            value={candy.price}
                            fullWidth
                            // Add onChange handler to update the candy price
                        />
                        <Button variant="contained" onClick={() => handleSaveCandy(candy)}>
                            Save
                        </Button>
                        </div>
                    ) : (
                        <div>
                        <Typography variant="h6">{candy.name}</Typography>
                        <Typography variant="body1">Price: ${candy.price}</Typography>
                        <IconButton
                            
                            onClick={() => handleEditCandy(candy)}
                            style={{ position: 'absolute', bottom: 8, right: 8 }}
                        >
                            <EditIcon />
                        </IconButton>
                        </div>
                    )}
                    </Paper>
                </Grid>
                ))}
            </Grid>
        </Stack>
    </Container>
  );
}

export default EditCandy;
