import React, { useState } from 'react';
import { View, Text, StyleSheet, TouchableOpacity, Alert, ScrollView, TextInput } from 'react-native';
import { useDispatch, useSelector } from 'react-redux';
import { AppDispatch, RootState } from '../store';
import { logout } from '../store/slices/authSlice';
import { updateUserProfile, clearUserProfile } from '../store/slices/userSlice';
import { MaterialCommunityIcons } from '@expo/vector-icons';

const ProfileScreen: React.FC = () => {
  const dispatch: AppDispatch = useDispatch();
  const { profile, loading } = useSelector((state: RootState) => state.user);
  const [isEditing, setIsEditing] = useState(false);
  const [editForm, setEditForm] = useState({
    name: profile?.name || '',
    email: profile?.email || '',
  });

  const handleLogout = () => {
    Alert.alert(
      'Logout',
      'Tem certeza que deseja sair da sua conta?',
      [
        { text: 'Cancelar', style: 'cancel' },
        { 
          text: 'Sair', 
          style: 'destructive', 
          onPress: () => {
            dispatch(logout());
            dispatch(clearUserProfile());
          }
        },
      ]
    );
  };

  const handleEditProfile = () => {
    setIsEditing(true);
    setEditForm({
      name: profile?.name || '',
      email: profile?.email || '',
    });
  };

  const handleSaveProfile = () => {
    if (!editForm.name.trim() || !editForm.email.trim()) {
      Alert.alert('Erro', 'Por favor, preencha todos os campos.');
      return;
    }
    
    dispatch(updateUserProfile(editForm));
    setIsEditing(false);
    Alert.alert('Sucesso', 'Perfil atualizado com sucesso!');
  };

  const handleCancelEdit = () => {
    setIsEditing(false);
    setEditForm({
      name: profile?.name || '',
      email: profile?.email || '',
    });
  };

  const menuItems = [
    { icon: 'history', title: 'Histórico de Compras', onPress: () => Alert.alert('Em breve', 'Funcionalidade em desenvolvimento') },
    { icon: 'heart', title: 'Produtos Favoritos', onPress: () => Alert.alert('Em breve', 'Funcionalidade em desenvolvimento') },
    { icon: 'bell', title: 'Notificações', onPress: () => Alert.alert('Em breve', 'Funcionalidade em desenvolvimento') },
    { icon: 'help-circle', title: 'Ajuda e Suporte', onPress: () => Alert.alert('Em breve', 'Funcionalidade em desenvolvimento') },
    { icon: 'information', title: 'Sobre o App', onPress: () => Alert.alert('Agilizia_AI', 'Versão 1.0.0\nDesenvolvido com React Native e Expo') },
  ];

  return (
    <ScrollView style={styles.container}>
      <View style={styles.header}>
        <View style={styles.avatarContainer}>
          <MaterialCommunityIcons name="account-circle" size={80} color="#2196F3" />
        </View>
        <Text style={styles.userName}>{profile?.name || 'Usuário'}</Text>
        <Text style={styles.userEmail}>{profile?.email || 'email@exemplo.com'}</Text>
      </View>

      <View style={styles.profileSection}>
        <View style={styles.sectionHeader}>
          <Text style={styles.sectionTitle}>Informações Pessoais</Text>
          {!isEditing && (
            <TouchableOpacity style={styles.editButton} onPress={handleEditProfile}>
              <MaterialCommunityIcons name="pencil" size={20} color="#2196F3" />
              <Text style={styles.editButtonText}>Editar</Text>
            </TouchableOpacity>
          )}
        </View>

        {isEditing ? (
          <View style={styles.editForm}>
            <View style={styles.inputContainer}>
              <Text style={styles.inputLabel}>Nome</Text>
              <TextInput
                style={styles.textInput}
                value={editForm.name}
                onChangeText={(text) => setEditForm({ ...editForm, name: text })}
                placeholder="Digite seu nome"
              />
            </View>
            <View style={styles.inputContainer}>
              <Text style={styles.inputLabel}>Email</Text>
              <TextInput
                style={styles.textInput}
                value={editForm.email}
                onChangeText={(text) => setEditForm({ ...editForm, email: text })}
                placeholder="Digite seu email"
                keyboardType="email-address"
              />
            </View>
            <View style={styles.editActions}>
              <TouchableOpacity style={styles.cancelButton} onPress={handleCancelEdit}>
                <Text style={styles.cancelButtonText}>Cancelar</Text>
              </TouchableOpacity>
              <TouchableOpacity style={styles.saveButton} onPress={handleSaveProfile}>
                <Text style={styles.saveButtonText}>Salvar</Text>
              </TouchableOpacity>
            </View>
          </View>
        ) : (
          <View style={styles.profileInfo}>
            <View style={styles.infoItem}>
              <MaterialCommunityIcons name="account" size={20} color="#666" />
              <Text style={styles.infoLabel}>Nome:</Text>
              <Text style={styles.infoValue}>{profile?.name || 'Não informado'}</Text>
            </View>
            <View style={styles.infoItem}>
              <MaterialCommunityIcons name="email" size={20} color="#666" />
              <Text style={styles.infoLabel}>Email:</Text>
              <Text style={styles.infoValue}>{profile?.email || 'Não informado'}</Text>
            </View>
          </View>
        )}
      </View>

      <View style={styles.menuSection}>
        <Text style={styles.sectionTitle}>Menu</Text>
        {menuItems.map((item, index) => (
          <TouchableOpacity key={index} style={styles.menuItem} onPress={item.onPress}>
            <MaterialCommunityIcons name={item.icon as any} size={24} color="#666" />
            <Text style={styles.menuItemText}>{item.title}</Text>
            <MaterialCommunityIcons name="chevron-right" size={24} color="#ccc" />
          </TouchableOpacity>
        ))}
      </View>

      <View style={styles.logoutSection}>
        <TouchableOpacity style={styles.logoutButton} onPress={handleLogout}>
          <MaterialCommunityIcons name="logout" size={24} color="#f44336" />
          <Text style={styles.logoutButtonText}>Sair da Conta</Text>
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
    alignItems: 'center',
    padding: 30,
    borderBottomWidth: 1,
    borderBottomColor: '#e0e0e0',
  },
  avatarContainer: {
    marginBottom: 15,
  },
  userName: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#333',
    marginBottom: 5,
  },
  userEmail: {
    fontSize: 16,
    color: '#666',
  },
  profileSection: {
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
  sectionHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 20,
  },
  sectionTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#333',
  },
  editButton: {
    flexDirection: 'row',
    alignItems: 'center',
    padding: 8,
  },
  editButtonText: {
    color: '#2196F3',
    marginLeft: 4,
    fontWeight: 'bold',
  },
  editForm: {
    marginTop: 10,
  },
  inputContainer: {
    marginBottom: 15,
  },
  inputLabel: {
    fontSize: 14,
    fontWeight: 'bold',
    color: '#333',
    marginBottom: 5,
  },
  textInput: {
    borderWidth: 1,
    borderColor: '#ddd',
    borderRadius: 8,
    padding: 12,
    fontSize: 16,
    backgroundColor: '#f9f9f9',
  },
  editActions: {
    flexDirection: 'row',
    justifyContent: 'flex-end',
    marginTop: 20,
  },
  cancelButton: {
    paddingHorizontal: 20,
    paddingVertical: 10,
    marginRight: 10,
    borderRadius: 6,
    borderWidth: 1,
    borderColor: '#ddd',
  },
  cancelButtonText: {
    color: '#666',
    fontWeight: 'bold',
  },
  saveButton: {
    backgroundColor: '#4CAF50',
    paddingHorizontal: 20,
    paddingVertical: 10,
    borderRadius: 6,
  },
  saveButtonText: {
    color: '#fff',
    fontWeight: 'bold',
  },
  profileInfo: {
    marginTop: 10,
  },
  infoItem: {
    flexDirection: 'row',
    alignItems: 'center',
    paddingVertical: 10,
    borderBottomWidth: 1,
    borderBottomColor: '#f0f0f0',
  },
  infoLabel: {
    fontSize: 16,
    color: '#666',
    marginLeft: 10,
    minWidth: 60,
  },
  infoValue: {
    fontSize: 16,
    color: '#333',
    flex: 1,
    marginLeft: 10,
  },
  menuSection: {
    backgroundColor: '#fff',
    margin: 20,
    borderRadius: 8,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 3,
  },
  menuItem: {
    flexDirection: 'row',
    alignItems: 'center',
    padding: 20,
    borderBottomWidth: 1,
    borderBottomColor: '#f0f0f0',
  },
  menuItemText: {
    fontSize: 16,
    color: '#333',
    flex: 1,
    marginLeft: 15,
  },
  logoutSection: {
    margin: 20,
  },
  logoutButton: {
    backgroundColor: '#fff',
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    padding: 20,
    borderRadius: 8,
    borderWidth: 1,
    borderColor: '#f44336',
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 3,
  },
  logoutButtonText: {
    color: '#f44336',
    fontSize: 16,
    fontWeight: 'bold',
    marginLeft: 8,
  },
});

export default ProfileScreen;
