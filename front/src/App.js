
import './assets/css/App.css';
import React, { useState } from 'react'

import { createMuiTheme, ThemeProvider } from '@material-ui/core/styles';
import { dark, light } from "./assets/js/themes"
import LegendWrapper from "./components/LegendWrapper"

import UploadPage from "./components/UploadPage"
import heatmap from "./assets/heatmap"
import DiagnosisPage from "./components/handleResponse/DiagnosisPage"



function App() {

  const [files, setFiles] = useState([]);
  const [diagnosis, setDiagnosis] = useState({})
  const [darkTheme, setDarkTheme] = useState(true)

  const theme = createMuiTheme({
    background: 'linear-gradient(45deg, #2196f3 30%, rgb(175, 61, 228) 90%)',
    palette: {
      type: darkTheme ? 'dark' : 'light'
    },
    nivo: darkTheme ? dark : light,
    appbar: darkTheme ? "#424242" : "#3f51b5"
  });

  const filesUpload = () => {
    const formData = new FormData()
    var n = 1
    Object.keys(files).forEach((key) => {
      const file = files[key]
      formData.append('file' + n, new Blob([file], { type: file.type }), file.name || 'file')
      n += 1
    })
    //Check that the correct files will be submited
    for (var value of formData.values()) { console.log(value); }
    fetch("/uploadData", { method: 'POST', body: formData})
      .then((response) => response.json())
      .then((json) => {
        json.heatmap = heatmap
        setDiagnosis(json)
      })
      .catch((error) => alert(error))

  }


  return (

    <ThemeProvider theme={theme}>
      <LegendWrapper setDarkTheme={setDarkTheme}
        darkTheme={darkTheme} />

      {diagnosis.leads ?
        <DiagnosisPage diagnosis={diagnosis} /> :
        <UploadPage setFiles={setFiles}
          filesUpload={filesUpload} />}

    </ThemeProvider>
  );
}

export default App;
