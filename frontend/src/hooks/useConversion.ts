import { useState, useCallback, useRef } from 'react'
import type {
  FileInfo,
  OutputFormat,
  FormatSuggestion,
  ProgressData,
  ConversionResult,
  ConversionState,
} from '../types'
import { fetchSuggestions, uploadAndConvert, createEventSource } from '../services/api'

export function useConversion() {
  const [state, setState] = useState<ConversionState>('idle')
  const [fileInfo, setFileInfo] = useState<FileInfo | null>(null)
  const [selectedFormat, setSelectedFormat] = useState<OutputFormat | null>(null)
  const [suggestion, setSuggestion] = useState<FormatSuggestion | null>(null)
  const [progress, setProgress] = useState<ProgressData | null>(null)
  const [result, setResult] = useState<ConversionResult | null>(null)
  const [error, setError] = useState<string | null>(null)
  const esRef = useRef<EventSource | null>(null)

  const setFile = useCallback(async (info: FileInfo | null) => {
    setFileInfo(info)
    setSelectedFormat(null)
    setResult(null)
    setProgress(null)
    setError(null)
    setState(info ? 'idle' : 'idle')

    if (info) {
      try {
        const res = await fetchSuggestions(info.extension)
        setSuggestion(res)
        if (res.suggested.length > 0) {
          setSelectedFormat(res.suggested[0])
        }
      } catch {
        setSuggestion(null)
      }
    } else {
      setSuggestion(null)
    }
  }, [])

  const startConversion = useCallback(async () => {
    if (!fileInfo || !selectedFormat) return

    setState('converting')
    setProgress({ step: 'initializing', message: 'Initializing conversion...', percent: 0 })
    setError(null)

    try {
      const jobId = await uploadAndConvert(fileInfo.file, selectedFormat.format)

      return new Promise<void>((resolve, reject) => {
        const es = createEventSource(jobId)
        esRef.current = es

        es.addEventListener('progress', (e) => {
          const data: ProgressData = JSON.parse(e.data)
          setProgress(data)
          if (data.step === 'error') {
            setError(data.message)
            setState('error')
            es.close()
            reject(new Error(data.message))
          }
        })

        es.addEventListener('complete', (e) => {
          const data: ConversionResult = JSON.parse(e.data)
          setResult(data)
          setState('done')
          es.close()
          resolve()
        })

        es.onerror = () => {
          setError('Connection lost. Please try again.')
          setState('error')
          es.close()
          reject(new Error('Connection lost'))
        }
      })
    } catch (err) {
      const msg = err instanceof Error ? err.message : 'Conversion failed'
      setError(msg)
      setState('error')
    }
  }, [fileInfo, selectedFormat])

  const reset = useCallback(() => {
    if (esRef.current) {
      esRef.current.close()
      esRef.current = null
    }
    setState('idle')
    setFileInfo(null)
    setSelectedFormat(null)
    setSuggestion(null)
    setProgress(null)
    setResult(null)
    setError(null)
  }, [])

  return {
    state,
    fileInfo,
    selectedFormat,
    suggestion,
    progress,
    result,
    error,
    setFile,
    setFormat: setSelectedFormat,
    startConversion,
    reset,
  } as const
}
