import { createClient } from 'redis';
const subscriber = createClient();
const redis = require('redis');

(async () => {
  subscriber.on('error', (err) => console.log("Redis client not connected to the server:", err));
  subscriber.on('connect', ()=> console.log("Redis client connected to the server"));

  subscriber.subscribe('holberton school channel');

  subscriber.on('message', (channel, message) => {
    console.log(message);

    if (message === 'KILL_SERVER') {
      subscriber.unsubscribe('holberton school channel');
      subscriber.quit()
    }
  });
})();
