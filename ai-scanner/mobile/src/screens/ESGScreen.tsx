import React, { useEffect } from 'react';
import { View, Text, StyleSheet, ScrollView, TouchableOpacity, Alert } from 'react-native';
import { useDispatch, useSelector } from 'react-redux';
import { AppDispatch, RootState } from '../store';
import { fetchESGScoreStart, fetchESGScoreSuccess, fetchESGScoreFailure } from '../store/slices/esgSlice';
import { MaterialCommunityIcons } from '@expo/vector-icons';

const ESGScreen: React.FC = () => {
  const dispatch: AppDispatch = useDispatch();
  const { productESG, overallESGScore, loading, error } = useSelector((state: RootState) => state.esg);
  const { items } = useSelector((state: RootState) => state.cart);

  useEffect(() => {
    // Simulate fetching ESG scores for cart items
    if (items.length > 0) {
      dispatch(fetchESGScoreStart());
      // Simulate API call
      setTimeout(() => {
        items.forEach((item) => {
          const mockESGScore = {
            productId: item.productId,
            score: Math.random() * 40 + 60, // Random score between 60-100
            category: 'Sustentabilidade',
            details: {
              environmental: Math.random() * 30 + 70,
              social: Math.random() * 30 + 70,
              governance: Math.random() * 30 + 70,
            },
          };
          dispatch(fetchESGScoreSuccess(mockESGScore));
        });
      }, 1000);
    }
  }, [items, dispatch]);

  const getScoreColor = (score: number) => {
    if (score >= 80) return '#4CAF50';
    if (score >= 60) return '#FF9800';
    return '#f44336';
  };

  const getScoreLabel = (score: number) => {
    if (score >= 80) return 'Excelente';
    if (score >= 60) return 'Bom';
    return 'Precisa Melhorar';
  };

  const handleRefreshScores = () => {
    if (items.length === 0) {
      Alert.alert('Carrinho Vazio', 'Adicione produtos ao carrinho para ver os scores ESG.');
      return;
    }
    dispatch(fetchESGScoreStart());
    // Simulate refresh
    setTimeout(() => {
      items.forEach((item) => {
        const mockESGScore = {
          productId: item.productId,
          score: Math.random() * 40 + 60,
          category: 'Sustentabilidade',
          details: {
            environmental: Math.random() * 30 + 70,
            social: Math.random() * 30 + 70,
            governance: Math.random() * 30 + 70,
          },
        };
        dispatch(fetchESGScoreSuccess(mockESGScore));
      });
    }, 1000);
  };

  const renderESGItem = (productId: string, esgData: any) => {
    const cartItem = items.find(item => item.productId === productId);
    if (!cartItem) return null;

    return (
      <View key={productId} style={styles.esgItem}>
        <View style={styles.itemHeader}>
          <MaterialCommunityIcons name="leaf" size={24} color={getScoreColor(esgData.score)} />
          <View style={styles.itemInfo}>
            <Text style={styles.itemName}>{cartItem.name}</Text>
            <Text style={styles.itemQuantity}>Qtd: {cartItem.quantity}</Text>
          </View>
          <View style={styles.scoreContainer}>
            <Text style={[styles.scoreValue, { color: getScoreColor(esgData.score) }]}>
              {esgData.score.toFixed(1)}%
            </Text>
            <Text style={styles.scoreLabel}>{getScoreLabel(esgData.score)}</Text>
          </View>
        </View>
        
        <View style={styles.detailsContainer}>
          <View style={styles.detailItem}>
            <MaterialCommunityIcons name="earth" size={16} color="#4CAF50" />
            <Text style={styles.detailLabel}>Ambiental</Text>
            <Text style={styles.detailValue}>{esgData.details.environmental.toFixed(1)}%</Text>
          </View>
          <View style={styles.detailItem}>
            <MaterialCommunityIcons name="account-group" size={16} color="#2196F3" />
            <Text style={styles.detailLabel}>Social</Text>
            <Text style={styles.detailValue}>{esgData.details.social.toFixed(1)}%</Text>
          </View>
          <View style={styles.detailItem}>
            <MaterialCommunityIcons name="shield-check" size={16} color="#FF9800" />
            <Text style={styles.detailLabel}>Governança</Text>
            <Text style={styles.detailValue}>{esgData.details.governance.toFixed(1)}%</Text>
          </View>
        </View>
      </View>
    );
  };

  if (items.length === 0) {
    return (
      <View style={styles.emptyContainer}>
        <MaterialCommunityIcons name="leaf-outline" size={80} color="#ccc" />
        <Text style={styles.emptyTitle}>Nenhum Produto no Carrinho</Text>
        <Text style={styles.emptySubtitle}>Adicione produtos para ver os scores ESG</Text>
        <TouchableOpacity style={styles.scanButton}>
          <MaterialCommunityIcons name="barcode-scan" size={24} color="#fff" />
          <Text style={styles.scanButtonText}>Escanear Produtos</Text>
        </TouchableOpacity>
      </View>
    );
  }

  return (
    <ScrollView style={styles.container}>
      <View style={styles.header}>
        <Text style={styles.title}>Dashboard ESG</Text>
        <TouchableOpacity style={styles.refreshButton} onPress={handleRefreshScores}>
          <MaterialCommunityIcons name="refresh" size={24} color="#2196F3" />
        </TouchableOpacity>
      </View>

      {overallESGScore && (
        <View style={styles.overallScoreContainer}>
          <Text style={styles.overallScoreTitle}>Score ESG Geral</Text>
          <View style={styles.overallScoreValue}>
            <Text style={[styles.overallScoreNumber, { color: getScoreColor(overallESGScore) }]}>
              {overallESGScore.toFixed(1)}%
            </Text>
            <Text style={styles.overallScoreLabel}>{getScoreLabel(overallESGScore)}</Text>
          </View>
          <View style={styles.progressBar}>
            <View 
              style={[
                styles.progressFill, 
                { 
                  width: `${overallESGScore}%`,
                  backgroundColor: getScoreColor(overallESGScore)
                }
              ]} 
            />
          </View>
        </View>
      )}

      <View style={styles.productsSection}>
        <Text style={styles.sectionTitle}>Scores por Produto</Text>
        {Object.entries(productESG).map(([productId, esgData]) => 
          renderESGItem(productId, esgData)
        )}
      </View>

      {loading && (
        <View style={styles.loadingContainer}>
          <MaterialCommunityIcons name="loading" size={24} color="#2196F3" />
          <Text style={styles.loadingText}>Calculando scores ESG...</Text>
        </View>
      )}

      {error && (
        <View style={styles.errorContainer}>
          <MaterialCommunityIcons name="alert-circle" size={24} color="#f44336" />
          <Text style={styles.errorText}>{error}</Text>
        </View>
      )}

      <View style={styles.infoSection}>
        <Text style={styles.infoTitle}>Sobre os Scores ESG</Text>
        <Text style={styles.infoText}>
          Os scores ESG avaliam o impacto ambiental, social e de governança dos produtos. 
          Scores mais altos indicam produtos mais sustentáveis e responsáveis.
        </Text>
      </View>
    </ScrollView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f5f5f5',
  },
  header: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    padding: 20,
    backgroundColor: '#fff',
    borderBottomWidth: 1,
    borderBottomColor: '#e0e0e0',
  },
  title: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#333',
  },
  refreshButton: {
    padding: 8,
  },
  overallScoreContainer: {
    backgroundColor: '#fff',
    margin: 20,
    padding: 20,
    borderRadius: 8,
    alignItems: 'center',
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 3,
  },
  overallScoreTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#333',
    marginBottom: 15,
  },
  overallScoreValue: {
    alignItems: 'center',
    marginBottom: 15,
  },
  overallScoreNumber: {
    fontSize: 48,
    fontWeight: 'bold',
  },
  overallScoreLabel: {
    fontSize: 16,
    color: '#666',
    marginTop: 5,
  },
  progressBar: {
    width: '100%',
    height: 8,
    backgroundColor: '#e0e0e0',
    borderRadius: 4,
    overflow: 'hidden',
  },
  progressFill: {
    height: '100%',
    borderRadius: 4,
  },
  productsSection: {
    padding: 20,
  },
  sectionTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#333',
    marginBottom: 15,
  },
  esgItem: {
    backgroundColor: '#fff',
    padding: 15,
    borderRadius: 8,
    marginBottom: 15,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 3,
  },
  itemHeader: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 15,
  },
  itemInfo: {
    flex: 1,
    marginLeft: 15,
  },
  itemName: {
    fontSize: 16,
    fontWeight: 'bold',
    color: '#333',
  },
  itemQuantity: {
    fontSize: 14,
    color: '#666',
    marginTop: 4,
  },
  scoreContainer: {
    alignItems: 'center',
  },
  scoreValue: {
    fontSize: 24,
    fontWeight: 'bold',
  },
  scoreLabel: {
    fontSize: 12,
    color: '#666',
    marginTop: 2,
  },
  detailsContainer: {
    flexDirection: 'row',
    justifyContent: 'space-around',
  },
  detailItem: {
    alignItems: 'center',
    flex: 1,
  },
  detailLabel: {
    fontSize: 12,
    color: '#666',
    marginTop: 4,
  },
  detailValue: {
    fontSize: 14,
    fontWeight: 'bold',
    color: '#333',
    marginTop: 2,
  },
  loadingContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    padding: 20,
  },
  loadingText: {
    color: '#2196F3',
    marginLeft: 8,
  },
  errorContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: '#ffebee',
    padding: 15,
    margin: 20,
    borderRadius: 8,
  },
  errorText: {
    color: '#f44336',
    marginLeft: 8,
    flex: 1,
  },
  infoSection: {
    backgroundColor: '#fff',
    margin: 20,
    padding: 20,
    borderRadius: 8,
  },
  infoTitle: {
    fontSize: 16,
    fontWeight: 'bold',
    color: '#333',
    marginBottom: 10,
  },
  infoText: {
    fontSize: 14,
    color: '#666',
    lineHeight: 20,
  },
  emptyContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    padding: 40,
    backgroundColor: '#f5f5f5',
  },
  emptyTitle: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#333',
    marginTop: 20,
    marginBottom: 10,
  },
  emptySubtitle: {
    fontSize: 16,
    color: '#666',
    textAlign: 'center',
    marginBottom: 30,
  },
  scanButton: {
    backgroundColor: '#2196F3',
    flexDirection: 'row',
    alignItems: 'center',
    paddingHorizontal: 30,
    paddingVertical: 15,
    borderRadius: 8,
  },
  scanButtonText: {
    color: '#fff',
    fontSize: 16,
    fontWeight: 'bold',
    marginLeft: 8,
  },
});

export default ESGScreen;
