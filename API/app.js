const express = require('express');
const app = express();
const predictionRoutes = require('./routes/predictionRoutes'); 
const growth_5_6_Routes = require('./routes/growth5_6_Route');
const growth_6_7_Routes = require('./routes/growth6_7_Route');
const growth_7_8_Routes = require('./routes/growth7_8_Route');
const growth_8_9_Routes = require('./routes/growth8_9_Route');
const growth_9_10_Routes = require('./routes/growth9_10_Route');


app.use('/api', predictionRoutes);
app.use('/api', growth_5_6_Routes);
app.use('/', growth_6_7_Routes);
app.use('/api', growth_7_8_Routes);
app.use('/api', growth_8_9_Routes);
app.use('/api', growth_9_10_Routes);

const PORT = 3000;
app.listen(PORT, () => {
  console.log(`Server is running on port ${PORT}`);
});
