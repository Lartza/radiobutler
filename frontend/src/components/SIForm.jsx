import React from 'react';
import Cookies from 'universal-cookie/es6';
import validator from 'validator';
import ReactModal from 'react-modal';
import { withTranslation } from 'react-i18next';
import PropTypes from 'prop-types';
import GalleryApp from './gallery';
import './i18n';

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
      logoimg: '',
      showModal: false,
      errors: {},
      success: false,
      modified: false,
    };

    this.handleOpenModal = this.handleOpenModal.bind(this);
    this.handleCloseModal = this.handleCloseModal.bind(this);
    this.selectImage = this.selectImage.bind(this);
  }

  componentDidMount() {
    window.addEventListener('beforeunload', this.beforeunload.bind(this));
    fetch('/api/services/')
      .then((response) => response.json())
      .then((json) => {
        const service = json[0];
        if (service !== undefined) {
          const {
            apiurl, bearers, shortName, mediumName,
            shortDescription, link, fqdn,
            serviceIdentifier,
          } = service;
          let { logo } = service;
          if (logo === null) {
            logo = '';
          }
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
          }, this.fetchLogo);
        }
      });
  }

  componentWillUnmount() {
    window.removeEventListener('beforeunload', this.beforeunload.bind(this));
  }

  handleOpenModal() {
    this.setState({ showModal: true });
  }

  handleCloseModal() {
    this.setState({ showModal: false });
  }

  beforeunload(e) {
    const { modified } = this.state;
    if (modified) {
      e.preventDefault();
      e.returnValue = true;
    }
  }

  fetchLogo() {
    const { logo } = this.state;
    if (logo) {
      fetch(logo)
        .then((response) => response.json())
        .then((json) => {
          this.setState({ logoimg: json.image });
        });
    }
  }

  selectImage(event) {
    this.setState({ logo: event.target.getAttribute('data-apiurl'), logoimg: event.target.src, modified: true });
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

    // medium name - 16 chars max
    if (!fields.mediumName) {
      isFormValid = false;
      errors.mediumName = 'Required!';
    }

    // link - 2000 chars max, must be link
    if (fields.link) {
      if (fields.link.length > 2000) {
        isFormValid = false;
        errors.link = 'Maximum 2000 characters.';
      }

      if (!validator.isURL(fields.link, {
        protocols: ['http', 'https'],
        /* eslint-disable camelcase */
        require_protocol: true,
        /* eslint-enable camelcase */
      })) {
        isFormValid = false;
        errors.link = 'Must be a link (must start with http(s)).';
      }
    }

    if (fields.ecc && fields.pi && fields.frequency) {
      // ecc - 2 chars
      if (fields.ecc.length !== 2) {
        isFormValid = false;
        errors.ecc = 'Must be two (2) characters.';
      }

      // pi - 4 chars
      if (fields.pi.length !== 4) {
        isFormValid = false;
        errors.pi = 'Must be four (4) characters.';
      }
    } else if (fields.ecc || fields.pi || fields.frequency) { // All the fields are required, if at least one is filled
      if (!fields.ecc) {
        isFormValid = false;
        errors.ecc = 'Required!';
      }

      if (!fields.pi) {
        isFormValid = false;
        errors.pi = 'Required!';
      }

      if (!fields.frequency) {
        isFormValid = false;
        errors.frequency = 'Required!';
      }
    }

    // ip url - 2000 chars max, must be link
    if (fields.url) {
      if (fields.url.length > 2000) {
        isFormValid = false;
        errors.url = 'Maximum 2000 characters.';
      } else if (!validator.isURL(fields.url, {
        protocols: ['http', 'https'],
        /* eslint-disable camelcase */
        require_protocol: true,
        /* eslint-enable camelcase */
      })) {
        isFormValid = false;
        errors.url = 'Must be a link (must start with http(s)).';
      }
    }

    // fqdn - domain without http
    if (!fields.fqdn) {
      isFormValid = false;
      errors.fqdn = 'Required!';
    } else if (!validator.isFQDN(fields.fqdn)) {
      isFormValid = false;
      errors.fqdn = 'Must be a domain name without protocol.';
    }

    // service identifier - 16 chars max, only lower case and numbers
    if (!fields.serviceIdentifier) {
      isFormValid = false;
      errors.serviceIdentifier = 'Required!';
    } else if (fields.serviceIdentifier.match(/^[a-z0-9]+$/) == null) {
      isFormValid = false;
      errors.serviceIdentifier = 'Only lower case letters and numbers allowed.';
    }

    this.setState({ errors });
    return isFormValid;
  }

  myChangeHandler(event) {
    const { name } = event.target;
    const { value } = event.target;
    const modified = true;
    this.setState({ [name]: value, modified });
  }

  mySubmitHandler(event) {
    event.preventDefault();
    let success = false;
    this.setState({ success });
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
        }).then((r) => {
          if (r.ok) {
            success = true;
            const modified = false;
            this.setState({ success, modified });
          } else {
            throw r;
          }
        }).catch((err) => {
          err.text().then((errorMessage) => {
            const errors = {};
            errors.backend = errorMessage;
            this.setState({ errors });
          });
        });
      } else {
        fetch(apiurl, {
          method: 'PUT',
          headers: {
            'X-CSRFToken': cookies.get('csrftoken'),
          },
          body: data,
        }).then((r) => {
          if (r.ok) {
            success = true;
            const modified = false;
            this.setState({ success, modified });
          } else {
            throw r;
          }
        }).catch((err) => {
          err.text().then((errorMessage) => {
            const errors = {};
            errors.backend = errorMessage;
            this.setState({ errors });
          });
        });
      }
    }
  }

  render() {
    const {
      shortName, mediumName, shortDescription, link, logo, fqdn, platform1, ecc, pi, frequency,
      platform2, url, mimeValue, bitrate, serviceIdentifier, errors, logoimg, showModal, success, modified,
    } = this.state;
    const { t } = this.props;
    return (
      <div>
        {modified && <div className="sticky">{t('form.unsubmitted')}</div>}
        <form onSubmit={this.mySubmitHandler.bind(this)}>

          <p>{t('form.required')}</p>
          <h2>{t('form.name')}</h2>
          <div className="grid-container">
            <div className="grid-item"><label htmlFor="shortname">{t('form.shortName')}</label></div>

            <div className="grid-item">
              <input
                defaultValue={shortName}
                type="text"
                name="shortName"
                id="shortname"
                maxLength="8"
                onChange={this.myChangeHandler.bind(this)}
              />
              <span className="errors">{errors.shortName}</span>
            </div>

            <div className="grid-item"><label htmlFor="mediumname">{t('form.mediumName')}</label></div>

            <div className="grid-item">
              <input
                defaultValue={mediumName}
                type="text"
                id="mediumname"
                name="mediumName"
                maxLength="16"
                onChange={this.myChangeHandler.bind(this)}
              />
              <span className="errors">{errors.mediumName}</span>
            </div>
          </div>

          <h2>{t('form.description')}</h2>
          <div className="grid-container">
            <div className="grid-item"><label htmlFor="desc">{t('form.shortDescription')}</label></div>

            <div className="grid-item">
              <textarea
                defaultValue={shortDescription}
                id="desc"
                name="shortDescription"
                maxLength="180"
                rows="4"
                onChange={this.myChangeHandler.bind(this)}
              />
              <span className="errors">{errors.shortDescription}</span>
            </div>
          </div>

          <h2>{t('form.websiteLink')}</h2>
          <div className="grid-container">
            <div className="grid-item"><label htmlFor="link">{t('form.websiteLink')}</label></div>

            <div className="grid-item">
              <input
                defaultValue={link}
                type="text"
                id="link"
                name="link"
                onChange={this.myChangeHandler.bind(this)}
              />
              <span className="errors">{errors.link}</span>
            </div>
          </div>

          <h2>{t('form.logo')}</h2>
          <div className="grid-container">
            <div className="grid-item">
              <label htmlFor="logo">{t('form.logoDescription')}</label>
              <br />
              <input type="hidden" id="logo" name="logo" value={logo} onChange={this.myChangeHandler.bind(this)} />
              <button type="button" onClick={this.handleOpenModal}>{t('form.openGallery')}</button>
            </div>

            <div className="grid-item">
              <img src={logoimg} alt="Selected logo" width="320" height="auto" />
            </div>
          </div>

          <h2>{t('form.bearers')}</h2>

          <h3>{t('form.bearer1')}</h3>
          <div className="grid-container">
            <div className="grid-item"><label htmlFor="bearer1Platform">{t('form.bearer1platform')}</label></div>

            <div className="grid-item">
              <select
                name="platform1"
                id="bearer1Platform"
                defaultValue={platform1}
                onChange={this.myChangeHandler.bind(this)}
              >
                <option value="fm">{t('form.fm')}</option>
              </select>
            </div>

            <div className="grid-item"><label htmlFor="ecc">{t('form.ecc')}</label></div>

            <div className="grid-item">
              <input
                defaultValue={ecc}
                type="text"
                id="ecc"
                name="ecc"
                maxLength="2"
                onChange={this.myChangeHandler.bind(this)}
              />
              <span className="errors">{errors.ecc}</span>
            </div>

            <div className="grid-item"><label htmlFor="pi">{t('form.pi')}</label></div>

            <div className="grid-item">
              <input
                defaultValue={pi}
                type="text"
                id="pi"
                name="pi"
                maxLength="4"
                onChange={this.myChangeHandler.bind(this)}
              />
              <span className="errors">{errors.pi}</span>
            </div>

            <div className="grid-item"><label htmlFor="frequency">{t('form.frequency')}</label></div>

            <div className="grid-item">
              <input
                defaultValue={frequency}
                type="number"
                step="0.01"
                min="87.0"
                max="108.9"
                id="frequency"
                name="frequency"
                onChange={this.myChangeHandler.bind(this)}
              />
              <span className="errors">{errors.frequency}</span>
            </div>
          </div>

          <h3>{t('form.bearer2')}</h3>
          <div className="grid-container">
            <div className="grid-item"><label htmlFor="bearer2Platform">{t('form.bearer2platform')}</label></div>

            <div className="grid-item">
              <select
                name="platform2"
                id="bearer1Platform"
                defaultValue={platform2}
                onChange={this.myChangeHandler.bind(this)}
              >
                <option value="ip">IP</option>
              </select>
            </div>

            <div className="grid-item"><label htmlFor="url">{t('form.url')}</label></div>

            <div className="grid-item">
              <input
                defaultValue={url}
                type="text"
                id="url"
                name="url"
                onChange={this.myChangeHandler.bind(this)}
              />
              <span className="errors">{errors.url}</span>
            </div>

            <div className="grid-item"><label htmlFor="audio/mpeg">{t('form.mime')}</label></div>

            <div className="grid-item">
              <select name="mimeValue" id="mimeValue" defaultValue={mimeValue}>
                <option value="audio/mpeg">mp3</option>
              </select>
            </div>

            <div className="grid-item"><label htmlFor="bitrate">{t('form.bitrate')}</label></div>

            <div className="grid-item">
              <input
                defaultValue={bitrate}
                type="number"
                id="bitrate"
                name="bitrate"
                min="1"
                max="10000"
                onChange={this.myChangeHandler.bind(this)}
              />
            </div>
          </div>

          <h2>{t('form.parameters')}</h2>
          <div className="grid-container">
            <div className="grid-item"><label htmlFor="fqdn">{t('form.fqdn')}</label></div>

            <div className="grid-item">
              <input defaultValue={fqdn} type="text" name="fqdn" id="fqdn" onChange={this.myChangeHandler.bind(this)} />
              <span className="errors">{errors.fqdn}</span>
            </div>

            <div className="grid-item"><label htmlFor="service_identifier">{t('form.serviceIdentifier')}</label></div>

            <div className="grid-item">
              <input
                defaultValue={serviceIdentifier}
                type="text"
                name="serviceIdentifier"
                id="fqdn"
                maxLength="16"
                onChange={this.myChangeHandler.bind(this)}
              />
              <span className="errors">{errors.serviceIdentifier}</span>
            </div>
          </div>

          <input type="submit" value={t('save')} />
          <span className="errors">{errors.backend}</span>
          {Object.keys(errors).length === 0 && success && <span className="success">{t('form.submitted')}</span>}
          {Object.keys(errors).length > 0 && <span className="errors">{t('form.failed')}</span>}

        </form>
        <ReactModal
          isOpen={showModal}
          contentLabel="Gallery Modal"
        >
          <button type="button" onClick={this.handleCloseModal}>{t('saveClose')}</button>
          <GalleryApp selectImage={this.selectImage} apiurl={logo} useSuspense={false} />
          <button type="button" onClick={this.handleCloseModal}>{t('saveClose')}</button>
        </ReactModal>
      </div>
    );
  }
}

MyForm.propTypes = {
  t: PropTypes.func.isRequired,
};

const FormApp = withTranslation()(MyForm);

export default FormApp;
