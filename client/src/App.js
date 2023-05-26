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

    fetch('/Python', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ code: EnglCode })
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

  DoExecute = () => {
    const outputTextBox = document.getElementById('outputTextBox');

    fetch('/RunCode', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' }
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
          <p>
            <label htmlFor="ToTranslate" style={{ verticalAlign: 'top' }}>
                The original
              </label>
            <textarea rows="4" cols="75" id="ToTranslate" name="ToTranslate"></textarea>
          </p>
          <button type="button" onClick={this.DoTranslate}>
            Translate
          </button>
          <p>
            <label htmlFor="Translation" style={{ verticalAlign: 'top' }}>
                Translation
              </label>
            <textarea rows="4" cols="75" id="Translation" name="Translation"></textarea>
          </p>


          <p>
            <button type="button" onClick={this.DoExecute}>
              Execute
            </button>
          </p>

            <label htmlFor="outputTextBox" style={{ verticalAlign: 'top' }}>
                Output String
              </label>
          <textarea rows="4" cols="75" id="outputTextBox" name="outputTextBox" readOnly></textarea>
        </div>
      </div>
    );
  }
}

export default App;
