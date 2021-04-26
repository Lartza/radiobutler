import React from 'react';
import Cookies from 'universal-cookie/es6';
import PropTypes from 'prop-types';
import { withTranslation } from 'react-i18next';
import './i18n';

class Gallery extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      results: {},
      current: '/api/images/',
      next: '',
      previous: '',
      count: -1,
      selected: {},
      error: '',
      sendError: '',
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

  getImageClassNames(apiurl, iApiurl) {
    let classes = 'modal-image';
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
    }).then((r) => {
      if (r.ok) {
        this.reloadGallery();
      } else {
        throw r;
      }
    }).catch((err) => {
      err.text().then((errorMessage) => {
        this.setState({ sendError: errorMessage });
      });
    });
  }

  selectImage(event) {
    const image = {};
    image.apiurl = event.target.getAttribute('data-apiurl');
    image.src = event.target.getAttribute('src');
    this.setState({ selected: image });
  }

  deleteImage() {
    const { selected } = this.state;
    const cookies = new Cookies();
    fetch(selected.apiurl, {
      method: 'DELETE',
      headers: {
        'X-CSRFToken': cookies.get('csrftoken'),
      },
    }).then((r) => {
      if (r.ok) {
        this.setState({ selected: {} });
        this.reloadGallery();
      } else {
        throw r;
      }
    }).catch((err) => {
      err.text().then((errorMessage) => {
        this.setState({ error: errorMessage });
      });
    });
  }

  render() {
    const {
      results, previous, next, count, selected, error, sendError,
    } = this.state;
    const { selectImage, apiurl } = this.props;
    const imgElements = Object.values(results).map(
      (i) => (
        <img
          key={i.apiurl}
          data-apiurl={i.apiurl}
          src={i.image}
          onClick={selectImage || this.selectImage.bind(this)}
          className={selectImage ? this.getImageClassNames(apiurl, i.apiurl)
            : this.getImageClassNames(selected.apiurl, i.apiurl)}
        />
      ),
    );

    return (
      <div>
        <form onSubmit={this.mySubmitHandler.bind(this)}>
          <h2>Add a new image to the gallery</h2>
          <label htmlFor="image">Allowed image types: jpeg, png </label>
          <br />
          <input
            type="file"
            name="image"
            id="image"
            accept=".png,.jpg,.jpeg"
            onChange={this.myChangeHandler.bind(this)}
          />
          <input type="submit" value="UPLOAD" />
          <span className="errors">{sendError}</span>
        </form>
        <div className={selectImage ? '' : 'main'}>
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
        {selectImage === null && (
        <div className="right">
          {Object.keys(selected).length > 0
          && (
          <div>
            <a target="_blank" href={selected.src} rel="noreferrer">{selected.src.split('/').pop()}</a>
            <br />
            <button type="button" onClick={this.deleteImage.bind(this)}>Delete</button>
            <span className="errors">{error}</span>
          </div>
          )}
        </div>
        )}
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

const GalleryApp = withTranslation()(Gallery);

export default GalleryApp;
