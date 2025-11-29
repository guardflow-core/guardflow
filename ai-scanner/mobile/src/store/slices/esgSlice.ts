import { createSlice, PayloadAction } from '@reduxjs/toolkit';

interface ESGScore {
  productId: string;
  score: number;
  category: string;
  details: { [key: string]: any };
}

interface ESGState {
  productESG: { [productId: string]: ESGScore };
  overallESGScore: number | null;
  loading: boolean;
  error: string | null;
}

const initialState: ESGState = {
  productESG: {},
  overallESGScore: null,
  loading: false,
  error: null,
};

const esgSlice = createSlice({
  name: 'esg',
  initialState,
  reducers: {
    fetchESGScoreStart: (state) => {
      state.loading = true;
      state.error = null;
    },
    fetchESGScoreSuccess: (state, action: PayloadAction<ESGScore>) => {
      state.productESG[action.payload.productId] = action.payload;
      state.loading = false;
      // Recalculate overall score (simple average for now)
      const scores = Object.values(state.productESG).map(item => item.score);
      state.overallESGScore = scores.length > 0 ? scores.reduce((a, b) => a + b, 0) / scores.length : null;
    },
    fetchESGScoreFailure: (state, action: PayloadAction<string>) => {
      state.error = action.payload;
      state.loading = false;
    },
    clearESGData: (state) => {
      state.productESG = {};
      state.overallESGScore = null;
      state.loading = false;
      state.error = null;
    },
  },
});

export const { fetchESGScoreStart, fetchESGScoreSuccess, fetchESGScoreFailure, clearESGData } = esgSlice.actions;
export default esgSlice.reducer;