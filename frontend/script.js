// ==================== CONFIGURACIÓN ====================
const API = {
  user: 'http://localhost:8001/auth',
  product: 'http://localhost:8002/products',
  cart: 'http://localhost:8003/cart',
  order: 'http://localhost:8004/orders',
  shipment: 'http://localhost:8005/shipments'
}

let token = localStorage.getItem('token') || null
let currentUser = null
let isLoginMode = true

// ==================== UTILIDADES ====================
function getHeaders() {
  return {
    'Content-Type': 'application/json',
    'Authorization': token ? `Bearer ${token}` : ''
  }
}

function showToast(message, type = 'success') {
  const toast = document.createElement('div')
  toast.className = `fixed bottom-6 right-6 px-6 py-3 rounded-2xl shadow-xl text-white flex items-center gap-2 z-50 ${
    type === 'success' ? 'bg-emerald-600' : 'bg-red-600'
  }`
  toast.innerHTML = `${type === 'success' ? '✅' : '❌'} ${message}`
  document.body.appendChild(toast)
  setTimeout(() => toast.remove(), 3000)
}

function updateCartCount() {
  if (!token) return
  fetch(API.cart, { headers: getHeaders() })
    .then(res => res.ok ? res.json() : { items: [] })
    .then(data => {
      const count = data.items ? data.items.length : 0
      const cartCountEl = document.getElementById('cart-count')
      if (cartCountEl) cartCountEl.textContent = count
    })
    .catch(() => {})
}

// ==================== NAVEGACIÓN ====================
async function navigate(page) {
  const content = document.getElementById('main-content')
  content.innerHTML = `
    <div class="flex justify-center py-20">
      <i class="fa-solid fa-spinner fa-spin text-4xl text-emerald-600"></i>
    </div>`

  if (!token && page !== 'catalog') {
    showLoginModal()
    return
  }

  switch (page) {
    case 'catalog': await loadCatalog(); break
    case 'cart': await loadCart(); break
    case 'orders': await loadOrders(); break
    case 'shipments': await loadShipments(); break
  }
}

// ==================== AUTH ====================
function updateAuthModalUI() {
  const title = document.getElementById('modal-title')
  const authBtn = document.getElementById('auth-btn')
  const toggleBtn = document.getElementById('toggle-btn')
  const fullNameInput = document.getElementById('full-name')

  title.textContent = isLoginMode ? 'Iniciar sesión' : 'Crear cuenta'
  authBtn.textContent = isLoginMode ? 'Iniciar sesión' : 'Registrarse'
  fullNameInput.classList.toggle('hidden', isLoginMode)
  toggleBtn.textContent = isLoginMode 
    ? '¿No tienes cuenta? Regístrate' 
    : '¿Ya tienes cuenta? Inicia sesión'
}

function showLoginModal() {
  document.getElementById('auth-modal').classList.remove('hidden')
  updateAuthModalUI()
}

function hideModal() {
  document.getElementById('auth-modal').classList.add('hidden')
}

function toggleAuthMode() {
  isLoginMode = !isLoginMode
  updateAuthModalUI()
}

async function handleAuth() {
  const email = document.getElementById('email').value.trim()
  const password = document.getElementById('password').value
  const fullName = document.getElementById('full-name').value.trim()

  if (!email || !password) {
    showToast('Completa email y contraseña', 'error')
    return
  }

  const url = isLoginMode ? `${API.user}/login` : `${API.user}/register`

  let headers = { 'Content-Type': 'application/json' }
  let body

  if (isLoginMode) {
    // Login usa form-urlencoded
    headers = { 'Content-Type': 'application/x-www-form-urlencoded' }
    body = new URLSearchParams({
      username: email,
      password: password
    })
  } else {
    // Register usa JSON
    body = JSON.stringify({
      email: email,
      password: password,
      full_name: fullName || email.split('@')[0]
    })
  }

  try {
    const res = await fetch(url, {
      method: 'POST',
      headers: headers,
      body: body
    })

    let data
    try {
      data = await res.json()
    } catch {
      data = {}
    }

    if (!res.ok) {
      const errorMsg = data.detail || data.message || `Error ${res.status}`
      console.error("Error del servidor:", data)
      showToast(errorMsg, 'error')
      return
    }

    // ÉXITO
    if (isLoginMode) {
      token = data.access_token
      localStorage.setItem('token', token)
      currentUser = { email }

      hideModal()
      document.getElementById('login-btn').classList.add('hidden')
      document.getElementById('user-info').classList.remove('hidden')
      document.getElementById('user-name').textContent = email

      showToast('¡Bienvenido a EcoShop!', 'success')
      navigate('catalog')
      updateCartCount()
    } else {
      showToast('¡Cuenta creada correctamente! Ahora inicia sesión', 'success')
      isLoginMode = true
      updateAuthModalUI()
    }
  } catch (e) {
    console.error("Error de conexión:", e)
    showToast('Error de conexión con el servidor', 'error')
  }
}

function logout() {
  localStorage.removeItem('token')
  token = null
  currentUser = null
  location.reload()
}

// ==================== CATÁLOGO ====================
async function loadCatalog() {
  const content = document.getElementById('main-content')
  content.innerHTML = `
    <div class="flex justify-center py-20">
      <i class="fa-solid fa-spinner fa-spin text-4xl text-emerald-600"></i>
    </div>`

  try {
    console.log("🔄 Intentando cargar catálogo desde:", API.product)

    const res = await fetch(API.product, {
      method: 'GET',
      headers: { 'Content-Type': 'application/json' }
    })

    console.log("📡 Respuesta del Product Service:", res.status, res.statusText)

    if (!res.ok) {
      throw new Error(`HTTP ${res.status} - ${res.statusText}`)
    }

    const products = await res.json()
    console.log("✅ Productos recibidos:", products.length, "productos")

    if (products.length === 0) {
      content.innerHTML = `<p class="text-center py-12 text-gray-400">No hay productos disponibles</p>`
      return
    }

    let html = `
      <h1 class="text-3xl font-semibold mb-2">Catálogo de Productos</h1>
      <p class="text-gray-500 mb-8">Encuentra lo que necesitas con un solo clic</p>
      <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
    `

    products.forEach(p => {
      html += `
        <div class="product-card bg-white rounded-3xl overflow-hidden border border-gray-100">
          <img src="${p.image_url}" alt="${p.name}" class="w-full h-48 object-cover">
          <div class="p-5">
            <h3 class="font-semibold text-lg">${p.name}</h3>
            <p class="text-gray-500 text-sm mt-1 mb-4 line-clamp-2">${p.description || ''}</p>
            <div class="flex justify-between items-end">
              <span class="text-3xl font-semibold">$${p.price}</span>
              <button onclick="addToCart(${p.id})" 
                      class="bg-emerald-600 hover:bg-emerald-700 text-white px-6 py-3 rounded-2xl transition flex items-center gap-2">
                <i class="fa-solid fa-cart-plus"></i> Agregar
              </button>
            </div>
          </div>
        </div>
      `
    })

    html += '</div>'
    content.innerHTML = html

  } catch (e) {
    console.error("❌ Error al cargar catálogo:", e)
    content.innerHTML = `
      <p class="text-red-500 text-center py-12">
        Error al cargar el catálogo.<br>
        <span class="text-sm text-gray-500">Revisa la consola (F12) para más detalles.</span>
      </p>`
  }
}

// ==================== CARRITO ====================
async function loadCart() {
  const content = document.getElementById('main-content')
  try {
    const res = await fetch(API.cart, { headers: getHeaders() })
    if (!res.ok) throw new Error()
    const cart = await res.json()

    if (!cart.items || cart.items.length === 0) {
      content.innerHTML = `
        <div class="text-center py-20">
          <i class="fa-solid fa-shopping-cart text-6xl text-gray-300 mb-6"></i>
          <h2 class="text-2xl font-medium text-gray-400">Tu carrito está vacío</h2>
          <button onclick="navigate('catalog')" class="mt-8 px-8 py-4 bg-emerald-600 text-white rounded-2xl hover:bg-emerald-700">
            Ir al catálogo
          </button>
        </div>
      `
      return
    }

    let html = `
      <h1 class="text-3xl font-semibold mb-2">Tu Carrito</h1>
      <p class="text-gray-500 mb-8">Total: <span class="font-semibold text-2xl">$${cart.total.toFixed(2)}</span></p>
      <div class="space-y-4">
    `

    cart.items.forEach(item => {
      html += `
        <div class="flex items-center gap-6 bg-white p-5 rounded-3xl border border-gray-100">
          <div class="flex-1">
            <h4 class="font-medium">Producto #${item.product_id}</h4>
            <p class="text-sm text-gray-500">Cantidad: ${item.quantity} × $${item.price}</p>
          </div>
          <div class="flex items-center gap-4">
            <button onclick="updateCartItem(${item.id}, ${item.quantity - 1})" class="w-9 h-9 flex items-center justify-center border rounded-2xl hover:bg-gray-100">-</button>
            <span class="w-8 text-center font-medium">${item.quantity}</span>
            <button onclick="updateCartItem(${item.id}, ${item.quantity + 1})" class="w-9 h-9 flex items-center justify-center border rounded-2xl hover:bg-gray-100">+</button>
            <button onclick="deleteCartItem(${item.id})" class="ml-4 text-red-500 hover:text-red-700">
              <i class="fa-solid fa-trash"></i>
            </button>
          </div>
          <div class="text-right font-semibold">$${(item.price * item.quantity).toFixed(2)}</div>
        </div>
      `
    })

    html += `
      </div>
      <div class="mt-10 flex justify-end">
        <button onclick="createOrder()" 
                class="px-10 py-5 bg-emerald-600 text-white text-xl rounded-3xl hover:bg-emerald-700 transition flex items-center gap-3">
          <i class="fa-solid fa-credit-card"></i>
          Generar Orden de Compra
        </button>
      </div>
    `

    content.innerHTML = html
  } catch (e) {
    content.innerHTML = `<p class="text-red-500 text-center py-12">Error al cargar el carrito</p>`
  }
}

async function addToCart(productId) {
  if (!token) {
    showLoginModal()
    return
  }
  try {
    const res = await fetch(API.cart, {
      method: 'POST',
      headers: getHeaders(),
      body: JSON.stringify({ product_id: productId, quantity: 1 })
    })
    if (res.ok) {
      showToast('Producto agregado al carrito')
      updateCartCount()
    } else {
      showToast('Error al agregar al carrito', 'error')
    }
  } catch (e) {
    showToast('Error de conexión', 'error')
  }
}

async function updateCartItem(itemId, newQuantity) {
  if (newQuantity < 1) {
    return deleteCartItem(itemId)
  }
  try {
    await fetch(`${API.cart}/${itemId}`, {
      method: 'PATCH',
      headers: getHeaders(),
      body: JSON.stringify({ quantity: newQuantity })
    })
    loadCart()
  } catch (e) {
    showToast('Error al actualizar cantidad', 'error')
  }
}

async function deleteCartItem(itemId) {
  if (!confirm('¿Eliminar este producto del carrito?')) return
  try {
    await fetch(`${API.cart}/${itemId}`, { 
      method: 'DELETE', 
      headers: getHeaders() 
    })
    loadCart()
    updateCartCount()
  } catch (e) {
    showToast('Error al eliminar', 'error')
  }
}

async function createOrder() {
  try {
    const res = await fetch(API.order, {
      method: 'POST',
      headers: getHeaders()
    })

    if (res.ok) {
      showToast('¡Orden generada correctamente!', 'success')
      updateCartCount()
      setTimeout(() => navigate('orders'), 1000)
    } else {
      const error = await res.text()
      showToast(`Error: ${error}`, 'error')
    }
  } catch (e) {
    showToast('Error de conexión con el servidor', 'error')
  }
}

// ==================== ÓRDENES Y ENVÍOS ====================
async function loadOrders() {
  const content = document.getElementById('main-content')
  try {
    const res = await fetch(API.order, { headers: getHeaders() })
    const orders = await res.json()

    let html = `<h1 class="text-3xl font-semibold mb-8">Mis Órdenes de Compra</h1>`

    if (!orders || orders.length === 0) {
      html += `<p class="text-gray-400 text-center py-12">Aún no tienes órdenes de compra</p>`
    } else {
      html += `<div class="space-y-6">`
      orders.forEach(order => {
        html += `
          <div class="bg-white rounded-3xl p-6 border border-gray-100">
            <div class="flex justify-between items-start">
              <div>
                <span class="font-medium text-lg">Orden #${order.id}</span>
                <p class="text-sm text-gray-500">${new Date(order.created_at).toLocaleDateString('es-MX')}</p>
              </div>
              <span class="px-5 py-2 bg-emerald-100 text-emerald-700 rounded-2xl font-semibold">$${order.total}</span>
            </div>
          </div>
        `
      })
      html += `</div>`
    }
    content.innerHTML = html
  } catch (e) {
    content.innerHTML = `<p class="text-red-500">Error al cargar órdenes</p>`
  }
}

async function loadShipments() {
  const content = document.getElementById('main-content')
  try {
    const res = await fetch(API.shipment, { headers: getHeaders() })
    const shipments = await res.json()

    let html = `<h1 class="text-3xl font-semibold mb-8">Mis Órdenes de Envío</h1>`

    if (!shipments || shipments.length === 0) {
      html += `<p class="text-gray-400 text-center py-12">Aún no tienes envíos</p>`
    } else {
      html += `<div class="space-y-6">`
      shipments.forEach(s => {
        const statusColor = s.status === 'pendiente' ? 'yellow' : s.status === 'en camino' ? 'blue' : 'emerald'
        html += `
          <div class="bg-white rounded-3xl p-6 border border-gray-100 flex justify-between items-center">
            <div>
              <span class="font-medium">Envío #${s.id} → Orden #${s.order_id}</span>
              <span class="ml-3 px-3 py-1 text-xs rounded-2xl bg-${statusColor}-100 text-${statusColor}-700">${s.status.toUpperCase()}</span>
            </div>
            <div class="text-right">
              <div class="text-sm text-gray-500">Tracking Number</div>
              <div class="font-mono font-medium text-lg">${s.tracking_number || '—'}</div>
            </div>
          </div>
        `
      })
      html += `</div>`
    }
    content.innerHTML = html
  } catch (e) {
    content.innerHTML = `<p class="text-red-500">Error al cargar envíos</p>`
  }
}

// ==================== INICIO DE LA APLICACIÓN ====================
document.addEventListener('DOMContentLoaded', () => {
  if (token) {
    document.getElementById('login-btn').classList.add('hidden')
    document.getElementById('user-info').classList.remove('hidden')
    document.getElementById('user-name').textContent = token ? 'Usuario' : ''
  }
  navigate('catalog')
  updateCartCount()
})