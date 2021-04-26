import React from 'react';
import { render } from 'react-dom';
import GalleryApp from './components/gallery';

const container = document.getElementById('app');
render(<GalleryApp useSuspense={false} />, container);
