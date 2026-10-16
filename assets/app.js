(function () {
  // mobile menu
  var btn = document.querySelector('.menu-btn'), nav = document.getElementById('nav');
  if (btn && nav) btn.addEventListener('click', function () {
    var open = nav.classList.toggle('open'); btn.setAttribute('aria-expanded', open);
  });

  // GA4 events for WhatsApp / phone clicks
  function track(name, params) { if (window.gtag) window.gtag('event', name, params || {}); }
  document.addEventListener('click', function (e) {
    var a = e.target.closest('[data-ev]'); if (a) track(a.getAttribute('data-ev'), { page: location.pathname });
  });

  // booking form → WhatsApp prefilled message
  var f = document.getElementById('book'); if (!f) return;
  var d = f.querySelector('[name=date]');
  if (d) { var t = new Date(); d.min = t.toISOString().slice(0, 10); }
  f.addEventListener('submit', function (e) {
    e.preventDefault();
    var v = function (n) { var el = f.querySelector('[name=' + n + ']'); return el ? el.value.trim() : ''; };
    if (!v('date')) { d.classList.add('err'); d.focus(); return; }
    d.classList.remove('err');
    var L = f.dataset.lang === 'en' ? {
      hi: "Hello, I'd like to book a transfer", route: 'Route', date: 'Date', time: 'Time', pax: 'Passengers',
      car: 'Car', flight: 'Flight', place: 'Address/hotel', name: 'Name'
    } : {
      hi: 'السلام عليكم، أرغب بحجز توصيل', route: 'المسار', date: 'التاريخ', time: 'الوقت', pax: 'عدد الركاب',
      car: 'نوع السيارة', flight: 'رقم الرحلة', place: 'العنوان/الفندق', name: 'الاسم'
    };
    var lines = [L.hi, L.route + ': ' + v('route'), L.date + ': ' + v('date')];
    if (v('time')) lines.push(L.time + ': ' + v('time'));
    lines.push(L.pax + ': ' + v('pax'), L.car + ': ' + v('car'));
    if (v('flight')) lines.push(L.flight + ': ' + v('flight'));
    if (v('place')) lines.push(L.place + ': ' + v('place'));
    if (v('name')) lines.push(L.name + ': ' + v('name'));
    track('generate_lead', { method: 'whatsapp_form', route: v('route') });
    window.open('https://wa.me/' + f.dataset.wa + '?text=' + encodeURIComponent(lines.join('\n')), '_blank');
  });
})();
