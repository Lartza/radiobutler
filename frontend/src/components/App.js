import React, {Component} from "react";
import {render} from "react-dom";
import Cookies from "universal-cookie/es6";

// React form
class MyForm extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      short_name: "",
      medium_name: "",
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

  mySubmitHandler = (event) => {
      event.preventDefault();
      const form = event.target;
      const data = new FormData(form);

      const cookies = new Cookies();

      fetch("/api/services/", {
        method: "POST",
        headers: {
          'X-CSRFToken': cookies.get('csrftoken')
        },
        body: data,

      }).then((response) => response.json())
        .then((data) => {
          console.log(data);
      });
  };

  render() {
    return (
      <form onSubmit={this.mySubmitHandler}>
        <h1>Edit station info - REACT</h1>
        <h2>Name</h2>
        <label htmlFor="shortname">Short name (8 chars) </label>
        <br/>
        <input type="text" name="short_name" onChange={this.myChangeHandler} />
        <br/>

        <label htmlFor="mediumname">Medium name (16 chars) </label>
        <br/>
        <input type="text" id="mediumnane" name="medium_name" onChange={this.myChangeHandler} />
        <br/>
        <h2>Description</h2>
        <label htmlFor="desc">Short description (180 chars)</label>
        <br/>
        <textarea id="desc" name="short_description" onChange={this.myChangeHandler} />
        <br/>

        <h2>Logo</h2>
        <label htmlFor="logo">Image type: jpeg, image size: 600 x 600 px</label>
        <br/>
        <input type="file" name="logo" onChange={this.myChangeHandler} />
        <br/>

        <h2>Bearers</h2>
        <h2>RadioDNS Parameters</h2>
        <label htmlFor="fqdn">FQDN</label>
        <br/>
        <input type="text" name="fqdn" onChange={this.myChangeHandler} />
        <br/>

        <label htmlFor="fqdn">Service Identifier</label>
        <br/>
        <input
          type="text"
          name="service_identifier"
          onChange={this.myChangeHandler}
        />
        <br/>

        <input type="submit" value="SAVE" />
      </form>
    );
  }
}

export default MyForm;

const container = document.getElementById("app");
render(<MyForm/>, container);