// ===== SIDEBAR TOGGLE =====
document.addEventListener('DOMContentLoaded', function() {
    const toggle = document.getElementById('sidebarToggle');
    const sidebar = document.getElementById('sidebar');
    
    if (toggle && sidebar) {
        toggle.addEventListener('click', function() {
            sidebar.classList.toggle('open');
        });
        
        document.addEventListener('click', function(e) {
            if (window.innerWidth <= 768) {
                if (!sidebar.contains(e.target) && !toggle.contains(e.target)) {
                    sidebar.classList.remove('open');
                }
            }
        });
    }
});

// ===== TOAST =====
function showToast(message, type = 'info') {
    const container = document.getElementById('toastContainer');
    if (!container) return;
    const toast = document.createElement('div');
    toast.className = `toast ${type}`;
    toast.innerHTML = message;
    container.appendChild(toast);
    setTimeout(() => {
        toast.style.opacity = '0';
        toast.style.transform = 'translateX(100%)';
        setTimeout(() => toast.remove(), 400);
    }, 5000);
}

// ===== FORMAT RUPIAH =====
function formatRupiah(amount) {
    return 'Rp ' + Number(amount).toLocaleString('id-ID');
}

// ===== PENANGANAN SUBMIT CONVERT ORDER =====
document.addEventListener('DOMContentLoaded', function() {
    // 1. Cari elemen form. Pastikan di file HTML Anda, tag <form> memiliki id="formOrder"
    const formOrder = document.getElementById('formOrder'); 
    
    if (formOrder) {
        formOrder.addEventListener('submit', function(e) {
            e.preventDefault(); // Menghentikan reload halaman otomatis bawaan HTML
            
            // 2. Cari tombol submit di dalam form Anda
            const submitBtn = formOrder.querySelector('button[type="submit"]') || document.querySelector('.btn-processing-selector');
            const originalText = submitBtn ? submitBtn.innerHTML : 'Kirim Order';
            
            // Ubah tombol ke mode loading (agar user tahu data sedang diproses)
            if (submitBtn) {
                submitBtn.disabled = true;
                submitBtn.innerHTML = '⏳ Processing...';
            }
            
            // Tampilkan teks pembantu jika ada elemen teks "Mengirim order..." terpisah di HTML
            const teksMengirim = document.getElementById('teksMengirim'); // sesuaikan ID jika ada
            if (teksMengirim) teksMengirim.style.display = 'block';

            // 3. Ambil data form. Wajib memakai FormData karena ada input FILE (bukti transfer)
            const formData = new FormData(formOrder);
            
            // 4. Kirim data ke backend Flask menggunakan Fetch API
            // SILAKAN GANTI '/order/submit' sesuai dengan route/URL penampung order di app.py Anda
            fetch('/order/submit', { 
                method: 'POST',
                body: formData // Kirim langsung objek FormData, jangan di-stringify!
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Server merespon dengan kode HTTP ' + response.status);
                }
                return response.json();
            })
            .then(data => {
                if (data.success) {
                    // Berhasil! Gunakan fungsi toast bawaan Anda
                    showToast('🎉 Order berhasil dikirim! Mohon tunggu konfirmasi admin.', 'success');
                    formOrder.reset(); // Kosongkan form kembali setelah sukses
                } else {
                    // Backend menolak permintaan (misal: validasi gagal)
                    showToast('❌ Gagal: ' + (data.error || 'Terjadi kesalahan.'), 'error');
                }
            })
            .catch(error => {
                console.error('Error saat submit order:', error);
                showToast('⚠️ Gagal mengirim data. Periksa jaringan Anda atau hubungi admin.', 'error');
            })
            .finally(() => {
                // 5. Apapun hasilnya (sukses/gagal), kembalikan tombol ke keadaan semula
                if (submitBtn) {
                    submitBtn.disabled = false;
                    submitBtn.innerHTML = originalText;
                }
                if (teksMengirim) teksMengirim.style.display = 'none';
            });
        });
    }
});

console.log('🚀 DavaOFC Web Loaded!');
