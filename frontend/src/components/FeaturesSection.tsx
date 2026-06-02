import { Upload, Sliders, Download, Image, Music, FileVideo, FileText, Cog } from 'lucide-react'

const features = [
  {
    icon: Upload,
    title: 'Drag & Drop Upload',
    desc: 'Drop any file from anywhere. Supports images, videos, audio, and documents up to 100MB.',
  },
  {
    icon: Sliders,
    title: 'Smart Format Suggestions',
    desc: 'Get auto-suggested output formats based on your file type. No need to guess.',
  },
  {
    icon: Cog,
    title: 'Real-time Progress',
    desc: 'Watch the conversion process step by step with live SSE progress updates.',
  },
  {
    icon: Download,
    title: 'Instant Download',
    desc: 'Your converted file is ready immediately. One click and you\'re done.',
  },
]

const categories = [
  { icon: Image, label: 'Image', formats: 'PNG, JPG, WebP, GIF, BMP, TIFF, ICO' },
  { icon: FileVideo, label: 'Video', formats: 'MP4, AVI, MKV, MOV, WebM, GIF' },
  { icon: Music, label: 'Audio', formats: 'MP3, WAV, FLAC, AAC, OGG, M4A, OPUS' },
  { icon: FileText, label: 'Document', formats: 'PDF, DOCX, TXT, MD, HTML, RTF' },
]

export default function FeaturesSection() {
  return (
    <section className="px-4 py-24">
      <div className="mx-auto max-w-5xl">
        <div className="text-center">
          <h2 className="text-2xl font-bold text-brand-navy sm:text-3xl">
            Everything you need
          </h2>
          <p className="mt-2 text-gray-500">
            Powerful conversion tools wrapped in a clean, simple experience.
          </p>
        </div>

        <div className="mt-16 grid gap-8 sm:grid-cols-2">
          {features.map(({ icon: Icon, title, desc }) => (
            <div key={title} className="card flex gap-4 transition-shadow hover:shadow-md">
              <div className="flex h-12 w-12 shrink-0 items-center justify-center rounded-xl bg-gradient-to-br from-brand-orange/10 to-brand-gold/10">
                <Icon className="h-6 w-6 text-brand-orange" />
              </div>
              <div>
                <h3 className="font-semibold text-brand-navy">{title}</h3>
                <p className="mt-1 text-sm text-gray-500">{desc}</p>
              </div>
            </div>
          ))}
        </div>

        <div className="mt-24">
          <h3 className="text-center text-xl font-bold text-brand-navy sm:text-2xl">
            Supported formats
          </h3>
          <div className="mt-10 grid gap-6 sm:grid-cols-2 lg:grid-cols-4">
            {categories.map(({ icon: Icon, label, formats }) => (
              <div key={label} className="card text-center transition-shadow hover:shadow-md">
                <div className="mx-auto flex h-12 w-12 items-center justify-center rounded-xl bg-gradient-to-br from-brand-orange/10 to-brand-gold/10">
                  <Icon className="h-6 w-6 text-brand-orange" />
                </div>
                <h4 className="mt-4 font-semibold text-brand-navy">{label}</h4>
                <p className="mt-1 text-xs text-gray-400">{formats}</p>
              </div>
            ))}
          </div>
        </div>
      </div>
    </section>
  )
}
