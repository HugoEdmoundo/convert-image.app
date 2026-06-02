import axios from 'axios'
import type { FormatCategory, FormatSuggestion } from '../types'

const API_BASE = import.meta.env.VITE_API_URL || '/api'

const http = axios.create({
  baseURL: API_BASE,
  timeout: 120_000,
})

export async function fetchFormats(): Promise<FormatCategory[]> {
  const { data } = await http.get('/formats')
  return data.categories
}

export async function fetchSuggestions(ext: string): Promise<FormatSuggestion> {
  const { data } = await http.get('/formats/suggestions', { params: { ext } })
  return data
}

export async function uploadAndConvert(
  file: File,
  format: string,
): Promise<string> {
  const form = new FormData()
  form.append('file', file)
  form.append('format', format)
  const { data } = await http.post('/convert', form)
  if (!data.success) throw new Error(data.error || 'Conversion failed')
  return data.job_id
}

export function createEventSource(jobId: string): EventSource {
  return new EventSource(`${API_BASE}/convert/${jobId}/stream`)
}

export function buildDownloadUrl(jobId: string): string {
  return `${API_BASE}/download/${jobId}`
}
