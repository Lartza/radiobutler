import React, { useState } from 'react';
import {
  StompSessionProvider,
  useSubscription,
} from 'react-stomp-hooks';

const Receiver = () => (
  <StompSessionProvider
    url="wss://radiodns.ltn.fi/stomp"
  >
    <h2>Now showing</h2>
    <p><b>Message:</b></p>
    <p><TextSubscribingComponent /></p>
    <p><b>Image:</b></p>
    <ImageSubscribingComponent />
    <h2>Next up - Show all</h2>
    <img src="https://via.placeholder.com/320x240" alt="Next up" width="320" height="240" />
    <p>Next image at (date and time here)</p>
  </StompSessionProvider>
);

function TextSubscribingComponent() {
  const [lastMessage, setLastMessage] = useState('No message received yet');

  useSubscription('/topic/fm/6e1/6024/09840/text', (message) => {
    if (message.body.startsWith('TEXT ')) {
      setLastMessage(message.body.replace('TEXT ', ''));
    }
  });
  return (
    <span>{lastMessage}</span>
  );
}

function ImageSubscribingComponent() {
  const [lastImage, setLastImage] = useState('https://via.placeholder.com/320x240');

  useSubscription('/topic/fm/6e1/6024/09840/image', (message) => {
    if (message.body.startsWith('SHOW ')) {
      console.log(message.headers);
      setLastImage(message.body.split(' ', 2)[1]);
    }
  });

  return (
    <img src={lastImage} alt="Now showing" width="320" height="240" />
  );
}

export default Receiver;
