import React from 'react';
import Cookies from 'universal-cookie/es6';
import { withTranslation } from 'react-i18next';
import './i18n';
import PropTypes from 'prop-types';

class TextSlideSender extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      errors: {},
      success: false,
    };
  }

  mySubmitHandler(event) {
    event.preventDefault();
    let success = false;
    this.setState({ success });

    const form = event.target;
    const data = new FormData(form);
    const cookies = new Cookies();

    fetch('/api/textslides/', {
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

  render() {
    const {
      errors, success,
    } = this.state;
    const { t, tReady } = this.props;
    if (!tReady) return null;
    return (
      <form onSubmit={this.mySubmitHandler.bind(this)}>
        <h2>Text Message</h2>
        <label htmlFor="message">Message (max 128 chars) </label>
        <br />
        <textarea id="message" name="message" rows="3" maxLength="128" />
        <br />

        <input type="submit" value="SEND TEXT" />
        <span className="errors">{errors.backend}</span>
        {Object.keys(errors).length === 0 && success && <span className="success">Submitted!</span>}
        {Object.keys(errors).length > 0 && <span className="errors">Failed!</span>}
        <br />
        <br />
      </form>
    );
  }
}

TextSlideSender.propTypes = {
  t: PropTypes.func.isRequired,
  tReady: PropTypes.bool,
};

TextSlideSender.defaultProps = {
  tReady: false,
};

const TextSlideSenderApp = withTranslation()(TextSlideSender);

export default TextSlideSenderApp;
