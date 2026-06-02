import { Upload, Sliders, Download } from 'lucide-react'

const steps = [
  {
    icon: Upload,
    title: 'Upload your file',
    desc: 'Drag & drop any file or click to browse. We support images, videos, audio, and documents up to 100MB.',
    color: 'from-brand-orange to-amber-500',
  },
  {
    icon: Sliders,
    title: 'Choose format',
    desc: 'Pick from smart suggestions tailored to your file type. Need something else? Browse all available formats.',
    color: 'from-brand-gold to-yellow-500',
  },
  {
    icon: Download,
    title: 'Download instantly',
    desc: 'Your converted file is processed and ready in seconds. We never store your data — complete privacy.',
    color: 'from-emerald-500 to-green-500',
  },
]

export default function HowItWorksSection() {
  return (
    <section className="bg-gray-50/50 px-4 py-24">
      <div className="mx-auto max-w-5xl">
        <h2 className="text-center text-2xl font-bold text-brand-navy sm:text-3xl">
          How it works
        </h2>
        <p className="mt-2 text-center text-gray-500">
          Three simple steps to convert any file.
        </p>

        <div className="mt-16 grid gap-8 md:grid-cols-3">
          {steps.map(({ icon: Icon, title, desc, color }, i) => (
            <div key={title} className="card relative text-center transition-shadow hover:shadow-md">
              <div className="absolute -top-4 left-1/2 -translate-x-1/2">
                <span className="inline-flex h-8 w-8 items-center justify-center rounded-full bg-brand-navy text-xs font-bold text-white shadow-lg">
                  {i + 1}
                </span>
              </div>
              <div className={`mx-auto mt-2 flex h-14 w-14 items-center justify-center rounded-2xl bg-gradient-to-br ${color} shadow-lg`}>
                <Icon className="h-7 w-7 text-white" />
              </div>
              <h3 className="mt-6 text-lg font-bold text-brand-navy">{title}</h3>
              <p className="mt-2 text-sm leading-relaxed text-gray-500">{desc}</p>
            </div>
          ))}
        </div>
      </div>
    </section>
  )
}
