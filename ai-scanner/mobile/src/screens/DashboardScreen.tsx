import React from 'react';
import { View, Text, StyleSheet, ScrollView, TouchableOpacity } from 'react-native';
import { useSelector } from 'react-redux';
import { RootState } from '../store';
import { MaterialCommunityIcons } from '@expo/vector-icons';

const DashboardScreen: React.FC = () => {
  const { profile } = useSelector((state: RootState) => state.user);
  const { items, totalAmount } = useSelector((state: RootState) => state.cart);
  const { overallESGScore } = useSelector((state: RootState) => state.esg);

  const stats = [
    { title: 'Itens no Carrinho', value: items.length.toString(), icon: 'cart', color: '#4CAF50' },
    { title: 'Total', value: `R$ ${totalAmount.toFixed(2)}`, icon: 'currency-usd', color: '#2196F3' },
    { title: 'Score ESG', value: overallESGScore ? `${overallESGScore.toFixed(1)}%` : 'N/A', icon: 'leaf', color: '#8BC34A' },
  ];

  return (
    <ScrollView style={styles.container}>
      <View style={styles.header}>
        <Text style={styles.welcomeText}>
          Bem-vindo, {profile?.name || 'Usuário'}!
        </Text>
        <Text style={styles.subtitle}>Agilizia_AI Mobile</Text>
      </View>

      <View style={styles.statsContainer}>
        {stats.map((stat, index) => (
          <View key={index} style={styles.statCard}>
            <MaterialCommunityIcons name={stat.icon as any} size={24} color={stat.color} />
            <Text style={styles.statValue}>{stat.value}</Text>
            <Text style={styles.statTitle}>{stat.title}</Text>
          </View>
        ))}
      </View>

      <View style={styles.quickActions}>
        <Text style={styles.sectionTitle}>Ações Rápidas</Text>
        <TouchableOpacity style={styles.actionButton}>
          <MaterialCommunityIcons name="barcode-scan" size={24} color="#fff" />
          <Text style={styles.actionButtonText}>Escanear Produto</Text>
        </TouchableOpacity>
        <TouchableOpacity style={styles.actionButton}>
          <MaterialCommunityIcons name="cart" size={24} color="#fff" />
          <Text style={styles.actionButtonText}>Ver Carrinho</Text>
        </TouchableOpacity>
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
    padding: 20,
    backgroundColor: '#fff',
    borderBottomWidth: 1,
    borderBottomColor: '#e0e0e0',
  },
  welcomeText: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#333',
  },
  subtitle: {
    fontSize: 16,
    color: '#666',
    marginTop: 4,
  },
  statsContainer: {
    flexDirection: 'row',
    justifyContent: 'space-around',
    padding: 20,
    backgroundColor: '#fff',
    marginTop: 10,
  },
  statCard: {
    alignItems: 'center',
    flex: 1,
  },
  statValue: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#333',
    marginTop: 8,
  },
  statTitle: {
    fontSize: 12,
    color: '#666',
    marginTop: 4,
    textAlign: 'center',
  },
  quickActions: {
    padding: 20,
    backgroundColor: '#fff',
    marginTop: 10,
  },
  sectionTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#333',
    marginBottom: 15,
  },
  actionButton: {
    backgroundColor: '#2196F3',
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    padding: 15,
    borderRadius: 8,
    marginBottom: 10,
  },
  actionButtonText: {
    color: '#fff',
    fontSize: 16,
    fontWeight: 'bold',
    marginLeft: 8,
  },
});

export default DashboardScreen;
