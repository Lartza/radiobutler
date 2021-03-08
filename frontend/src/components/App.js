import React, {Component} from "react";
import {render} from "react-dom";

/* React form
class MyForm extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      shortname: "",
      mediumname: "",
      short_description: "",
      link: "",
      logo: "",
      service_identifier: ""
    };
  }
  myChangeHandler = (event) => {
    let name = event.target.name;
    let value = event.target.value;
    this.setState({ [name]: value });
  };
  render() {
    return (
      <form>
        <h1>Edit station info - REACT</h1>
        <h2>Name</h2>
        <label for="shortname">Short name (8 chars) </label>
        <br></br>
        <input type="text" name="shortname" onChange={this.myChangeHandler} />
        <br></br>

        <label for="mediumname">Medium name (16 chars) </label>
        <br></br>
        <input type="text" name="mediumname" onChange={this.myChangeHandler} />
        <br></br>
        <h2>Description</h2>
        <label for="sshort_description">Short description (180 chars)</label>
        <br></br>
        <textarea
          id="desc"
          name="short_description"
          onChange={this.myChangeHandler}
        ></textarea>
        <br></br>

        <h2>Logo</h2>
        <label for="logo">Image type: jpeg, image size: 600 x 600 px</label>
        <br></br>
        <input type="file" name="logo" onChange={this.myChangeHandler} />
        <br></br>

        <h2>Bearers</h2>
        <h2>RadioDNS Parameters</h2>
        <label for="fqdn">FQDN</label>
        <br></br>
        <input type="text" name="fqdn" onChange={this.myChangeHandler} />
        <br></br>

        <label for="fqdn">Service Identifier</label>
        <br></br>
        <input
          type="text"
          name="service_identifier"
          onChange={this.myChangeHandler}
        />
        <br></br>

        <input type="submit" value="SAVE" />
      </form>
    );
  }
}
*/

class App extends Component {
    constructor(props) {
        super(props);
        this.state = {
            data: [],
            loaded: false,
            placeholder: "Loading"
        };
    }

    componentDidMount() {
        fetch("api/helloworld")
            .then(response => {
                if (response.status > 400) {
                    return this.setState(() => {
                        return {placeholder: "Something went wrong!"};
                    });
                }
                return response.json();
            })
            .then(data => {
                this.setState(() => {
                    return {
                        data,
                        loaded: true
                    };
                });
            });
    }

    render() {
        return (
            <span>
                {this.state.data.toString()}
            </span>
        );
    }
}

export default App;

const container = document.getElementById("app");
render(<App/>, container);