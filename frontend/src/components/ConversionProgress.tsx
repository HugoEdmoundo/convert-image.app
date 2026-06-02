import type { ProgressData, StepId } from '../types'

interface Props {
  progress: ProgressData
}

const STEPS: { id: StepId; label: string }[] = [
  { id: 'initializing', label: 'Initializing' },
  { id: 'validating', label: 'Validating file' },
  { id: 'analyzing', label: 'Analyzing format' },
  { id: 'extracting', label: 'Extracting data' },
  { id: 'converting', label: 'Converting' },
  { id: 'optimizing', label: 'Optimizing output' },
  { id: 'done', label: 'Complete!' },
]

const STEP_ORDER: StepId[] = STEPS.map((s) => s.id)

export default function ConversionProgress({ progress }: Props) {
  const currentIdx = STEP_ORDER.indexOf(progress.step as StepId)

  return (
    <div className="card space-y-6">
      <div className="flex items-center justify-between">
        <h3 className="text-sm font-semibold text-gray-700">Conversion Progress</h3>
        <span className="text-sm font-bold text-brand-orange">{progress.percent}%</span>
      </div>

      <div className="h-2.5 w-full overflow-hidden rounded-full bg-gray-100">
        <div
          className="h-full rounded-full bg-gradient-to-r from-brand-orange to-brand-gold transition-all duration-500 ease-out"
          style={{ width: `${progress.percent}%` }}
        />
      </div>

      <div className="space-y-3">
        {STEPS.map((step, i) => {
          const isDone = i < currentIdx
          const isActive = i === currentIdx
          return (
            <div key={step.id} className="flex items-center gap-3">
              <div
                className={`flex h-7 w-7 shrink-0 items-center justify-center rounded-full text-xs font-bold transition-all duration-300 ${
                  isDone
                    ? 'bg-brand-orange text-white'
                    : isActive
                      ? 'border-2 border-brand-orange bg-orange-50 text-brand-orange'
                      : 'border-2 border-gray-200 bg-white text-gray-300'
                }`}
              >
                {isDone ? '✓' : isActive ? '●' : i + 1}
              </div>
              <span
                className={`text-sm transition-all duration-300 ${
                  isDone
                    ? 'font-medium text-gray-900'
                    : isActive
                      ? 'font-semibold text-brand-orange'
                      : 'text-gray-400'
                }`}
              >
                {step.label}
              </span>
            </div>
          )
        })}
      </div>

      <p className="animate-pulse text-center text-sm font-medium text-brand-orange">
        {progress.message}
      </p>
    </div>
  )
}
