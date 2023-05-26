const express = require('express')
const fetch = require('node-fetch')
const path = require('path');
//const admin = require('firebase-admin'); // uncomment to use Firebase
const app = express()

app.use(express.static(path.join(__dirname, 'client/build')));
app.use(express.json());

// MUST INSTALL:  npm install body-parser
const bodyParser = require('body-parser');
const fs = require('fs');
//app.use(bodyParser.json());
//app.use(bodyParser.urlencoded({ extended: true }));


// Firebase starter code appears below

// let serviceAccount = require('[YOUR JSON FILE PATH HERE]');
// admin.initializeApp({
// credential: admin.credential.cert(serviceAccount)
// });
// let db = admin.firestore();

//const codeText = ["print('Hello World')"];

var result = [''];

// this code seems to correctly run a simple Python program and store the output in teh "result" variable
const { exec } = require('child_process');
exec('python test_proc.py', (error, stdout, stderr) => {
    result = [stdout];
    console.log(result);
});

//for testing
/*
app.get('/', (req, res) => {
  res.send('Hello World!')
})*/

app.get('/Python', (req, res) => {
    //res.json(codeText)
    // gets the value of "result" after execution of the py program above
    res.json(result)
})

// NOTE:  CHATGPT HELPED EXTENSIVELY ON THIS FUNCTION
// this is for translation
app.post('/Python', (req, res) => {
  const code = req.body.code;
  console.log('code:', code);

  const filename = 'code.py';

  fs.writeFile(filename, code, (error) => {
    if (error) {
      console.error('Error writing Python code to file:', error);
      res.status(500).json({ error: 'Error writing Python code to file' });
      return;
    }

    console.log('Python code written to file:', filename);

    exec(`python StringCodeTranslator.py code.py English French .frpy`, (error, stdout, stderr) => {
      if (error) {
        console.error('Error translating Python code:', error);
        res.status(500).json({ error: 'Error translating Python code' });
        return;
      }
      
      console.log('code.py translated');
      const this_result = stdout.trim(); // Assign the result to the variable and remove leading/trailing whitespace
      console.log('returning:', this_result);
      
      // Send the result to the frontend
      res.status(200).json({ result: this_result });
    });
  });
});


// this is for execution
app.get('/RunCode',(req, res) => {
    res.json(result)
})
app.post('/RunCode',(req, res) => {
    // Executing the french code!
    // WARNING:  CONSIDER CYBERSECURITY RISKS OF CODE EXECUTION
    let this_result = ''
    exec(`python frpython.py code.frpy`, (error, stdout, stderr) => {
        this_result = [stdout];
        console.log('returning output:',this_result);
        
        // Send the result to the frontend
        res.status(200).json({ result: this_result });
    });
});

// The "catchall" handler: for any request that doesn't
// match one above, send back React's index.html file.
app.get('*', (req, res) => {
  res.sendFile(path.join(__dirname+'/client/build/index.html'));
});

module.exports = app;
