import { initializeApp } from "firebase/app";

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

export {app, authErrorCodes}
