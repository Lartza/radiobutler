import React from 'react';
import Cookies from 'universal-cookie/es6';
import ReactModal from 'react-modal';
import Gallery from './gallery';

class ImageSlideSender extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      apiurl: '',
      image: '',
      showModal: false,
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

  mySubmitHandler(event) {
    event.preventDefault();
    const form = event.target;
    const data = new FormData(form);
    const cookies = new Cookies();

    if (data.get('date') !== '' && data.get('time') !== '') {
      const date = data.get('date');
      const time = data.get('time');
      data.delete('date');
      data.delete('time');
      data.append('trigger_time', `${date}T${time}`);
    }

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

  selectImage(event) { this.setState({ apiurl: event.target.getAttribute('data-apiurl'), image: event.target.src }); }

  render() {
    const { apiurl, image, showModal } = this.state;
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
            <Gallery selectImage={this.selectImage} apiurl={apiurl} />
            <button type="button" onClick={this.handleCloseModal}>Save & Close gallery</button>
          </ReactModal>
        </div>
        <form onSubmit={this.mySubmitHandler.bind(this)}>

          <label htmlFor="image">Selected image </label>
          <br />
          <input type="hidden" id="image" name="image" value={apiurl} />
          <img src={image} alt="Selected image" width="320" height="auto" />
          <br />
          <br />
          <label htmlFor="image_link">Link URL </label>
          <br />
          <input type="url" id="image_link" name="image_link" />
          <br />
          <br />
          <label htmlFor="trigger_time">Trigger time </label>
          <br />
          <input type="date" id="trigger_time" name="date" />
          <input type="time" id="trigger_time" name="time" step="1" />
          <br />

          <input type="submit" value="SEND IMAGE" />
          <br />
          <br />
        </form>
      </div>
    );
  }
}

export default ImageSlideSender;
