import React from 'react';

class Receiver extends React.Component {
  render() {
    return (
      <div>
        <h2>Now showing</h2>
        <p><b>Message:</b></p>
        <p>(Active text message here)</p>
        <p><b>Image:</b></p>
        <img src="https://via.placeholder.com/320x240" alt="Now showing" width="320" height="240" />
        <h2>Next up - Show all</h2>
        <img src="https://via.placeholder.com/320x240" alt="Next up" width="320" height="240" />
        <p>Next image at (date and time here)</p>
      </div>
    );
  }
}

export default Receiver;
