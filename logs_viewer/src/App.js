import logo from './logo.svg';
import Button from 'react-bootstrap/Button';
import Container from 'react-bootstrap/Container';
import InputGroup from 'react-bootstrap/InputGroup'
import FormControl from 'react-bootstrap/FormControl'; 
import Col from 'react-bootstrap/Col';
import Row from 'react-bootstrap/Row';
import StateLogCard from './components/StateLogCard';
import LogCard from './components/LogCard';
import { useRef, useState } from 'react';
import './App.css';
import 'bootstrap/dist/css/bootstrap.css';


function App() {
  const [stateLogFile, setStateLogFile] = useState(null);
  const [networkLogFile, setNetworkLogFile] = useState(null);
  const [stateLogs, setStateLogs] = useState([]);
  const [networkLogs, setNetworkLogs] = useState([]);
  const [stateLogFilter, setStateLogfilter] = useState({});
  const [networkLogFilter, setNetworkLogfilter] = useState({});

  const updateLogDisplay = (content, setStateFunc) => {
    var newLogs = [];
    var log_lines = content.split("\n");
    for (var i = 0; i < log_lines.length; ++i) {
      // First, get the round number
      const log_components = log_lines[i].split("|")
      if (log_components.length < 3) {
        continue;
      }
      const round = log_components[0];
      const id = log_components[1];
      log_components.splice(0,2);
      const state = log_components.join();
      // console.log(state);
      // console.log(JSON.parse(state));
      newLogs.push( {
        "round": "" + round,
        "id": "" + id,
        "state": JSON.parse(state)
      }
      );
    }
    setStateFunc(newLogs);
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
  const onLogFileChange = event => {
    // Update the state 
    setStateLogFile(event.target.files[0]);
  }; 

  const onNetworkFileChange = event => {
    setNetworkLogFile(event.target.files[0]);
  }

  const handleFilterChange = (e, key, original_dict, setterFunc) => {
    var new_dict = JSON.parse(JSON.stringify(original_dict))
    console.log(e.target.value, typeof(e.target.value))
    if (e.target.value.length == 0) {
      if (new_dict.hasOwnProperty(key)) {
        delete new_dict[key];
      }
    }
    else {
      new_dict[key] = e.target.value;
    }
    setterFunc(new_dict)
  }

  const cardDisplay = (logs, filter) => {
    // Only display the cards that are not filtered out
    var displayedCards = [];
    for (var i = 0; i < logs.length; ++i) {
      const round = logs[i]["round"];
      const id = logs[i]["id"];
      const state = logs[i]["state"];
      if ((!("round" in filter) || 
          (round.length >= filter["round"].length && filter["round"] == round.substring(0, filter["round"].length))) 
          && 
          (!("id" in filter) || 
          (id.length >= filter["id"].length && filter["id"] == id.substring(0, filter["id"].length))) ) {
        displayedCards.push(
          <LogCard
            round={round}
            id={id}
            state={state}
          />
        );
      }
    }

    return displayedCards;
  }

  // On file upload (click the upload button) 
  const onFileUpload = (logfile, setStateFunc) => {

    if (logfile && logfile.type == "text/plain") {
      // // Create an object of formData 
      // const formData = new FormData();

      // // Update the formData object 
      // formData.append(
      //   "myFile",
      //   logfile,
      //   logfile.name
      // );
      // Details of the uploaded file 
      console.log(logfile);
      // console.log(formData);
      readFileContent(logfile).then(content => {
        updateLogDisplay(content, setStateFunc)
      }).catch(error => console.log(error))
    }


  }; 

  const fileData = (logfile) => {
    if (logfile) {

      return (
        <div>
          <h2>File Details:</h2>
          <p>File Name: {logfile.name}</p>
          <p>File Type: {logfile.type}</p>
          <p>
            Last Modified:{" "}
            {logfile.lastModifiedDate.toDateString()}
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
            <input type="file" onChange={onLogFileChange} />
            <button onClick={() => onFileUpload(stateLogFile, setStateLogs)}>
                Upload State Log
              </button> 
            {fileData(stateLogFile)}
          </Col>
          <Col>
            <input type="file" onChange={onNetworkFileChange} />
            <button onClick={() => onFileUpload(networkLogFile, setNetworkLogs)}>
              Upload Network Log
              </button>
            {fileData(networkLogFile)}
          </Col>
        </Row>
        <Row>
          <Col>
            <InputGroup className="mb-3">
              <InputGroup.Prepend>
                <InputGroup.Text id="basic-addon1">Round</InputGroup.Text>
              </InputGroup.Prepend>
              <FormControl
                placeholder="Round"
                aria-label="Round"
                aria-describedby="basic-addon1"
                onChange={(e) => { handleFilterChange(e, "round", stateLogFilter, setStateLogfilter) }}
                type="number"
              />
            </InputGroup>
          </Col>
          <Col>
            <InputGroup className="mb-3">
              <InputGroup.Prepend>
                <InputGroup.Text id="basic-addon1">Round</InputGroup.Text>
              </InputGroup.Prepend>
              <FormControl
                placeholder="Round"
                aria-label="Round"
                aria-describedby="basic-addon1"
                onChange={(e) => { handleFilterChange(e, "round", networkLogFilter, setNetworkLogfilter) }}
                type="number"
              />
            </InputGroup>
          </Col>
        </Row>

        <Row>
          <Col>
            <InputGroup className="mb-3">
              <InputGroup.Prepend>
                <InputGroup.Text id="basic-addon1">ID</InputGroup.Text>
              </InputGroup.Prepend>
              <FormControl
                placeholder="ID"
                aria-label="ID"
                aria-describedby="basic-addon1"
                onChange={(e) => { handleFilterChange(e, "id", stateLogFilter, setStateLogfilter) }}
              />
            </InputGroup>
          </Col>
          <Col>
            <InputGroup className="mb-3">
              <InputGroup.Prepend>
                <InputGroup.Text id="basic-addon1">ID</InputGroup.Text>
              </InputGroup.Prepend>
              <FormControl
                placeholder="ID"
                aria-label="ID"
                aria-describedby="basic-addon1"
                onChange={(e) => { handleFilterChange(e, "id", networkLogFilter, setNetworkLogfilter) }}
              />
            </InputGroup>
          </Col>
        </Row>

        <Row>
          <Col>
            {cardDisplay(stateLogs, stateLogFilter)}
          </Col>
          <Col>
            {cardDisplay(networkLogs, networkLogFilter)}
          </Col>
        </Row>
      </Container>
    </div>
  );
}

export default App;
