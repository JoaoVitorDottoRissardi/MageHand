import { createTheme, alpha, getContrastRatio,  } from '@mui/material/styles';

const violetBase = '#7F00FF';
const violetMain = alpha(violetBase, 0.7);

const redBase = '#FF0000';
const redMain = alpha(redBase, 0.7);

const greenBase = '#00FF00';
const greenMain = alpha(greenBase, 0.7);

const yellowBase = '#FFFF00';
const yellowMain = alpha(yellowBase, 0.7);

const blueBase = '#0000FF';
const blueMain = alpha(blueBase, 0.7);

const orangeBase = '#FF7F00';
const orangeMain = alpha(orangeBase, 0.7);

export const theme = createTheme({
  palette: {
    violet: {
      main: violetMain,
      light: alpha(violetBase, 0.5),
      dark: alpha(violetBase, 0.9),
      contrastText: getContrastRatio(violetMain, '#fff') > 10.5 ? '#fff' : '#111',
    },
    red: {
      main: redMain,
      light: alpha(redBase, 0.5),
      dark: alpha(redBase, 0.9),
      contrastText: getContrastRatio(redMain, '#fff') > 10.5 ? '#fff' : '#111',
    },
    green: {
      main: greenMain,
      light: alpha(greenBase, 0.5),
      dark: alpha(greenBase, 0.9),
      contrastText: getContrastRatio(greenMain, '#fff') > 1.5 ? '#fff' : '#111',
    },
    yellow: {
        main: yellowMain,
        light: alpha(yellowBase, 0.5),
        dark: alpha(yellowBase, 0.9),
        contrastText: getContrastRatio(yellowMain, '#fff') > 1.5 ? '#fff' : '#111',    
    },
    blue: {
        main: blueMain,
        light: alpha(blueBase, 0.5),
        dark: alpha(blueBase, 0.9),
        contrastText: getContrastRatio(blueMain, '#fff') > 10.5 ? '#fff' : '#111', 
    },
    orange: {
        main: orangeMain,
        light: alpha(orangeBase, 0.5),
        dark: alpha(orangeBase, 0.9),
        contrastText: getContrastRatio(orangeMain, '#fff') > 10.5 ? '#fff' : '#111', 
    }
  },
});