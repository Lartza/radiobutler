/**
 * Copyright 2021 Radio Moreeni
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

import React, { useState, useEffect } from 'react';
import {
  StompSessionProvider,
  useSubscription,
} from 'react-stomp-hooks';

// !!!!!!!!!!!!!!!!!!!!!!!!!!
// DO NOT TRANSLATE THIS FILE
// !!!!!!!!!!!!!!!!!!!!!!!!!!

function compare(a, b) {
  if (Date.parse(a.headers['trigger-time']) < Date.parse(b.headers['trigger-time'])) {
    return -1;
  }
  if (Date.parse(a.headers['trigger-time']) > Date.parse(b.headers['trigger-time'])) {
    return 1;
  }
  // a must be equal to b
  return 0;
}

const ReceiverLite = () => (
  <div>
    {window.service ? (
      <StompSessionProvider url={`wss://${window.service}/stomp`}>
        {window.bearer ? <ImageSubscribingComponent /> : 'Bearer not available'}
        {window.bearer ? <TextSubscribingComponent /> : 'Bearer not available'}
      </StompSessionProvider>
    ) : 'Service not available'}
  </div>
);

function TextSubscribingComponent() {
  const [lastMessage, setLastMessage] = useState('');

  useSubscription(`${window.bearer}/text`, (message) => {
    if (message.body.startsWith('TEXT ')) {
      setLastMessage(message.body.replace('TEXT ', ''));
    }
  });
  return (
    <span>{lastMessage}</span>
  );
}

function ImageSubscribingComponent() {
  const [lastImage, setLastImage] = useState(`https://${window.service}/static/frontend/noimage.jpg`);
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
          const newMessages = [...messages];
          newMessages.splice(i, 1);
          setMessages(newMessages);
        } else if (delta < 0) {
          const newMessages = [...messages];
          newMessages.splice(i, 1);
          setMessages(newMessages);
        }
      }
    }, 1000);
    return () => clearInterval(interval);
  });

  useSubscription(`${window.bearer}/image`, (message) => {
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
          const newMessages = [...messages, message];
          newMessages.sort(compare);
          setMessages(newMessages);
        }
      }
    }
  });

  return (
    <div>
      <img src={lastImage} alt="Now showing" height="240" />
      <p>
        {lastLink ? <a href={lastLink}>{lastLink}</a> : ''}
      </p>
    </div>
  );
}

export default ReceiverLite;
