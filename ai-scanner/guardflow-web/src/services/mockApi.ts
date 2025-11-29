/**
 * Mock API para demonstração
 * Simula as respostas do backend
 */

export const mockApi = {
  // Health check
  health: () => Promise.resolve({
    data: {
      status: "healthy",
      service: "GuardFlow API",
      version: "0.1.0"
    }
  }),

  // Scanner stats
  getScanStats: () => Promise.resolve({
    data: {
      success: true,
      data: {
        total_scans: 1250,
        successful_scans: 1180,
        success_rate: 94.4,
        avg_scan_time_ms: 850
      }
    }
  }),

  // ESG Dashboard
  getEsgDashboard: () => Promise.resolve({
    data: {
      success: true,
      data: {
        total_score: 87,
        total_points: 2450,
        total_tokens: 125
      }
    }
  }),

  // Products
  getProducts: () => Promise.resolve({
    data: {
      success: true,
      data: {
        total: 150,
        products: [
          { id: 1, name: "Produto 1", price: 10.50 },
          { id: 2, name: "Produto 2", price: 15.75 }
        ]
      }
    }
  })
};
