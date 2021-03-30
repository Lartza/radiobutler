import React from 'react';
import Cookies from 'universal-cookie/es6';

class ImageSlideSender extends React.Component {
  static mySubmitHandler(event) {
    event.preventDefault();
    const form = event.target;
    const data = new FormData(form);
    const cookies = new Cookies();

    fetch('/api/imageslides/', {
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
        <h2>Images</h2>
        <label htmlFor="image">Image type: jpeg, png</label>
        <br />
        <input type="file" id="image" name="image" />
        <br />
        <img src="https://via.placeholder.com/320x240" alt="Uploaded image" width="320" height="240" />
        <br />
        <br />
        <label htmlFor="image_link">Link URL </label>
        <br />
        <input type="url" id="image_link" name="image_link" />
        <br />
        <br />
        <label htmlFor="trigger_time">Trigger time</label>
        <br />
        <input type="datetime-local" id="trigger_time" name="trigger_time" />
        <br />
        <br />

        <input type="submit" value="SEND IMAGE" />
        <br />
        <br />
      </form>
    );
  }
}

export default ImageSlideSender;
