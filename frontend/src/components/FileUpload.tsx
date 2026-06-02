import { useCallback, useRef, useState, type DragEvent } from 'react'
import type { FileInfo } from '../types'
import { getCategoryForExtension, formatFileSize } from '../constants/formats'

interface Props {
  onFile: (info: FileInfo | null) => void
  fileInfo: FileInfo | null
}

export default function FileUpload({ onFile, fileInfo }: Props) {
  const inputRef = useRef<HTMLInputElement>(null)
  const [dragging, setDragging] = useState(false)

  const handleFile = useCallback(
    (file: File) => {
      const ext = '.' + file.name.split('.').pop()?.toLowerCase()

      const info: FileInfo = { file, name: file.name, size: file.size, extension: ext }

      if (file.type.startsWith('image/')) {
        const reader = new FileReader()
        reader.onload = () => {
          info.preview = reader.result as string
          onFile(info)
        }
        reader.readAsDataURL(file)
      } else {
        onFile(info)
      }
    },
    [onFile],
  )

  const onDrop = useCallback(
    (e: DragEvent) => {
      e.preventDefault()
      setDragging(false)
      const f = e.dataTransfer.files[0]
      if (f) handleFile(f)
    },
    [handleFile],
  )

  const onDragOver = useCallback((e: DragEvent) => {
    e.preventDefault()
    setDragging(true)
  }, [])

  const onDragLeave = useCallback(() => setDragging(false), [])

  const onChange = useCallback(
    (e: React.ChangeEvent<HTMLInputElement>) => {
      const f = e.target.files?.[0]
      if (f) handleFile(f)
    },
    [handleFile],
  )

  if (fileInfo) {
    const cat = getCategoryForExtension(fileInfo.extension)
    return (
      <div className="rounded-2xl border-2 border-brand-orange/20 bg-orange-50/50 p-6">
        <div className="flex items-start gap-4">
          <div className="flex h-14 w-14 shrink-0 items-center justify-center rounded-xl bg-gradient-to-br from-brand-orange/10 to-brand-gold/10 text-2xl">
            {cat?.emoji ?? '📁'}
          </div>
          <div className="min-w-0 flex-1">
            <p className="truncate font-medium text-gray-900">{fileInfo.name}</p>
            <p className="text-sm text-gray-500">{formatFileSize(fileInfo.size)}</p>
          </div>
          <button
            onClick={() => onFile(null)}
            className="shrink-0 rounded-lg p-2 text-gray-400 transition-colors hover:bg-gray-200 hover:text-gray-600"
            title="Remove file"
          >
            ✕
          </button>
        </div>
        {fileInfo.preview && (
          <img
            src={fileInfo.preview}
            alt="Preview"
            className="mt-4 max-h-48 w-full rounded-xl object-contain bg-white"
          />
        )}
      </div>
    )
  }

  return (
    <div
      onDrop={onDrop}
      onDragOver={onDragOver}
      onDragLeave={onDragLeave}
      onClick={() => inputRef.current?.click()}
      className={`upload-zone ${dragging ? 'dragging' : ''}`}
    >
      <input
        ref={inputRef}
        type="file"
        className="hidden"
        onChange={onChange}
      />
      <div className="mb-4 flex h-16 w-16 items-center justify-center rounded-2xl bg-gradient-to-br from-brand-orange/10 to-brand-gold/10 text-3xl text-brand-orange">
        ⬆
      </div>
      <p className="text-lg font-semibold text-gray-700">
        Drop your file here
      </p>
      <p className="mt-1 text-sm text-gray-500">
        or click to browse &mdash; any file, any format
      </p>
      <p className="mt-4 text-xs text-gray-400">
        Max 100MB &middot; Files are never stored permanently
      </p>
    </div>
  )
}
