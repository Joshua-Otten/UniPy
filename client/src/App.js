import React, { Component } from 'react';
import './App.css';

class App extends Component {
  state = {
    selectedLang1: 'English',
    selectedLang2: 'Spanish',
    translation: [],
    output: []
  };

  componentDidMount() {
    this.getCodeText();
    // Add event listener for Tab key in the textareas
      const textarea1 = document.getElementById('ToTranslate');
      textarea1.addEventListener('keydown', this.handleTabKey);
      textarea1.addEventListener('keydown', this.handleEnterKey);
      const textarea2 = document.getElementById('Translation');
      textarea2.addEventListener('keydown', this.handleTabKey);
  }

  getCodeText() {
    fetch('/Python')
      .then(res => res.json())
      .then(codeText => this.setState({ codeText }));
  }
    
    Swap = () => {
        
        // swap what's in the editor boxes
        const box1 = document.getElementById('ToTranslate');
        const code1 = box1.value;
        const box2 = document.getElementById('Translation');
        const code2 = box2.value;
        
        box1.value = code2;
        box2.value = code1;
        
        // swap the languages
        const lang1 = document.getElementById('Language1');
        const lang2 = document.getElementById('Language2');
        const temp = lang1.value;
        lang1.value = lang2.value;
        lang2.value = temp;
        
    }
    

  DoTranslate = () => {
    const englBox = document.getElementById('ToTranslate');
    const EnglCode = englBox.value;
    const textBox = document.getElementById('Translation');
    const Language1Box = document.getElementById('Language1');
    const Language1 = Language1Box.value;
    const Language2Box = document.getElementById('Language2');
    const Language2 = Language2Box.value;

    fetch('/Translate', {
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
    changeLanguage1 = (event) => {
        this.setState({ selectedLang1: event.target.value });
    };
    changeLanguage2 = (event) => {
        this.setState({ selectedLang2: event.target.value });
    };
    // NOTE: CHATGPT helped extensively with these next two functions
    handleTabKey = (event) => {
      if (event.key === 'Tab') {
        event.preventDefault();

        const textarea = event.target;
        const { selectionStart, selectionEnd, value } = textarea;
        const tabCharacter = '\t';

        // Insert a tab character at the current caret position
        textarea.value =
          value.substring(0, selectionStart) +
          tabCharacter +
          value.substring(selectionEnd);

        // Adjust the caret position
        textarea.selectionStart = textarea.selectionEnd = selectionStart + tabCharacter.length;
      } else if (event.key === 'Enter') {
        event.preventDefault();

        const textarea = event.target;
        const { selectionStart, value } = textarea;
        const tabCount = this.countPreviousTabs(value, selectionStart);
        const tabCharacters = '\t'.repeat(tabCount);

        // Insert new line with tabs at the current caret position
        textarea.value =
          value.substring(0, selectionStart) +
          '\n' +
          tabCharacters +
          value.substring(selectionStart);

        // Adjust the caret position
        textarea.selectionStart = textarea.selectionEnd = selectionStart + tabCharacters.length + 1;
      }
    };

    countPreviousTabs = (value, position) => {
      let tabCount = 0;
      let lineStart = value.lastIndexOf('\n', position - 1) + 1;

      for (let i = lineStart; i < position; i++) {
        if (value[i] === '\t') {
          tabCount++;
        } else {
          break;
        }
      }
      return tabCount;
    };

    
    

  render() {
    const { translation } = this.state;

    return (
            <div className="App">
              <div>
                <h1>UniPy</h1>
                
            <div className="translate">
            <button type="button" onClick={this.DoTranslate} style={{ fontSize: '1.2em', padding: '5px' }}>
                    Translate &rarr;
                  </button>
                </div>
            <div className="swapButton">
            <button type="button" onClick={this.Swap} style={{fontSize: '0.75em', padding: '5px' }}>Swap</button>
            </div>
            <div className="Language">
            <select id="Language1" name="Language1" onChange={this.changeLanguage1}>
                <option value="English">English</option>
                <option value="Spanish">Spanish</option>
                <option value="French">French</option>
                <option value="Greek">Greek</option>
                <option value="Hindi">Hindi</option>
                <option value="Bengali">Bengali</option>
                <option value="Mandarin">Mandarin</option>
                <option value="Kurdish">Kurdish</option>
              </select>

            <select id="Language2" name="Language2" onChange={this.changeLanguage2}>
                <option value="Spanish">Spanish</option>
                <option value="French">French</option>
                <option value="Greek">Greek</option>
                <option value="Hindi">Hindi</option>
                <option value="Bengali">Bengali</option>
                <option value="Mandarin">Mandarin</option>
                <option value="Kurdish">Kurdish</option>
                <option value="English">English</option>
              </select>
            </div>
            <div className="editor">
              <p>
                <label htmlFor="ToTranslate" style={{ verticalAlign: 'top' }}>
                </label>
                <textarea rows="22" cols="35" id="ToTranslate" name="ToTranslate" className={this.state.selectedLang1 === 'Kurdish' ? 'rtl-textbox' : ''}></textarea>
                      </p>
                      <p>
                        <label htmlFor="Translation" style={{ verticalAlign: 'top' }}>
                        </label>
                <textarea rows="22" cols="35" id="Translation" name="Translation" className={this.state.selectedLang2 === 'Kurdish' ? 'rtl-textbox' : ''}></textarea>
                      </p>
            </div>
            <div className="exec">
                  <p>
            <button type="button" onClick={this.DoExecuteOriginal} style={{ fontSize: '1.2em', padding: '5px' }}>
                      Execute
                    </button>
            <button type="button" onClick={this.DoExecuteForeign} style={{ fontSize: '1.2em', padding: '5px' }}>
                      Execute
                    </button>
                  </p>
                </div>
                <div className="outputBoxes">
                  <label htmlFor="outputTextBox1" style={{ verticalAlign: 'top' }}></label>
                  <textarea rows="4" cols="35" id="outputTextBox1" name="outputTextBox" readOnly></textarea>

                  <label htmlFor="outputTextBox2" style={{ verticalAlign: 'top' }}></label>
                  <textarea rows="4" cols="35" id="outputTextBox2" name="outputTextBox2" readOnly></textarea>
                </div>
              </div>
            </div>

            
    );
  }
}

export default App;
