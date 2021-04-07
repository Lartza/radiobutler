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
          <button type="button" onClick={this.handleOpenModal}>Open gallery</button>
          <ReactModal
            isOpen={showModal}
            contentLabel="Minimal Modal Example"
          >
            <button type="button" onClick={this.handleCloseModal}>Close gallery</button>
            <Gallery selectImage={this.selectImagen} />
          </ReactModal>
        </div>
        <form onSubmit={this.mySubmitHandler.bind(this)}>

          <label htmlFor="image">Image type: jpeg, png</label>
          <br />
          <input type="hidden" id="image" name="image" value={apiurl} />
          <br />
          <img src={image} alt="Uploaded image" width="320" height="240" />
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
      </div>
    );
  }
}

export default ImageSlideSender;
