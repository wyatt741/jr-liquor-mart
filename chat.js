/* Chat assistant — quote wizard + free-text answers, runs client-side.
   Set LEAD_URL to actually SEND leads (FormSubmit inbox or a Worker /lead). Empty = demo only.
   Baked in: quote wizard -> lead email (with the full chat transcript), a proactive nudge
   (once/session), and soft follow-up capture for people who chat but skip the wizard.

   TWO chat modes, chosen by WORKER_URL in the CONFIG block below:
   - FREE (WORKER_URL empty): free-text hits the deterministic canned ANSWERS. No backend, no cost.
   - HYBRID AI (WORKER_URL set): free-text POSTs to a Cloudflare Worker /chat (Claude, PLAYBOOK §6)
     for real answers, ~2c/convo. The canned ANSWERS stay as the fallback on ANY error, so the
     bot never dies to a "couldn't connect." The wizard, nudge, and follow-up work in both modes. */
(function () {
  var root = document.getElementById("cw");
  if (!root) return;
  var bubble = document.getElementById("cw-bubble"), panel = document.getElementById("cw-panel"),
      closeB = document.getElementById("cw-close"), log = document.getElementById("cw-log"),
      form = document.getElementById("cw-form"), input = document.getElementById("cw-input"),
      sendB = document.getElementById("cw-send");

  // ============================ CONFIG (customize) ============================
  var PHONE = "805-388-3288";
  var ADDR = "2616 E Ventura Blvd Unit 106, Camarillo, CA 93010";   // match build.py ADDR so the bot links it
  var MAPS = "https://maps.google.com/?q=2616+E+Ventura+Blvd+Unit+106,+Camarillo,+CA+93010";
  var ADDR_RE = ADDR.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
  // WHERE LEADS GO. Empty string = demo only (nothing is sent). Otherwise one of:
  //   FormSubmit (client-side, no backend): "https://formsubmit.co/ajax/inbox@example.com"
  //   Cloudflare Worker /lead (with AI):    "https://chat.jrliquormart.com/lead"
  // TODO: set once the owner's inbox lands (same pending inbox as build.py EMAIL).
  var LEAD_URL = "";
  // CHAT MODE: HYBRID AI (intake decision). Free-text routes to the Cloudflare Worker in
  // worker/ (Claude, ~1-3 cents/convo) once it's deployed on chat.jrliquormart.com; until
  // then every request falls back to the canned ANSWERS below, so the bot still works.
  // Set to "" to drop back to FREE deterministic mode.
  var WORKER_URL = "https://chat.jrliquormart.com";
  var GREETING = "Hi! I'm the JR Liquor Mart assistant. Ask about hours, delivery, or what we carry.";
  var ANSWERS = {
    services: "Five corners of the store: bourbon and whiskey, the walk-in Beer Cave, tequila and agave, wine, and snacks. Hunting something specific? I can send the counter a bottle request.",
    hours:    "We're open daily 8am-10pm at " + ADDR + ". Free parking right outside.",
    price:    "Prices change too often for me to quote here. Call or text " + PHONE + " and the counter will check for you.",
    delivery: "We do same-day delivery and curbside pickup through the delivery apps, or come grab it cold in the store.",
    contact:  "Call or text " + PHONE + ", or use the form on the contact page. Want me to send the counter a bottle request instead?",
    thanks:   "Anytime! Anything else I can check for you?",
    fallback: "Good question. The counter will know for sure, call or text " + PHONE + ". Or I can send them a bottle request."
  };
  function answer(text) {
    var q = text.toLowerCase(), has = function (a) { return a.some(function (w) { return q.indexOf(w) !== -1; }); };
    if (has(["do you have", "do you carry", "in stock", "looking for", "special order", "request", "find a bottle"])) return startWizard;
    if (has(["price", "cost", "how much", "pricing", "$"])) return ANSWERS.price;
    if (has(["hour", "open", "close", "where", "location", "address", "directions", "parking"])) return ANSWERS.hours;
    if (has(["deliver", "doordash", "instacart", "uber eats", "grubhub", "curbside", "pickup", "pick up"])) return ANSWERS.delivery;
    if (has(["contact", "call", "text", "phone", "email", "reach"])) return ANSWERS.contact;
    if (has(["carry", "stock", "service", "offer", "what do", "sell", "help"])) return ANSWERS.services;
    if (has(["thank", "thanks", "great", "awesome", "perfect"])) return ANSWERS.thanks;
    return ANSWERS.fallback;
  }
  var STEPS = [
    { key: "category", q: "Happy to help! What are you after?", opts: ["Bourbon or whiskey", "Beer", "Tequila", "Wine", "Something else"] },
    { key: "bottle",   q: "Which bottle or brand? Size helps too.", text: true },
    { key: "details",  q: "Anything else we should know (when you need it, backup picks)? Or skip.", text: true, optional: true },
    { key: "name",     q: "Got it. What's your name?", text: true },
    { key: "contact",  q: "Best phone or email for you?", text: true }
  ];
  // ===========================================================================

  var mode = "chat", started = false, busy = false, convo = [];
  function el(t, c, x) { var n = document.createElement(t); if (c) n.className = c; if (x != null) n.textContent = x; return n; }
  function scroll() { log.scrollTop = log.scrollHeight; }
  function setInput(on, ph) { input.disabled = !on; sendB.disabled = !on; input.placeholder = ph || "Type your message..."; }
  function linkify(box, text) {
    var re = new RegExp("(https?:\\/\\/[^\\s)]+)|(\\d{3}-\\d{3}-\\d{4})|(" + ADDR_RE + ")", "g"), last = 0, m;
    while ((m = re.exec(text))) {
      if (m.index > last) box.appendChild(document.createTextNode(text.slice(last, m.index)));
      var a = document.createElement("a");
      if (m[1]) { a.href = m[1]; a.target = "_blank"; a.rel = "noopener"; a.textContent = m[1].replace(/^https?:\/\//, "").replace(/\/$/, ""); }
      else if (m[2]) { a.href = "tel:+1" + m[2].replace(/\D/g, ""); a.textContent = m[2]; }
      else { a.href = MAPS; a.target = "_blank"; a.rel = "noopener"; a.textContent = m[3]; }
      box.appendChild(a); last = m.index + m[0].length;
    }
    if (last < text.length) box.appendChild(document.createTextNode(text.slice(last)));
  }
  function addMsg(role, text) { var d = el("div", "cw-msg cw-" + role); linkify(d, text); log.appendChild(d); scroll(); convo.push((role === "user" ? "Visitor: " : "Assistant: ") + text); return d; }
  function typing() { var t = el("div", "cw-typing"); t.appendChild(el("span")); t.appendChild(el("span")); t.appendChild(el("span")); log.appendChild(t); scroll(); return t; }
  function botSay(text, then) { var t = typing(); setTimeout(function () { t.remove(); addMsg("bot", text); if (then) then(); }, 420); }
  function chips(items) {
    var wrap = el("div", "cw-chips");
    items.forEach(function (it) {
      var b = el("button", "cw-chip" + (it.ghost ? " cw-chip-ghost" : ""), it.label); b.type = "button";
      b.addEventListener("click", function () { wrap.remove(); it.act(); });
      wrap.appendChild(b);
    });
    log.appendChild(wrap); scroll(); return wrap;
  }
  function transcript() { return convo.join("\n"); }

  // ---- HYBRID AI path (only used when WORKER_URL is set) ----
  // aiHistory holds committed user/assistant pairs for /chat context (the wizard's convo
  // strings aren't API-shaped, so we keep this parallel role/content log instead).
  var aiHistory = [];
  // Harden a Claude reply into safe DOM: house-style dashes, real bold, bullets, then the
  // existing linkify for URLs/phones/address. All DOM nodes (no innerHTML) -> XSS-safe.
  function renderAI(box, text) {
    text = text.replace(/\s*—\s*/g, ", ").replace(/–/g, "-");   // em -> ", ", en -> "-"
    text.split("\n").forEach(function (line, i) {
      if (i) box.appendChild(el("br"));
      line = line.replace(/^[ \t]*[-*]\s+/, "• ");         // leading "- "/"* " -> bullet
      line.split(/\*\*([^*\n]+)\*\*/).forEach(function (seg, j) {  // odd chunks = **bold**
        if (!seg) return;
        if (j % 2) { var b = el("strong"); linkify(b, seg); box.appendChild(b); }
        else linkify(box, seg);
      });
    });
  }
  function addAIMsg(text) {
    var d = el("div", "cw-msg cw-bot"); renderAI(d, text);
    log.appendChild(d); scroll(); convo.push("Assistant: " + text); return d;
  }
  // AI primary, canned answer() as the fallback on ANY error. fallbackText is the canned
  // string already computed for this message, reused so a fallback never re-triggers the wizard.
  function aiReply(text, fallbackText) {
    var t = typing();
    var msgs = aiHistory.concat([{ role: "user", content: text }]).slice(-16);
    fetch(WORKER_URL.replace(/\/+$/, "") + "/chat", {
      method: "POST", headers: { "content-type": "application/json" },
      body: JSON.stringify({ messages: msgs })
    })
      .then(function (r) { return r.ok ? r.json() : Promise.reject(r.status); })
      .then(function (d) {
        var reply = (d && d.reply) ? String(d.reply) : "";
        if (!reply) return Promise.reject("empty");
        t.remove();
        aiHistory.push({ role: "user", content: text }, { role: "assistant", content: reply });
        aiHistory = aiHistory.slice(-16);
        addAIMsg(reply); maybeOfferFollowup();
      })
      .catch(function () { t.remove(); addMsg("bot", fallbackText); maybeOfferFollowup(); });
  }

  // ---- lead sender: wizard + follow-up both route here ----
  function sendLead(fields, okMsg) {
    if (!LEAD_URL) {   // demo mode: nothing wired up yet
      botSay(okMsg + " (In the live site this sends straight to us. For now, call or text " + PHONE + ".)", function () { setInput(true, "Ask anything else..."); });
      return;
    }
    setInput(false, "Sending...");
    var payload = { _subject: "Bottle request from jrliquormart.com", _template: "table", _captcha: "false", transcript: transcript() };
    for (var k in fields) if (fields.hasOwnProperty(k)) payload[k] = fields[k];
    fetch(LEAD_URL, { method: "POST", headers: { "content-type": "application/json", "accept": "application/json" }, body: JSON.stringify(payload) })
      .then(function (r) { return r.json(); })
      .then(function (d) { var ok = d && (d.ok || d.success === "true" || d.success === true); botSay(ok ? okMsg : ("I couldn't send that just now. Please call or text " + PHONE + "."), function () { setInput(true, "Ask anything else..."); }); })
      .catch(function () { botSay("I couldn't connect to send that. Please call or text " + PHONE + ".", function () { setInput(true, "Ask anything else..."); }); });
  }

  function open() {
    panel.hidden = false; bubble.setAttribute("aria-expanded", "true"); root.classList.add("cw--open");
    if (!started) { started = true; showMenu(); }
    setTimeout(function () { (input.disabled ? bubble : input).focus(); }, 60);
  }
  function close() { panel.hidden = true; bubble.setAttribute("aria-expanded", "false"); root.classList.remove("cw--open"); bubble.focus(); }
  bubble.addEventListener("click", function () { panel.hidden ? open() : close(); });
  closeB.addEventListener("click", close);
  document.addEventListener("keydown", function (e) { if (e.key === "Escape" && !panel.hidden) close(); });
  // any [data-open-chat] element (e.g. a hero "Ask our assistant" link) opens the panel
  Array.prototype.forEach.call(document.querySelectorAll("[data-open-chat]"), function (t) {
    t.addEventListener("click", function (e) { e.preventDefault(); open(); });
  });

  function showMenu() {
    mode = "chat";
    addMsg("bot", GREETING);
    chips([
      { label: "Request a bottle", act: startWizard },
      { label: "What do you carry?", act: function () { addMsg("user", "What do you carry?"); botSay(ANSWERS.services); } },
      { label: "Hours & location", act: function () { addMsg("user", "Where are you?"); botSay(ANSWERS.hours); } }
    ]);
    setInput(true, "Or type your question...");
  }

  // ---- quote wizard -> lead email ----
  var answers = {}, step = 0, skipWrap = null;
  function startWizard() { mode = "wizard"; answers = {}; step = 0; addMsg("user", "I'm looking for a bottle"); botSay(STEPS[0].q, renderStep); }
  function runStep() { if (step >= STEPS.length) return submitQuote(); botSay(STEPS[step].q, renderStep); }
  function renderStep() {
    var s = STEPS[step];
    if (s.opts) {
      setInput(false, "Pick an option above");
      chips(s.opts.map(function (o) { return { label: o, act: function () { addMsg("user", o); answers[s.key] = o; step++; runStep(); } }; }));
    } else {
      setInput(true, s.optional ? "Type, or click Skip" : "Type your answer...");
      skipWrap = s.optional ? chips([{ label: "Skip", ghost: true, act: function () { skipWrap = null; answers[s.key] = ""; step++; runStep(); } }]) : null;
      input.focus();
    }
  }
  function wizardText(text) {
    if (skipWrap) { skipWrap.remove(); skipWrap = null; }
    addMsg("user", text); answers[STEPS[step].key] = text; step++; runStep();
  }
  function submitQuote() { mode = "chat"; sendLead(answers, "Perfect, that's everything" + (answers.name ? ", " + answers.name : "") + "! We'll check the shelf and get back to you."); }

  // ---- proactive nudge (once per session, tasteful, dismissible) ----
  function showNudge() {
    if (started || !panel.hidden) return;
    try { if (sessionStorage.getItem("cw-nudged")) return; sessionStorage.setItem("cw-nudged", "1"); } catch (e) {}
    var n = el("div", "cw-nudge");
    var msg = el("button", "cw-nudge-msg", "Questions? I can help 👋"); msg.type = "button";
    var x = el("button", "cw-nudge-x"); x.type = "button"; x.setAttribute("aria-label", "Dismiss"); x.textContent = "×";
    n.appendChild(msg); n.appendChild(x); root.appendChild(n);
    requestAnimationFrame(function () { n.classList.add("in"); });
    var kill = function () { n.classList.remove("in"); setTimeout(function () { if (n.parentNode) n.parentNode.removeChild(n); }, 350); };
    msg.addEventListener("click", function () { kill(); open(); });
    x.addEventListener("click", function (e) { e.stopPropagation(); kill(); });
    setTimeout(function () { if (panel.hidden) kill(); }, 9000);
  }
  setTimeout(showNudge, 20000);
  window.addEventListener("scroll", function onScroll() { if (window.scrollY > 700) { showNudge(); window.removeEventListener("scroll", onScroll); } }, { passive: true });

  // ---- soft follow-up capture (chatters who skip the wizard; never on close) ----
  var asked = 0, followOffered = false, fu = {}, fuStep = 0;
  var FU = [{ key: "name", q: "Sure. What's your name?" }, { key: "contact", q: "Best phone or email to reach you?" }];
  function maybeOfferFollowup() {
    if (followOffered || asked < 2 || mode !== "chat") return;
    followOffered = true;
    addMsg("bot", "Want the team to follow up with you? I can pass along what you've asked.");
    chips([
      { label: "Yes, follow up", act: startFollowup },
      { label: "No thanks", ghost: true, act: function () { botSay("No problem, ask away. You can also reach us at " + PHONE + "."); } }
    ]);
  }
  function startFollowup() { mode = "followup"; fu = {}; fuStep = 0; runFu(); }
  function runFu() { if (fuStep >= FU.length) return submitFollowup(); botSay(FU[fuStep].q, function () { setInput(true, "Type your answer..."); input.focus(); }); }
  function fuText(text) { addMsg("user", text); fu[FU[fuStep].key] = text; fuStep++; runFu(); }
  function submitFollowup() { mode = "chat"; sendLead({ name: fu.name, contact: fu.contact, needs: "Chat follow-up (skipped the bottle-request wizard)" }, "Got it" + (fu.name ? ", " + fu.name : "") + ". We'll be in touch soon."); }

  // ---- input routes by mode ----
  form.addEventListener("submit", function (e) {
    e.preventDefault();
    var text = input.value.trim(); if (!text || busy) return; input.value = "";
    if (mode === "followup") { fuText(text); return; }
    if (mode === "wizard" && STEPS[step] && STEPS[step].text) { wizardText(text); return; }
    addMsg("user", text); asked++;
    var res = answer(text);
    if (typeof res === "function") { res(); return; }   // keyword hit the wizard trigger
    if (WORKER_URL) { aiReply(text, res); }             // HYBRID: AI primary, res = canned fallback
    else { botSay(res, maybeOfferFollowup); }           // FREE: deterministic canned answer
  });
})();
