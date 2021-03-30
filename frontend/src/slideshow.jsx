import React from 'react';
import { render } from 'react-dom';
import ImageSlideSender from './components/slideshow_imagesender';
import TextSlideSender from './components/slideshow_textsender';
import Receiver from './components/slideshow_receiver';

const imagesenderContainer = document.getElementById('app1');
render(<ImageSlideSender />, imagesenderContainer);

const textsenderContainer = document.getElementById('app2');
render(<TextSlideSender />, textsenderContainer);

const receiverContainer = document.getElementById('app3');
render(<Receiver />, receiverContainer);
