import { createClient } from 'redis';
const client = createClient();
const redis = require('redis');

(async () => {
  client.on('error', (err) => console.log("Redis client not connected to the server:", err));
  client.on('connect', ()=> console.log("Redis client connected to the server"));
})();

const holbertonSchools = {
  Portland: 50,
  Seattle: 80,
  'New York': 20,
  Bogota: 20,
  Cali: 40,
  Paris: 2
};

for (const [key, value] of Object.entries(holbertonSchools)) {
  client.hset('HolbertonSchools', key, value, redis.print);
}

client.hgetall('HolbertonSchools', (err, obj) => {
  if (obj) {
    console.log(obj);
  } else {
    throw err;
  }
});
