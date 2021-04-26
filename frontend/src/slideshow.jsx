import React from 'react';
import { render } from 'react-dom';
import ImageSlideSenderApp from './components/slideshow_imagesender';
import TextSlideSenderApp from './components/slideshow_textsender';
import ReceiverApp from './components/slideshow_receiver';

const imagesenderContainer = document.getElementById('app1');
render(<ImageSlideSenderApp useSuspense={false} />, imagesenderContainer);

const textsenderContainer = document.getElementById('app2');
render(<TextSlideSenderApp useSuspense={false} />, textsenderContainer);

const receiverContainer = document.getElementById('app3');
render(<ReceiverApp useSuspense={false} />, receiverContainer);
