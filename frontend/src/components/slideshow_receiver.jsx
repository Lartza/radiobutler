import React, { useState, useEffect } from 'react';
import {
  StompSessionProvider,
  useSubscription,
} from 'react-stomp-hooks';
import Modal from 'react-modal';
import { useTranslation, Translation } from 'react-i18next';

Modal.setAppElement('#app3');

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

const Receiver = () => (
  <StompSessionProvider url="wss://radiodns.ltn.fi/stomp">
    <Translation useSuspense={false}>
      {(t) => (
        <div>
          <h2>{t('receiver.nowShowing')}</h2>
          <p><b>{t('receiver.message')}</b></p>
          <p>{window.bearer ? <TextSubscribingComponent /> : t('receiver.notAvailable')}</p>
          <p><b>{t('receiver.image')}</b></p>
          {window.bearer ? <ImageSubscribingComponent /> : t('receiver.notAvailable')}
        </div>
      )}
    </Translation>
  </StompSessionProvider>
);

function TextSubscribingComponent() {
  const { t, ready } = useTranslation('', { useSuspense: false });
  const [lastMessage, setLastMessage] = useState(t('receiver.noMessage'));

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
  const { t, ready } = useTranslation('', { useSuspense: false });
  const [lastImage, setLastImage] = useState('/static/frontend/noimage.jpg');
  const [lastLink, setLastLink] = useState('');
  const [messages, setMessages] = useState([]);
  const [modalIsOpen, setIsOpen] = useState(false);

  function openModal() {
    setIsOpen(true);
  }

  function closeModal() {
    setIsOpen(false);
  }

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

  const msgElements = Object.values(messages).map(
    (m) => (
      <div key={m.headers['message-id']}>
        <img
          src={m.body.split(' ', 2)[1]}
        />
        <div>{m.headers.link}</div>
        <div>{m.headers['trigger-time']}</div>
      </div>
    ),
  );

  return (
    <div>
      <div className="imagebox">
        <img src={lastImage} alt={t('receiver.nowShowing')} height="240" />
      </div>
      <p>
        Link:
        {' '}
        {lastLink ? <a href={lastLink}>{lastLink}</a> : t('none')}
      </p>
      <h2>
        Next up -
        {' '}
        <button type="button" onClick={openModal}>{t('receiver.show')}</button>
      </h2>
      <Modal
        isOpen={modalIsOpen}
        onRequestClose={closeModal}
        contentLabel="Receiver Modal"
      >
        <button type="button" onClick={closeModal}>{t('close')}</button>
        <div>{msgElements.length > 0 ? msgElements : <span>{t('receiver.imagesScheduled')}</span>}</div>
      </Modal>
      <div className="imagebox">
        <img
          src={messages[0] ? messages[0].body.split(' ', 2)[1] : '/static/frontend/noimage.jpg'}
          alt={t('receiver.next')}
        />
      </div>
      <p>
        Link:
        {' '}
        {messages[0] ? <a href={messages[0].headers.link}>{messages[0].headers.link}</a> : t('none')}
      </p>
      <p>
        {messages[0] ? `${t('receiver.nextImage')} ${messages[0].headers['trigger-time']}`
          : t('receiver.imageScheduled')}
      </p>
    </div>
  );
}

export default Receiver;
