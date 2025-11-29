import { createSlice, PayloadAction } from '@reduxjs/toolkit';

interface AnalyticsMetric {
  name: string;
  value: number;
  unit: string;
  trend: 'up' | 'down' | 'stable';
  change_percentage: number;
}

interface AnalyticsChart {
  id: string;
  title: string;
  type: 'line' | 'bar' | 'pie' | 'doughnut';
  data: any[];
  labels: string[];
  colors: string[];
}

interface AnalyticsDashboard {
  id: string;
  name: string;
  metrics: AnalyticsMetric[];
  charts: AnalyticsChart[];
  last_updated: string;
}

interface AnalyticsState {
  dashboards: AnalyticsDashboard[];
  currentDashboard: AnalyticsDashboard | null;
  loading: boolean;
  error: string | null;
  lastUpdated: string | null;
}

const initialState: AnalyticsState = {
  dashboards: [],
  currentDashboard: null,
  loading: false,
  error: null,
  lastUpdated: null,
};

const analyticsSlice = createSlice({
  name: 'analytics',
  initialState,
  reducers: {
    fetchDashboardsStart: (state) => {
      state.loading = true;
      state.error = null;
    },

    fetchDashboardsSuccess: (state, action: PayloadAction<AnalyticsDashboard[]>) => {
      state.dashboards = action.payload;
      state.loading = false;
      state.lastUpdated = new Date().toISOString();
    },

    fetchDashboardsFailure: (state, action: PayloadAction<string>) => {
      state.error = action.payload;
      state.loading = false;
    },

    fetchDashboardStart: (state) => {
      state.loading = true;
      state.error = null;
    },

    fetchDashboardSuccess: (state, action: PayloadAction<AnalyticsDashboard>) => {
      state.currentDashboard = action.payload;
      state.loading = false;
      state.lastUpdated = new Date().toISOString();
    },

    fetchDashboardFailure: (state, action: PayloadAction<string>) => {
      state.error = action.payload;
      state.loading = false;
    },

    createDashboard: (state, action: PayloadAction<AnalyticsDashboard>) => {
      state.dashboards.push(action.payload);
    },

    updateDashboard: (state, action: PayloadAction<AnalyticsDashboard>) => {
      const index = state.dashboards.findIndex(d => d.id === action.payload.id);
      if (index !== -1) {
        state.dashboards[index] = action.payload;
      }
      
      if (state.currentDashboard?.id === action.payload.id) {
        state.currentDashboard = action.payload;
      }
    },

    deleteDashboard: (state, action: PayloadAction<string>) => {
      state.dashboards = state.dashboards.filter(d => d.id !== action.payload);
      
      if (state.currentDashboard?.id === action.payload) {
        state.currentDashboard = null;
      }
    },

    setCurrentDashboard: (state, action: PayloadAction<string>) => {
      const dashboard = state.dashboards.find(d => d.id === action.payload);
      if (dashboard) {
        state.currentDashboard = dashboard;
      }
    },

    clearCurrentDashboard: (state) => {
      state.currentDashboard = null;
    },

    clearError: (state) => {
      state.error = null;
    },

    resetAnalytics: (state) => {
      state.dashboards = [];
      state.currentDashboard = null;
      state.loading = false;
      state.error = null;
      state.lastUpdated = null;
    },
  },
});

export const { 
  fetchDashboardsStart, 
  fetchDashboardsSuccess, 
  fetchDashboardsFailure,
  fetchDashboardStart,
  fetchDashboardSuccess,
  fetchDashboardFailure,
  createDashboard,
  updateDashboard,
  deleteDashboard,
  setCurrentDashboard,
  clearCurrentDashboard,
  clearError,
  resetAnalytics
} = analyticsSlice.actions;

export default analyticsSlice.reducer;