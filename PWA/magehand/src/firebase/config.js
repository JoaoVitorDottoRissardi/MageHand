import { initializeApp } from "firebase/app";
import { getMessaging, getToken, onMessage } from "firebase/messaging";


const firebaseConfig = {
    apiKey: "AIzaSyBkGsg9PPQ7ACpefGrB83KpSsq-KpOU_js",
    authDomain: "mage-hand-demo.firebaseapp.com",
    databaseURL: "https://mage-hand-demo-default-rtdb.firebaseio.com",
    projectId: "mage-hand-demo",
    storageBucket: "mage-hand-demo.appspot.com",
    messagingSenderId: "39973077999",
    appId: "1:39973077999:web:69799603315d3a1d88ec1a"
  };

const app = initializeApp(firebaseConfig);
const messaging = getMessaging(app);

export const getTken = (setTokenFound) => {
  return getToken(messaging, {vapidKey: 'BFtz_VKNIQIE4AEGu4FDPFNycZJlJhFSYhwzgTd5m1pBdCEJfGv2KedI6GySvxDj6MPGDMoRzQa2LahabnRhZNI'}).then((currentToken) => {
    if (currentToken) {
      setTokenFound(true);
      return currentToken;
      // Track the token -> client mapping, by sending to backend server
      // show on the UI that permission is secured
    } else {
      console.log('No registration token available. Request permission to generate one.');
      setTokenFound(false);
      // shows on the UI that permission is required 
    }
  }).catch((err) => {
    console.log('An error occurred while retrieving token. ', err);
    // catch error while creating client token
  });
}

// export const onMessageListener = () =>
//   new Promise((resolve) => {
//     onMessage(messaging, (payload) => {
//       resolve(payload);
//     });
// });

const authErrorCodes = {
  'auth/email-already-in-use' : "Error: email already in use!",
  'auth/invalid-email' : "Error: invalid email!",
  'auth/invalid-password' : "Error: invalid password!",
  'auth/weak-password' : "Error: weak password!",
  'auth/invalid-login-credentials' : 'Error: invalid login credentials!',
  'auth/missing-password': 'Error: missing password!',
  'auth/too-many-requests': 'Error: too many requests, login temporarily blocked!',
  'auth/requires-recent-login': 'Error: login timeout. Redirecting to login page!',
}

const storageErrorCodes = {
  'storage/object-not-found' : "Warning: candy image was not found. Please set up one."
}

export {app, messaging, authErrorCodes, storageErrorCodes}
