import type { ConversionResult, FileInfo } from '../types'

interface Props {
  result: ConversionResult
  fileInfo: FileInfo
  onReset: () => void
}

export default function ResultCard({ result, fileInfo, onReset }: Props) {
  return (
    <div className="card space-y-6 text-center">
      <div className="mx-auto flex h-16 w-16 items-center justify-center rounded-full bg-green-100 text-3xl text-green-600">
        ✓
      </div>

      <div>
        <h3 className="text-lg font-bold text-gray-900">Conversion Complete!</h3>
        <p className="mt-1 text-sm text-gray-500">
          {fileInfo.name} → {result.format}
        </p>
      </div>

      <div className="grid grid-cols-2 gap-4 rounded-xl bg-gray-50 p-4 text-sm">
        <div>
          <p className="text-gray-500">Output Size</p>
          <p className="font-semibold text-gray-900">{result.size}</p>
        </div>
        <div>
          <p className="text-gray-500">Format</p>
          <p className="font-semibold text-gray-900">{result.format}</p>
        </div>
      </div>

      <div className="flex flex-col gap-3 sm:flex-row">
        <a
          href={result.download_url}
          className="btn-primary flex-1"
        >
          ⬇ Download
        </a>
        <button onClick={onReset} className="btn-secondary flex-1">
          Convert Another
        </button>
      </div>
    </div>
  )
}
