import FileUpload from '../components/FileUpload'
import FormatSelector from '../components/FormatSelector'
import ConversionProgress from '../components/ConversionProgress'
import ResultCard from '../components/ResultCard'
import { useConversion } from '../hooks/useConversion'

export default function ConverterPage() {
  const {
    state,
    fileInfo,
    selectedFormat,
    suggestion,
    progress,
    result,
    error,
    setFile,
    setFormat,
    startConversion,
    reset,
  } = useConversion()

  const isSubmitting = state === 'converting'

  return (
    <div className="mx-auto max-w-2xl px-4 py-12">
      <div className="mb-8 text-center">
        <h1 className="text-2xl font-bold text-gray-900 sm:text-3xl">Convert your file</h1>
        <p className="mt-2 text-sm text-gray-500">
          Upload, choose format, and download &mdash; that&apos;s it.
        </p>
      </div>

      {/* Step indicator */}
      <div className="mb-10 flex items-center justify-center gap-0">
        {[
          { label: 'Upload', step: 0 },
          { label: 'Convert', step: 1 },
          { label: 'Done', step: 2 },
        ].map((s, i) => {
          const currentStep = state === 'done' ? 2 : fileInfo ? 1 : 0
          const isActive = currentStep === s.step
          const isDone = currentStep > s.step

          return (
            <div key={s.label} className="flex items-center">
              <div
                className={`step-dot ${isDone ? 'done' : isActive ? 'active' : 'pending'}`}
              >
                {isDone ? '✓' : s.step + 1}
              </div>
              <span
                className={`ml-2 text-xs font-medium ${
                  isActive ? 'text-indigo-600' : isDone ? 'text-gray-700' : 'text-gray-400'
                }`}
              >
                {s.label}
              </span>
              {i < 2 && (
                <div
                  className={`step-line mx-3 w-12 sm:w-20 ${
                    isDone ? 'done' : 'pending'
                  }`}
                />
              )}
            </div>
          )
        })}
      </div>

      {error && state === 'error' && (
        <div className="mb-6 flex items-start gap-3 rounded-xl border border-red-200 bg-red-50 p-4 text-sm text-red-700">
          <span className="mt-0.5">⚠️</span>
          <div className="flex-1">
            <p className="font-medium">Conversion failed</p>
            <p className="mt-0.5 text-red-600">{error}</p>
          </div>
          <button
            onClick={reset}
            className="shrink-0 rounded-lg px-3 py-1.5 text-xs font-medium text-red-600 hover:bg-red-100"
          >
            Try again
          </button>
        </div>
      )}

      {state === 'done' && result && fileInfo ? (
        <ResultCard result={result} fileInfo={fileInfo} onReset={reset} />
      ) : (
        <div className="space-y-6">
          <FileUpload onFile={setFile} fileInfo={fileInfo} />

          {suggestion && fileInfo && (
            <FormatSelector
              suggestion={suggestion}
              selected={selectedFormat}
              onSelect={setFormat}
            />
          )}

          {fileInfo && selectedFormat && state !== 'converting' && (
            <button
              onClick={startConversion}
              disabled={isSubmitting}
              className="btn-primary w-full py-4 text-base"
            >
              {isSubmitting ? (
                <span className="flex items-center gap-2">
                  <span className="h-4 w-4 animate-spin rounded-full border-2 border-white border-t-transparent" />
                  Converting...
                </span>
              ) : (
                <span className="flex items-center justify-center gap-2">
                  ✦ Convert to {selectedFormat.name}
                </span>
              )}
            </button>
          )}

          {progress && <ConversionProgress progress={progress} />}
        </div>
      )}

      <div className="mt-12 rounded-xl bg-gray-50 p-4 text-center text-xs text-gray-400">
        <p>
          🔒 Your files are processed in memory and deleted immediately after download.
          We never store or share your data.
        </p>
      </div>
    </div>
  )
}
