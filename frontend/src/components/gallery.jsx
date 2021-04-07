import React from 'react';
import Cookies from 'universal-cookie/es6';

class Gallery extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      images: {},
    };
  }

  componentDidMount() {
    this.reloadGallery();
  }

  reloadGallery() {
    fetch('/api/images/')
      .then((response) => response.json())
      .then((json) => {
        this.setState({ images: json });
      });
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
    fetch('/api/images/', {
      method: 'POST',
      headers: {
        'X-CSRFToken': cookies.get('csrftoken'),
      },
      body: data,
    }).then((r) => r.json())
      .then((json) => {
        console.log(json);
        this.reloadGallery();
      });
  }

  render() {
    const { images } = this.state;
    const { selectImage } = this.props;
    const imgElements = Object.values(images).map(
      (i) => <img key={i.apiurl} data-apiurl={i.apiurl} src={i.image} onClick={selectImage} />,
    );
    return (
      <div id="gallery">
        <h2>Add a new image to the gallery</h2>
        <form onSubmit={this.mySubmitHandler.bind(this)}>
          <label htmlFor="image">Image type: jpeg, png</label>
          <br />
          <input type="file" name="image" id="image" onChange={this.myChangeHandler.bind(this)} />
          <input type="submit" value="UPLOAD" />
        </form>
        <h2>Gallery items</h2>
        <div className="gallery-container" id="list">{imgElements}</div>
      </div>
    );
  }
}

export default Gallery;
