// v-reveal — element ekranga kirganda "scroll-reveal is-visible" klassini yoqadi.
// IntersectionObserver orqali ishlaydi, hech qanday kutubxona talab qilmaydi.
export const revealDirective = {
  mounted(el) {
    el.classList.add('scroll-reveal')
    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            el.classList.add('is-visible')
            observer.unobserve(el)
          }
        })
      },
      { threshold: 0.15 }
    )
    observer.observe(el)
  },
}
