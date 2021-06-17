import React, { Component } from 'react';
import Files from 'react-files'
import "../assets/css/FileComponent.css"
import { Grid } from "@material-ui/core"
import { withTheme } from '@material-ui/core/styles';

class FilesComponent extends Component {

  constructor(props) {
    super(props)
    this.state = {
      files: []
    }
    this.getAcceptance.bind(this)
    this.onFilesChange.bind(this)
  }

  onFilesChange = (files) => {
    this.setState({
      files
    }, () => {
      this.props.setCount(this.state.files.length)
      this.props.setFiles(this.state.files)
    })
  }

  onFilesError = (error, file) => {
    console.log('error code ' + error.code + ': ' + error.message)
  }

  filesRemoveOne = (file) => {
    this.refs.files.removeFile(file)
  }

  filesRemoveAll = () => {
    this.refs.files.removeFiles()
  }



  getAcceptance = () => {
    if (this.state.files.length === 0) {
      return ['.hea', '.mat',]
    } else if (this.state.files.length === 1) {
      if (this.state.files[0].name.includes(".mat")) {
        return [".hea"]
      } else {
        return [".mat"]
      }
    }
  }

  render() {
    return (
      <div className="container">
        <Files
          ref={"files"}
          className={this.state.files.length === 0 ? 'files-dropzone-list' : 'files-dropzone-list-shrinked'}
          onChange={this.onFilesChange}
          onError={this.onFilesError}
          multiple
          style={{ backgroundColor: this.props.theme.palette.background.paper }}
          maxFiles={2}
          maxFileSize={10000000}
          minFileSize={0}
          clickable
          accepts={this.getAcceptance()}
        >
          <p>
            Drag your ECG into the application (.hea and .mat files)
                </p>
          <p>
            Click here to open your file browser
                </p>
        </Files>

        {
          this.state.files.length > 0
            ? <Grid container className='files-list'>
              {this.state.files.map((file) =>
                <Grid item key={file.id}>
                  <div className='files-list-item' key={file.id}>
                    <div className='files-list-item-preview'>
                      {file.preview.type === 'image'
                        ? <img className='files-list-item-preview-image' src={file.preview.url} alt="preview" />
                        : <div className='files-list-item-preview-extension' >{file.extension}</div>}
                    </div>
                    <div className='files-list-item-content'>
                      <div className='files-list-item-content-item files-list-item-content-item-1'>{file.name}</div>
                      <div className='files-list-item-content-item files-list-item-content-item-2'>{file.sizeReadable}</div>
                    </div>
                    <div
                      id={file.id}
                      className='files-list-item-remove'
                      onClick={this.filesRemoveOne.bind(this, file)} // eslint-disable-line
                    />
                  </div>
                </Grid>
              )}
            </Grid>
            : null
        }
      </div>
    )
  }
}

export default withTheme(FilesComponent);

