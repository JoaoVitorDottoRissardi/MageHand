import { initializeApp } from "firebase/app";

const firebaseConfig = {
    apiKey: "AIzaSyD_s7uNhswVGllvWXXxRCuFcWgiWMGUwCU",
    authDomain: "quandrix-a938a.firebaseapp.com",
    projectId: "quandrix-a938a",
    storageBucket: "quandrix-a938a.appspot.com",
    messagingSenderId: "540539394133",
    appId: "1:540539394133:web:21991f69b3391780d6dcdc"
};

const app = initializeApp(firebaseConfig);

const authErrorCodes = {
    'auth/email-already-in-use' : "Erro: email já cadastrado!",
    'auth/invalid-email' : "Erro: email inválido!",
    'auth/invalid-password' : "Erro: senha inválida!",
    'auth/weak-password' : "Erro: senha muito fraca!",
    'auth/invalid-login-credentials' : 'Erro: credenciais de login inválidas',
}

export {app, authErrorCodes}
