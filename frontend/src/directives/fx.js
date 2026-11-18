// src/directives/fx.js — Interactive micro-animation directives
// All effects check localStorage 'qulay_animations', system prefers-reduced-motion, and hover/pointer support.

let mediaReducedMotion = null
let mediaFineHover = null

if (typeof window !== 'undefined' && window.matchMedia) {
  mediaReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)')
  mediaFineHover = window.matchMedia('(hover: hover) and (pointer: fine)')

  // Listen to system prefers-reduced-motion change
  const handleReducedMotionChange = () => {
    updateRootClass()
  }
  if (typeof mediaReducedMotion.addEventListener === 'function') {
    mediaReducedMotion.addEventListener('change', handleReducedMotionChange)
  } else if (typeof mediaReducedMotion.addListener === 'function') {
    mediaReducedMotion.addListener(handleReducedMotionChange)
  }
}

export function isMotionReduced() {
  return mediaReducedMotion ? mediaReducedMotion.matches : false
}

export function canHoverFine() {
  return mediaFineHover ? mediaFineHover.matches : true
}

export function animationsEnabled() {
  if (isMotionReduced()) return false
  try {
    return localStorage.getItem('qulay_animations') !== 'false'
  } catch {
    return true
  }
}

export function updateRootClass() {
  if (typeof document === 'undefined') return
  const isEnabled = animationsEnabled()
  document.documentElement.classList.toggle('qulay-disable-animations', !isEnabled)
}

// Initialize root class on module load
if (typeof document !== 'undefined') {
  updateRootClass()
}

// ── v-tilt ────────────────────────────────────────────────────────────────────
// Adds 3-D tilt + spotlight-glow on hover. Apply to cards/panels. Only on fine pointer devices.
export const vTilt = {
  mounted(el) {
    if (!canHoverFine()) return
    el._tiltHandlers = {
      mousemove(e) {
        if (!animationsEnabled()) return
        const rect = el.getBoundingClientRect()
        const cx = rect.left + rect.width / 2
        const cy = rect.top + rect.height / 2
        const dx = (e.clientX - cx) / (rect.width / 2)
        const dy = (e.clientY - cy) / (rect.height / 2)
        const tiltX = -(dy * 6).toFixed(2)
        const tiltY = (dx * 6).toFixed(2)
        const px = ((e.clientX - rect.left) / rect.width) * 100
        const py = ((e.clientY - rect.top) / rect.height) * 100
        el.style.transform = `perspective(900px) rotateX(${tiltX}deg) rotateY(${tiltY}deg) scale3d(1.02,1.02,1.02)`
        el.style.transition = 'transform 0.1s ease'
        el.style.setProperty('--spotlight-x', `${px}%`)
        el.style.setProperty('--spotlight-y', `${py}%`)
        el.classList.add('tilt-active')
      },
      mouseleave() {
        el.style.transform = 'perspective(900px) rotateX(0deg) rotateY(0deg) scale3d(1,1,1)'
        el.style.transition = 'transform 0.4s cubic-bezier(0.16,1,0.3,1)'
        el.classList.remove('tilt-active')
      },
    }
    el.addEventListener('mousemove', el._tiltHandlers.mousemove)
    el.addEventListener('mouseleave', el._tiltHandlers.mouseleave)
  },
  unmounted(el) {
    if (el._tiltHandlers) {
      el.removeEventListener('mousemove', el._tiltHandlers.mousemove)
      el.removeEventListener('mouseleave', el._tiltHandlers.mouseleave)
      delete el._tiltHandlers
    }
  },
}

// ── v-magnet ──────────────────────────────────────────────────────────────────
// Makes element softly follow the cursor (magnetic feel). Apply to buttons/icons. Only on fine pointer devices.
export const vMagnet = {
  mounted(el) {
    if (!canHoverFine()) return
    el._magnetHandlers = {
      mousemove(e) {
        if (!animationsEnabled()) return
        const rect = el.getBoundingClientRect()
        const cx = rect.left + rect.width / 2
        const cy = rect.top + rect.height / 2
        const dx = (e.clientX - cx) * 0.3
        const dy = (e.clientY - cy) * 0.3
        el.style.transform = `translate(${dx}px, ${dy}px)`
        el.style.transition = 'transform 0.2s cubic-bezier(0.16,1,0.3,1)'
      },
      mouseleave() {
        el.style.transform = 'translate(0,0)'
        el.style.transition = 'transform 0.4s cubic-bezier(0.16,1,0.3,1)'
      },
    }
    el.addEventListener('mousemove', el._magnetHandlers.mousemove)
    el.addEventListener('mouseleave', el._magnetHandlers.mouseleave)
  },
  unmounted(el) {
    if (el._magnetHandlers) {
      el.removeEventListener('mousemove', el._magnetHandlers.mousemove)
      el.removeEventListener('mouseleave', el._magnetHandlers.mouseleave)
      delete el._magnetHandlers
    }
  },
}

// ── v-ripple ──────────────────────────────────────────────────────────────────
// Material-style ripple on click. Apply to buttons/interactive surfaces. Works on all devices.
export const vRipple = {
  mounted(el) {
    el.style.position = 'relative'
    el.style.overflow = 'hidden'
    el._rippleHandler = function (e) {
      if (!animationsEnabled()) return
      const rect = el.getBoundingClientRect()
      const size = Math.max(rect.width, rect.height) * 2
      const x = e.clientX - rect.left - size / 2
      const y = e.clientY - rect.top - size / 2
      const ripple = document.createElement('span')
      ripple.style.cssText = `
        position:absolute;
        left:${x}px;top:${y}px;
        width:${size}px;height:${size}px;
        border-radius:50%;
        background:rgb(255 255 255 / 0.25);
        pointer-events:none;
        transform:scale(0);
        animation:rippleExpand 0.5s cubic-bezier(0.16,1,0.3,1) forwards;
        z-index:9;
      `
      el.appendChild(ripple)
      ripple.addEventListener('animationend', () => ripple.remove())
    }
    el.addEventListener('pointerdown', el._rippleHandler)
  },
  unmounted(el) {
    if (el._rippleHandler) {
      el.removeEventListener('pointerdown', el._rippleHandler)
      delete el._rippleHandler
    }
  },
}

// ── v-glow ────────────────────────────────────────────────────────────────────
// Adds a soft ambient glow halo that follows the cursor inside the element. Only on fine pointer devices.
export const vGlow = {
  mounted(el) {
    if (!canHoverFine()) return
    el._glowHandlers = {
      mousemove(e) {
        if (!animationsEnabled()) return
        const rect = el.getBoundingClientRect()
        const x = e.clientX - rect.left
        const y = e.clientY - rect.top
        el.style.setProperty('--glow-x', `${x}px`)
        el.style.setProperty('--glow-y', `${y}px`)
        el.classList.add('glow-active')
      },
      mouseleave() {
        el.classList.remove('glow-active')
      },
    }
    el.addEventListener('mousemove', el._glowHandlers.mousemove)
    el.addEventListener('mouseleave', el._glowHandlers.mouseleave)
  },
  unmounted(el) {
    if (el._glowHandlers) {
      el.removeEventListener('mousemove', el._glowHandlers.mousemove)
      el.removeEventListener('mouseleave', el._glowHandlers.mouseleave)
      delete el._glowHandlers
    }
  },
}
