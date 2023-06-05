import React, { Component } from 'react';
import './App.css';

class App extends Component {
  state = {
    /*codeText: [],*/
    translation: [],
    output: []
  };

  componentDidMount() {
    this.getCodeText();
  }


  getCodeText() {
    fetch('/Python')
      .then(res => res.json())
      .then(codeText => this.setState({ codeText }));
  }

  DoTranslate = () => {
    const englBox = document.getElementById('ToTranslate');
    const EnglCode = englBox.value;
    const textBox = document.getElementById('Translation');
    const Language1Box = document.getElementById('Language1');
    const Language1 = Language1Box.value;
    const Language2Box = document.getElementById('Language2');
    const Language2 = Language2Box.value;

    fetch('/Python', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ code: EnglCode, lang1: Language1, lang2: Language2 })
    })
      .then(response => {
        if (response.ok) {
          console.log('Translation request sent successfully');
          return response.json();
        } else {
          throw new Error('Error: ' + response.status);
        }
      })
      .then(data => {
        console.log('Response from backend:', data.result);
        if (textBox) {
          textBox.value = data.result;
        }
      })
      .catch(error => {
        console.error('Error:', error);
      });
  };

    DoExecuteOriginal = () => {
      const CodeToRun = document.getElementById('ToTranslate').value;
      const outputTextBox = document.getElementById('outputTextBox1');
      const Language1Box = document.getElementById('Language1');
      const Language1 = Language1Box.value;
        
      fetch('/RunCode', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ code: CodeToRun, lang: Language1 })
      })
        .then(response => {
          if (response.ok) {
            console.log('Execution request sent successfully');
            return response.json();
          } else {
            throw new Error('Error: ' + response.status);
          }
        })
        .then(data => {
          console.log('Result from backend:', data.result);
          if (outputTextBox) {
            outputTextBox.value = data.result;
          }
        })
        .catch(error => {
          console.error('Error:', error);
        });
    };
    
  DoExecuteForeign = () => {
    const CodeToRun = document.getElementById('Translation').value;
    const outputTextBox = document.getElementById('outputTextBox2');
    const Language1Box = document.getElementById('Language1');
    const Language1 = Language1Box.value;
    const Language2Box = document.getElementById('Language2');
    const Language2 = Language2Box.value;
      
    fetch('/RunCode2', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ code: CodeToRun, lang: Language2 })
    })
      .then(response => {
        if (response.ok) {
          console.log('Execution request sent successfully');
          return response.json();
        } else {
          throw new Error('Error: ' + response.status);
        }
      })
      .then(data => {
        console.log('Result from backend:', data.result);
        if (outputTextBox) {
          outputTextBox.value = data.result;
        }
      })
      .catch(error => {
        console.error('Error:', error);
      });
  };

  render() {
    const { translation } = this.state;

    return (
      <div className="App">
        <div>
          <h1>Python Project</h1>
            <div class="editor">
          <p>
            <select id="Language1" name="Language1">
                <option value="English">English</option>
                <option value="French">French</option>
                <option value="Spanish">Spanish</option>
                <option value="Greek">Greek</option>
                <option value="Mandarin">Mandarin</option>
            </select>
            <label htmlFor="ToTranslate" style={{ verticalAlign: 'top' }}>
                The original
              </label>
            <textarea rows="22" cols="35" id="ToTranslate" name="ToTranslate"></textarea>
          </p>
          <button type="button" onClick={this.DoTranslate}>
            Translate
          </button>
          <p>
            <select id="Language2" name="Language2">
                <option value="French">French</option>
                <option value="Spanish">Spanish</option>
                <option value="Greek">Greek</option>
                <option value="Mandarin">Mandarin</option>
                <option value="English">English</option>
            </select>
            <label htmlFor="Translation" style={{ verticalAlign: 'top' }}>
                Translation
              </label>
            <textarea rows="22" cols="35" id="Translation" name="Translation"></textarea>
          </p>
            </div>

          <p>
            <button type="button" onClick={this.DoExecuteOriginal}>
              Execute
            </button>
            <button type="button" onClick={this.DoExecuteForeign}>
              Execute
            </button>
          </p>
            <div class='outputBoxes'>
            <label htmlFor="outputTextBox1" style={{ verticalAlign: 'top' }}>
                Output Original
              </label>
          <textarea rows="4" cols="35" id="outputTextBox1" name="outputTextBox" readOnly></textarea>
            
            <label htmlFor="outputTextBox2" style={{ verticalAlign: 'top' }}>
                Output Foreign
              </label>
          <textarea rows="4" cols="35" id="outputTextBox2" name="outputTextBox2" readOnly></textarea>
            </div>
        </div>
      </div>
    );
  }
}

export default App;
