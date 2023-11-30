import { createClient } from 'redis';
const client = createClient();
const redis = require('redis');

(async () => {
  client.on('error', (err) => console.log("Redis client not connected to the server:", err));
  client.on('connect', ()=> console.log("Redis client connected to the server"));
})();

function setNewSchool(schoolName, value){
  client.set(schoolName, value, redis.print);
}

async function displaySchoolValue(schoolName){
  await client.get(schoolName, redis.print);
}

displaySchoolValue('Holberton');
setNewSchool('HolbertonSanFrancisco', '100');
displaySchoolValue('HolbertonSanFrancisco');
