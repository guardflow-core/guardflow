import { createSlice, PayloadAction } from '@reduxjs/toolkit';

interface ThemeState {
  mode: 'light' | 'dark';
  primaryColor: string;
  secondaryColor: string;
  accentColor: string;
  backgroundColor: string;
  textColor: string;
  isCustomTheme: boolean;
}

const initialState: ThemeState = {
  mode: 'light',
  primaryColor: '#1976d2',
  secondaryColor: '#dc004e',
  accentColor: '#4caf50',
  backgroundColor: '#ffffff',
  textColor: '#000000',
  isCustomTheme: false,
};

const themeSlice = createSlice({
  name: 'theme',
  initialState,
  reducers: {
    toggleTheme: (state) => {
      state.mode = state.mode === 'light' ? 'dark' : 'light';
      
      if (state.mode === 'dark') {
        state.backgroundColor = '#121212';
        state.textColor = '#ffffff';
      } else {
        state.backgroundColor = '#ffffff';
        state.textColor = '#000000';
      }
    },

    setTheme: (state, action: PayloadAction<'light' | 'dark'>) => {
      state.mode = action.payload;
      
      if (state.mode === 'dark') {
        state.backgroundColor = '#121212';
        state.textColor = '#ffffff';
      } else {
        state.backgroundColor = '#ffffff';
        state.textColor = '#000000';
      }
    },

    setPrimaryColor: (state, action: PayloadAction<string>) => {
      state.primaryColor = action.payload;
      state.isCustomTheme = true;
    },

    setSecondaryColor: (state, action: PayloadAction<string>) => {
      state.secondaryColor = action.payload;
      state.isCustomTheme = true;
    },

    setAccentColor: (state, action: PayloadAction<string>) => {
      state.accentColor = action.payload;
      state.isCustomTheme = true;
    },

    setCustomTheme: (state, action: PayloadAction<Partial<ThemeState>>) => {
      Object.assign(state, action.payload);
      state.isCustomTheme = true;
    },

    resetTheme: (state) => {
      state.mode = 'light';
      state.primaryColor = '#1976d2';
      state.secondaryColor = '#dc004e';
      state.accentColor = '#4caf50';
      state.backgroundColor = '#ffffff';
      state.textColor = '#000000';
      state.isCustomTheme = false;
    },
  },
});

export const { 
  toggleTheme, 
  setTheme, 
  setPrimaryColor, 
  setSecondaryColor, 
  setAccentColor, 
  setCustomTheme, 
  resetTheme 
} = themeSlice.actions;

export default themeSlice.reducer;