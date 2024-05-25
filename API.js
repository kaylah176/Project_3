const express = require('express');
const axios = require('./modules/axios');
const app = express();
const port = 3000;

const ZILLOW_API_KEY = '8ff9e4152ab9ce20e55663fa30e895c0';

app.get('/getZestimate/:propertyId', async (req, res) => {
    const propertyId = req.params.propertyId;
    try {
        const response = await axios.get(`https://api.zillow.com/property/${propertyId}/zestimate`, {
            headers: {
                'Authorization': `Bearer ${ZILLOW_API_KEY}`
            }
        });
        res.json(response.data);
    } catch (error) {
        res.status(500).send(error.toString());
    }
});

app.listen(port, () => {
    console.log(`Server running at http://localhost:${port}`);
});