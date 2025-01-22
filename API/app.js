const express = require('express');
const app = express();
const predictionRoutes = require('./routes/predictionRoutes'); 
const growth_5_6_Routes = require('./routes/growth5_6_Route');
const growth_6_7_Routes = require('./routes/growth6_7_Route');

app.use('/api', predictionRoutes);
app.use('/api', growth_5_6_Routes);
app.use('/', growth_6_7_Routes);

const PORT = 3000;
app.listen(PORT, () => {
  console.log(`Server is running on port ${PORT}`);
});
