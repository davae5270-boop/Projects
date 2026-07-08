// ================================================================
//  DAVAOFC WEB - MAIN JAVASCRIPT (FULL VERSION + REGISTER + OTP)
//  OPTIMIZED - NO LAG, NO STUTTER, FAST ON ALL DEVICES
// ================================================================

// ============================================================
// 🚀 PERFORMANCE OPTIMIZATION (GLOBAL)
// ============================================================

// 1. CEGAH DOUBLE SUBMIT (GLOBAL)
window._isSubmitting = {};

// 2. CEGAH REQUEST BERLEBIHAN (DEBOUNCE)
window._debounceTimers = {};

// 3. ABORT CONTROLLER (TIMEOUT)
window._abortControllers = {};

// 4. FUNGSI DEBOUNCE UNIVERSAL
window.debounce = function(key, fn, delay) {
    delay = delay || 500;
    if (window._debounceTimers[key]) {
        clearTimeout(window._debounceTimers[key]);
    }
    window._debounceTimers[key] = setTimeout(function() {
        fn();
        delete window._debounceTimers[key];
    }, delay);
};

// 5. FUNGSI FETCH DENGAN TIMEOUT (UNIVERSAL) - CEKAT LOADING MULU
window.fetchWithTimeout = function(url, options, timeout) {
    timeout = timeout || 30000;
    var controller = new AbortController();
    var timeoutId = setTimeout(function() {
        controller.abort();
    }, timeout);
    
    var key = url + (options ? JSON.stringify(options) : '');
    if (window._abortControllers[key]) {
        window._abortControllers[key].abort();
    }
    window._abortControllers[key] = controller;
    
    return fetch(url, {
        ...options,
        signal: controller.signal
    }).then(function(response) {
        clearTimeout(timeoutId);
        delete window._abortControllers[key];
        return response;
    }).catch(function(err) {
        clearTimeout(timeoutId);
        delete window._abortControllers[key];
        if (err.name === 'AbortError') {
            throw new Error('Request timeout');
        }
        throw err;
    });
};

// 6. REQUESTANIMATIONFRAME WRAPPER (UNTUK UI UPDATE YANG SMOOTH)
window.safeUpdate = function(fn) {
    if (typeof requestAnimationFrame === 'function') {
        requestAnimationFrame(fn);
    } else {
        setTimeout(fn, 16);
    }
};

// 7. CEGAH ANIMASI BERAT DI HP LEMAH
if (window.matchMedia('(prefers-reduced-motion: reduce)').matches || 
    (navigator.hardwareConcurrency && navigator.hardwareConcurrency < 4)) {
    document.querySelectorAll('.animate-*, .animate-slide-up, .animate-slide-down, .animate-scale-in, .animate-bounce-in').forEach(function(el) {
        if (el) {
            el.style.animation = 'none';
            el.style.opacity = '1';
            el.style.transform = 'none';
        }
    });
    console.log('⚡ Reduced motion mode active for low-end devices');
}

// 8. MONITOR PERFORMANCE (FPS) - HANYA DEBUG
if (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1') {
    var fpsFrames = 0;
    var fpsLastTime = Date.now();
    function checkFPS() {
        fpsFrames++;
        var now = Date.now();
        if (now - fpsLastTime >= 1000) {
            var fps = Math.round(fpsFrames * 1000 / (now - fpsLastTime));
            if (fps < 20) {
                console.warn('⚠️ Low FPS detected:', fps);
            }
            fpsFrames = 0;
            fpsLastTime = now;
        }
        requestAnimationFrame(checkFPS);
    }
    requestAnimationFrame(checkFPS);
}

console.log('⚡ DavaOFC Performance Optimizer Active!');
console.log('✅ Debounce, Timeout, AbortController, FPS Monitor loaded');

// ================================================================
//  DAVAOFC WEB - MAIN JAVASCRIPT (FULL VERSION + REGISTER + OTP)
// ================================================================

document.addEventListener('DOMContentLoaded', function() {
    console.log('🚀 DavaOFC Web Loaded!');

    // =============================================================
    // 1. SIDEBAR TOGGLE
    // =============================================================
    var toggle = document.getElementById('sidebarToggle');
    var sidebar = document.getElementById('sidebar');
    if (toggle && sidebar) {
        toggle.addEventListener('click', function() {
            sidebar.classList.toggle('open');
        });
        document.addEventListener('click', function(e) {
            if (window.innerWidth <= 768 && !sidebar.contains(e.target) && !toggle.contains(e.target)) {
                sidebar.classList.remove('open');
            }
        });
    }

    // =============================================================
    // 2. TOAST NOTIFICATION
    // =============================================================
    window.showToast = function(message, type) {
        type = type || 'info';
        var container = document.getElementById('toastContainer');
        if (!container) {
            console.log('Toast:', message);
            return;
        }
        var toast = document.createElement('div');
        toast.className = 'toast ' + type;
        toast.textContent = message;
        container.appendChild(toast);
        setTimeout(function() {
            toast.style.opacity = '0';
            toast.style.transform = 'translateX(100px)';
            setTimeout(function() {
                if (toast.parentNode) toast.remove();
            }, 400);
        }, 4000);
    };

    // =============================================================
    // 3. FORMAT RUPIAH (MANUAL - STABIL SEMUA BROWSER)
    // =============================================================
    window.formatRupiah = function(amount) {
        if (amount === undefined || amount === null || isNaN(amount)) return 'Rp 0';
        var num = Math.round(Number(amount));
        var str = num.toString();
        var result = '';
        var count = 0;
        for (var i = str.length - 1; i >= 0; i--) {
            result = str[i] + result;
            count++;
            if (count % 3 === 0 && i !== 0) {
                result = '.' + result;
            }
        }
        return 'Rp ' + result;
    };

    // =============================================================
    // 4. FORMAT USD
    // =============================================================
    window.formatUSD = function(amount) {
        if (amount === undefined || amount === null || isNaN(amount)) return '$0.00';
        return '$' + Number(amount).toFixed(2);
    };

    // =============================================================
    // 5. FORMAT TANGGAL
    // =============================================================
    window.formatDate = function(dateStr) {
        if (!dateStr) return '-';
        var d = new Date(dateStr);
        if (isNaN(d.getTime())) return '-';
        var months = ['Jan', 'Feb', 'Mar', 'Apr', 'Mei', 'Jun', 'Jul', 'Agu', 'Sep', 'Okt', 'Nov', 'Des'];
        var day = d.getDate().toString().padStart(2, '0');
        var month = months[d.getMonth()];
        var year = d.getFullYear();
        var hours = d.getHours().toString().padStart(2, '0');
        var mins = d.getMinutes().toString().padStart(2, '0');
        return day + ' ' + month + ' ' + year + ' ' + hours + ':' + mins;
    };

    // =============================================================
    // 6. COPY TEXT
    // =============================================================
    window.copyText = function(text) {
        if (!text) return;
        if (navigator.clipboard && navigator.clipboard.writeText) {
            navigator.clipboard.writeText(text).then(function() {
                showToast('✅ Copied!', 'success');
            }).catch(function() {
                fallbackCopy(text);
            });
        } else {
            fallbackCopy(text);
        }
    };

    function fallbackCopy(text) {
        var input = document.createElement('input');
        input.value = text;
        document.body.appendChild(input);
        input.select();
        try {
            document.execCommand('copy');
            showToast('✅ Copied!', 'success');
        } catch (e) {
            showToast('❌ Failed to copy', 'error');
        }
        document.body.removeChild(input);
    }

    // =============================================================
    // 7. PROFILE FUNCTIONS
    // =============================================================

    // 7a. EDIT PROFILE
    window.editProfile = function() {
        var modal = document.getElementById('editProfileModal');
        if (modal) {
            modal.style.display = 'flex';
            modal.style.animation = 'fadeIn 0.3s ease-out forwards';
        }
    };

    window.closeEditProfile = function() {
        var modal = document.getElementById('editProfileModal');
        if (modal) {
            modal.style.display = 'none';
        }
    };

    window.saveProfile = async function() {
        var fullName = document.getElementById('editFullName');
        var username = document.getElementById('editUsername');
        var email = document.getElementById('editEmail');
        var phone = document.getElementById('editPhone');
        var btn = document.querySelector('#editProfileModal .btn-save');

        if (!fullName || !username || !email || !phone) {
            showToast('❌ Data tidak lengkap!', 'error');
            return;
        }

        if (!fullName.value.trim()) {
            showToast('❌ Nama lengkap wajib diisi!', 'error');
            fullName.focus();
            return;
        }

        if (!username.value.trim()) {
            showToast('❌ Username wajib diisi!', 'error');
            username.focus();
            return;
        }

        if (!email.value.trim()) {
            showToast('❌ Email wajib diisi!', 'error');
            email.focus();
            return;
        }

        if (btn) {
            btn.disabled = true;
            btn.textContent = 'Menyimpan...';
        }

        try {
            var response = await fetch('/api/profile/update', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    full_name: fullName.value.trim(),
                    username: username.value.trim(),
                    email: email.value.trim(),
                    phone: phone.value.trim()
                })
            });

            var data = await response.json();

            if (data.success) {
                showToast('✅ Profil berhasil diperbarui!', 'success');
                setTimeout(function() {
                    location.reload();
                }, 1000);
            } else {
                showToast('❌ ' + (data.error || 'Gagal menyimpan profil!'), 'error');
            }
        } catch (e) {
            console.error('Save profile error:', e);
            showToast('❌ Gagal terhubung ke server!', 'error');
        } finally {
            if (btn) {
                btn.disabled = false;
                btn.textContent = '💾 Simpan Perubahan';
            }
        }
    };

    // 7b. CHANGE PASSWORD
    window.changePassword = function() {
        var modal = document.getElementById('changePasswordModal');
        if (modal) {
            modal.style.display = 'flex';
            modal.style.animation = 'fadeIn 0.3s ease-out forwards';
        }
    };

    window.closeChangePassword = function() {
        var modal = document.getElementById('changePasswordModal');
        if (modal) {
            modal.style.display = 'none';
        }
    };

    window.savePassword = async function() {
        var oldPass = document.getElementById('oldPassword');
        var newPass = document.getElementById('newPassword');
        var confirmPass = document.getElementById('confirmPassword');
        var btn = document.querySelector('#changePasswordModal .btn-save');

        if (!oldPass || !newPass || !confirmPass) {
            showToast('❌ Data tidak lengkap!', 'error');
            return;
        }

        if (!oldPass.value.trim()) {
            showToast('❌ Password lama wajib diisi!', 'error');
            oldPass.focus();
            return;
        }

        if (newPass.value.length < 6) {
            showToast('❌ Password baru minimal 6 karakter!', 'error');
            newPass.focus();
            return;
        }

        if (newPass.value !== confirmPass.value) {
            showToast('❌ Password baru tidak sama!', 'error');
            confirmPass.focus();
            return;
        }

        if (btn) {
            btn.disabled = true;
            btn.textContent = 'Menyimpan...';
        }

        try {
            var response = await fetch('/api/profile/password', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    old_password: oldPass.value.trim(),
                    new_password: newPass.value.trim()
                })
            });

            var data = await response.json();

            if (data.success) {
                showToast('✅ Password berhasil diubah!', 'success');
                oldPass.value = '';
                newPass.value = '';
                confirmPass.value = '';
                closeChangePassword();
            } else {
                showToast('❌ ' + (data.error || 'Gagal mengubah password!'), 'error');
            }
        } catch (e) {
            console.error('Change password error:', e);
            showToast('❌ Gagal terhubung ke server!', 'error');
        } finally {
            if (btn) {
                btn.disabled = false;
                btn.textContent = '🔒 Ubah Password';
            }
        }
    };

    // =============================================================
    // 8. DEPOSIT FUNCTIONS
    // =============================================================

    // 8a. UPDATE DEPOSIT INFO
    window.updateDepositInfo = function() {
        var amount = document.getElementById('depositAmount');
        var method = document.getElementById('depositMethod');
        var infoBox = document.getElementById('depositInfo');

        if (!amount || !method || !infoBox) return;

        var val = parseInt(amount.value) || 0;
        var methodText = method.options[method.selectedIndex] ? method.options[method.selectedIndex].text : '-';

        if (val >= 10000) {
            infoBox.style.display = 'grid';
            var infoAmount = document.getElementById('infoAmount');
            var infoMethod = document.getElementById('infoMethod');
            if (infoAmount) infoAmount.textContent = window.formatRupiah(val);
            if (infoMethod) infoMethod.textContent = methodText;
        } else {
            infoBox.style.display = 'none';
        }
    };

    // 8b. SET QUICK AMOUNT
    window.setAmount = function(value) {
        var input = document.getElementById('depositAmount');
        if (!input) return;
        input.value = value;
        window.updateDepositInfo();
        input.focus();
        input.style.borderColor = '#00C853';
        input.style.transform = 'scale(1.02)';
        setTimeout(function() {
            input.style.borderColor = '';
            input.style.transform = '';
        }, 500);
        window.showToast('✅ Nominal ' + window.formatRupiah(value) + ' dipilih!', 'success');
    };

    // 8c. SELECT METHOD
    window.selectMethod = function(method) {
        var select = document.getElementById('depositMethod');
        if (!select) return;
        for (var i = 0; i < select.options.length; i++) {
            if (select.options[i].value === method) {
                select.selectedIndex = i;
                break;
            }
        }
        window.updateMethodInfo();
        window.showToast('✅ Metode ' + method + ' dipilih!', 'success');
    };

    // 8d. UPDATE METHOD INFO
    window.updateMethodInfo = function() {
        var method = document.getElementById('depositMethod');
        var methodName = document.getElementById('methodName');
        var methodAddress = document.getElementById('methodAddress');
        var methodOwner = document.getElementById('methodOwner');

        if (!method || !methodName || !methodAddress || !methodOwner) return;

        var selected = method.value;
        var data = window.methodData ? window.methodData[selected] : null;
        if (!data) data = { icon: '💜', name: selected, address: '085869291109', owner: 'Admin Dava' };

        methodName.textContent = data.icon + ' ' + data.name;
        methodAddress.textContent = data.address;
        methodOwner.textContent = data.owner;

        var detail = document.getElementById('methodDetail');
        if (detail) {
            detail.style.animation = 'none';
            setTimeout(function() {
                detail.style.animation = 'scaleIn 0.4s cubic-bezier(0.175,0.885,0.32,1.275) forwards';
            }, 10);
        }

        window.updateDepositInfo();
    };

    // 8e. COPY METHOD ADDRESS
    window.copyMethodAddress = function() {
        var address = document.getElementById('methodAddress');
        if (!address) return;
        window.copyText(address.textContent);
    };

    // 8f. REMOVE FILE
    window.removeFile = function() {
        var input = document.getElementById('depositPhoto');
        var preview = document.getElementById('uploadPreview');
        var area = document.getElementById('uploadArea');
        if (input) input.value = '';
        if (preview) preview.style.display = 'none';
        if (area) area.style.borderColor = '';
        window.showToast('🗑️ File berhasil dihapus', 'info');
    };

    // 8g. SUBMIT DEPOSIT - OPTIMIZED (TANPA LOADING MULU)
window.submitDeposit = function() {
    var btn = document.getElementById('depositBtn');
    var amount = document.getElementById('depositAmount');
    var method = document.getElementById('depositMethod');
    var photo = document.getElementById('depositPhoto');
    var result = document.getElementById('depositResult');

    if (!btn || !amount || !method || !photo || !result) {
        window.showToast('❌ Form deposit tidak lengkap!', 'error');
        return;
    }

    // Cegah double submit
    var submitKey = 'deposit_' + Date.now();
    if (window._isSubmitting[submitKey]) {
        window.showToast('⏳ Sedang memproses...', 'info');
        return;
    }
    window._isSubmitting[submitKey] = true;

    var amountVal = parseInt(amount.value) || 0;
    var methodVal = method.value;
    var photoFile = photo.files[0];

    // VALIDASI
    if (amountVal < 10000) {
        window.showToast('❌ Minimal deposit Rp 10.000!', 'error');
        amount.focus();
        amount.style.borderColor = '#FF1744';
        setTimeout(function() { amount.style.borderColor = ''; }, 2000);
        window._isSubmitting[submitKey] = false;
        return;
    }
    if (!photoFile) {
        window.showToast('❌ Upload bukti transfer!', 'error');
        var uploadArea = document.getElementById('uploadArea');
        if (uploadArea) {
            uploadArea.style.borderColor = '#FF1744';
            setTimeout(function() { uploadArea.style.borderColor = ''; }, 2000);
        }
        window._isSubmitting[submitKey] = false;
        return;
    }
    if (photoFile.size > 2 * 1024 * 1024) {
        window.showToast('❌ Ukuran foto maksimal 2MB!', 'error');
        photo.value = '';
        var preview = document.getElementById('uploadPreview');
        if (preview) preview.style.display = 'none';
        window._isSubmitting[submitKey] = false;
        return;
    }

    // DISABLE BUTTON
    btn.disabled = true;
    btn.innerHTML = '<span class="loading-spinner"></span> Processing...';
    btn.style.opacity = '0.7';

    // CONVERT PHOTO TO BASE64
    var reader = new FileReader();
    reader.readAsDataURL(photoFile);

    reader.onload = function() {
        window.fetchWithTimeout('/api/deposit', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                amount: amountVal,
                method: methodVal,
                proof: reader.result
            })
        }, 30000)
        .then(function(response) { return response.json(); })
        .then(function(data) {
            window.safeUpdate(function() {
                if (data.success) {
                    result.style.display = 'block';
                    result.innerHTML = `
                        <div class="result-success animate-bounce-in">
                            ✅ Deposit Berhasil Diajukan!
                            <br><strong style="font-size:18px;color:#FFD600;">ID: ${data.dep_number}</strong>
                            <br><small style="color:rgba(255,255,255,0.5);">Nominal: ${window.formatRupiah(amountVal)}
                            <br>Status: <span style="color:#FFD600;font-weight:600;">Menunggu Konfirmasi</span></small>
                        </div>
                    `;
                    window.showToast('✅ Deposit berhasil diajukan! ID: ' + data.dep_number, 'success');

                    // RESET FORM
                    amount.value = '';
                    photo.value = '';
                    var preview = document.getElementById('uploadPreview');
                    if (preview) preview.style.display = 'none';
                    var infoBox = document.getElementById('depositInfo');
                    if (infoBox) infoBox.style.display = 'none';

                    setTimeout(function() {
                        result.scrollIntoView({ behavior: 'smooth', block: 'center' });
                    }, 300);

                } else {
                    result.style.display = 'block';
                    result.innerHTML = `
                        <div class="result-error animate-shake">
                            ❌ ${data.error || 'Gagal submit deposit!'}
                            <br><small style="color:rgba(255,255,255,0.3);">Silakan coba lagi.</small>
                        </div>
                    `;
                    window.showToast('❌ ' + (data.error || 'Gagal submit deposit!'), 'error');
                }
            });
        })
        .catch(function(err) {
            window.safeUpdate(function() {
                result.style.display = 'block';
                if (err.message === 'Request timeout') {
                    result.innerHTML = `
                        <div class="result-error">
                            ⏳ Server tidak merespons!<br>
                            <small style="color:rgba(255,255,255,0.3);">Silakan coba lagi nanti.</small>
                        </div>
                    `;
                    window.showToast('⏳ Server tidak merespons! Coba lagi nanti.', 'warning');
                } else {
                    result.innerHTML = `
                        <div class="result-error">
                            ❌ Gagal terhubung ke server!<br>
                            <small style="color:rgba(255,255,255,0.3);">Periksa koneksi internet Anda.</small>
                        </div>
                    `;
                    window.showToast('❌ Gagal terhubung ke server!', 'error');
                }
                console.error('Submit error:', err);
            });
        })
        .finally(function() {
            window.safeUpdate(function() {
                btn.disabled = false;
                btn.innerHTML = '<i class="fas fa-arrow-down"></i> Submit Deposit';
                btn.style.opacity = '1';
                window._isSubmitting[submitKey] = false;
            });
        });
    };

    reader.onerror = function() {
        window.safeUpdate(function() {
            window.showToast('❌ Gagal membaca file!', 'error');
            btn.disabled = false;
            btn.innerHTML = '<i class="fas fa-arrow-down"></i> Submit Deposit';
            btn.style.opacity = '1';
            window._isSubmitting[submitKey] = false;
        });
    };
};

    // =============================================================
    // 9. METHOD DATA
    // =============================================================
    window.methodData = {
        'DANA': { icon: '💜', name: 'DANA', address: '085869291109', owner: 'Admin Dava' },
        'GOPAY': { icon: '💚', name: 'GOPAY', address: '085869291109', owner: 'Admin Dava' },
        'OVO': { icon: '💜', name: 'OVO', address: '085869291109', owner: 'Admin Dava' },
        'ShopeePay': { icon: '🛒', name: 'ShopeePay', address: '085869291109', owner: 'Admin Dava' },
        'LinkAja': { icon: '🔗', name: 'LinkAja', address: '085869291109', owner: 'Admin Dava' },
        'SeaBank': { icon: '🏦', name: 'SeaBank', address: '901947918818', owner: 'Admin Dava' },
        'BCA': { icon: '🏦', name: 'BCA', address: '901947918818', owner: 'Admin Dava' },
        'BRI': { icon: '🏦', name: 'BRI', address: '901947918818', owner: 'Admin Dava' },
        'BNI': { icon: '🏦', name: 'BNI', address: '901947918818', owner: 'Admin Dava' },
        'Mandiri': { icon: '🏦', name: 'Mandiri', address: '901947918818', owner: 'Admin Dava' },
        'CIMB': { icon: '🏦', name: 'CIMB Niaga', address: '901947918818', owner: 'Admin Dava' },
        'Permata': { icon: '🏦', name: 'Permata Bank', address: '901947918818', owner: 'Admin Dava' },
        'BTN': { icon: '🏦', name: 'BTN', address: '901947918818', owner: 'Admin Dava' },
        'Danamon': { icon: '🏦', name: 'Danamon', address: '901947918818', owner: 'Admin Dava' },
        'Maybank': { icon: '🏦', name: 'Maybank', address: '901947918818', owner: 'Admin Dava' },
        'USDT BEP-20': { icon: '🪙', name: 'USDT BEP-20', address: '0x7a51ceE3216Bd7E2d4C245a374bFAA98858A298b', owner: 'Admin Dava' },
        'USDT TRC-20': { icon: '🪙', name: 'USDT TRC-20', address: 'TM7ySbKFBUGroDEs2snuttcJmV8qkFBRYx', owner: 'Admin Dava' },
        'BTC': { icon: '₿', name: 'Bitcoin', address: '1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa', owner: 'Admin Dava' },
        'ETH': { icon: '⟠', name: 'Ethereum', address: '0x7a51ceE3216Bd7E2d4C245a374bFAA98858A298b', owner: 'Admin Dava' },
        'BNB': { icon: '🟡', name: 'BNB', address: '0x7a51ceE3216Bd7E2d4C245a374bFAA98858A298b', owner: 'Admin Dava' },
        'SOL': { icon: '◎', name: 'Solana', address: 'So11111111111111111111111111111111111111112', owner: 'Admin Dava' }
    };

    // =============================================================
    // 10. CONVERT FUNCTIONS
    // =============================================================

    // 10a. ESTIMATE - OPTIMIZED (DEBOUNCE + TIMEOUT)
window.updateEstimate = function() {
    var amountInput = document.getElementById('amountUsd');
    var cryptoSelect = document.getElementById('cryptoType');
    var estimateBox = document.getElementById('estimateResult');

    if (!amountInput || !cryptoSelect || !estimateBox) return;

    var amount = parseFloat(amountInput.value) || 0;
    var crypto = cryptoSelect.value;

    if (amount < 0.1) {
        estimateBox.style.display = 'none';
        return;
    }

    // Gunakan debounce agar tidak request berlebihan
    window.debounce('updateEstimate', function() {
        estimateBox.style.display = 'block';
        var loading = estimateBox.querySelector('.estimate-loading');
        var content = estimateBox.querySelector('.estimate-content');
        if (loading) loading.style.display = 'block';
        if (content) content.style.display = 'none';

        window.fetchWithTimeout('/api/get_estimate?crypto=' + encodeURIComponent(crypto) + '&amount=' + amount, {
            method: 'GET'
        }, 10000)
        .then(function(response) { return response.json(); })
        .then(function(data) {
            window.safeUpdate(function() {
                if (data.success) {
                    if (loading) loading.style.display = 'none';
                    if (content) content.style.display = 'block';
                    
                    var estimateAmount = document.getElementById('estimateAmount');
                    var estimateTotal = document.getElementById('estimateTotal');
                    var estimateFee = document.getElementById('estimateFee');
                    
                    if (estimateAmount) estimateAmount.textContent = window.formatRupiah(data.amount_idr);
                    if (estimateTotal) estimateTotal.textContent = window.formatRupiah(data.total_idr);
                    if (estimateFee) estimateFee.textContent = window.formatRupiah(data.fee_idr);
                }
            });
        })
        .catch(function(err) {
            console.error('Estimate error:', err);
            window.safeUpdate(function() {
                if (loading) loading.style.display = 'none';
                if (content) content.style.display = 'block';
                var estimateAmount = document.getElementById('estimateAmount');
                if (estimateAmount) estimateAmount.textContent = 'Rp 0';
            });
        });
    }, 500);
};

    // 10b. WALLET DATA
    window.walletData = {
        'USDT BEP-20': { address: '0x7a51ceE3216Bd7E2d4C245a374bFAA98858A298b', icon: '🪙' },
        'USDT TRC-20': { address: 'TM7ySbKFBUGroDEs2snuttcJmV8qkFBRYx', icon: '🪙' },
        'USDT ERC-20': { address: '0x7a51ceE3216Bd7E2d4C245a374bFAA98858A298b', icon: '🪙' },
        'USDT POL': { address: 'GyDR5PghMLF7dsJ6ha1K4r23GxxlyWbWsfacT931e2XjV', icon: '🪙' },
        'USDC POL': { address: '0x7a51ceE3216Bd7E2d4C245a374bFAA98858A298b', icon: '💎' },
        'BTC': { address: '1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa', icon: '₿' },
        'ETH': { address: '0x7a51ceE3216Bd7E2d4C245a374bFAA98858A298b', icon: '⟠' },
        'BNB': { address: '0x7a51ceE3216Bd7E2d4C245a374bFAA98858A298b', icon: '🟡' },
        'SOL': { address: 'So11111111111111111111111111111111111111112', icon: '◎' },
        'DOGE': { address: 'DLfP6qoUd6wowJ1Wao4WZRfUEjanC8PzvS', icon: '🐕' }
    };

    // 10c. UPDATE WALLET ADDRESS
    window.updateWalletAddress = function() {
        var cryptoSelect = document.getElementById('cryptoType');
        var walletTokenName = document.getElementById('walletTokenName');
        var walletAddress = document.getElementById('walletAddress');

        if (!cryptoSelect || !walletTokenName || !walletAddress) return;

        var crypto = cryptoSelect.value;
        var data = window.walletData[crypto] || window.walletData['USDT BEP-20'];

        if (data) {
            walletTokenName.textContent = (data.icon || '🪙') + ' ' + crypto;
            walletAddress.textContent = data.address || 'Alamat tidak tersedia';
        }

        if (typeof window.updateEstimate === 'function') {
            window.updateEstimate();
        }
    };

    // 10d. SUBMIT CONVERT - OPTIMIZED (TANPA LOADING MULU)
window.submitConvert = function() {
    var btn = document.getElementById('convertBtn');
    var crypto = document.getElementById('cryptoType').value;
    var bank = document.getElementById('paymentMethod').value;
    var fullName = document.getElementById('fullName').value.trim();
    var account = document.getElementById('accountNumber').value.trim();
    var amountUsd = document.getElementById('amountUsd').value;
    var photo = document.getElementById('proofPhoto').files[0];
    var result = document.getElementById('convertResult');

    // Cegah double submit
    var submitKey = 'convert_' + Date.now();
    if (window._isSubmitting[submitKey]) {
        window.showToast('⏳ Sedang memproses...', 'info');
        return;
    }
    window._isSubmitting[submitKey] = true;

    // Reset result
    result.style.display = 'none';
    result.innerHTML = '';

    // VALIDASI
    if (!fullName) {
        window.showToast('❌ Nama lengkap wajib diisi!', 'error');
        document.getElementById('fullName').focus();
        window._isSubmitting[submitKey] = false;
        return;
    }
    if (!account) {
        window.showToast('❌ Nomor rekening wajib diisi!', 'error');
        document.getElementById('accountNumber').focus();
        window._isSubmitting[submitKey] = false;
        return;
    }
    if (!amountUsd || parseFloat(amountUsd) < 0.1) {
        window.showToast('❌ Minimal $0.1 USD!', 'error');
        document.getElementById('amountUsd').focus();
        window._isSubmitting[submitKey] = false;
        return;
    }
    if (!photo) {
        window.showToast('❌ Upload bukti transfer!', 'error');
        var uploadArea = document.getElementById('uploadArea');
        if (uploadArea) {
            uploadArea.style.borderColor = '#FF1744';
            setTimeout(function() { uploadArea.style.borderColor = ''; }, 2000);
        }
        window._isSubmitting[submitKey] = false;
        return;
    }
    if (photo.size > 2 * 1024 * 1024) {
        window.showToast('❌ Ukuran foto maksimal 2MB!', 'error');
        document.getElementById('proofPhoto').value = '';
        document.getElementById('uploadPreview').style.display = 'none';
        window._isSubmitting[submitKey] = false;
        return;
    }

    // DISABLE BUTTON
    btn.disabled = true;
    btn.innerHTML = '<span class="loading-spinner"></span> Processing...';
    btn.style.opacity = '0.7';

    // CONVERT PHOTO TO BASE64
    var reader = new FileReader();
    reader.readAsDataURL(photo);

    reader.onload = function() {
        window.fetchWithTimeout('/api/convert', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                crypto: crypto,
                bank: bank,
                full_name: fullName,
                account: account,
                amount_usd: parseFloat(amountUsd),
                proof: reader.result
            })
        }, 30000)
        .then(function(response) { return response.json(); })
        .then(function(data) {
            window.safeUpdate(function() {
                if (data.success) {
                    result.style.display = 'block';
                    result.innerHTML = `
                        <div class="result-success animate-bounce-in">
                            ✅ Order Berhasil!
                            <br><strong style="font-size:18px;color:#FFD600;">ID: ${data.order_number}</strong>
                            <br><small style="color:rgba(255,255,255,0.5);">
                                Total: ${window.formatRupiah(data.amount_idr)}
                                <br>Status: <span style="color:#FFD600;font-weight:600;">Menunggu Konfirmasi</span>
                            </small>
                        </div>
                    `;
                    window.showToast('✅ Order berhasil! ID: ' + data.order_number, 'success');

                    // RESET FORM
                    document.getElementById('fullName').value = '';
                    document.getElementById('accountNumber').value = '';
                    document.getElementById('amountUsd').value = '';
                    document.getElementById('proofPhoto').value = '';
                    document.getElementById('uploadPreview').style.display = 'none';
                    document.getElementById('estimateResult').style.display = 'none';

                    setTimeout(function() {
                        result.scrollIntoView({ behavior: 'smooth', block: 'center' });
                    }, 300);

                } else {
                    result.style.display = 'block';
                    result.innerHTML = `
                        <div class="result-error animate-shake">
                            ❌ ${data.error || 'Gagal submit order!'}
                            <br><small style="color:rgba(255,255,255,0.3);">Silakan coba lagi.</small>
                        </div>
                    `;
                    window.showToast('❌ ' + (data.error || 'Gagal submit order!'), 'error');
                }
            });
        })
        .catch(function(err) {
            window.safeUpdate(function() {
                result.style.display = 'block';
                if (err.message === 'Request timeout') {
                    result.innerHTML = `
                        <div class="result-error">
                            ⏳ Server tidak merespons!<br>
                            <small style="color:rgba(255,255,255,0.3);">Silakan coba lagi nanti.</small>
                        </div>
                    `;
                    window.showToast('⏳ Server tidak merespons! Coba lagi nanti.', 'warning');
                } else {
                    result.innerHTML = `
                        <div class="result-error">
                            ❌ Gagal terhubung ke server!<br>
                            <small style="color:rgba(255,255,255,0.3);">Periksa koneksi internet Anda.</small>
                        </div>
                    `;
                    window.showToast('❌ Gagal terhubung ke server!', 'error');
                }
                console.error('Submit error:', err);
            });
        })
        .finally(function() {
            window.safeUpdate(function() {
                btn.disabled = false;
                btn.innerHTML = '<i class="fas fa-paper-plane"></i> Submit Order';
                btn.style.opacity = '1';
                window._isSubmitting[submitKey] = false;
            });
        });
    };

    reader.onerror = function() {
        window.safeUpdate(function() {
            window.showToast('❌ Gagal membaca file!', 'error');
            btn.disabled = false;
            btn.innerHTML = '<i class="fas fa-paper-plane"></i> Submit Order';
            btn.style.opacity = '1';
            window._isSubmitting[submitKey] = false;
        });
    };
};

    // =============================================================
    // 11. ADMIN FUNCTIONS
    // =============================================================

    window.approveOrder = async function(orderId) {
        if (!confirm('✅ Setujui order ' + orderId + '?')) return;
        try {
            var res = await fetch('/api/admin/order/approve', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ order_id: orderId })
            });
            var data = await res.json();
            if (data.success) {
                window.showToast('✅ Order disetujui!', 'success');
                setTimeout(function() { location.reload(); }, 1000);
            } else {
                window.showToast('❌ ' + (data.error || 'Gagal approve!'), 'error');
            }
        } catch (e) {
            window.showToast('❌ Gagal terhubung!', 'error');
        }
    };

    window.rejectOrder = async function(orderId) {
        if (!confirm('❌ Tolak order ' + orderId + '?')) return;
        try {
            var res = await fetch('/api/admin/order/reject', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ order_id: orderId })
            });
            var data = await res.json();
            if (data.success) {
                window.showToast('❌ Order ditolak!', 'warning');
                setTimeout(function() { location.reload(); }, 1000);
            } else {
                window.showToast('❌ ' + (data.error || 'Gagal reject!'), 'error');
            }
        } catch (e) {
            window.showToast('❌ Gagal terhubung!', 'error');
        }
    };

    window.approveDeposit = async function(depId) {
        if (!confirm('✅ Setujui deposit ' + depId + '?')) return;
        try {
            var res = await fetch('/api/admin/deposit/approve', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ deposit_id: depId })
            });
            var data = await res.json();
            if (data.success) {
                window.showToast('✅ Deposit disetujui!', 'success');
                setTimeout(function() { location.reload(); }, 1000);
            } else {
                window.showToast('❌ ' + (data.error || 'Gagal approve!'), 'error');
            }
        } catch (e) {
            window.showToast('❌ Gagal terhubung!', 'error');
        }
    };

    window.rejectDeposit = async function(depId) {
        if (!confirm('❌ Tolak deposit ' + depId + '?')) return;
        try {
            var res = await fetch('/api/admin/deposit/reject', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ deposit_id: depId })
            });
            var data = await res.json();
            if (data.success) {
                window.showToast('❌ Deposit ditolak!', 'warning');
                setTimeout(function() { location.reload(); }, 1000);
            } else {
                window.showToast('❌ ' + (data.error || 'Gagal reject!'), 'error');
            }
        } catch (e) {
            window.showToast('❌ Gagal terhubung!', 'error');
        }
    };

    window.approveWithdraw = async function(wdId) {
        if (!confirm('✅ Setujui withdraw ' + wdId + '?')) return;
        try {
            var res = await fetch('/api/admin/withdraw/approve', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ withdraw_id: wdId })
            });
            var data = await res.json();
            if (data.success) {
                window.showToast('✅ Withdraw disetujui!', 'success');
                setTimeout(function() { location.reload(); }, 1000);
            } else {
                window.showToast('❌ ' + (data.error || 'Gagal approve!'), 'error');
            }
        } catch (e) {
            window.showToast('❌ Gagal terhubung!', 'error');
        }
    };

    window.rejectWithdraw = async function(wdId) {
        if (!confirm('❌ Tolak withdraw ' + wdId + '?')) return;
        try {
            var res = await fetch('/api/admin/withdraw/reject', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ withdraw_id: wdId })
            });
            var data = await res.json();
            if (data.success) {
                window.showToast('❌ Withdraw ditolak!', 'warning');
                setTimeout(function() { location.reload(); }, 1000);
            } else {
                window.showToast('❌ ' + (data.error || 'Gagal reject!'), 'error');
            }
        } catch (e) {
            window.showToast('❌ Gagal terhubung!', 'error');
        }
    };

// ============================================================
// 12a. REGISTER FORM SUBMIT - FIX (OTP LANGSUNG KE EMAIL)
// ============================================================
var registerForm = document.getElementById('registerForm');
if (registerForm) {
    registerForm.addEventListener('submit', function(e) {
        e.preventDefault();
        
        var email = document.getElementById('email').value.trim();
        var username = document.getElementById('username').value.trim();
        var fullName = document.getElementById('full_name').value.trim();
        var password = document.getElementById('password').value;
        var confirmPassword = document.getElementById('confirmPassword').value;
        var phone = document.getElementById('phone') ? document.getElementById('phone').value.trim() : '';
        var referralCode = document.getElementById('referralCode') ? document.getElementById('referralCode').value.trim() : '';
        var terms = document.getElementById('terms') ? document.getElementById('terms').checked : true;
        
        // VALIDASI
        if (!fullName) {
            showToast('❌ Nama lengkap wajib diisi!', 'error');
            document.getElementById('full_name').focus();
            return;
        }
        if (!username) {
            showToast('❌ Username wajib diisi!', 'error');
            document.getElementById('username').focus();
            return;
        }
        if (username.length < 3) {
            showToast('❌ Username minimal 3 karakter!', 'error');
            document.getElementById('username').focus();
            return;
        }
        if (!email) {
            showToast('❌ Email wajib diisi!', 'error');
            document.getElementById('email').focus();
            return;
        }
        var emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailRegex.test(email)) {
            showToast('❌ Format email tidak valid!', 'error');
            document.getElementById('email').focus();
            return;
        }
        if (!password) {
            showToast('❌ Password wajib diisi!', 'error');
            document.getElementById('password').focus();
            return;
        }
        if (password.length < 6) {
            showToast('❌ Password minimal 6 karakter!', 'error');
            document.getElementById('password').focus();
            return;
        }
        if (password !== confirmPassword) {
            showToast('❌ Password tidak sama!', 'error');
            document.getElementById('confirmPassword').focus();
            return;
        }
        if (!terms) {
            showToast('❌ Anda harus menyetujui syarat & ketentuan!', 'error');
            return;
        }
        
        var btn = document.getElementById('registerBtn');
        if (btn) {
            btn.disabled = true;
            btn.innerHTML = '<span class="loading-spinner"></span> Mendaftar...';
        }
        
        // Kirim ke API Register
        fetch('/api/register', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                email: email,
                username: username,
                full_name: fullName,
                password: password,
                phone: phone,
                referral_code: referralCode
            })
        })
        .then(function(response) { 
            return response.json(); 
        })
        .then(function(data) {
            if (btn) {
                btn.disabled = false;
                btn.innerHTML = '<i class="fas fa-user-plus"></i> Daftar Sekarang';
            }
            
            console.log('📥 Register Response:', data);
            
            if (data.success) {
                // Ambil OTP dari response
                var otpCode = data.otp || data.dev_otp || '';
                
                showToast('✅ ' + data.message, 'success');
                
                // Simpan ke sessionStorage
                sessionStorage.setItem('register_email', data.email);
                sessionStorage.setItem('register_otp', otpCode);
                
                // Tampilkan OTP di console
                console.log('🔑 OTP CODE:', otpCode);
                console.log('📧 Email:', data.email);
                
                // Redirect ke verify dengan email DAN OTP
                setTimeout(function() {
                    window.location.href = '/verify?email=' + encodeURIComponent(data.email) + '&otp=' + encodeURIComponent(otpCode);
                }, 1500);
            } else {
                showToast('❌ ' + (data.error || 'Gagal registrasi!'), 'error');
            }
        })
        .catch(function(err) {
            console.error('Register error:', err);
            if (btn) {
                btn.disabled = false;
                btn.innerHTML = '<i class="fas fa-user-plus"></i> Daftar Sekarang';
            }
            showToast('❌ Gagal terhubung ke server!', 'error');
        });
    });
}

// ============================================================
// 12b. VERIFY OTP - FIX (AMBIL OTP DARI URL ATAU SESSION)
// ============================================================
var verifyBtn = document.getElementById('verifyOtpBtn');
if (verifyBtn) {
    verifyBtn.addEventListener('click', function() {
        // Ambil email dari URL atau session
        var urlParams = new URLSearchParams(window.location.search);
        var email = urlParams.get('email') || sessionStorage.getItem('register_email') || '';
        var otp = document.getElementById('otpCode') ? document.getElementById('otpCode').value.trim() : '';
        
        // Auto fill OTP dari URL
        var urlOtp = urlParams.get('otp');
        if (urlOtp && !otp) {
            otp = urlOtp;
            if (document.getElementById('otpCode')) {
                document.getElementById('otpCode').value = otp;
            }
        }
        
        // Auto fill OTP dari session
        if (!otp) {
            otp = sessionStorage.getItem('register_otp') || '';
            if (document.getElementById('otpCode')) {
                document.getElementById('otpCode').value = otp;
            }
        }
        
        if (!email) {
            showToast('❌ Email tidak ditemukan! Silakan daftar ulang.', 'error');
            return;
        }
        if (!otp) {
            showToast('❌ Masukkan kode OTP!', 'error');
            if (document.getElementById('otpCode')) {
                document.getElementById('otpCode').focus();
            }
            return;
        }
        if (otp.length !== 6) {
            showToast('❌ Kode OTP harus 6 digit!', 'error');
            return;
        }
        
        verifyBtn.disabled = true;
        verifyBtn.innerHTML = '<span class="loading-spinner"></span> Memverifikasi...';
        
        fetch('/api/verify_otp', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                email: email,
                otp: otp
            })
        })
        .then(function(response) { return response.json(); })
        .then(function(data) {
            console.log('📥 Verify Response:', data);
            
            if (data.success) {
                showToast('✅ ' + data.message, 'success');
                // Hapus session
                sessionStorage.removeItem('register_email');
                sessionStorage.removeItem('register_otp');
                setTimeout(function() {
                    window.location.href = data.redirect || '/login';
                }, 2000);
            } else {
                showToast('❌ ' + (data.error || 'OTP tidak valid!'), 'error');
                verifyBtn.disabled = false;
                verifyBtn.innerHTML = '<i class="fas fa-check"></i> Verifikasi';
            }
        })
        .catch(function(err) {
            console.error('Verify OTP error:', err);
            showToast('❌ Gagal terhubung ke server!', 'error');
            verifyBtn.disabled = false;
            verifyBtn.innerHTML = '<i class="fas fa-check"></i> Verifikasi';
        });
    });
}

// ============================================================
// 12c. RESEND OTP - FIX
// ============================================================
var resendBtn = document.getElementById('resendOtpBtn');
if (resendBtn) {
    resendBtn.addEventListener('click', function() {
        var urlParams = new URLSearchParams(window.location.search);
        var email = urlParams.get('email') || sessionStorage.getItem('register_email') || '';
        
        if (!email) {
            showToast('❌ Email tidak ditemukan!', 'error');
            return;
        }
        resendBtn.disabled = true;
        resendBtn.innerHTML = '<span class="loading-spinner"></span> Mengirim...';
        
        fetch('/api/resend_otp', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email: email })
        })
        .then(function(response) { return response.json(); })
        .then(function(data) {
            console.log('📥 Resend Response:', data);
            
            if (data.success) {
                var newOtp = data.otp || data.dev_otp || '';
                sessionStorage.setItem('register_otp', newOtp);
                console.log('🔑 New OTP:', newOtp);
                
                // Auto fill OTP baru
                if (document.getElementById('otpCode')) {
                    document.getElementById('otpCode').value = newOtp;
                }
                
                // Auto fill OTP digits
                var otpDigits = document.querySelectorAll('.otp-digit');
                if (otpDigits.length === 6) {
                    var digits = newOtp.toString().split('');
                    otpDigits.forEach(function(input, index) {
                        if (digits[index]) {
                            input.value = digits[index];
                        }
                    });
                }
                
                showToast('✅ ' + data.message, 'success');
                startCountdown(60);
            } else {
                showToast('❌ ' + (data.error || 'Gagal mengirim ulang!'), 'error');
            }
            resendBtn.disabled = false;
            resendBtn.innerHTML = '<i class="fas fa-sync"></i> Kirim Ulang OTP';
        })
        .catch(function(err) {
            console.error('Resend OTP error:', err);
            showToast('❌ Gagal terhubung ke server!', 'error');
            resendBtn.disabled = false;
            resendBtn.innerHTML = '<i class="fas fa-sync"></i> Kirim Ulang OTP';
        });
    });
}

// ============================================================
// 12k. AUTO FILL OTP DARI URL (SAAT PAGE LOAD)
// ============================================================
(function autoFillOTPFromURL() {
    var urlParams = new URLSearchParams(window.location.search);
    var email = urlParams.get('email');
    var otp = urlParams.get('otp');
    
    if (email) {
        sessionStorage.setItem('register_email', email);
        // Set email field if exists
        var otpEmail = document.getElementById('otpEmail');
        if (otpEmail) {
            otpEmail.value = email;
            otpEmail.textContent = email;
        }
    }
    
    if (otp) {
        sessionStorage.setItem('register_otp', otp);
        console.log('🔑 OTP from URL:', otp);
        
        // Auto fill OTP input
        var otpInput = document.getElementById('otpCode');
        if (otpInput) {
            otpInput.value = otp;
        }
        
        // Auto fill OTP digits
        var otpDigits = document.querySelectorAll('.otp-digit');
        if (otpDigits.length === 6) {
            var digits = otp.toString().split('');
            otpDigits.forEach(function(input, index) {
                if (digits[index]) {
                    input.value = digits[index];
                }
            });
        }
        
        // Auto verify OTP after 1 second
        setTimeout(function() {
            var verifyBtn = document.getElementById('verifyOtpBtn');
            if (verifyBtn && !verifyBtn.disabled && otp.length === 6) {
                verifyBtn.click();
            }
        }, 1000);
    }
})();

// ============================================================
// 12e. OTP INPUT AUTO-FOCUS + AUTO VERIFY (UPDATED)
// ============================================================
var otpInputs = document.querySelectorAll('.otp-digit');
if (otpInputs.length > 0) {
    otpInputs.forEach(function(input, index) {
        input.addEventListener('input', function() {
            // Hanya angka
            this.value = this.value.replace(/\D/g, '');
            if (this.value.length === 1 && index < otpInputs.length - 1) {
                otpInputs[index + 1].focus();
            }
            // Gabung OTP
            var otp = '';
            otpInputs.forEach(function(inp) {
                otp += inp.value;
            });
            var otpCodeInput = document.getElementById('otpCode');
            if (otpCodeInput) {
                otpCodeInput.value = otp;
            }
            // Auto verify jika 6 digit
            if (otp.length === 6) {
                var verifyBtn = document.getElementById('verifyOtpBtn');
                if (verifyBtn && !verifyBtn.disabled) {
                    setTimeout(function() {
                        verifyBtn.click();
                    }, 500);
                }
            }
        });
        input.addEventListener('keydown', function(e) {
            if (e.key === 'Backspace' && this.value.length === 0 && index > 0) {
                otpInputs[index - 1].focus();
            }
        });
        // Paste support
        input.addEventListener('paste', function(e) {
            e.preventDefault();
            var paste = (e.clipboardData || window.clipboardData).getData('text');
            var digits = paste.replace(/\D/g, '').slice(0, 6);
            digits.split('').forEach(function(d, i) {
                if (otpInputs[i]) otpInputs[i].value = d;
            });
            if (otpInputs[digits.length - 1]) otpInputs[digits.length - 1].focus();
            // Trigger auto verify
            if (digits.length === 6) {
                var verifyBtn = document.getElementById('verifyOtpBtn');
                if (verifyBtn && !verifyBtn.disabled) {
                    setTimeout(function() { verifyBtn.click(); }, 500);
                }
            }
        });
    });
}

    // 12f. SHOW/HIDE PASSWORD
    var togglePassword = document.getElementById('togglePassword');
    if (togglePassword) {
        togglePassword.addEventListener('click', function() {
            var passwordInput = document.getElementById('password');
            var icon = this.querySelector('i');
            if (passwordInput.type === 'password') {
                passwordInput.type = 'text';
                icon.className = 'fas fa-eye-slash';
            } else {
                passwordInput.type = 'password';
                icon.className = 'fas fa-eye';
            }
        });
    }
    
    var toggleConfirmPassword = document.getElementById('toggleConfirmPassword');
    if (toggleConfirmPassword) {
        toggleConfirmPassword.addEventListener('click', function() {
            var passwordInput = document.getElementById('confirmPassword');
            var icon = this.querySelector('i');
            if (passwordInput.type === 'password') {
                passwordInput.type = 'text';
                icon.className = 'fas fa-eye-slash';
            } else {
                passwordInput.type = 'password';
                icon.className = 'fas fa-eye';
            }
        });
    }

    // 12g. PASSWORD STRENGTH INDICATOR
    var passwordInput = document.getElementById('password');
    if (passwordInput) {
        passwordInput.addEventListener('input', function() {
            var strength = document.getElementById('passwordStrength');
            var text = document.getElementById('passwordStrengthText');
            var val = this.value;
            if (!strength || !text) return;
            if (val.length === 0) {
                strength.className = 'password-strength';
                strength.style.width = '0%';
                text.textContent = 'Masukkan password';
                text.style.color = 'rgba(255,255,255,0.3)';
                return;
            }
            var score = 0;
            if (val.length >= 6) score++;
            if (val.length >= 10) score++;
            if (/[a-z]/.test(val) && /[A-Z]/.test(val)) score++;
            if (/[0-9]/.test(val)) score++;
            if (/[^a-zA-Z0-9]/.test(val)) score++;
            var level = '';
            var color = '';
            if (score <= 2) {
                level = 'Lemah';
                color = '#FF1744';
            } else if (score === 3) {
                level = 'Sedang';
                color = '#FFD600';
            } else if (score === 4) {
                level = 'Kuat';
                color = '#00C853';
            } else {
                level = 'Sangat Kuat';
                color = '#00E676';
            }
            strength.className = 'password-strength ' + level.toLowerCase();
            strength.style.width = (score / 5 * 100) + '%';
            strength.style.background = color;
            text.textContent = level + ' (' + score + '/5)';
            text.style.color = color;
        });
    }

    // 12h. AUTO DETECT REFERRAL CODE
    var urlParams = new URLSearchParams(window.location.search);
    var refCode = urlParams.get('ref');
    if (refCode) {
        var referralInput = document.getElementById('referralCode');
        if (referralInput) {
            referralInput.value = refCode;
        }
    }

    // 12i. CHECK EMAIL AVAILABILITY
    var emailInput = document.getElementById('email');
    if (emailInput) {
        var emailTimeout = null;
        emailInput.addEventListener('input', function() {
            clearTimeout(emailTimeout);
            var email = this.value.trim();
            var checkResult = document.getElementById('emailCheckResult');
            if (!checkResult) return;
            if (email.length < 3) {
                checkResult.textContent = '';
                return;
            }
            var emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            if (!emailRegex.test(email)) {
                checkResult.textContent = '❌ Format email tidak valid';
                checkResult.style.color = '#FF1744';
                return;
            }
            emailTimeout = setTimeout(function() {
                checkResult.textContent = '⏳ Mengecek...';
                checkResult.style.color = '#FFD600';
                fetch('/api/check_email?email=' + encodeURIComponent(email))
                .then(function(response) { return response.json(); })
                .then(function(data) {
                    if (data.exists) {
                        checkResult.textContent = '❌ Email sudah terdaftar';
                        checkResult.style.color = '#FF1744';
                    } else {
                        checkResult.textContent = '✅ Email tersedia';
                        checkResult.style.color = '#00C853';
                    }
                })
                .catch(function() {
                    checkResult.textContent = '';
                });
            }, 500);
        });
    }

    // 12j. CHECK USERNAME AVAILABILITY
    var usernameInput = document.getElementById('username');
    if (usernameInput) {
        var usernameTimeout = null;
        usernameInput.addEventListener('input', function() {
            clearTimeout(usernameTimeout);
            var username = this.value.trim();
            var checkResult = document.getElementById('usernameCheckResult');
            if (!checkResult) return;
            if (username.length < 3) {
                checkResult.textContent = '';
                return;
            }
            usernameTimeout = setTimeout(function() {
                checkResult.textContent = '⏳ Mengecek...';
                checkResult.style.color = '#FFD600';
                fetch('/api/check_username?username=' + encodeURIComponent(username))
                .then(function(response) { return response.json(); })
                .then(function(data) {
                    if (data.exists) {
                        checkResult.textContent = '❌ Username sudah digunakan';
                        checkResult.style.color = '#FF1744';
                    } else {
                        checkResult.textContent = '✅ Username tersedia';
                        checkResult.style.color = '#00C853';
                    }
                })
                .catch(function() {
                    checkResult.textContent = '';
                });
            }, 500);
        });
    }

    // =============================================================
    // 13. EVENT LISTENERS (EXISTING)
    // =============================================================

    // Deposit Amount Input
    var depositAmount = document.getElementById('depositAmount');
    if (depositAmount) {
        depositAmount.addEventListener('input', function() {
            if (typeof window.updateDepositInfo === 'function') {
                window.updateDepositInfo();
            }
        });
    }

    // Deposit Method Select
    var depositMethod = document.getElementById('depositMethod');
    if (depositMethod) {
        depositMethod.addEventListener('change', function() {
            if (typeof window.updateMethodInfo === 'function') {
                window.updateMethodInfo();
            }
        });
    }

    // Deposit Button
    var depositBtn = document.getElementById('depositBtn');
    if (depositBtn) {
        depositBtn.addEventListener('click', function(e) {
            e.preventDefault();
            if (typeof window.submitDeposit === 'function') {
                window.submitDeposit();
            }
        });
    }

    // Convert Amount Input
    var amountUsd = document.getElementById('amountUsd');
    if (amountUsd) {
        amountUsd.addEventListener('input', function() {
            if (typeof window.updateEstimate === 'function') {
                window.updateEstimate();
            }
        });
    }

    // Crypto Select
    var cryptoSelect = document.getElementById('cryptoType');
    if (cryptoSelect) {
        cryptoSelect.addEventListener('change', function() {
            if (typeof window.updateWalletAddress === 'function') {
                window.updateWalletAddress();
            }
        });
    }

    // Convert Button
    var convertBtn = document.getElementById('convertBtn');
    if (convertBtn) {
        convertBtn.addEventListener('click', function(e) {
            e.preventDefault();
            if (typeof window.submitConvert === 'function') {
                window.submitConvert();
            }
        });
    }

    // =============================================================
    // 14. UPLOAD AREA (Deposit Page)
    // =============================================================

    var uploadArea = document.getElementById('uploadArea');
    var depositPhoto = document.getElementById('depositPhoto');

    if (uploadArea && depositPhoto) {
        uploadArea.addEventListener('click', function() {
            depositPhoto.click();
        });

        depositPhoto.addEventListener('change', function() {
            if (this.files && this.files[0]) {
                var preview = document.getElementById('uploadPreview');
                var fileName = document.getElementById('uploadFileName');
                if (preview) preview.style.display = 'block';
                if (fileName) fileName.textContent = this.files[0].name;
                if (uploadArea) uploadArea.style.borderColor = '#00C853';
                window.showToast('✅ File berhasil diupload: ' + this.files[0].name, 'success');
            }
        });

        uploadArea.addEventListener('dragover', function(e) {
            e.preventDefault();
            this.classList.add('dragover');
        });

        uploadArea.addEventListener('dragleave', function(e) {
            e.preventDefault();
            this.classList.remove('dragover');
        });

        uploadArea.addEventListener('drop', function(e) {
            e.preventDefault();
            this.classList.remove('dragover');
            if (e.dataTransfer.files && e.dataTransfer.files[0]) {
                depositPhoto.files = e.dataTransfer.files;
                depositPhoto.dispatchEvent(new Event('change'));
            }
        });
    }

    // =============================================================
    // 15. KEYBOARD SHORTCUTS
    // =============================================================

    document.addEventListener('keydown', function(e) {
        // ESC untuk tutup modal
        if (e.key === 'Escape') {
            var modals = document.querySelectorAll('.modal');
            modals.forEach(function(modal) {
                if (modal.style.display === 'flex') {
                    modal.style.display = 'none';
                }
            });
        }
        // Ctrl+Enter untuk submit deposit
        if (e.ctrlKey && e.key === 'Enter') {
            var btn = document.getElementById('depositBtn');
            if (btn && !btn.disabled) {
                btn.click();
            }
        }
        // Jika di OTP input, trigger verify
        if (e.key === 'Enter') {
            if (document.activeElement && document.activeElement.classList.contains('otp-digit')) {
                var verifyBtn = document.getElementById('verifyOtpBtn');
                if (verifyBtn && !verifyBtn.disabled) {
                    verifyBtn.click();
                }
            }
        }
    });

    // =============================================================
    // 16. MODAL CLOSE ON OVERLAY CLICK
    // =============================================================

    document.querySelectorAll('.modal').forEach(function(modal) {
        modal.addEventListener('click', function(e) {
            if (e.target === this) {
                this.style.display = 'none';
            }
        });
    });

    // =============================================================
    // 17. INIT
    // =============================================================

    // Set default wallet address (Convert Page)
    if (typeof window.updateWalletAddress === 'function') {
        window.updateWalletAddress();
    }

    // Set default method info (Deposit Page)
    if (typeof window.updateMethodInfo === 'function') {
        window.updateMethodInfo();
    }

    // Load rate
    fetch('/api/settings')
        .then(function(res) { return res.json(); })
        .then(function(data) {
            var rateDisplay = document.getElementById('rateDisplay');
            if (rateDisplay && data.usd_rate) {
                rateDisplay.textContent = 'Rp ' + parseInt(data.usd_rate).toString().replace(/\B(?=(\d{3})+(?!\d))/g, '.');
            }
        })
        .catch(function() {});

    console.log('✅ DavaOFC Web Fully Loaded!');
    console.log('📅 ' + new Date().toLocaleDateString('id-ID', { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' }));
    console.log('🕐 ' + new Date().toLocaleTimeString('id-ID'));
    console.log('💳 ' + Object.keys(window.methodData || {}).length + ' metode deposit tersedia!');
    console.log('🪙 ' + Object.keys(window.walletData || {}).length + ' crypto tersedia!');
    console.log('📝 Register & OTP functions loaded!');
});