import React from 'react';
import { render } from 'react-dom';
import FormApp from './components/SIForm';

const container = document.getElementById('app');
render(<FormApp useSuspense={false} />, container);
