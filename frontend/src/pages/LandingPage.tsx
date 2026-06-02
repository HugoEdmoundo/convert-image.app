import { Link } from 'react-router-dom'
import { CATEGORIES } from '../constants/formats'

export default function LandingPage() {
  return (
    <div>
      <section className="relative overflow-hidden bg-gradient-to-br from-indigo-600 via-indigo-700 to-purple-800 px-4 pb-32 pt-20 text-white">
        <div className="absolute inset-0 bg-[url('data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNjAiIGhlaWdodD0iNjAiIHZpZXdCb3g9IjAgMCA2MCA2MCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48ZyBmaWxsPSJub25lIiBmaWxsLXJ1bGU9ImV2ZW5vZGQiPjxnIGZpbGw9IiNmZmYiIGZpbGwtb3BhY2l0eT0iMC4wNSI+PHBhdGggZD0iTTM2IDE4YzEuNjU3IDAgMy0xLjM0MyAzLTNzLTEuMzQzLTMtMy0zLTMgMS4zNDMtMyAzIDEuMzQzIDMgMyAzem0wIDM2YzEuNjU3IDAgMy0xLjM0MyAzLTNzLTEuMzQzLTMtMy0zLTMgMS4zNDMtMyAzIDEuMzQzIDMgMyAzem0tMTgtMTBjMS42NTcgMCAzLTEuMzQzIDMtM3MtMS4zNDMtMy0zLTMtMyAxLjM0My0zIDMgMS4zNDMgMyAzIDN6bTM2IDBjMS42NTcgMCAzLTEuMzQzIDMtM3MtMS4zNDMtMy0zLTMtMyAxLjM0My0zIDMgMS4zNDMgMyAzIDN6TTE4IDE4YzEuNjU3IDAgMy0xLjM0MyAzLTNzLTEuMzQzLTMtMy0zLTMgMS4zNDMtMyAzIDEuMzQzIDMgMyAzem0zNiAwYzEuNjU3IDAgMy0xLjM0MyAzLTNzLTEuMzQzLTMtMy0zLTMgMS4zNDMtMyAzIDEuMzQzIDMgMyAzeiIvPjwvZz48L2c+PC9zdmc+')] opacity-30" />

        <div className="relative mx-auto max-w-4xl text-center">
          <div className="mb-6 inline-flex items-center gap-2 rounded-full bg-white/10 px-4 py-1.5 text-sm font-medium text-white/80 backdrop-blur-sm">
            <span>✦</span>
            <span>Zero storage &middot; Privacy first</span>
          </div>
          <h1 className="text-4xl font-extrabold leading-tight sm:text-6xl">
            Convert{' '}
            <span className="bg-gradient-to-r from-amber-300 to-orange-400 bg-clip-text text-transparent">
              anything
            </span>{' '}
            to any format
          </h1>
          <p className="mx-auto mt-6 max-w-2xl text-lg text-white/70">
            Upload any file &mdash; image, video, audio, or document &mdash; and convert it
            to exactly the format you need. No accounts, no storage, no hassle.
          </p>
          <div className="mt-10 flex flex-col items-center gap-4 sm:flex-row sm:justify-center">
            <Link
              to="/convert"
              className="inline-flex items-center gap-2 rounded-xl bg-white px-8 py-4 text-base font-bold text-indigo-700 shadow-lg transition-all hover:bg-indigo-50 hover:shadow-xl"
            >
              ✦ Start Converting
              <span className="text-lg">→</span>
            </Link>
          </div>

          <div className="mt-16 grid grid-cols-2 gap-4 sm:grid-cols-4">
            {CATEGORIES.map((cat) => (
              <div
                key={cat.id}
                className="rounded-xl border border-white/10 bg-white/5 p-4 text-center backdrop-blur-sm"
              >
                <div className="text-3xl">{cat.emoji}</div>
                <p className="mt-2 text-sm font-semibold text-white">{cat.name}</p>
                <p className="mt-0.5 text-xs text-white/50">
                  {cat.output_formats.length} formats
                </p>
              </div>
            ))}
          </div>
        </div>
      </section>

      <section className="mx-auto max-w-5xl px-4 py-24">
        <h2 className="text-center text-2xl font-bold text-gray-900 sm:text-3xl">
          How it works
        </h2>
        <div className="mt-16 grid gap-8 sm:grid-cols-3">
          {[
            {
              step: '1',
              title: 'Upload your file',
              desc: 'Drag & drop any file. We support images, videos, audio, and documents.',
              icon: '⬆',
            },
            {
              step: '2',
              title: 'Choose format',
              desc: 'Pick from smart suggestions tailored to your file type, or browse all formats.',
              icon: '🎯',
            },
            {
              step: '3',
              title: 'Download instantly',
              desc: 'Your converted file is ready in seconds. We never store your data.',
              icon: '⚡',
            },
          ].map((item) => (
            <div key={item.step} className="card text-center">
              <div className="mx-auto flex h-14 w-14 items-center justify-center rounded-2xl bg-indigo-100 text-2xl text-indigo-600">
                {item.icon}
              </div>
              <p className="mt-4 text-sm font-bold text-indigo-600">Step {item.step}</p>
              <h3 className="mt-1 text-lg font-bold text-gray-900">{item.title}</h3>
              <p className="mt-2 text-sm text-gray-500">{item.desc}</p>
            </div>
          ))}
        </div>
      </section>

      <section className="border-t border-gray-100 bg-gray-50/50 px-4 py-20">
        <div className="mx-auto max-w-3xl text-center">
          <h2 className="text-2xl font-bold text-gray-900 sm:text-3xl">
            What can you convert?
          </h2>
          <div className="mt-10 grid gap-6 sm:grid-cols-2">
            {CATEGORIES.map((cat) => (
              <div key={cat.id} className="card text-left">
                <div className="mb-3 text-2xl">{cat.emoji}</div>
                <h3 className="font-bold text-gray-900">{cat.name}</h3>
                <div className="mt-2 flex flex-wrap gap-1.5">
                  {cat.output_formats.map((f) => (
                    <span
                      key={f.format}
                      className="rounded-md bg-gray-100 px-2 py-0.5 text-xs font-medium text-gray-600"
                    >
                      {f.name}
                    </span>
                  ))}
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>
    </div>
  )
}
