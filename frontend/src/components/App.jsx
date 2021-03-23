import React from 'react';
import Cookies from 'universal-cookie/es6';

// React form
class MyForm extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      url: '',
      bearers: [],
      shortName: '',
      mediumName: '',
      shortDescription: '',
      link: '',
      fqdn: '',
      serviceIdentifier: '',
      logo: '',
      errors: {}
    };
  }

  //Returns True if fields are valid and updates states.errors
  validator () {
    let fields = this.state;
    let errors = {};
    let isFormValid = true;

    //short name - 8 chars max
    if (!fields["shortName"]) {
      isFormValid = false;
      errors["shortName"] = "Required!";
    }
    if (typeof fields["shortName"] !== "undefined") {
      if (fields["shortName"].length > 8) {
        isFormValid = false;
        errors["shortName"] = "Maximum eight (8) characters.";
      }
    }

    //mediumname - 16 chars max
    if (!fields["mediumName"]) {
      isFormValid = false;
      errors["mediumName"] = "Required!";
    }
    if (typeof fields["mediumName"] !== "undefined") {
      if (fields["mediumName"].length > 16) {
        isFormValid = false;
        errors["mediumName"] = "Maximum sixteen (16) characters.";
      }
    }
    this.setState({errors: errors});
    return isFormValid;
   }

  componentDidMount() {
    fetch('/api/services/')
      .then((response) => response.json())
      .then((json) => {
        const service = json[0];
        if (service !== undefined) {
          const {
            url, bearers, short_name: shortName, medium_name: mediumName,
            short_description: shortDescription, link, fqdn,
            service_identifier: serviceIdentifier, logo,
          } = service;
          this.setState({
            url,
            bearers,
            shortName,
            mediumName,
            shortDescription,
            link,
            fqdn,
            serviceIdentifier,
            logo,
          });
        }
      });
  }

  myChangeHandler(event) {
    const { name } = event.target;
    const { value } = event.target;
    this.setState({ [name]: value });
  }

  mySubmitHandler(event) {
    event.preventDefault();
    if (this.validator()){
      const form = event.target;
      const data = new FormData(form);

      const cookies = new Cookies();

      const { url } = this.state;
      if (url === '') {
        fetch('/api/services/', {
          method: 'POST',
          headers: {
            'X-CSRFToken': cookies.get('csrftoken'),
          },
          body: data,
        }).then((r) => r.json())
          .then((json) => {
            console.log(json);
          });
      } else {
        fetch(url, {
          method: 'PUT',
         headers: {
           'X-CSRFToken': cookies.get('csrftoken'),
         },
         body: data,
        }).then((r) => {
         if (!r.ok) {
            throw r;
         }
          return r.json();
       }).then((json) => {
         console.log(json);
       }).catch((err) => {
         err.text().then((errorMessage) => {
           alert(errorMessage);
         });
       });
     }
    }
  }

  render() {
    const {
      shortName, mediumName, shortDescription, link, logo, fqdn, serviceIdentifier,
    } = this.state;
    return (
      <form onSubmit={this.mySubmitHandler.bind(this)}>
        <h2>Name</h2>
        <label htmlFor="shortname">Short name (8 chars) </label>
        <br />
        <input
          value={shortName}
          type="text"
          name="short_name"
          id="shortname"
          onChange={this.myChangeHandler.bind(this)}
        />
        <span style={{color: "red"}}>{this.state.errors["shortName"]}</span>
        <br />
        <label htmlFor="mediumname">Medium name (16 chars) </label>
        <br />
        <input
          value={mediumName}
          type="text"
          id="mediumname"
          name="medium_name"
          onChange={this.myChangeHandler.bind(this)}
        />
        <span style={{color: "red"}}>{this.state.errors["mediumName"]}</span>
        <br />
        <h2>Description</h2>
        <label htmlFor="desc">Short description (180 chars)</label>
        <br />
        <textarea
          value={shortDescription}
          id="desc"
          name="short_description"
          onChange={this.myChangeHandler.bind(this)}
        />
        <br />

        <h2>Link</h2>
        <label htmlFor="link">Website link</label>
        <br />
        <input
          value={link}
          type="text"
          id="link"
          name="link"
          onChange={this.myChangeHandler.bind(this)}
        />
        <br />

        <h2>Logo</h2>
        <label htmlFor="logo">Image type: jpeg, image size: 600 x 600 px</label>
        <br />
        <input type="file" name="logo" id="logo" onChange={this.myChangeHandler.bind(this)} />
        <br />
        {logo !== null && logo.startsWith('file://') && <img alt="Logo" src={logo} />}

        <h2>Bearers</h2>
        <h2>RadioDNS Parameters</h2>
        <label htmlFor="fqdn">FQDN</label>
        <br />
        <input value={fqdn} type="text" name="fqdn" id="fqdn" onChange={this.myChangeHandler.bind(this)} />
        <br />

        <label htmlFor="service_identifier">Service Identifier</label>
        <br />
        <input
          value={serviceIdentifier}
          type="text"
          name="service_identifier"
          id="fqdn"
          onChange={this.myChangeHandler.bind(this)}
        />
        <br />

        <input type="submit" value="SAVE" />
      </form>
    );
  }
}

export default MyForm;