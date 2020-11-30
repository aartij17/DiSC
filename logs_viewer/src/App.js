import logo from './logo.svg';
import Button from 'react-bootstrap/Button';
import Container from 'react-bootstrap/Container';
import Col from 'react-bootstrap/Col';
import Row from 'react-bootstrap/Row';
import StateLogCard from './components/StateLogCard';
import { useRef, useState } from 'react';
import './App.css';
import 'bootstrap/dist/css/bootstrap.css';


function App() {
  const [stateLogFile, setStateLogFile] = useState(null);
  const [stateLogs, setStateLogs] = useState([]);

  const updateLogDisplay = (content) => {
    var newLogs = [];
    var log_lines = content.split("\n");
    for (var i = 0; i < log_lines.length; ++i) {
      console.log(log_lines[i]);
      // First, get the round number
      const log_components = log_lines[i].split("|")
      if (log_components.length < 3) {
        continue;
      }
      const round = log_components[0];
      const nodeid = log_components[1];
      log_components.splice(0,2);
      const state = log_components.join();
      // console.log(state);
      // console.log(JSON.parse(state));
      newLogs.push(
        <StateLogCard 
          round={round}
          nodeid={nodeid}
          state={JSON.parse(state)}
        />
      );
    }
    setStateLogs(newLogs);
  }

  const readFileContent = file => {
    const reader = new FileReader()
    return new Promise((resolve, reject) => {
      reader.onload = event => resolve(event.target.result)
      reader.onerror = error => reject(error)
      reader.readAsText(file)
    })
  }

  // On file select (from the pop up) 
  const onFileChange = event => {
    // Update the state 
    setStateLogFile(event.target.files[0]);
  }; 

  // On file upload (click the upload button) 
  const onFileUpload = () => {

    if (stateLogFile && stateLogFile.type == "text/plain") {
      // // Create an object of formData 
      // const formData = new FormData();

      // // Update the formData object 
      // formData.append(
      //   "myFile",
      //   stateLogFile,
      //   stateLogFile.name
      // );
      // Details of the uploaded file 
      console.log(stateLogFile);
      // console.log(formData);
      readFileContent(stateLogFile).then(content => {
        updateLogDisplay(content)
      }).catch(error => console.log(error))
    }


  }; 

  const fileData = () => {

    if (stateLogFile) {

      return (
        <div>
          <h2>File Details:</h2>
          <p>File Name: {stateLogFile.name}</p>
          <p>File Type: {stateLogFile.type}</p>
          <p>
            Last Modified:{" "}
            {stateLogFile.lastModifiedDate.toDateString()}
          </p>
        </div>
      );
    } else {
      return (
        <div>
          <br />
          <h4>Choose before Pressing the Upload button</h4>
        </div>
      );
    }
  }; 

  return (
    <div className="App">
      <Container>
        <Row>
          <Col>
            <input type="file" onChange={onFileChange} />
              <button onClick={onFileUpload}>
                Upload State Log
              </button> 
            {fileData()}
          </Col>
          <Col><Button variant="outline-primary">Upload Network Process Log</Button></Col>
        </Row>
        <Row>
          <Col>
            {stateLogs}
          </Col>
          <Col>
            
            <StateLogCard />
          </Col>
        </Row>
      </Container>
    </div>
  );
}

export default App;
