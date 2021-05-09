/**
 * Copyright 2021 Radio Moreeni
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

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
    const { t } = this.props;

    // Image has to be selected before sending
    if (!fields.image) {
      isFormValid = false;
      errors.image = t('errors.imageSelected');
    }

    // Api url - 512 chars max, must be a link
    if (fields.link) {
      if (fields.link.length > 512) {
        isFormValid = false;
        errors.link = t('errors.max512');
      } else if (!validator.isURL(fields.link, {
        protocols: ['http', 'https'],
        /* eslint-disable camelcase */
        require_protocol: true,
        /* eslint-enable camelcase */
      })) {
        isFormValid = false;
        errors.link = t('errors.link');
      }
    }

    // Trigger time - should be later than current time. Both
    // date and time have to be selected, if either one is selected.
    if (fields.date && fields.time) {
      const date = Date.parse(`${fields.date}T${fields.time}`);
      const now = Date.now();

      if (date < now) {
        isFormValid = false;
        errors.date = t('errors.date');
      }
    } else if ((fields.date && !fields.time) || (!fields.date && fields.time)) {
      isFormValid = false;
      errors.date = t('errors.dateTime');
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
        <h2>{t('sender.images')}</h2>
        <div>
          <p>{t('sender.chooseImage')}</p>
          <button type="button" onClick={this.handleOpenModal}>{t('sender.openGallery')}</button>
          <ReactModal
            isOpen={showModal}
            contentLabel="Gallery Modal"
          >
            <button type="button" onClick={this.handleCloseModal}>{t('saveClose')}</button>
            <GalleryApp selectImage={this.selectImage} apiurl={apiurl} useSuspense={false} />
            <button type="button" onClick={this.handleCloseModal}>{t('saveClose')}</button>
          </ReactModal>
        </div>
        <form onSubmit={this.mySubmitHandler.bind(this)}>

          <label htmlFor="image">{t('sender.selectedImage')}</label>
          <br />
          <br />
          <input type="hidden" id="image" name="image" value={apiurl} onChange={this.myChangeHandler.bind(this)} />
          <img src={image} alt={t('sender.alt')} height="240" />
          <span className="errors">{errors.image}</span>
          <br />
          <br />
          <label htmlFor="image_link">{t('sender.linkUrl')}</label>
          <div className="tooltip">
            {' '}
            ?
            <span className="tooltiptext">{t('sender.linkTooltip')}</span>
          </div>
          <br />
          <input type="text" id="image_link" name="link" value={link} onChange={this.myChangeHandler.bind(this)} />
          <span className="errors">{errors.link}</span>
          <br />
          <br />
          <label htmlFor="trigger_time">{t('sender.triggerTime')}</label>
          <div className="tooltip">
            {' '}
            ?
            <span className="tooltiptext">{t('sender.triggerTooltip')}</span>
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

          <input type="submit" value={t('sender.sendImage')} />
          <span className="errors">{errors.backend}</span>
          {Object.keys(errors).length === 0 && success && <span className="success">{t('submitted')}</span>}
          {Object.keys(errors).length > 0 && <span className="errors">{t('failed')}</span>}
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
