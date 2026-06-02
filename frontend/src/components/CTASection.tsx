import { Link } from 'react-router-dom'
import { ArrowRight, Lock } from 'lucide-react'

export default function CTASection() {
  return (
    <section className="relative overflow-hidden bg-brand-navy px-4 py-24">
      <div className="pointer-events-none absolute inset-0 bg-[radial-gradient(ellipse_at_center,_#ff790010,_transparent_60%)]" />
      <div className="relative mx-auto max-w-2xl text-center">
        <div className="mx-auto flex h-14 w-14 items-center justify-center rounded-2xl bg-brand-orange/20">
          <Lock className="h-7 w-7 text-brand-orange" />
        </div>
        <h2 className="mt-6 text-2xl font-bold text-white sm:text-3xl">
          Your privacy matters
        </h2>
        <p className="mt-4 text-white/60">
          Files are processed in memory and deleted immediately after download.
          No accounts, no tracking, no storage. Just conversion.
        </p>
        <div className="mt-10">
          <Link
            to="/convert"
            className="inline-flex items-center gap-2 rounded-xl bg-brand-orange px-8 py-4 text-base font-bold text-white shadow-lg shadow-brand-orange/30 transition-all hover:bg-amber-600 hover:shadow-xl"
          >
            Start Converting Now
            <ArrowRight className="h-5 w-5" />
          </Link>
        </div>
      </div>
    </section>
  )
}
