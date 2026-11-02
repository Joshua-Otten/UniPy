const express = require('express')
const fetch = require('node-fetch')
const path = require('path');

const app = express()

app.use(express.static(path.join(__dirname, 'client/build')));
app.use(express.json());

// MUST INSTALL:  npm install body-parser
const bodyParser = require('body-parser');
const fs = require('fs');

var result = [''];

const {exec} = require('child_process');


app.get('/Translate', (req, res) => {
    res.json(result)
})

// NOTE:  CHATGPT HELPED EXTENSIVELY ON THIS FUNCTION
// this is for translation
app.post('/Translate', (req, res) => {
  const code = req.body.code;
  const lang1 = req.body.lang1;
  const lang2 = req.body.lang2;
  console.log('code:', code);
  console.log('lang1:', lang1);
  console.log('lang2:', lang2);

  const filename = 'code1.unipy';

  fs.writeFile(filename, code, (error) => {
    if (error) {
      console.error('Error writing Python code to file:', error);
      res.status(500).json({ error: 'Error writing Python code to file' });
      return;
    }

    console.log('Python code written to file:', filename);

    exec(`python3 StringCodeTranslator.py code1.unipy `+lang1+` `+lang2+` .unipy`, (error, stdout, stderr) => {
      if (error) {
        console.error('Error translating Python code:', error);
        console.error('stderr:', stderr);
        res.status(500).json({ error: 'Error translating Python code' });
        return;
      }

      console.log('code1.unipy translated');
      const this_result = stdout;
      console.log('returning:', this_result);

      res.status(200).json({ result: this_result });
    });
  });
});


// this is for execution
app.get('/RunCode',(req, res) => {
    res.json(result)
})
app.post('/RunCode',(req, res) => {
    const code = req.body.code;
    const lang = req.body.lang;
    console.log('language indicated for execution:', lang);
    const filename = 'code1.unipy';

    // FIX: exec must be INSIDE the writeFile callback so the file exists before running Python
    fs.writeFile(filename, code, (error) => {
        if (error) {
            console.error('Error writing Python code to file:', error);
            res.status(500).json({ error: 'Error writing Python code to file' });
            return;
        }

        console.log('Python code written to file:', filename);

        // Executing the foreign code!
        // WARNING:  CONSIDER CYBERSECURITY RISKS OF CODE EXECUTION
        exec(`python3 uniPython.py `+lang+` code1.unipy`, (error, stdout, stderr) => {
            console.log('stdout:', stdout);
            console.log('stderr:', stderr);
            const this_result = [stdout];
            console.log('returning output:',this_result);

            res.status(200).json({ result: this_result });
        });
    });
});

app.post('/RunCode2',(req, res) => {
    const code = req.body.code;
    console.log('code is:',code)
    const lang = req.body.lang;
    console.log('language indicated for execution:', lang);
    const filename = 'code2.unipy';

    // FIX: exec must be INSIDE the writeFile callback so the file exists before running Python
    fs.writeFile(filename, code, (error) => {
        if (error) {
            console.error('Error writing Python code to file:', error);
            res.status(500).json({ error: 'Error writing Python code to file' });
            return;
        }

        console.log('Python code written to file:', filename);

        // Executing the foreign code!
        // WARNING:  CONSIDER CYBERSECURITY RISKS OF CODE EXECUTION
        exec(`python3 uniPython.py `+lang+` code2.unipy`, (error, stdout, stderr) => {
            console.log('stdout:', stdout);
            console.log('stderr:', stderr);
            const this_result = [stdout];
            console.log('returning output:',this_result);

            res.status(200).json({ result: this_result });
        });
    });
});


// The "catchall" handler: for any request that doesn't
// match one above, send back React's index.html file.
app.get('*', (req, res) => {
  res.sendFile(path.join(__dirname+'/client/build/index.html'));
});

module.exports = app;
