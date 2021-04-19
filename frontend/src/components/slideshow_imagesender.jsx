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
      date: '',
      time: '',
      link: '',
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

  myChangeHandler(event) {
    const { name } = event.target;
    const { value } = event.target;
    this.setState({ [name]: value });
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
      data.append('trigger_time', `${date}T${time}+0300`);
    }

    fetch('/api/imageslides/', {
      method: 'POST',
      headers: {
        'X-CSRFToken': cookies.get('csrftoken'),
      },
      body: data,
    }).then((r) => {
      if (r.ok) {
        this.setState({
          apiurl: '', image: '', date: '', time: '', link: '',
        });
      } else {
        throw r;
      }
    }).catch((err) => {
      err.text().then((errorMessage) => {
        console.log(errorMessage);
      });
    });
  }

  selectImage(event) { this.setState({ apiurl: event.target.getAttribute('data-apiurl'), image: event.target.src }); }

  render() {
    const {
      apiurl, image, date, time, link, showModal,
    } = this.state;
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
          <input type="hidden" id="image" name="image" value={apiurl} onChange={this.myChangeHandler.bind(this)} />
          <img src={image} alt="Selected" width="320" height="auto" />
          <br />
          <br />
          <label htmlFor="image_link">Link URL </label>
          <br />
          <input type="url" id="image_link" name="link" value={link} onChange={this.myChangeHandler.bind(this)} />
          <br />
          <br />
          <label htmlFor="trigger_time">Trigger time </label>
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
