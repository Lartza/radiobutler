import React from 'react';
import Cookies from 'universal-cookie/es6';
import { withTranslation } from 'react-i18next';
import './i18n';

class TextSlideSender extends React.Component {
  constructor(props) {
    super(props);
  }

  mySubmitHandler(event) {
    event.preventDefault();
    const form = event.target;
    const data = new FormData(form);
    const cookies = new Cookies();

    fetch('/api/textslides/', {
      method: 'POST',
      headers: {
        'X-CSRFToken': cookies.get('csrftoken'),
      },
      body: data,
    }).then((r) => r.json())
      .then((json) => {
        console.log(json);
      });
  }

  render() {
    return (
      <form onSubmit={this.mySubmitHandler.bind(this)}>
        <h2>Text Message</h2>
        <label htmlFor="message">Message (max 128 chars) </label>
        <br />
        <textarea id="message" name="message" rows="3" maxLength="128" />
        <br />

        <input type="submit" value="SEND TEXT" />
        <br />
        <br />
      </form>
    );
  }
}

const TextSlideSenderApp = withTranslation()(TextSlideSender);

export default TextSlideSenderApp;
