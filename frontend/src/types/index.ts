export interface OutputFormat {
  format: string
  name: string
  mime: string
  category: string
}

export interface FormatCategory {
  id: string
  name: string
  emoji: string
  output_formats: OutputFormat[]
}

export interface FormatSuggestion {
  category: { id: string; name: string; emoji: string } | null
  suggested: OutputFormat[]
  all: OutputFormat[]
}

export interface FileInfo {
  file: File
  name: string
  size: number
  extension: string
  preview?: string
}

export type StepId =
  | 'initializing'
  | 'validating'
  | 'analyzing'
  | 'extracting'
  | 'converting'
  | 'optimizing'
  | 'done'

export interface ProgressData {
  step: StepId | 'error'
  message: string
  percent: number
}

export interface ConversionResult {
  download_url: string
  filename: string
  size: string
  format: string
}

export type ConversionState = 'idle' | 'uploading' | 'converting' | 'done' | 'error'

export interface ConversionContextType {
  state: ConversionState
  fileInfo: FileInfo | null
  selectedFormat: OutputFormat | null
  suggestion: FormatSuggestion | null
  progress: ProgressData | null
  result: ConversionResult | null
  error: string | null
  setFile: (file: FileInfo | null) => void
  setFormat: (fmt: OutputFormat | null) => void
  startConversion: () => Promise<void>
  reset: () => void
}
