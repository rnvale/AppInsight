import { ref, onMounted, onUnmounted, nextTick, type Ref } from 'vue'
import gsap from 'gsap'
import { ScrollTrigger } from 'gsap/ScrollTrigger'

gsap.registerPlugin(ScrollTrigger)

export const easeOut = 'power3.out'
export const easeSpring = 'back.out(1.7)'

export function useCountUp(duration = 1.2) {
  const display = ref('0')
  let ctx: gsap.Context | null = null
  const animate = (endVal: number) => {
    if (ctx) ctx.revert()
    ctx = gsap.context(() => {
      const obj = { val: 0 }
      gsap.to(obj, {
        val: endVal, duration, ease: easeOut,
        onUpdate: () => { display.value = Math.round(obj.val).toLocaleString() },
      })
    })
  }
  onUnmounted(() => ctx?.revert())
  return { display, animate }
}

export function useFadeInUp(elRef: Ref<HTMLElement | null>, delay = 0) {
  let ctx: gsap.Context | null = null
  onMounted(() => {
    nextTick(() => {
      if (!elRef.value) return
      ctx = gsap.context(() => {
        gsap.from(elRef.value, { y: 30, opacity: 0, duration: 0.7, delay, ease: easeOut })
      }, elRef.value)
    })
  })
  onUnmounted(() => ctx?.revert())
}

export function useScrollReveal(elRef: Ref<HTMLElement | null>) {
  let ctx: gsap.Context | null = null
  onMounted(() => {
    nextTick(() => {
      if (!elRef.value) return
      ctx = gsap.context(() => {
        gsap.from(elRef.value, {
          scrollTrigger: { trigger: elRef.value, start: 'top 85%' },
          y: 40, opacity: 0, duration: 0.8, ease: easeOut,
        })
      }, elRef.value)
    })
  })
  onUnmounted(() => ctx?.revert())
}

export function useHoverScale(ref: Ref<HTMLElement | null>, scale = 1.03) {
  let ctx: gsap.Context | null = null
  onMounted(() => {
    if (!ref.value) return
    ctx = gsap.context(() => {
      const el = ref.value!
      el.addEventListener('mouseenter', () => gsap.to(el, { scale, duration: 0.3, ease: easeOut }))
      el.addEventListener('mouseleave', () => gsap.to(el, { scale: 1, duration: 0.3, ease: easeOut }))
    }, ref.value)
  })
  onUnmounted(() => ctx?.revert())
}

export { gsap, ScrollTrigger }
