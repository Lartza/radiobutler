import React from 'react';
import Cookies from 'universal-cookie/es6';

// React form
class MyForm extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      apiurl: '',
      shortName: '',
      mediumName: '',
      shortDescription: '',
      link: '',
      fqdn: '',
      serviceIdentifier: '',
      logo: '',
      platform1: '',
      ecc: '',
      pi: '',
      frequency: '',
      platform2: '',
      bitrate: '',
      url: '',
      errors: {},
    };
  }

  componentDidMount() {
    fetch('/api/services/')
      .then((response) => response.json())
      .then((json) => {
        const service = json[0];
        if (service !== undefined) {
          const {
            apiurl, bearers, shortName, mediumName,
            shortDescription, link, fqdn,
            serviceIdentifier, logo,
          } = service;
          if (bearers.length > 0) {
            const {
              platform: platform1, ecc, pi, frequency,
            } = bearers[0];
            this.setState({
              platform1,
              ecc,
              pi,
              frequency,
            });
          }
          if (bearers.length > 1) {
            const {
              platform: platform2, url, mimeValue, bitrate,
            } = bearers[1];
            this.setState({
              platform2,
              url,
              mimeValue,
              bitrate,
            });
          }
          this.setState({
            apiurl,
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

  // Returns True if fields are valid and updates states.errors
  validator() {
    const fields = this.state;
    const errors = {};
    let isFormValid = true;

    // short name - 8 chars max
    if (!fields.shortName) {
      isFormValid = false;
      errors.shortName = 'Required!';
    }
    if (typeof fields.shortName !== 'undefined') {
      if (fields.shortName.length > 8) {
        isFormValid = false;
        errors.shortName = 'Maximum eight (8) characters.';
      }
    }

    // mediumname - 16 chars max
    if (!fields.mediumName) {
      isFormValid = false;
      errors.mediumName = 'Required!';
    }
    if (typeof fields.mediumName !== 'undefined') {
      if (fields.mediumName.length > 16) {
        isFormValid = false;
        errors.mediumName = 'Maximum sixteen (16) characters.';
      }
    }
    this.setState({ errors });
    return isFormValid;
  }

  myChangeHandler(event) {
    const { name } = event.target;
    const { value } = event.target;
    this.setState({ [name]: value });
  }

  mySubmitHandler(event) {
    event.preventDefault();
    if (this.validator()) {
      const form = event.target;
      const data = new FormData(form);

      const { apiurl } = this.state;
      const names = ['platform1', 'ecc', 'pi', 'frequency', 'platform2', 'url', 'mimeValue', 'bitrate'];

      if (data.get('ecc') !== '') {
        data.append('bearers[0][platform]', data.get('platform1'));
        data.append('bearers[0][ecc]', data.get('ecc'));
        data.append('bearers[0][pi]', data.get('pi'));
        data.append('bearers[0][frequency]', data.get('frequency'));
        if (apiurl !== '') {
          data.append('bearers[0][service]', apiurl);
        }
      }
      if (data.get('url') !== '') {
        data.append('bearers[1][platform]', data.get('platform2'));
        data.append('bearers[1][url]', data.get('url'));
        data.append('bearers[1][mimeValue]', data.get('mimeValue'));
        data.append('bearers[1][bitrate]', data.get('bitrate'));
        if (apiurl !== '') {
          data.append('bearers[1][service]', apiurl);
        }
      }

      names.forEach((name) => {
        data.delete(name);
      });

      const cookies = new Cookies();

      if (apiurl === '') {
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
        fetch(apiurl, {
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
      shortName, mediumName, shortDescription, link, logo, fqdn, platform1, ecc, pi, frequency,
      platform2, url, mimeValue, bitrate, serviceIdentifier, errors,
    } = this.state;
    return (
      <form onSubmit={this.mySubmitHandler.bind(this)}>
        <h2>Name</h2>
        <label htmlFor="shortname">Short name (max 8 chars) </label>
        <br />
        <input
          defaultValue={shortName}
          type="text"
          name="shortName"
          id="shortname"
          onChange={this.myChangeHandler.bind(this)}
        />
        <span style={{ color: 'red' }}>{errors.shortName}</span>
        <br />
        <label htmlFor="mediumname">Medium name (max 16 chars) </label>
        <br />
        <input
          defaultValue={mediumName}
          type="text"
          id="mediumname"
          name="mediumName"
          onChange={this.myChangeHandler.bind(this)}
        />
        <span style={{ color: 'red' }}>{errors.mediumName}</span>
        <br />
        <h2>Description</h2>
        <label htmlFor="desc">Short description (max 180 chars)</label>
        <br />
        <textarea
          defaultValue={shortDescription}
          id="desc"
          name="shortDescription"
          onChange={this.myChangeHandler.bind(this)}
        />
        <br />

        <h2>Link</h2>
        <label htmlFor="link">Website link</label>
        <br />
        <input
          defaultValue={link}
          type="text"
          id="link"
          name="link"
          onChange={this.myChangeHandler.bind(this)}
        />
        <br />

        <h2>Logo</h2>
        <label htmlFor="logo">Image type: jpeg, size: 600 x 600 px</label>
        <br />
        <input type="file" name="logo" id="logo" onChange={this.myChangeHandler.bind(this)} />
        <br />
        {logo !== null && <img alt="Logo" src={logo} />}

        <h2>Bearers</h2>

        <label htmlFor="bearer1Platform">Bearer 1 platform</label>
        <br />
        <select name="platform1" id="bearer1Platform" defaultValue={platform1} onChange={this.myChangeHandler.bind(this)}>
          <option value="fm">FM-RDS</option>
        </select>
        <br />

        <label htmlFor="ecc">RDS ECC </label>
        <br />
        <input
          defaultValue={ecc}
          type="text"
          id="ecc"
          name="ecc"
          onChange={this.myChangeHandler.bind(this)}
        />
        <br />

        <label htmlFor="pi">RDS PI</label>
        <br />
        <input
          defaultValue={pi}
          type="text"
          id="pi"
          name="pi"
          onChange={this.myChangeHandler.bind(this)}
        />
        <br />

        <label htmlFor="frequency">Frequency (MHz) </label>
        <br />
        <input
          defaultValue={frequency}
          type="number"
          step="0.01"
          id="frequency"
          name="frequency"
          onChange={this.myChangeHandler.bind(this)}
        />
        <br />
        <br />

        <label htmlFor="bearer2Platform">Bearer 2 platform</label>
        <br />
        <select name="platform2" id="bearer1Platform" defaultValue={platform2} onChange={this.myChangeHandler.bind(this)}>
          <option value="ip">IP</option>
        </select>
        <br />

        <label htmlFor="url">IP URL</label>
        <br />
        <input
          defaultValue={url}
          type="text"
          id="url"
          name="url"
          onChange={this.myChangeHandler.bind(this)}
        />
        <br />

        <label htmlFor="audio/mpeg">IP MIME</label>
        <br />
        <select name="mimeValue" id="mimeValue" defaultValue={mimeValue}>
          <option value="audio/mpeg">mp3</option>
        </select>
        <br />

        <label htmlFor="bitrate">IP bitrate (kbps) </label>
        <br />
        <input
          defaultValue={bitrate}
          type="number"
          id="bitrate"
          name="bitrate"
          min="1"
          max="10000"
          onChange={this.myChangeHandler.bind(this)}
        />
        <br />

        <h2>RadioDNS Parameters</h2>
        <label htmlFor="fqdn">FQDN</label>
        <br />
        <input defaultValue={fqdn} type="text" name="fqdn" id="fqdn" onChange={this.myChangeHandler.bind(this)} />
        <br />

        <label htmlFor="service_identifier">Service Identifier</label>
        <br />
        <input
          defaultValue={serviceIdentifier}
          type="text"
          name="serviceIdentifier"
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