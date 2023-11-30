import express from 'express';
import bodyParser from 'body-parser';
import { createClient } from 'redis';
import util from 'util';

const listProducts = [
  {
    Id: 1,
    name: 'Suitcase 250',
    price: 50,
    stock: 4
  },
  {
    Id: 2,
    name: 'Suitcase 450',
    price: 100,
    stock: 10
  },
  {
    Id: 3,
    name: 'Suitcase 650',
    price: 350,
    stock: 2
  },
  {
    Id: 4,
    name: 'Suitcase 1050',
    price: 550,
    stock: 5
  },
];

const getItemById = (id) => {
  return listProducts.find(item => item.Id === id);
};

// Server
const app = express();
app.use(bodyParser.json());
const port = 1245;

// Routes
app.get('/list_products', (req, res) => {
  const productList = listProducts.map(item => {
    return {
      itemId: item.Id,
      itemName: item.name,
      price: item.price,
      initialAvailableQuantity: item.stock
    };
  });
  res.send(productList);
});

app.get('/list_products/:itemId', async (req, res) => {
  const itemId = req.params.itemId;
  const item = getItemById(parseInt(itemId));

  if (item) {
    const stock = await getCurrentReservedStockById(itemId);
    const curItem = {
      itemId: item.Id,
      itemName: item.name,
      price: item.price,
      initialAvailableQuantity: item.stock,
      currentQuantity: stock !== null ? parseInt(stock) : item.stock,
    };
    res.send(curItem);
  } else {
    res.status(404).send({
      "status": "Product not found"
    });
  }
});

app.get('/reserve_product/:itemId', async (req, res) => {
  const itemId = req.params.itemId;
  const curItem = getItemById(parseInt(itemId));

  if (!curItem) {
    res.status(404).send({
      "status": "Product not found"
    });
  } else {
    const stock = await getCurrentReservedStockById(itemId);
    if (stock !== null) {
      stock = parseInt(stock);
      if (stock > 0) {
        reserveStockById(itemId, stock);
        res.status(200).send({
          "status": "Reservation confirmed",
          "itemId": itemId,
        });
      } else {
        res.status(404).send({
          "status": "Not enough stock available",
          "itemId": itemId
        });
      }
    } else {
      reserveStockById(itemId, curItem.stock);
      res.status(200).send({
        "status": "Reservation confirmed",
        "itemId": itemId,
      });
    }
  }
});


// Redis
const client = createClient();
client.get = util.promisify(client.get);

(async () => {
  client.on('error', (err) => {
    console.log(`Redis client not connected to the server: ${err}`);
  });

  client.on('connect', () => {
    console.log('Redis client connected to the server');
  });
})();

const reserveStockById = (itemId, stock) => {
  client.set(itemId, (stock - 1));
};

const getCurrentReservedStockById = async (itemId) => {
  const stockNew = await client.get(itemId);
  return stockNew;
};

app.listen(port, () => {
  console.log(`App listening on port ${port}`)
});
