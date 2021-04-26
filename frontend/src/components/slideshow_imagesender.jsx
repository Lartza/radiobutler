import React from 'react';
import Cookies from 'universal-cookie/es6';
import validator from 'validator';
import ReactModal from 'react-modal';
import { withTranslation } from 'react-i18next';
import PropTypes from 'prop-types';
import GalleryApp from './gallery';
import './i18n';

ReactModal.setAppElement('#app1');

class ImageSlideSender extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      apiurl: '',
      image: '',
      date: '',
      time: '',
      link: '',
      showModal: false,
      errors: {},
      success: false,
    };

    this.handleOpenModal = this.handleOpenModal.bind(this);
    this.handleCloseModal = this.handleCloseModal.bind(this);
    this.selectImage = this.selectImage.bind(this);
  }

  handleOpenModal() {
    this.setState({ showModal: true });
  }

  handleCloseModal() {
    this.setState({ showModal: false });
  }

  // Returns True if fields are valid and updates states.errors
  validator() {
    const fields = this.state;
    const errors = {};
    let isFormValid = true;

    // image has to be selected before sending
    if (!fields.image) {
      isFormValid = false;
      errors.image = 'Image has to be selected before sending.';
    }

    // api url - 512 chars max, must be link
    if (fields.link) {
      if (fields.link.length > 512) {
        isFormValid = false;
        errors.link = 'Maximum 512 characters.';
      } else if (!validator.isURL(fields.link, {
        protocols: ['http', 'https'],
        /* eslint-disable camelcase */
        require_protocol: true,
        /* eslint-enable camelcase */
      })) {
        isFormValid = false;
        errors.link = 'Must be a link (must start with http(s)).';
      }
    }

    // trigger time - should be later than current time. Both
    // date and time has to be selected, if either one is selected.
    if (fields.date && fields.time) {
      const date = Date.parse(`${fields.date}T${fields.time}`);
      const now = Date.now();

      if (date < now) {
        isFormValid = false;
        errors.date = 'Date and time cannot be in the past.';
      }
    } else if ((fields.date && !fields.time) || (!fields.date && fields.time)) {
      isFormValid = false;
      errors.date = 'Both date and time has to be selected.';
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
    let success = false;
    this.setState({ success });

    if (this.validator()) {
      const form = event.target;
      const data = new FormData(form);
      const cookies = new Cookies();

      if (data.get('date') !== '' && data.get('time') !== '') {
        const date = data.get('date');
        const time = data.get('time');
        data.delete('date');
        data.delete('time');
        const timezoneOffset = (new Date()).getTimezoneOffset() * -1;
        const hours = Math.floor(timezoneOffset / 60);
        const minutes = timezoneOffset % 60;
        data.append('trigger_time',
          `${date}T${time}+${hours < 10 ? '0' : ''}${hours}${minutes < 10 ? '0' : ''}${minutes}`);
      }

      fetch('/api/imageslides/', {
        method: 'POST',
        headers: {
          'X-CSRFToken': cookies.get('csrftoken'),
        },
        body: data,
      }).then((r) => {
        if (r.ok) {
          success = true;
          this.setState({ success });
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

  selectImage(event) { this.setState({ apiurl: event.target.getAttribute('data-apiurl'), image: event.target.src }); }

  render() {
    const {
      apiurl, image, date, time, link, showModal, errors, success,
    } = this.state;
    const { t, tReady } = this.props;

    if (!tReady) return null;

    return (
      <div>
        <h2>Images</h2>
        <div>
          <p>Choose an image from the gallery.</p>
          <button type="button" onClick={this.handleOpenModal}>Open gallery</button>
          <ReactModal
            isOpen={showModal}
            contentLabel="Gallery Modal"
          >
            <button type="button" onClick={this.handleCloseModal}>Save & Close gallery</button>
            <GalleryApp selectImage={this.selectImage} apiurl={apiurl} useSuspense={false} />
            <button type="button" onClick={this.handleCloseModal}>Save & Close gallery</button>
          </ReactModal>
        </div>
        <form onSubmit={this.mySubmitHandler.bind(this)}>

          <label htmlFor="image">Selected image </label>
          <br />
          <br />
          <input type="hidden" id="image" name="image" value={apiurl} onChange={this.myChangeHandler.bind(this)} />
          <img src={image} alt="Selected" height="240" />
          <span className="errors">{errors.image}</span>
          <br />
          <br />
          <label htmlFor="image_link">Link URL </label>
          <div className="tooltip">
            ?
            <span className="tooltiptext">Provide a click-through link for the image</span>
          </div>
          <br />
          <input type="text" id="image_link" name="link" value={link} onChange={this.myChangeHandler.bind(this)} />
          <span className="errors">{errors.link}</span>
          <br />
          <br />
          <label htmlFor="trigger_time">Trigger time </label>
          <div className="tooltip">
            ?
            <span className="tooltiptext">Choose when to show the image</span>
          </div>
          <br />
          <input type="date" id="trigger_time" name="date" value={date} onChange={this.myChangeHandler.bind(this)} />
          <input
            type="time"
            id="trigger_time"
            name="time"
            step="1"
            value={time}
            onChange={this.myChangeHandler.bind(this)}
          />
          <span className="errors">{errors.date}</span>
          <br />

          <input type="submit" value="SEND IMAGE" />
          <span className="errors">{errors.backend}</span>
          {Object.keys(errors).length === 0 && success && <span className="success">Submitted!</span>}
          {Object.keys(errors).length > 0 && <span className="errors">Failed!</span>}
          <br />
          <br />
        </form>
      </div>
    );
  }
}

ImageSlideSender.propTypes = {
  t: PropTypes.func.isRequired,
  tReady: PropTypes.bool,
};

ImageSlideSender.defaultProps = {
  tReady: false,
};

const ImageSlideSenderApp = withTranslation()(ImageSlideSender);

export default ImageSlideSenderApp;
