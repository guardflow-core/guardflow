/**
 * GuardFlow Users Management Page
 * Página de gestão de usuários com CRUD completo
 */

import React, { useState, useEffect, useCallback } from 'react';
import {
  Box,
  Card,
  CardContent,
  Typography,
  Button,
  Alert,
  CircularProgress,
  Chip,
  Avatar,
  List,
  ListItem,
  ListItemAvatar,
  ListItemText,
  IconButton,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField,
  Grid,
  Divider,
  Paper,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  TablePagination,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Tooltip,
  Menu,
  MenuList,
  MenuItem as MenuItemComponent,
  ListItemIcon,
  Fab,
  InputAdornment,
} from '@mui/material';
import {
  People,
  Add,
  Edit,
  Delete,
  Search,
  FilterList,
  MoreVert,
  PersonAdd,
  Block,
  CheckCircle,
  Warning,
  AdminPanelSettings,
  Person,
  Store,
  Security,
  Email,
  Phone,
  LocationOn,
  CalendarToday,
  TrendingUp,
  Assignment,
  Visibility,
  VisibilityOff,
} from '@mui/icons-material';

interface User {
  id: string;
  name: string;
  email: string;
  phone?: string;
  role: 'admin' | 'manager' | 'cashier' | 'customer';
  status: 'active' | 'inactive' | 'blocked';
  store?: string;
  lastLogin?: string;
  createdAt: string;
  avatar?: string;
  permissions: string[];
  esgScore?: number;
  totalPurchases?: number;
  totalSpent?: number;
}

interface UserFormData {
  name: string;
  email: string;
  phone: string;
  role: 'admin' | 'manager' | 'cashier' | 'customer';
  status: string;
  store: string;
  permissions: string[];
}

const UsersPage: React.FC = () => {
  const [users, setUsers] = useState<User[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [searchTerm, setSearchTerm] = useState('');
  const [roleFilter, setRoleFilter] = useState('all');
  const [statusFilter, setStatusFilter] = useState('all');
  const [page, setPage] = useState(0);
  const [rowsPerPage, setRowsPerPage] = useState(10);
  const [showUserDialog, setShowUserDialog] = useState(false);
  const [editingUser, setEditingUser] = useState<User | null>(null);
  const [userForm, setUserForm] = useState<UserFormData>({
    name: '',
    email: '',
    phone: '',
    role: 'customer',
    status: 'active',
    store: '',
    permissions: [],
  });
  const [anchorEl, setAnchorEl] = useState<null | HTMLElement>(null);
  const [selectedUser, setSelectedUser] = useState<User | null>(null);

  const roles = [
    { value: 'admin', label: 'Administrador', icon: <AdminPanelSettings />, color: 'error' },
    { value: 'manager', label: 'Gerente', icon: <Assignment />, color: 'warning' },
    { value: 'cashier', label: 'Operador', icon: <Person />, color: 'info' },
    { value: 'customer', label: 'Cliente', icon: <People />, color: 'primary' },
  ];

  const statuses = [
    { value: 'active', label: 'Ativo', color: 'success' },
    { value: 'inactive', label: 'Inativo', color: 'default' },
    { value: 'blocked', label: 'Bloqueado', color: 'error' },
  ];

  const stores = [
    'Loja Centro',
    'Loja Shopping',
    'Loja Bairro',
    'Loja Norte',
    'Loja Sul',
  ];

  const permissions = [
    'users.read',
    'users.write',
    'products.read',
    'products.write',
    'sales.read',
    'sales.write',
    'reports.read',
    'reports.write',
    'settings.read',
    'settings.write',
  ];

  useEffect(() => {
    loadUsers();
  }, []);

  const loadUsers = useCallback(async () => {
    setLoading(true);
    try {
      // Simular carregamento de usuários
      // Em produção, faria chamada para API
      const mockUsers: User[] = [
        {
          id: '1',
          name: 'João Silva',
          email: 'joao.silva@guardflow.com',
          phone: '+55 11 99999-9999',
          role: 'admin',
          status: 'active',
          store: 'Loja Centro',
          lastLogin: '2025-10-20T10:30:00Z',
          createdAt: '2025-01-15T08:00:00Z',
          permissions: ['users.read', 'users.write', 'products.read', 'products.write', 'sales.read', 'sales.write', 'reports.read', 'reports.write', 'settings.read', 'settings.write'],
          esgScore: 8.5,
          totalPurchases: 0,
          totalSpent: 0,
        },
        {
          id: '2',
          name: 'Maria Santos',
          email: 'maria.santos@guardflow.com',
          phone: '+55 11 88888-8888',
          role: 'manager',
          status: 'active',
          store: 'Loja Shopping',
          lastLogin: '2025-10-20T09:15:00Z',
          createdAt: '2025-02-10T09:30:00Z',
          permissions: ['products.read', 'products.write', 'sales.read', 'sales.write', 'reports.read'],
          esgScore: 7.8,
          totalPurchases: 0,
          totalSpent: 0,
        },
        {
          id: '3',
          name: 'Carlos Oliveira',
          email: 'carlos.oliveira@guardflow.com',
          phone: '+55 11 77777-7777',
          role: 'cashier',
          status: 'active',
          store: 'Loja Centro',
          lastLogin: '2025-10-20T08:45:00Z',
          createdAt: '2025-03-05T14:20:00Z',
          permissions: ['sales.read', 'sales.write'],
          esgScore: 6.9,
          totalPurchases: 0,
          totalSpent: 0,
        },
        {
          id: '4',
          name: 'Ana Costa',
          email: 'ana.costa@email.com',
          phone: '+55 11 66666-6666',
          role: 'customer',
          status: 'active',
          lastLogin: '2025-10-19T20:30:00Z',
          createdAt: '2025-05-20T16:45:00Z',
          permissions: [],
          esgScore: 8.2,
          totalPurchases: 45,
          totalSpent: 1250.80,
        },
        {
          id: '5',
          name: 'Pedro Almeida',
          email: 'pedro.almeida@email.com',
          phone: '+55 11 55555-5555',
          role: 'customer',
          status: 'inactive',
          lastLogin: '2025-09-15T12:00:00Z',
          createdAt: '2025-04-10T11:30:00Z',
          permissions: [],
          esgScore: 7.1,
          totalPurchases: 12,
          totalSpent: 345.60,
        },
      ];

      setUsers(mockUsers);
    } catch (err) {
      setError('Erro ao carregar usuários');
      console.error('Load users error:', err);
    } finally {
      setLoading(false);
    }
  }, []);

  const handleCreateUser = () => {
    setEditingUser(null);
    setUserForm({
      name: '',
      email: '',
      phone: '',
      role: 'customer',
      status: 'active',
      store: '',
      permissions: [],
    });
    setShowUserDialog(true);
  };

  const handleEditUser = (user: User) => {
    setEditingUser(user);
    setUserForm({
      name: user.name,
      email: user.email,
      phone: user.phone || '',
      role: user.role,
      status: user.status,
      store: user.store || '',
      permissions: user.permissions,
    });
    setShowUserDialog(true);
    setAnchorEl(null);
  };

  const handleDeleteUser = async (userId: string) => {
    if (!window.confirm('Tem certeza que deseja excluir este usuário?')) {
      return;
    }

    try {
      setUsers(prev => prev.filter(user => user.id !== userId));
      setAnchorEl(null);
    } catch (err) {
      setError('Erro ao excluir usuário');
    }
  };

  const handleSaveUser = async () => {
    if (!userForm.name || !userForm.email) {
      setError('Nome e email são obrigatórios');
      return;
    }

    try {
      setLoading(true);

      if (editingUser) {
        // Atualizar usuário existente
        setUsers(prev => prev.map(user => 
          user.id === editingUser.id 
            ? { 
                ...user, 
                ...userForm,
                permissions: userForm.permissions,
              }
            : user
        ));
      } else {
        // Criar novo usuário
        const newUser: User = {
          id: `user_${Date.now()}`,
          ...userForm,
          createdAt: new Date().toISOString(),
          esgScore: Math.round((Math.random() * 3 + 6) * 10) / 10,
          totalPurchases: 0,
          totalSpent: 0,
        };
        setUsers(prev => [newUser, ...prev]);
      }

      setShowUserDialog(false);
      setError(null);
    } catch (err) {
      setError('Erro ao salvar usuário');
    } finally {
      setLoading(false);
    }
  };

  const handleToggleUserStatus = async (userId: string, newStatus: string) => {
    try {
      setUsers(prev => prev.map(user => 
        user.id === userId ? { ...user, status: newStatus as any } : user
      ));
      setAnchorEl(null);
    } catch (err) {
      setError('Erro ao alterar status do usuário');
    }
  };

  const filteredUsers = users.filter(user => {
    const matchesSearch = user.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         user.email.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesRole = roleFilter === 'all' || user.role === roleFilter;
    const matchesStatus = statusFilter === 'all' || user.status === statusFilter;
    
    return matchesSearch && matchesRole && matchesStatus;
  });

  const paginatedUsers = filteredUsers.slice(page * rowsPerPage, page * rowsPerPage + rowsPerPage);

  const getRoleInfo = (role: 'admin' | 'manager' | 'cashier' | 'customer') => roles.find(r => r.value === role) || roles[3];
  const getStatusInfo = (status: string) => statuses.find(s => s.value === status) || statuses[0];

  const handleMenuClick = (event: React.MouseEvent<HTMLElement>, user: User) => {
    setAnchorEl(event.currentTarget);
    setSelectedUser(user);
  };

  const handleMenuClose = () => {
    setAnchorEl(null);
    setSelectedUser(null);
  };

  return (
    <Box sx={{ p: 3, maxWidth: 1400, mx: 'auto' }}>
      {/* Header */}
      <Box sx={{ mb: 4 }}>
        <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
          <Box>
            <Typography variant="h4" fontWeight="bold" gutterBottom>
              👥 Gestão de Usuários
            </Typography>
            <Typography variant="body1" color="text.secondary">
              {filteredUsers.length} usuários encontrados
            </Typography>
          </Box>
          <Button
            variant="contained"
            startIcon={<PersonAdd />}
            onClick={handleCreateUser}
            size="large"
          >
            Novo Usuário
          </Button>
        </Box>

        {error && (
          <Alert severity="error" sx={{ mb: 3 }} onClose={() => setError(null)}>
            {error}
          </Alert>
        )}
      </Box>

      {/* Filtros */}
      <Card sx={{ mb: 3 }}>
        <CardContent>
          <Grid container spacing={2} alignItems="center">
            <Grid item xs={12} md={4}>
              <TextField
                fullWidth
                placeholder="Buscar usuários..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                InputProps={{
                  startAdornment: (
                    <InputAdornment position="start">
                      <Search />
                    </InputAdornment>
                  ),
                }}
              />
            </Grid>
            <Grid item xs={12} md={3}>
              <FormControl fullWidth>
                <InputLabel>Função</InputLabel>
                <Select
                  value={roleFilter}
                  label="Função"
                  onChange={(e) => setRoleFilter(e.target.value)}
                >
                  <MenuItem value="all">Todas as funções</MenuItem>
                  {roles.map((role) => (
                    <MenuItem key={role.value} value={role.value}>
                      {role.label}
                    </MenuItem>
                  ))}
                </Select>
              </FormControl>
            </Grid>
            <Grid item xs={12} md={3}>
              <FormControl fullWidth>
                <InputLabel>Status</InputLabel>
                <Select
                  value={statusFilter}
                  label="Status"
                  onChange={(e) => setStatusFilter(e.target.value)}
                >
                  <MenuItem value="all">Todos os status</MenuItem>
                  {statuses.map((status) => (
                    <MenuItem key={status.value} value={status.value}>
                      {status.label}
                    </MenuItem>
                  ))}
                </Select>
              </FormControl>
            </Grid>
            <Grid item xs={12} md={2}>
              <Button
                variant="outlined"
                startIcon={<FilterList />}
                onClick={() => {
                  setSearchTerm('');
                  setRoleFilter('all');
                  setStatusFilter('all');
                }}
                fullWidth
              >
                Limpar
              </Button>
            </Grid>
          </Grid>
        </CardContent>
      </Card>

      {/* Tabela de usuários */}
      <Card>
        <TableContainer>
          <Table>
            <TableHead>
              <TableRow>
                <TableCell>Usuário</TableCell>
                <TableCell>Função</TableCell>
                <TableCell>Status</TableCell>
                <TableCell>Loja</TableCell>
                <TableCell>Último Login</TableCell>
                <TableCell align="center">ESG Score</TableCell>
                <TableCell align="center">Compras</TableCell>
                <TableCell align="right">Ações</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {loading ? (
                <TableRow>
                  <TableCell colSpan={8} align="center" sx={{ py: 4 }}>
                    <CircularProgress />
                  </TableCell>
                </TableRow>
              ) : paginatedUsers.length === 0 ? (
                <TableRow>
                  <TableCell colSpan={8} align="center" sx={{ py: 4 }}>
                    <Typography variant="body1" color="text.secondary">
                      Nenhum usuário encontrado
                    </Typography>
                  </TableCell>
                </TableRow>
              ) : (
                paginatedUsers.map((user) => {
                  const roleInfo = getRoleInfo(user.role);
                  const statusInfo = getStatusInfo(user.status);
                  
                  return (
                    <TableRow key={user.id} hover>
                      <TableCell>
                        <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
                          <Avatar sx={{ bgcolor: `${roleInfo.color}.main` }}>
                            {user.name.charAt(0).toUpperCase()}
                          </Avatar>
                          <Box>
                            <Typography variant="subtitle2" fontWeight="bold">
                              {user.name}
                            </Typography>
                            <Typography variant="body2" color="text.secondary">
                              {user.email}
                            </Typography>
                            {user.phone && (
                              <Typography variant="caption" color="text.secondary">
                                {user.phone}
                              </Typography>
                            )}
                          </Box>
                        </Box>
                      </TableCell>
                      <TableCell>
                        <Chip
                          icon={roleInfo.icon}
                          label={roleInfo.label}
                          color={roleInfo.color as any}
                          size="small"
                        />
                      </TableCell>
                      <TableCell>
                        <Chip
                          label={statusInfo.label}
                          color={statusInfo.color as any}
                          size="small"
                          variant={user.status === 'active' ? 'filled' : 'outlined'}
                        />
                      </TableCell>
                      <TableCell>
                        {user.store ? (
                          <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                            <Store fontSize="small" />
                            <Typography variant="body2">{user.store}</Typography>
                          </Box>
                        ) : (
                          <Typography variant="body2" color="text.secondary">
                            -
                          </Typography>
                        )}
                      </TableCell>
                      <TableCell>
                        {user.lastLogin ? (
                          <Typography variant="body2">
                            {new Date(user.lastLogin).toLocaleDateString('pt-BR')}
                          </Typography>
                        ) : (
                          <Typography variant="body2" color="text.secondary">
                            Nunca
                          </Typography>
                        )}
                      </TableCell>
                      <TableCell align="center">
                        {user.esgScore ? (
                          <Chip
                            label={user.esgScore.toFixed(1)}
                            color={user.esgScore >= 8 ? "success" : user.esgScore >= 6 ? "warning" : "error"}
                            size="small"
                          />
                        ) : (
                          <Typography variant="body2" color="text.secondary">
                            -
                          </Typography>
                        )}
                      </TableCell>
                      <TableCell align="center">
                        {user.totalPurchases ? (
                          <Box>
                            <Typography variant="body2" fontWeight="bold">
                              {user.totalPurchases}
                            </Typography>
                            <Typography variant="caption" color="text.secondary">
                              R$ {user.totalSpent?.toFixed(2)}
                            </Typography>
                          </Box>
                        ) : (
                          <Typography variant="body2" color="text.secondary">
                            -
                          </Typography>
                        )}
                      </TableCell>
                      <TableCell align="right">
                        <IconButton
                          onClick={(e) => handleMenuClick(e, user)}
                          size="small"
                        >
                          <MoreVert />
                        </IconButton>
                      </TableCell>
                    </TableRow>
                  );
                })
              )}
            </TableBody>
          </Table>
        </TableContainer>

        <TablePagination
          component="div"
          count={filteredUsers.length}
          page={page}
          onPageChange={(_, newPage) => setPage(newPage)}
          rowsPerPage={rowsPerPage}
          onRowsPerPageChange={(e) => {
            setRowsPerPage(parseInt(e.target.value, 10));
            setPage(0);
          }}
          rowsPerPageOptions={[5, 10, 25, 50]}
          labelRowsPerPage="Linhas por página:"
          labelDisplayedRows={({ from, to, count }) => `${from}-${to} de ${count}`}
        />
      </Card>

      {/* Menu de ações */}
      <Menu
        anchorEl={anchorEl}
        open={Boolean(anchorEl)}
        onClose={handleMenuClose}
      >
        <MenuItemComponent onClick={() => selectedUser && handleEditUser(selectedUser)}>
          <ListItemIcon>
            <Edit fontSize="small" />
          </ListItemIcon>
          Editar
        </MenuItemComponent>
        
        {selectedUser?.status === 'active' && (
          <MenuItemComponent onClick={() => selectedUser && handleToggleUserStatus(selectedUser.id, 'inactive')}>
            <ListItemIcon>
              <VisibilityOff fontSize="small" />
            </ListItemIcon>
            Desativar
          </MenuItemComponent>
        )}
        
        {selectedUser?.status === 'inactive' && (
          <MenuItemComponent onClick={() => selectedUser && handleToggleUserStatus(selectedUser.id, 'active')}>
            <ListItemIcon>
              <Visibility fontSize="small" />
            </ListItemIcon>
            Ativar
          </MenuItemComponent>
        )}
        
        {selectedUser?.status !== 'blocked' && (
          <MenuItemComponent onClick={() => selectedUser && handleToggleUserStatus(selectedUser.id, 'blocked')}>
            <ListItemIcon>
              <Block fontSize="small" />
            </ListItemIcon>
            Bloquear
          </MenuItemComponent>
        )}
        
        <Divider />
        
        <MenuItemComponent 
          onClick={() => selectedUser && handleDeleteUser(selectedUser.id)}
          sx={{ color: 'error.main' }}
        >
          <ListItemIcon>
            <Delete fontSize="small" sx={{ color: 'error.main' }} />
          </ListItemIcon>
          Excluir
        </MenuItemComponent>
      </Menu>

      {/* Dialog de criação/edição */}
      <Dialog open={showUserDialog} onClose={() => setShowUserDialog(false)} maxWidth="md" fullWidth>
        <DialogTitle>
          {editingUser ? 'Editar Usuário' : 'Novo Usuário'}
        </DialogTitle>
        <DialogContent>
          <Grid container spacing={2} sx={{ mt: 1 }}>
            <Grid item xs={12} md={6}>
              <TextField
                label="Nome Completo"
                fullWidth
                required
                value={userForm.name}
                onChange={(e) => setUserForm(prev => ({ ...prev, name: e.target.value }))}
              />
            </Grid>
            <Grid item xs={12} md={6}>
              <TextField
                label="Email"
                type="email"
                fullWidth
                required
                value={userForm.email}
                onChange={(e) => setUserForm(prev => ({ ...prev, email: e.target.value }))}
              />
            </Grid>
            <Grid item xs={12} md={6}>
              <TextField
                label="Telefone"
                fullWidth
                value={userForm.phone}
                onChange={(e) => setUserForm(prev => ({ ...prev, phone: e.target.value }))}
              />
            </Grid>
            <Grid item xs={12} md={6}>
              <FormControl fullWidth required>
                <InputLabel>Função</InputLabel>
                <Select
                  value={userForm.role}
                  label="Função"
                  onChange={(e) => setUserForm(prev => ({ ...prev, role: e.target.value }))}
                >
                  {roles.map((role) => (
                    <MenuItem key={role.value} value={role.value}>
                      <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                        {role.icon}
                        {role.label}
                      </Box>
                    </MenuItem>
                  ))}
                </Select>
              </FormControl>
            </Grid>
            <Grid item xs={12} md={6}>
              <FormControl fullWidth required>
                <InputLabel>Status</InputLabel>
                <Select
                  value={userForm.status}
                  label="Status"
                  onChange={(e) => setUserForm(prev => ({ ...prev, status: e.target.value }))}
                >
                  {statuses.map((status) => (
                    <MenuItem key={status.value} value={status.value}>
                      {status.label}
                    </MenuItem>
                  ))}
                </Select>
              </FormControl>
            </Grid>
            {(userForm.role === 'manager' || userForm.role === 'cashier') && (
              <Grid item xs={12} md={6}>
                <FormControl fullWidth>
                  <InputLabel>Loja</InputLabel>
                  <Select
                    value={userForm.store}
                    label="Loja"
                    onChange={(e) => setUserForm(prev => ({ ...prev, store: e.target.value }))}
                  >
                    {stores.map((store) => (
                      <MenuItem key={store} value={store}>
                        {store}
                      </MenuItem>
                    ))}
                  </Select>
                </FormControl>
              </Grid>
            )}
            
            {userForm.role !== 'customer' && (
              <Grid item xs={12}>
                <Typography variant="subtitle2" gutterBottom>
                  Permissões
                </Typography>
                <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1 }}>
                  {permissions.map((permission) => (
                    <Chip
                      key={permission}
                      label={permission}
                      clickable
                      color={userForm.permissions.includes(permission) ? "primary" : "default"}
                      onClick={() => {
                        setUserForm(prev => ({
                          ...prev,
                          permissions: prev.permissions.includes(permission)
                            ? prev.permissions.filter(p => p !== permission)
                            : [...prev.permissions, permission]
                        }));
                      }}
                    />
                  ))}
                </Box>
              </Grid>
            )}
          </Grid>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setShowUserDialog(false)}>
            Cancelar
          </Button>
          <Button
            onClick={handleSaveUser}
            variant="contained"
            disabled={loading || !userForm.name || !userForm.email}
          >
            {loading ? <CircularProgress size={24} /> : editingUser ? 'Salvar' : 'Criar'}
          </Button>
        </DialogActions>
      </Dialog>

      {/* FAB para adicionar usuário */}
      <Fab
        color="primary"
        sx={{ position: 'fixed', bottom: 16, right: 16 }}
        onClick={handleCreateUser}
      >
        <Add />
      </Fab>
    </Box>
  );
};

export default UsersPage;
