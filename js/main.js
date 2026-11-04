(() => {
  const feed = document.querySelector('.feed');
  const feedEmpty = feed.querySelector('.feed-empty');
  const projects = [...feed.querySelectorAll('.feed-project')];
  const menuList = document.querySelector('.menu-list');
  const menuItems = [...menuList.querySelectorAll('.menu-item')];

  /* Разворот ленты на весь экран */

  const EXPAND_MS = 600;
  let anchorFrame;
  let anchorRatio = 0;

  // Пока панель меняет размер, картинки растут вместе с ней.
  // Держим ту же долю прокрутки, чтобы на экране оставалась та же работа.
  function keepScrollAnchor() {
    cancelAnimationFrame(anchorFrame);
    anchorRatio = feed.scrollTop / feed.scrollHeight;
    const end = performance.now() + EXPAND_MS;
    const tick = (now) => {
      feed.scrollTop = anchorRatio * feed.scrollHeight;
      if (now < end) anchorFrame = requestAnimationFrame(tick);
    };
    anchorFrame = requestAnimationFrame(tick);
  }

  function isExpanded() {
    return feed.classList.contains('is-expanded');
  }

  function expand() {
    if (isExpanded()) return;
    keepScrollAnchor();
    feed.classList.remove('is-collapsing');
    feed.classList.add('is-expanded');
    feed.setAttribute('aria-label', 'Лента работ. Нажмите ещё раз, чтобы свернуть');
    document.body.classList.add('feed-open');
  }

  function collapse() {
    if (!isExpanded()) return;
    keepScrollAnchor();
    feed.classList.add('is-collapsing');
    feed.classList.remove('is-expanded');
    feed.setAttribute('aria-label', 'Лента работ. Нажмите, чтобы развернуть на весь экран');
    document.body.classList.remove('feed-open');
  }

  // Первый тап разворачивает ленту, второй — сворачивает
  function toggle() {
    if (isExpanded()) collapse();
    else expand();
  }

  feed.addEventListener('transitionend', (e) => {
    if (e.target !== feed || e.propertyName !== 'width') return;
    // Если вкладка была в фоне и кадры не шли, доводим прокрутку по окончании анимации
    cancelAnimationFrame(anchorFrame);
    feed.scrollTop = anchorRatio * feed.scrollHeight;
    if (!isExpanded()) feed.classList.remove('is-collapsing');
  });

  feed.addEventListener('click', toggle);
  feed.addEventListener('keydown', (e) => {
    if (e.key === 'Enter' || e.key === ' ') {
      e.preventDefault();
      toggle();
    }
  });
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') collapse();
  });

  /* Видео в ленте грузятся и играют, только пока их видно */

  const videoObserver = new IntersectionObserver((entries) => {
    entries.forEach(({ target, isIntersecting }) => {
      if (isIntersecting) target.play().catch(() => {});
      else target.pause();
    });
  }, { root: feed, threshold: 0.25 });
  feed.querySelectorAll('video').forEach((video) => videoObserver.observe(video));

  /* Картинка, которая следует за курсором. По умолчанию стоит в центре блока;
     пока мышь внутри — плавно догоняет курсор, но не выходит за края,
     а когда мышь уходит — возвращается в центр. */

  const FOLLOW_SPEED = 10;   // чем больше, тем быстрее догоняет (1/с)
  const FOLLOW_INSET = 0.04; // отступ от краёв блока в долях его ширины
  const reducedMotion = matchMedia('(prefers-reduced-motion: reduce)');

  document.querySelectorAll('.cursor-follow').forEach((box) => {
    const img = box.querySelector('img');
    const pos = { x: 0, y: 0 };
    const target = { x: 0, y: 0 };
    let frame = null;
    let last = 0;

    function render() {
      img.style.setProperty('--follow-x', `${pos.x.toFixed(2)}px`);
      img.style.setProperty('--follow-y', `${pos.y.toFixed(2)}px`);
    }

    function tick(now) {
      // Плавность не зависит от частоты кадров
      const dt = Math.min((now - last) / 1000, 0.05);
      last = now;
      const k = 1 - Math.exp(-FOLLOW_SPEED * dt);
      pos.x += (target.x - pos.x) * k;
      pos.y += (target.y - pos.y) * k;
      const done = Math.abs(target.x - pos.x) < 0.1 && Math.abs(target.y - pos.y) < 0.1;
      if (done) {
        pos.x = target.x;
        pos.y = target.y;
      }
      render();
      frame = done ? null : requestAnimationFrame(tick);
    }

    function moveTo(x, y) {
      target.x = x;
      target.y = y;
      if (!frame) {
        last = performance.now();
        frame = requestAnimationFrame(tick);
      }
    }

    box.addEventListener('pointermove', (e) => {
      if (e.pointerType === 'touch' || reducedMotion.matches) return;
      const rect = box.getBoundingClientRect();
      const inset = box.clientWidth * FOLLOW_INSET;
      const maxX = (box.clientWidth - img.offsetWidth) / 2 - inset;
      const maxY = (box.clientHeight - img.offsetHeight) / 2 - inset;
      const x = e.clientX - rect.left - rect.width / 2;
      const y = e.clientY - rect.top - rect.height / 2;
      moveTo(Math.max(-maxX, Math.min(maxX, x)), Math.max(-maxY, Math.min(maxY, y)));
    });
    box.addEventListener('pointerleave', () => moveTo(0, 0));
  });

  /* Меню проектов: пункт под розовой плашкой — текущий проект */

  // Точная геометрия списка. offsetTop и clientHeight округляют до целых,
  // а на краю барабана ошибка в доли пикселя на каждую строку уже заметна.
  let rowH = 0;
  let firstCenter = 0;
  let viewH = 0;

  function measureMenu() {
    const li = menuItems[0].parentElement;
    rowH = li.getBoundingClientRect().height;
    firstCenter = parseFloat(getComputedStyle(li.parentElement).paddingTop) + rowH / 2;
    viewH = menuList.getBoundingClientRect().height;
  }

  function itemCenter(item) {
    return firstCenter + menuItems.indexOf(item) * rowH;
  }

  function viewMid() {
    return menuList.scrollTop + viewH / 2;
  }

  function scrollToItem(item, behavior) {
    menuList.scrollTo({ top: itemCenter(item) - viewH / 2, behavior });
  }

  function itemUnderBar() {
    const mid = viewMid();
    return menuItems.reduce((best, item) =>
      Math.abs(itemCenter(item) - mid) < Math.abs(itemCenter(best) - mid) ? item : best
    );
  }

  function highlight(item) {
    menuItems.forEach((i) => {
      const active = i === item;
      i.classList.toggle('is-active', active);
      if (active) i.setAttribute('aria-current', 'true');
      else i.removeAttribute('aria-current');
    });
  }

  let shownProject = 'sochi-park';

  function showProject(name) {
    if (name === shownProject) return;
    shownProject = name;
    let found = false;
    projects.forEach((p) => {
      const match = p.dataset.project === name;
      p.hidden = !match;
      found = found || match;
    });
    feedEmpty.hidden = found;
    feed.scrollTop = 0;
  }

  // Копия списка для плашки: в ней пункты окрашены в цвет выбранного
  // и видны только в пределах плашки.
  const focusLayer = document.createElement('div');
  focusLayer.className = 'menu-focus';
  focusLayer.setAttribute('aria-hidden', 'true');
  focusLayer.inert = true;
  const focusList = menuList.cloneNode(true);
  focusList.classList.add('is-focus');
  focusList.removeAttribute('aria-label');
  focusLayer.append(focusList);
  menuList.after(focusLayer);
  const focusItems = [...focusList.querySelectorAll('.menu-item')];

  // Барабан по модели UIPickerView (обмерено по скриншоту iOS).
  // Строки сидят на цилиндре, длина дуги между соседними равна высоте строки.
  // Строка стоит на высоте R·sin(угла) и сжата по высоте на cos(угла),
  // поэтому промежутки сокращаются вместе с буквами и не схлопываются.
  // Радиус цилиндра берём от высоты панели, чтобы барабан занимал её целиком.
  // Перспектива слабая: строки лишь чуть сужаются, положение она не меняет.
  // Яркость вне плашки почти ровная — как в iOS, где выделяет сама плашка.
  const DRUM_FILL = 0.97;          // радиус цилиндра в долях половины высоты панели
  const DRUM_PERSPECTIVE = 7.4;    // расстояние до зрителя в радиусах цилиндра
  const DRUM_EDGE_OPACITY = 0.7;   // яркость строки у самого края цилиндра
  let drumFrame;

  function updateDrum() {
    drumFrame = null;
    const radius = (viewH / 2) * DRUM_FILL;
    const step = rowH / radius;
    const persp = DRUM_PERSPECTIVE * radius;
    const mid = viewMid();

    menuItems.forEach((item, i) => {
      const rows = (itemCenter(item) - mid) / rowH;
      const angle = rows * step;
      let transform = 'none';
      let opacity = 0;
      if (Math.abs(angle) < Math.PI / 2) {
        const cos = Math.cos(angle);
        const shift = radius * Math.sin(angle) - rows * rowH;
        const z = radius * (cos - 1);
        transform =
          `translateY(${shift.toFixed(2)}px) perspective(${persp.toFixed(1)}px) ` +
          `translateZ(${z.toFixed(2)}px) rotateX(${(-angle).toFixed(4)}rad)`;
        opacity = 1 - (1 - cos) * (1 - DRUM_EDGE_OPACITY);
      }
      for (const el of [item, focusItems[i]]) {
        el.style.setProperty('--drum-transform', transform);
        el.style.setProperty('--drum-opacity', opacity.toFixed(3));
      }
    });
    focusList.scrollTop = menuList.scrollTop;
  }

  function requestDrum() {
    if (!drumFrame) drumFrame = requestAnimationFrame(updateDrum);
  }

  // Колесо мыши: один щелчок — одна строка. Тачпад шлёт много мелких
  // событий, их копим, пока не наберётся порог.
  const WHEEL_STEP = 40;
  let wheelTarget = 0;
  let wheelAccum = 0;

  menuList.addEventListener('wheel', (e) => {
    if (e.ctrlKey) return;
    e.preventDefault();
    wheelAccum += e.deltaMode === 1 ? e.deltaY * WHEEL_STEP : e.deltaY;
    if (Math.abs(wheelAccum) < WHEEL_STEP) return;
    const dir = Math.sign(wheelAccum);
    wheelAccum = 0;
    const next = Math.min(Math.max(wheelTarget + dir, 0), menuItems.length - 1);
    if (next === wheelTarget) return;
    wheelTarget = next;
    scrollToItem(menuItems[wheelTarget], 'smooth');
  }, { passive: false });

  let settleTimer;
  menuList.addEventListener('scroll', () => {
    const item = itemUnderBar();
    highlight(item);
    requestDrum();
    clearTimeout(settleTimer);
    settleTimer = setTimeout(() => {
      wheelTarget = menuItems.indexOf(item);
      showProject(item.dataset.project);
    }, 150);
  });

  menuItems.forEach((item, index) => {
    item.addEventListener('click', () => {
      wheelTarget = index;
      scrollToItem(item, 'smooth');
    });
  });

  const initial = menuItems.find((i) => i.classList.contains('is-active'));
  wheelTarget = menuItems.indexOf(initial);
  measureMenu();
  scrollToItem(initial, 'instant');
  highlight(initial);
  updateDrum();
  window.addEventListener('resize', () => {
    measureMenu();
    scrollToItem(menuList.querySelector('.menu-item.is-active'), 'instant');
    requestDrum();
  });
})();
