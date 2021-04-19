import React, { useState, useEffect } from 'react';
import {
  StompSessionProvider,
  useSubscription,
} from 'react-stomp-hooks';

const Receiver = () => (
  <StompSessionProvider url="wss://radiodns.ltn.fi/stomp">
    <h2>Now showing</h2>
    <p><b>Message: </b></p>
    <p><TextSubscribingComponent /></p>
    <p><b>Image: </b></p>
    <ImageSubscribingComponent />
    <h2>Next up - Show all</h2>
    <img src="https://via.placeholder.com/320x240" alt="Next up" width="320" height="auto" />
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
  const [lastLink, setLastLink] = useState('');
  const [messages, setMessages] = useState([]);

  useEffect(() => {
    const interval = setInterval(() => {
      for (let i = messages.length - 1; i >= 0; i -= 1) {
        const triggerTime = Date.parse(messages[i].headers['trigger-time']);
        const now = Date.now();
        const delta = triggerTime - now;
        if (delta > 0 && delta < 1000) {
          setLastImage(messages[i].body.split(' ', 2)[1]);
          if (messages[i].headers.link !== undefined) {
            setLastLink(messages[i].headers.link);
          } else {
            setLastLink('');
          }
          messages.splice(i, 1);
        }
      }
    }, 1000);
    return () => clearInterval(interval);
  });

  useSubscription('/topic/fm/6e1/6024/09840/image', (message) => {
    if (message.body.startsWith('SHOW ')) {
      if (message.headers['trigger-time'] === 'NOW') {
        setLastImage(message.body.split(' ', 2)[1]);
        if (message.headers.link !== undefined) {
          setLastLink(message.headers.link);
        } else {
          setLastLink('');
        }
      } else {
        const triggerTime = Date.parse(message.headers['trigger-time']);
        const now = Date.now();
        const delta = triggerTime - now;
        if (delta > 0 && delta < 1000) {
          setLastImage(message.body.split(' ', 2)[1]);
          if (message.headers.link !== undefined) {
            setLastLink(message.headers.link);
          } else {
            setLastLink('');
          }
        } else if (now < triggerTime) {
          setMessages((prev) => [...prev, message]);
        }
      }
    }
  });

  return (
    <div>
      <img src={lastImage} alt="Now showing" width="320" height="240" />
      <div>
        Link:
        <a href={lastLink}>{lastLink}</a>
      </div>
    </div>
  );
}

export default Receiver;
