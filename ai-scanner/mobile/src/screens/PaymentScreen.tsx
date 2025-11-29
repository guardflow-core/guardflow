import React, { useState } from 'react';
import { View, Text, StyleSheet, TouchableOpacity, Alert, ScrollView, TextInput } from 'react-native';
import { useDispatch, useSelector } from 'react-redux';
import { AppDispatch, RootState } from '../store';
import { initiatePayment, paymentSuccess, paymentFailed, resetPayment } from '../store/slices/paymentSlice';
import { clearCart } from '../store/slices/cartSlice';
import { MaterialCommunityIcons } from '@expo/vector-icons';

const PaymentScreen: React.FC = () => {
  const dispatch: AppDispatch = useDispatch();
  const { items, totalAmount } = useSelector((state: RootState) => state.cart);
  const { status, transactionId, amount, method, error } = useSelector((state: RootState) => state.payment);
  
  const [selectedPaymentMethod, setSelectedPaymentMethod] = useState<'pix' | 'card' | 'cash'>('pix');
  const [cardInfo, setCardInfo] = useState({
    number: '',
    expiry: '',
    cvv: '',
    name: '',
  });

  const paymentMethods = [
    { id: 'pix', name: 'PIX', icon: 'qrcode', color: '#32BCAD' },
    { id: 'card', name: 'Cartão', icon: 'credit-card', color: '#2196F3' },
    { id: 'cash', name: 'Dinheiro', icon: 'cash', color: '#4CAF50' },
  ];

  const handlePayment = () => {
    if (items.length === 0) {
      Alert.alert('Erro', 'Carrinho vazio. Adicione produtos antes de pagar.');
      return;
    }

    if (selectedPaymentMethod === 'card' && (!cardInfo.number || !cardInfo.expiry || !cardInfo.cvv || !cardInfo.name)) {
      Alert.alert('Erro', 'Preencha todos os dados do cartão.');
      return;
    }

    dispatch(initiatePayment({ amount: totalAmount, method: selectedPaymentMethod }));
    
    // Simulate payment processing
    setTimeout(() => {
      const success = Math.random() > 0.1; // 90% success rate
      if (success) {
        const transactionId = `TXN${Date.now()}`;
        dispatch(paymentSuccess(transactionId));
        dispatch(clearCart());
        Alert.alert(
          'Pagamento Aprovado!',
          `Transação: ${transactionId}\nValor: R$ ${totalAmount.toFixed(2)}`,
          [{ text: 'OK', onPress: () => dispatch(resetPayment()) }]
        );
      } else {
        dispatch(paymentFailed('Falha no processamento do pagamento. Tente novamente.'));
        Alert.alert('Erro', 'Falha no processamento do pagamento. Tente novamente.');
      }
    }, 2000);
  };

  const handleResetPayment = () => {
    dispatch(resetPayment());
  };

  const renderCartSummary = () => (
    <View style={styles.cartSummary}>
      <Text style={styles.summaryTitle}>Resumo do Pedido</Text>
      {items.map((item) => (
        <View key={item.productId} style={styles.cartItem}>
          <Text style={styles.itemName}>{item.name}</Text>
          <Text style={styles.itemQuantity}>x{item.quantity}</Text>
          <Text style={styles.itemPrice}>R$ {(item.price * item.quantity).toFixed(2)}</Text>
        </View>
      ))}
      <View style={styles.totalRow}>
        <Text style={styles.totalLabel}>Total:</Text>
        <Text style={styles.totalAmount}>R$ {totalAmount.toFixed(2)}</Text>
      </View>
    </View>
  );

  const renderPaymentMethod = () => (
    <View style={styles.paymentMethodSection}>
      <Text style={styles.sectionTitle}>Método de Pagamento</Text>
      <View style={styles.paymentMethods}>
        {paymentMethods.map((method) => (
          <TouchableOpacity
            key={method.id}
            style={[
              styles.paymentMethodButton,
              selectedPaymentMethod === method.id && styles.paymentMethodButtonSelected
            ]}
            onPress={() => setSelectedPaymentMethod(method.id as any)}
          >
            <MaterialCommunityIcons 
              name={method.icon as any} 
              size={24} 
              color={selectedPaymentMethod === method.id ? '#fff' : method.color} 
            />
            <Text style={[
              styles.paymentMethodText,
              selectedPaymentMethod === method.id && styles.paymentMethodTextSelected
            ]}>
              {method.name}
            </Text>
          </TouchableOpacity>
        ))}
      </View>
    </View>
  );

  const renderCardForm = () => {
    if (selectedPaymentMethod !== 'card') return null;

    return (
      <View style={styles.cardForm}>
        <Text style={styles.formTitle}>Dados do Cartão</Text>
        <TextInput
          style={styles.input}
          placeholder="Número do cartão"
          value={cardInfo.number}
          onChangeText={(text) => setCardInfo({ ...cardInfo, number: text })}
          keyboardType="numeric"
        />
        <View style={styles.row}>
          <TextInput
            style={[styles.input, styles.halfInput]}
            placeholder="MM/AA"
            value={cardInfo.expiry}
            onChangeText={(text) => setCardInfo({ ...cardInfo, expiry: text })}
          />
          <TextInput
            style={[styles.input, styles.halfInput]}
            placeholder="CVV"
            value={cardInfo.cvv}
            onChangeText={(text) => setCardInfo({ ...cardInfo, cvv: text })}
            keyboardType="numeric"
            secureTextEntry
          />
        </View>
        <TextInput
          style={styles.input}
          placeholder="Nome no cartão"
          value={cardInfo.name}
          onChangeText={(text) => setCardInfo({ ...cardInfo, name: text })}
        />
      </View>
    );
  };

  const renderPaymentStatus = () => {
    if (status === 'idle') return null;

    return (
      <View style={styles.statusContainer}>
        {status === 'processing' && (
          <View style={styles.processingContainer}>
            <MaterialCommunityIcons name="loading" size={24} color="#2196F3" />
            <Text style={styles.statusText}>Processando pagamento...</Text>
          </View>
        )}
        
        {status === 'success' && (
          <View style={styles.successContainer}>
            <MaterialCommunityIcons name="check-circle" size={24} color="#4CAF50" />
            <Text style={styles.statusText}>Pagamento aprovado!</Text>
            <Text style={styles.transactionId}>Transação: {transactionId}</Text>
          </View>
        )}
        
        {status === 'failed' && (
          <View style={styles.errorContainer}>
            <MaterialCommunityIcons name="alert-circle" size={24} color="#f44336" />
            <Text style={styles.statusText}>{error}</Text>
            <TouchableOpacity style={styles.retryButton} onPress={handleResetPayment}>
              <Text style={styles.retryButtonText}>Tentar Novamente</Text>
            </TouchableOpacity>
          </View>
        )}
      </View>
    );
  };

  if (items.length === 0) {
    return (
      <View style={styles.emptyContainer}>
        <MaterialCommunityIcons name="cart-outline" size={80} color="#ccc" />
        <Text style={styles.emptyTitle}>Carrinho Vazio</Text>
        <Text style={styles.emptySubtitle}>Adicione produtos ao carrinho antes de pagar</Text>
      </View>
    );
  }

  return (
    <ScrollView style={styles.container}>
      <View style={styles.header}>
        <Text style={styles.title}>Pagamento</Text>
      </View>

      {renderCartSummary()}
      {renderPaymentMethod()}
      {renderCardForm()}
      {renderPaymentStatus()}

      <View style={styles.footer}>
        <TouchableOpacity
          style={[
            styles.payButton,
            status === 'processing' && styles.payButtonDisabled
          ]}
          onPress={handlePayment}
          disabled={status === 'processing'}
        >
          <MaterialCommunityIcons name="credit-card" size={24} color="#fff" />
          <Text style={styles.payButtonText}>
            {status === 'processing' ? 'Processando...' : `Pagar R$ ${totalAmount.toFixed(2)}`}
          </Text>
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
    backgroundColor: '#fff',
    padding: 20,
    borderBottomWidth: 1,
    borderBottomColor: '#e0e0e0',
  },
  title: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#333',
    textAlign: 'center',
  },
  cartSummary: {
    backgroundColor: '#fff',
    margin: 20,
    padding: 20,
    borderRadius: 8,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 3,
  },
  summaryTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#333',
    marginBottom: 15,
  },
  cartItem: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    paddingVertical: 8,
    borderBottomWidth: 1,
    borderBottomColor: '#f0f0f0',
  },
  itemName: {
    fontSize: 14,
    color: '#333',
    flex: 1,
  },
  itemQuantity: {
    fontSize: 14,
    color: '#666',
    marginHorizontal: 10,
  },
  itemPrice: {
    fontSize: 14,
    fontWeight: 'bold',
    color: '#333',
  },
  totalRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginTop: 15,
    paddingTop: 15,
    borderTopWidth: 1,
    borderTopColor: '#e0e0e0',
  },
  totalLabel: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#333',
  },
  totalAmount: {
    fontSize: 20,
    fontWeight: 'bold',
    color: '#2196F3',
  },
  paymentMethodSection: {
    backgroundColor: '#fff',
    margin: 20,
    padding: 20,
    borderRadius: 8,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 3,
  },
  sectionTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#333',
    marginBottom: 15,
  },
  paymentMethods: {
    flexDirection: 'row',
    justifyContent: 'space-around',
  },
  paymentMethodButton: {
    flexDirection: 'row',
    alignItems: 'center',
    padding: 15,
    borderRadius: 8,
    borderWidth: 2,
    borderColor: '#e0e0e0',
    flex: 1,
    marginHorizontal: 5,
    justifyContent: 'center',
  },
  paymentMethodButtonSelected: {
    backgroundColor: '#2196F3',
    borderColor: '#2196F3',
  },
  paymentMethodText: {
    fontSize: 14,
    fontWeight: 'bold',
    color: '#666',
    marginLeft: 8,
  },
  paymentMethodTextSelected: {
    color: '#fff',
  },
  cardForm: {
    backgroundColor: '#fff',
    margin: 20,
    padding: 20,
    borderRadius: 8,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 3,
  },
  formTitle: {
    fontSize: 16,
    fontWeight: 'bold',
    color: '#333',
    marginBottom: 15,
  },
  input: {
    borderWidth: 1,
    borderColor: '#ddd',
    borderRadius: 8,
    padding: 12,
    fontSize: 16,
    backgroundColor: '#f9f9f9',
    marginBottom: 15,
  },
  row: {
    flexDirection: 'row',
    justifyContent: 'space-between',
  },
  halfInput: {
    width: '48%',
  },
  statusContainer: {
    margin: 20,
  },
  processingContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: '#e3f2fd',
    padding: 15,
    borderRadius: 8,
  },
  successContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: '#e8f5e8',
    padding: 15,
    borderRadius: 8,
  },
  errorContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: '#ffebee',
    padding: 15,
    borderRadius: 8,
  },
  statusText: {
    color: '#333',
    marginLeft: 8,
    flex: 1,
  },
  transactionId: {
    color: '#666',
    fontSize: 12,
    marginLeft: 8,
  },
  retryButton: {
    backgroundColor: '#f44336',
    paddingHorizontal: 15,
    paddingVertical: 8,
    borderRadius: 6,
    marginLeft: 10,
  },
  retryButtonText: {
    color: '#fff',
    fontSize: 12,
    fontWeight: 'bold',
  },
  footer: {
    backgroundColor: '#fff',
    padding: 20,
    borderTopWidth: 1,
    borderTopColor: '#e0e0e0',
  },
  payButton: {
    backgroundColor: '#4CAF50',
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    padding: 15,
    borderRadius: 8,
  },
  payButtonDisabled: {
    backgroundColor: '#ccc',
  },
  payButtonText: {
    color: '#fff',
    fontSize: 18,
    fontWeight: 'bold',
    marginLeft: 8,
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
  },
});

export default PaymentScreen;
