// API Configuration and Helper Functions for Frontend

const API_BASE_URL = "http://127.0.0.1:8001/api";


// Helper function for API requests
async function apiRequest(endpoint, method = 'GET', body = null, needsAuth = true) {
  const headers = {
    'Content-Type': 'application/json',
  };

  // Add authorization token if needed
  if (needsAuth) {
    const token = localStorage.getItem('access_token');
    if (token) {
      headers['Authorization'] = `Bearer ${token}`;
    }
  }

  const options = {
    method,
    headers,
  };

  if (body) {
    options.body = JSON.stringify(body);
  }

  try {
    const response = await fetch(`${API_BASE_URL}${endpoint}`, options);

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || 'API Error');
    }

    const data = await response.json();
    return { success: true, data };
  } catch (error) {
    console.error('API Error:', error);
    return { success: false, error: error.message };
  }
}



async function signupUser(userData) {
  return apiRequest('/auth/signup', 'POST', userData, false);
}

async function loginUser(email, password) {
  return apiRequest('/auth/login', 'POST', { email, password }, false);
}


function storeAuthToken(tokenData) {
  localStorage.setItem('access_token', tokenData.access_token);
  localStorage.setItem('user_id', tokenData.user_id);
  localStorage.setItem('user_email', tokenData.email);
  localStorage.setItem('user_role', tokenData.role);
}

// Logout user
function logoutUser() {
  localStorage.removeItem('access_token');
  localStorage.removeItem('user_id');
  localStorage.removeItem('user_email');
  localStorage.removeItem('user_role');
}

// Get stored user info
function getStoredUser() {
  return {
    id: localStorage.getItem('user_id'),
    email: localStorage.getItem('user_email'),
    role: localStorage.getItem('user_role'),
    token: localStorage.getItem('access_token'),
  };
}


async function getUserProfile(userId) {
  return apiRequest(`/users/${userId}`);
}

async function updateUserProfile(userId, userData) {
  return apiRequest(`/users/${userId}`, 'PUT', userData);
}

async function deleteUserAccount(userId) {
  return apiRequest(`/users/${userId}`, 'DELETE');
}

// ============================================
// PRODUCT ENDPOINTS
// ============================================

async function getAllProducts() {
  return apiRequest('/products/', 'GET', null, false);
}

async function getProductById(productId) {
  return apiRequest(`/products/${productId}`, 'GET', null, false);
}

async function createProduct(productData) {
  return apiRequest('/products/', 'POST', productData);
}

async function updateProduct(productId, productData) {
  return apiRequest(`/products/${productId}`, 'PUT', productData);
}

async function deleteProduct(productId) {
  return apiRequest(`/products/${productId}`, 'DELETE');
}

// ============================================
// ORDER ENDPOINTS
// ============================================

async function getUserOrders(userId) {
  return apiRequest(`/orders/user/${userId}`);
}

async function getOrderById(orderId) {
  return apiRequest(`/orders/${orderId}`);
}

async function createOrder(userId, orderData) {
  return apiRequest(`/orders/`, 'POST', {
    ...orderData,
    user_id: userId,
  });
}

async function updateOrderStatus(orderId, status) {
  return apiRequest(`/orders/${orderId}`, 'PUT', { status });
}

async function cancelOrder(orderId) {
  return apiRequest(`/orders/${orderId}`, 'DELETE');
}

// ============================================
// SUPPLIER ENDPOINTS
// ============================================

async function getAllSuppliers() {
  return apiRequest('/suppliers/');
}

async function getSupplierById(supplierId) {
  return apiRequest(`/suppliers/${supplierId}`);
}

async function createSupplier(supplierData) {
  return apiRequest('/suppliers/', 'POST', supplierData);
}

async function updateSupplier(supplierId, supplierData) {
  return apiRequest(`/suppliers/${supplierId}`, 'PUT', supplierData);
}

async function deleteSupplier(supplierId) {
  return apiRequest(`/suppliers/${supplierId}`, 'DELETE');
}

// ============================================
// DASHBOARD ENDPOINTS
// ============================================

async function getAdminStats() {
  return apiRequest('/dashboard/admin-stats');
}

async function getUserStats(userId) {
  return apiRequest(`/dashboard/user-stats/${userId}`);
}

async function getRecentOrders(limit = 10) {
  return apiRequest(`/dashboard/recent-orders?limit=${limit}`);
}

async function getLowStockProducts(threshold = 20) {
  return apiRequest(`/dashboard/low-stock-products?threshold=${threshold}`);
}

// ============================================
// INVENTORY ENDPOINTS
// ============================================

async function getInventory() {
  return apiRequest('/inventory/');
}

async function getProductStock(productId) {
  return apiRequest(`/inventory/${productId}`);
}

async function addProductStock(productId, quantity) {
  return apiRequest(`/inventory/${productId}/add-stock`, 'PUT', { quantity });
}

async function reduceProductStock(productId, quantity) {
  return apiRequest(`/inventory/${productId}/reduce-stock`, 'PUT', { quantity });
}

// ============================================
// CONTACT ENDPOINTS
// ============================================

async function sendContactMessage(contactData) {
  return apiRequest('/contact/send', 'POST', contactData, false);
}

async function getContactInfo() {
  return apiRequest('/contact/info', 'GET', null, false);
}

// ============================================
// EXPORT ALL FUNCTIONS
// ============================================

export {
  // Auth
  signupUser,
  loginUser,
  storeAuthToken,
  logoutUser,
  getStoredUser,

  // Users
  getUserProfile,
  updateUserProfile,
  deleteUserAccount,

  // Products
  getAllProducts,
  getProductById,
  createProduct,
  updateProduct,
  deleteProduct,

  // Orders
  getUserOrders,
  getOrderById,
  createOrder,
  updateOrderStatus,
  cancelOrder,

  // Suppliers
  getAllSuppliers,
  getSupplierById,
  createSupplier,
  updateSupplier,
  deleteSupplier,

  // Dashboard
  getAdminStats,
  getUserStats,
  getRecentOrders,
  getLowStockProducts,

  // Inventory
  getInventory,
  getProductStock,
  addProductStock,
  reduceProductStock,

  // Contact
  sendContactMessage,
  getContactInfo,
};
