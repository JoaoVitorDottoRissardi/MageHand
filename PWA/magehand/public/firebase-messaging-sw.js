
// Scripts for firebase and firebase messaging
importScripts('https://www.gstatic.com/firebasejs/9.0.0/firebase-app-compat.js');
importScripts('https://www.gstatic.com/firebasejs/9.0.0/firebase-messaging-compat.js');

const firebaseConfig = {
    apiKey: "AIzaSyBkGsg9PPQ7ACpefGrB83KpSsq-KpOU_js",
    authDomain: "mage-hand-demo.firebaseapp.com",
    databaseURL: "https://mage-hand-demo-default-rtdb.firebaseio.com",
    projectId: "mage-hand-demo",
    storageBucket: "mage-hand-demo.appspot.com",
    messagingSenderId: "39973077999",
    appId: "1:39973077999:web:69799603315d3a1d88ec1a"
  };

firebase.initializeApp(firebaseConfig);

// Retrieve firebase messaging
const messaging = firebase.messaging();

/*
messaging.onBackgroundMessage(function(payload) {
  console.log('Received background message ', payload);

  const notificationTitle = payload.notification.title;
  const notificationOptions = {
    body: payload.notification.body,
  };

  self.registration.showNotification(notificationTitle,
    notificationOptions);
});
*/

messaging.onBackgroundMessage(function (payload) {

    // const fcmChannel = new BroadcastChannel("fcm-channel");
    // fcmChannel.postMessage(payload);
    
    const promiseChain = clients
        .matchAll({
            type: "window",
            includeUncontrolled: true
        })
        .then(windowClients => {
            for (let i = 0; i < windowClients.length; i++) {
                const windowClient = windowClients[i];
                windowClient.postMessage(payload);
            }
        })
        .then(() => {
            return registration.showNotification("New Message");
        });
    return promiseChain;
});
/*
self.addEventListener('notificationclick', function (event) {
    console.log('notification received: ', event)
});
*/