import React from 'react';
import Cookies from 'universal-cookie/es6';
import PropTypes from 'prop-types';

class Gallery extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      results: {},
      current: '/api/images/',
      next: '',
      previous: '',
      count: -1,
    };
  }

  componentDidMount() {
    this.reloadGallery();
  }

  handleBtnPrevious() {
    const { previous } = this.state;
    this.setState({ current: previous }, this.reloadGallery);
  }

  handleBtnNext() {
    const { next } = this.state;
    this.setState({ current: next }, this.reloadGallery);
  }

  getImageClassNames(apiurl, iApiurl, selectImage) {
    let classes = '';
    if (selectImage !== null) {
      classes += ' modal-image';
    }
    if (apiurl === iApiurl) {
      classes += ' selected';
    }
    return classes;
  }

  reloadGallery() {
    const { current } = this.state;
    fetch(current)
      .then((response) => response.json())
      .then((json) => {
        const {
          count, next, previous, results,
        } = json;
        this.setState({
          results, next, previous, count,
        });
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
    const {
      results, previous, next, count,
    } = this.state;
    const { selectImage, apiurl } = this.props;
    const imgElements = Object.values(results).map(
      (i) => (
        <img
          key={i.apiurl}
          data-apiurl={i.apiurl}
          src={i.image}
          onClick={selectImage}
          className={this.getImageClassNames(apiurl, i.apiurl, selectImage)}
        />
      ),
    );

    return (
      <div id="gallery">
        <h2>Add a new image to the gallery</h2>
        <form onSubmit={this.mySubmitHandler.bind(this)}>
          <label htmlFor="image">Allowed image types: jpeg, png </label>
          <br />
          <input type="file" name="image" id="image" onChange={this.myChangeHandler.bind(this)} />
          <input type="submit" value="UPLOAD" />
        </form>
        <h2>Gallery items</h2>
        <div className="gallery-container" id="list">{imgElements}</div>
        {count > 0 && (
          <div>
            {count}
            {' '}
            images
          </div>
        )}
        {previous && <button type="button" onClick={this.handleBtnPrevious.bind(this)}>Previous page</button>}
        {next && <button type="button" onClick={this.handleBtnNext.bind(this)}>Next page</button>}

      </div>
    );
  }
}

Gallery.propTypes = {
  selectImage: PropTypes.func,
  apiurl: PropTypes.string,
};

Gallery.defaultProps = {
  selectImage: null,
  apiurl: null,
};

export default Gallery;
