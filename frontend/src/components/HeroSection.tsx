import { Link } from 'react-router-dom'
import { ArrowRight, Shield, Zap, Globe } from 'lucide-react'

const stats = [
  { icon: Shield, label: 'Zero Storage', desc: 'Privacy first' },
  { icon: Zap, label: 'Fast Conversion', desc: 'Seconds only' },
  { icon: Globe, label: 'Any Format', desc: '30+ formats' },
]

export default function HeroSection() {
  return (
    <section className="relative overflow-hidden bg-brand-navy px-4 pb-32 pt-20">
      <div className="pointer-events-none absolute inset-0 bg-[radial-gradient(ellipse_at_top_right,_#ff790015,_transparent_60%),radial-gradient(ellipse_at_bottom_left,_#ff970008,_transparent_50%)]" />
      <div className="pointer-events-none absolute inset-0 bg-[url('data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNDAiIGhlaWdodD0iNDAiIHZpZXdCb3g9IjAgMCA0MCA0MCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48ZyBmaWxsPSJub25lIiBmaWxsLXJ1bGU9ImV2ZW5vZGQiPjxnIGZpbGw9IiNmZmYiIGZpbGwtb3BhY2l0eT0iMC4wMyI+PGNpcmNsZSBjeD0iMjAiIGN5PSIyMCIgcj0iMiIvPjwvZz48L2c+PC9zdmc+')]" />

      <div className="relative mx-auto max-w-4xl text-center">
        <div className="mb-8 inline-flex items-center gap-2 rounded-full border border-white/10 bg-white/5 px-4 py-1.5 text-sm font-medium text-white/70 backdrop-blur-sm">
          <Zap className="h-3.5 w-3.5 text-brand-orange" />
          <span>No accounts &middot; No storage &middot; No hassle</span>
        </div>

        <div className="mb-8 flex justify-center">
          <img
            src="/logo.png"
            alt="ConvertX Logo"
            className="h-24 w-24 rounded-2xl shadow-2xl shadow-brand-orange/20 sm:h-32 sm:w-32"
          />
        </div>

        <h1 className="text-4xl font-extrabold leading-tight text-white sm:text-6xl">
          Convert{' '}
          <span className="bg-gradient-to-r from-brand-orange to-brand-gold bg-clip-text text-transparent">
            anything
          </span>
          <br />
          to any format
        </h1>

        <p className="mx-auto mt-6 max-w-2xl text-lg text-white/60">
          Upload any file &mdash; image, video, audio, or document &mdash; and convert it
          to exactly the format you need. No sign-up required.
        </p>

        <div className="mt-10 flex flex-col items-center gap-4 sm:flex-row sm:justify-center">
          <Link
            to="/convert"
            className="inline-flex items-center gap-2 rounded-xl bg-brand-orange px-8 py-4 text-base font-bold text-white shadow-lg shadow-brand-orange/30 transition-all hover:bg-amber-600 hover:shadow-xl hover:shadow-brand-orange/40"
          >
            Start Converting
            <ArrowRight className="h-5 w-5" />
          </Link>
        </div>

        <div className="mt-16 grid grid-cols-3 gap-4">
          {stats.map(({ icon: Icon, label, desc }) => (
            <div
              key={label}
              className="rounded-xl border border-white/10 bg-white/5 p-4 text-center backdrop-blur-sm"
            >
              <Icon className="mx-auto h-6 w-6 text-brand-orange" />
              <p className="mt-2 text-sm font-semibold text-white">{label}</p>
              <p className="mt-0.5 text-xs text-white/40">{desc}</p>
            </div>
          ))}
        </div>
      </div>
    </section>
  )
}
