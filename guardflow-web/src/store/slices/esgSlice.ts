import { createSlice, PayloadAction } from '@reduxjs/toolkit';

interface ESGScore {
  overall: number;
  environmental: number;
  social: number;
  governance: number;
  last_updated: string;
}

interface ESGReport {
  id: string;
  user_id: string;
  period: string;
  scores: ESGScore;
  breakdown: {
    environmental: {
      carbon_footprint: number;
      waste_reduction: number;
      energy_efficiency: number;
      sustainable_products: number;
    };
    social: {
      fair_trade: number;
      local_support: number;
      community_impact: number;
      diversity_support: number;
    };
    governance: {
      transparency: number;
      ethical_practices: number;
      data_privacy: number;
      compliance: number;
    };
  };
  recommendations: string[];
  achievements: string[];
  created_at: string;
}

interface ESGState {
  currentScore: ESGScore | null;
  reports: ESGReport[];
  loading: boolean;
  error: string | null;
  lastCalculated: string | null;
}

const initialState: ESGState = {
  currentScore: null,
  reports: [],
  loading: false,
  error: null,
  lastCalculated: null,
};

const esgSlice = createSlice({
  name: 'esg',
  initialState,
  reducers: {
    fetchESGStart: (state) => {
      state.loading = true;
      state.error = null;
    },

    fetchESGSuccess: (state, action: PayloadAction<ESGScore>) => {
      state.currentScore = action.payload;
      state.loading = false;
      state.lastCalculated = new Date().toISOString();
    },

    fetchESGFailure: (state, action: PayloadAction<string>) => {
      state.error = action.payload;
      state.loading = false;
    },

    fetchReportsStart: (state) => {
      state.loading = true;
      state.error = null;
    },

    fetchReportsSuccess: (state, action: PayloadAction<ESGReport[]>) => {
      state.reports = action.payload;
      state.loading = false;
    },

    fetchReportsFailure: (state, action: PayloadAction<string>) => {
      state.error = action.payload;
      state.loading = false;
    },

    calculateESGStart: (state) => {
      state.loading = true;
      state.error = null;
    },

    calculateESGSuccess: (state, action: PayloadAction<ESGScore>) => {
      state.currentScore = action.payload;
      state.loading = false;
      state.lastCalculated = new Date().toISOString();
    },

    calculateESGFailure: (state, action: PayloadAction<string>) => {
      state.error = action.payload;
      state.loading = false;
    },

    clearError: (state) => {
      state.error = null;
    },

    resetESG: (state) => {
      state.currentScore = null;
      state.reports = [];
      state.loading = false;
      state.error = null;
      state.lastCalculated = null;
    },
  },
});

export const { 
  fetchESGStart, 
  fetchESGSuccess, 
  fetchESGFailure,
  fetchReportsStart,
  fetchReportsSuccess,
  fetchReportsFailure,
  calculateESGStart,
  calculateESGSuccess,
  calculateESGFailure,
  clearError,
  resetESG
} = esgSlice.actions;

export default esgSlice.reducer;