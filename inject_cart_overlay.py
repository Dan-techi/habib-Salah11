from pathlib import Path

pages = ['samsung.html', 'infinix.html', 'tecno.html', 'itel.html']

cart_html = '''
<button class="cart-fab" onclick="openReceipt()">
  <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><circle cx="9" cy="21" r="1"/><circle cx="20" cy="21" r="1"/><path d="M1 1h4l2.68 13.39a2 2 0 0 0 2 1.61h9.72a2 2 0 0 0 2-1.61L23 6H6"/></svg>
  View Cart
  <span class="cart-count" id="cartCount">0</span>
</button>

<div class="receipt-overlay" id="receiptOverlay">
  <div class="receipt-modal">
    <div class="receipt-header">
      <img src="https://address-restaurant2.odoo.com/web/image/1649-d6d52ad7/gm%20logo.webp" class="r-logo" alt="Logo">
      <h3>Your Order</h3>
      <p>Guma Smart Phone Enterprise</p>
      <button class="receipt-close" onclick="closeReceipt()">?</button>
    </div>
    <div class="receipt-body">
      <div class="receipt-row"><span class="label">Date</span><span class="value" id="r-date"></span></div>
      <div class="receipt-row"><span class="label">Receipt No.</span><span class="value" id="r-ref"></span></div>
      <hr class="receipt-divider">
      <div class="cart-items-list" id="cartItemsList"></div>
      <hr class="receipt-divider">
      <div class="receipt-total">
        <span class="label">Total Amount</span>
        <span class="value" id="r-total">UGX 0</span>
      </div>
    </div>
    <div class="receipt-footer">
      <button class="receipt-email-btn" id="r-email-btn" onclick="sendReceiptEmail()">
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"/><polyline points="22,6 12,13 2,6"/></svg>
        Send Receipt to Email
      </button>
      <div class="receipt-or">or</div>
      <a class="receipt-wa-btn" id="r-wa-btn" href="#" target="_blank">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="white"><path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 0 1-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 0 1-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 0 1 2.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0 0 12.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 0 0 5.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 0 0-3.48-8.413z"/></svg>
        Confirm Order on WhatsApp
      </a>
      <button class="receipt-cancel" onclick="closeReceipt()">Continue Shopping</button>
    </div>
  </div>
</div>
'''

cart_script = '''
<script src="https://cdn.jsdelivr.net/npm/@emailjs/browser@4/dist/email.min.js"></script>
<script>
emailjs.init('jtf5FqMIsmP4JL3oF');
let cart = [];
function openReceipt(name, priceStr) {
  if (name && priceStr) {
    const num = parseInt(priceStr.replace(/[^0-9]/g, ''));
    const existing = cart.find(i => i.name === name);
    if (existing) {
      existing.qty += 1;
    } else {
      cart.push({name, price: num, qty: 1});
    }
    updateCartCount();
    showCartNotification(name);
  }
  renderCart();
  document.getElementById('receiptOverlay').classList.add('active');
}
function updateCartCount() {
  const total = cart.reduce((sum, item) => sum + item.qty, 0);
  const counter = document.getElementById('cartCount');
  if (counter) counter.textContent = total;
  const fab = document.querySelector('.cart-fab');
  if (fab) fab.style.display = total > 0 ? 'flex' : 'none';
}
function showCartNotification(name) {
  const note = document.createElement('div');
  note.style.cssText = 'position:fixed;bottom:90px;left:28px;background:#0f8972;color:white;padding:10px 16px;border-radius:10px;font-size:0.82rem;font-weight:600;z-index:9998;animation:fadeInUp 0.3s ease;box-shadow:0 4px 16px rgba(0,0,0,0.2)';
  note.textContent = '✓ ' + name + ' added to cart';
  document.body.appendChild(note);
  setTimeout(() => note.remove(), 2000);
}
function changeQty(name, delta) {
  const item = cart.find(i => i.name === name);
  if (!item) return;
  item.qty += delta;
  if (item.qty <= 0) cart = cart.filter(i => i.name !== name);
  updateCartCount();
  renderCart();
}
function removeItem(name) {
  cart = cart.filter(i => i.name !== name);
  updateCartCount();
  renderCart();
}
function renderCart() {
  const now = new Date();
  document.getElementById('r-date').textContent = now.toLocaleDateString('en-UG', { day:'2-digit', month:'short', year:'numeric' });
  document.getElementById('r-ref').textContent = 'GS-' + now.getFullYear() + '-' + String(Math.floor(Math.random() * 90000) + 10000);
  const list = document.getElementById('cartItemsList');
  if (!list) return;
  if (cart.length === 0) {
    list.innerHTML = '<div class="receipt-empty">Your cart is empty.<br>Add items using "Order Now".</div>';
    document.getElementById('r-total').textContent = 'UGX 0';
    document.getElementById('r-wa-btn').href = '#';
    return;
  }
  list.innerHTML = cart.map(item => `
    <div class="cart-item-row">
      <span class="ci-name">${item.name}</span>
      <div class="ci-qty">
        <button onclick="changeQty('${item.name}', -1)">-</button>
        <span>${item.qty}</span>
        <button onclick="changeQty('${item.name}', 1)">+</button>
      </div>
      <span class="ci-price">UGX ${(item.price * item.qty).toLocaleString()}</span>
      <button class="ci-remove" onclick="removeItem('${item.name}')">?</button>
    </div>
  `).join('');
  const total = cart.reduce((sum, item) => sum + item.price * item.qty, 0);
  document.getElementById('r-total').textContent = 'UGX ' + total.toLocaleString();
  const date = document.getElementById('r-date').textContent;
  const ref = document.getElementById('r-ref').textContent;
  const itemLines = cart.map(i => `  - ${i.name} x${i.qty} = UGX ${(i.price*i.qty).toLocaleString()}`).join('\n');
  const msg = encodeURIComponent(
    '*ORDER RECEIPT*\n' +
    '\n' +
    '*Guma Smart Phone Enterprise*\n' +
    'Fort Portal, Uganda\n' +
    '\n' +
    ' Date: ' + date + '\n' +
    ' Ref: ' + ref + '\n' +
    '\n' +
    'Items:\n' + itemLines + '\n' +
    '\n' +
    ' *Total: UGX ' + total.toLocaleString() + '*\n\n' +
    'Please confirm this order. Thank you!'
  );
  document.getElementById('r-wa-btn').href = 'https://wa.me/256706721334?text=' + msg;
}
function sendReceiptEmail() {
  if (cart.length === 0) { alert('Your cart is empty.'); return; }
  const btn = document.getElementById('r-email-btn');
  btn.disabled = true;
  btn.textContent = 'Sending...';
  const date = document.getElementById('r-date').textContent;
  const ref = document.getElementById('r-ref').textContent;
  const total = cart.reduce((sum, item) => sum + item.price * item.qty, 0);
  const itemsHtml = cart.map(i => `
    <tr>
      <td style="padding:10px 12px;border-bottom:1px solid #f0f0f0;font-size:14px;color:#333">${i.name}</td>
      <td style="padding:10px 12px;border-bottom:1px solid #f0f0f0;font-size:14px;text-align:center;color:#333">${i.qty}</td>
      <td style="padding:10px 12px;border-bottom:1px solid #f0f0f0;font-size:14px;text-align:right;color:#0f8972;font-weight:700">UGX ${(i.price).toLocaleString()}</td>
      <td style="padding:10px 12px;border-bottom:1px solid #f0f0f0;font-size:14px;text-align:right;color:#0f8972;font-weight:700">UGX ${(i.price*i.qty).toLocaleString()}</td>
    </tr>
  `).join('');
  const receiptHtml = `
  <div style="font-family:'Inter',Arial,sans-serif;max-width:600px;margin:0 auto;background:#f5f7f6;padding:20px">
    <div style="background:linear-gradient(135deg,#0a7a62,#0f8972);border-radius:16px 16px 0 0;padding:32px;text-align:center">
      <img src="https://address-restaurant2.odoo.com/web/image/1649-d6d52ad7/gm%20logo.webp" style="height:60px;object-fit:contain;margin-bottom:12px" alt="Guma Smart">
      <h1 style="color:white;font-size:22px;font-weight:800;margin:0">Order Receipt</h1>
      <p style="color:rgba(255,255,255,0.75);font-size:13px;margin:6px 0 0">Guma Smart Phone Enterprise &bull; Fort Portal, Uganda</p>
    </div>
    <div style="background:white;padding:28px;border-left:1px solid #e8e8e8;border-right:1px solid #e8e8e8">
      <table style="width:100%;margin-bottom:20px">
        <tr>
          <td style="font-size:13px;color:#777">Date</td>
          <td style="font-size:13px;font-weight:700;color:#111;text-align:right">${date}</td>
        </tr>
        <tr>
          <td style="font-size:13px;color:#777;padding-top:6px">Receipt No.</td>
          <td style="font-size:13px;font-weight:700;color:#111;text-align:right;padding-top:6px">${ref}</td>
        </tr>
      </table>
      <div style="border-top:2px dashed #e0e0e0;margin:16px 0"></div>
      <table style="width:100%;border-collapse:collapse">
        <thead>
          <tr style="background:#f8f8f8">
            <th style="padding:10px 12px;font-size:12px;color:#777;text-align:left;font-weight:600;text-transform:uppercase">Item</th>
            <th style="padding:10px 12px;font-size:12px;color:#777;text-align:center;font-weight:600;text-transform:uppercase">Qty</th>
            <th style="padding:10px 12px;font-size:12px;color:#777;text-align:right;font-weight:600;text-transform:uppercase">Unit Price</th>
            <th style="padding:10px 12px;font-size:12px;color:#777;text-align:right;font-weight:600;text-transform:uppercase">Subtotal</th>
          </tr>
        </thead>
        <tbody>${itemsHtml}</tbody>
      </table>
      <div style="border-top:2px dashed #e0e0e0;margin:16px 0"></div>
      <div style="background:linear-gradient(135deg,rgba(15,137,114,0.08),rgba(210,31,31,0.05));border-radius:12px;padding:16px 20px;display:flex;justify-content:space-between;align-items:center">
        <span style="font-size:16px;font-weight:800;color:#111">Total Amount</span>
        <span style="font-size:22px;font-weight:900;color:#0f8972">UGX ${total.toLocaleString()}</span>
      </div>
      <p style="text-align:center;color:#aaa;font-size:12px;margin-top:20px">Thank you for choosing Guma Smart Phone Enterprise!</p>
    </div>
    <div style="background:linear-gradient(135deg,#0a7a62,#0f8972);border-radius:0 0 16px 16px;padding:20px;text-align:center">
      <p style="color:rgba(255,255,255,0.7);font-size:12px;margin:0">+256 706 721334 &bull; Fort Portal, Uganda &bull; Mon-Sat 8am-8pm</p>
    </div>
  </div>`;
  emailjs.send('service_98q9vwe', 'template_uw5wtda', {
    to_email: 'tumwesigehabib@gmail.com',
    from_name: 'Guma Smart Phone Enterprise',
    reply_to: 'tumwesigehabib@gmail.com',
    receipt_html: receiptHtml,
    ref: ref,
    date: date,
    total: 'UGX ' + total.toLocaleString()
  }).then(() => {
    btn.disabled = false;
    btn.innerHTML = '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"/></svg> Receipt Sent!';
    setTimeout(() => { btn.innerHTML = '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"/><polyline points="22,6 12,13 2,6"/></svg> Send Receipt to Email'; }, 3000);
  }).catch(() => {
    btn.disabled = false;
    btn.textContent = 'Failed. Try again.';
    setTimeout(() => { btn.innerHTML = '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"/><polyline points="22,6 12,13 2,6"/></svg> Send Receipt to Email'; }, 3000);
  });
}
function closeReceipt() {
  document.getElementById('receiptOverlay').classList.remove('active');
}
document.addEventListener('DOMContentLoaded', function() {
  document.querySelectorAll('.model-card button').forEach(function(button) {
    button.addEventListener('click', function() {
      const card = button.closest('.model-card');
      if (!card) return;
      const title = card.querySelector('h3');
      const price = card.querySelector('.price');
      if (title && price) {
        openReceipt(title.textContent.trim(), price.textContent.trim());
      }
    });
  });
  document.getElementById('receiptOverlay').addEventListener('click', function(event) {
    if (event.target === this) {
      closeReceipt();
    }
  });
  updateCartCount();
});
</script>
'''

for page in pages:
    file_path = Path(page)
    content = file_path.read_text(encoding='utf-8')
    if 'id="receiptOverlay"' in content or 'cart-fab' in content and 'openReceipt' in content:
        print(f'Skipping {page} because cart content already exists')
        continue
    if '</body>' not in content:
        raise ValueError(f'No </body> found in {page}')
    content = content.replace('</body>', cart_html + cart_script + '\n</body>', 1)
    file_path.write_text(content, encoding='utf-8')
    print(f'Updated {page}')
