/* =========================================================
   GLOW VPN — общие скрипты: фон, шапка, корзина, хелперы
   ========================================================= */
(() => {
    const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

    /* ---------- хелперы (доступны всем страницам как Glow.*) ---------- */
    const escapeHtml = (value) => String(value ?? '')
        .replaceAll('&', '&amp;')
        .replaceAll('<', '&lt;')
        .replaceAll('>', '&gt;')
        .replaceAll('"', '&quot;')
        .replaceAll("'", '&#39;');

    const normalizePhotoPath = (photo) => {
        if (!photo) return '';
        const p = String(photo).trim();
        if (/^https?:\/\//i.test(p) || p.startsWith('/')) return p;
        if (p.startsWith('static/')) return `/${p}`;
        if (p.startsWith('uploads/')) return `/static/${p}`;
        if (!p.includes('/')) return `/static/uploads/${p}`;
        return `/${p}`;
    };

    const formatPrice = (value) => {
        const n = Number(value);
        if (!Number.isFinite(n)) return '—';
        return new Intl.NumberFormat('ru-RU').format(n);
    };

    /* cookie корзины: без неё бэкенд не сможет добавить тариф */
    let cartReady = null;
    const ensureCart = () => {
        if (!cartReady) {
            cartReady = fetch('/api/cart/get-uuid', {credentials: 'include'})
                .then(r => r.json())
                .catch(() => null);
        }
        return cartReady;
    };

    const updateCartCount = async () => {
        const badge = document.getElementById('cartCount');
        if (!badge) return;
        try {
            const r = await fetch('/api/cart', {credentials: 'include'});
            const items = await r.json();
            const count = Array.isArray(items) ? items.length : 0;
            badge.textContent = count;
            badge.hidden = count === 0;
        } catch { badge.hidden = true; }
    };

    const toast = (title, text = '', link = null) => {
        document.querySelector('.toast')?.remove();
        const el = document.createElement('div');
        el.className = 'toast';
        el.innerHTML = `<strong>${escapeHtml(title)}</strong>${text ? `<span>${escapeHtml(text)}</span>` : ''}${link ? `<a href="${escapeHtml(link.href)}">${escapeHtml(link.label)} →</a>` : ''}`;
        document.body.appendChild(el);
        requestAnimationFrame(() => el.classList.add('show'));
        setTimeout(() => { el.classList.remove('show'); setTimeout(() => el.remove(), 400); }, 4500);
    };

    /* покупка тарифа: кладём в корзину и ведём к оформлению */
    const buy = async (productId, button) => {
        const original = button ? button.innerHTML : '';
        if (button) { button.disabled = true; button.innerHTML = '<span class="spinner"></span>Секунду…'; }
        try {
            await ensureCart();
            const r = await fetch(`/api/carts/add/${encodeURIComponent(productId)}`, {method: 'POST', credentials: 'include'});
            const result = await r.json();
            if (result.status === 'success') {
                window.location.href = '/cart';
                return;
            }
            if (result.status === 'already_in_cart') {
                toast('Тариф уже в корзине', 'Можно оформить один тариф за раз', {href: '/cart', label: 'Перейти в корзину'});
            } else {
                toast('Не получилось добавить тариф', 'Обнови страницу и попробуй ещё раз');
            }
        } catch {
            toast('Нет связи с сервером', 'Проверь интернет и попробуй ещё раз');
        }
        if (button) { button.disabled = false; button.innerHTML = original; }
    };

    window.Glow = {escapeHtml, normalizePhotoPath, formatPrice, ensureCart, updateCartCount, toast, buy, reduceMotion};

    /* ---------- прелоадер ---------- */
    const loader = document.getElementById('loader');
    if (loader) {
        window.addEventListener('load', () => setTimeout(() => loader.classList.add('hide'), 300));
        setTimeout(() => loader.classList.add('hide'), 2200);
    }

    const year = document.getElementById('year');
    if (year) year.textContent = new Date().getFullYear();

    /* ---------- шапка ---------- */
    const header = document.getElementById('header');
    const tgFloat = document.getElementById('tgFloat');
    const onScroll = () => {
        const y = window.scrollY;
        header?.classList.toggle('scrolled', y > 30);
        tgFloat?.classList.toggle('show', y > window.innerHeight * 0.6);
    };
    window.addEventListener('scroll', onScroll, {passive: true});
    onScroll();

    const burger = document.getElementById('burger');
    const nav = document.getElementById('nav');
    if (burger && nav) {
        let savedY = 0;
        burger.setAttribute('aria-expanded', 'false');
        burger.setAttribute('aria-controls', 'nav');

        const toggleMenu = (force) => {
            const open = typeof force === 'boolean' ? force : !nav.classList.contains('open');
            if (open === nav.classList.contains('open')) return;

            if (open) {
                /* блокировка прокрутки, которая работает и в iOS Safari */
                savedY = window.scrollY;
                document.body.style.top = `-${savedY}px`;
                document.body.classList.add('menu-open');
            } else {
                document.body.classList.remove('menu-open');
                document.body.style.top = '';
                window.scrollTo({top: savedY, behavior: 'instant'});
            }
            nav.classList.toggle('open', open);
            burger.classList.toggle('active', open);
            burger.setAttribute('aria-expanded', String(open));
            burger.setAttribute('aria-label', open ? 'Закрыть меню' : 'Меню');
        };

        burger.addEventListener('click', () => toggleMenu());
        nav.querySelectorAll('a').forEach(a => a.addEventListener('click', () => toggleMenu(false)));
        /* тап по пустому месту меню — закрыть */
        nav.addEventListener('click', (e) => { if (e.target === nav) toggleMenu(false); });
        document.addEventListener('keydown', (e) => { if (e.key === 'Escape') toggleMenu(false); });
        /* повернули телефон / расширили окно до десктопа — закрыть */
        window.matchMedia('(min-width: 821px)').addEventListener('change', (e) => { if (e.matches) toggleMenu(false); });
    }

    /* ---------- появление блоков при скролле ---------- */
    const io = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (!entry.isIntersecting) return;
            const el = entry.target;
            const siblings = [...el.parentElement.children].filter(c => c.classList.contains('reveal'));
            el.style.transitionDelay = `${Math.min(siblings.indexOf(el), 6) * 80}ms`;
            el.classList.add('visible');
            io.unobserve(el);
        });
    }, {threshold: .12, rootMargin: '0px 0px -40px 0px'});
    Glow.observeReveal = (root = document) => root.querySelectorAll('.reveal:not(.visible)').forEach(el => io.observe(el));
    Glow.observeReveal();

    /* ---------- светлячки ---------- */
    const canvas = document.getElementById('fireflies');
    if (canvas) {
        const ctx = canvas.getContext('2d');
        let W, H, flies = [];
        const resize = () => {
            const dpr = Math.min(window.devicePixelRatio || 1, 2);
            W = window.innerWidth; H = window.innerHeight;
            canvas.width = W * dpr; canvas.height = H * dpr;
            ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
            const count = Math.round(Math.min(70, (W * H) / 22000));
            flies = Array.from({length: count}, () => ({
                x: Math.random() * W, y: Math.random() * H,
                r: Math.random() * 1.8 + .6,
                vx: (Math.random() - .5) * .35, vy: (Math.random() - .5) * .35 - .08,
                phase: Math.random() * Math.PI * 2, speed: .01 + Math.random() * .025,
                hue: 265 + Math.random() * 30
            }));
        };
        resize();
        window.addEventListener('resize', resize);
        const draw = () => {
            ctx.clearRect(0, 0, W, H);
            for (const f of flies) {
                f.phase += f.speed;
                f.x += f.vx + Math.sin(f.phase * .7) * .2;
                f.y += f.vy + Math.cos(f.phase * .5) * .15;
                if (f.x < -20) f.x = W + 20;
                if (f.x > W + 20) f.x = -20;
                if (f.y < -20) f.y = H + 20;
                if (f.y > H + 20) f.y = -20;
                const a = .65 + Math.sin(f.phase) * .35;
                const R = f.r * 7;
                const g = ctx.createRadialGradient(f.x, f.y, 0, f.x, f.y, R);
                g.addColorStop(0, `hsla(${f.hue}, 100%, 85%, ${a})`);
                g.addColorStop(.25, `hsla(${f.hue}, 100%, 65%, ${a * .5})`);
                g.addColorStop(1, `hsla(${f.hue}, 100%, 50%, 0)`);
                ctx.fillStyle = g;
                ctx.beginPath(); ctx.arc(f.x, f.y, R, 0, Math.PI * 2); ctx.fill();
            }
            if (!reduceMotion) requestAnimationFrame(draw);
        };
        draw();
    }

    ensureCart().then(updateCartCount);
})();
