import type { FormatCategory } from '../types'

export const CATEGORIES: (FormatCategory & { input_extensions: string[] })[] = [
  {
    id: 'image',
    name: 'Image',
    emoji: '🖼️',
    input_extensions: ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp', '.tiff', '.tif', '.ico', '.svg', '.heic', '.heif'],
    output_formats: [
      { format: 'png', name: 'PNG', mime: 'image/png', category: 'image' },
      { format: 'jpg', name: 'JPEG', mime: 'image/jpeg', category: 'image' },
      { format: 'webp', name: 'WebP', mime: 'image/webp', category: 'image' },
      { format: 'gif', name: 'GIF', mime: 'image/gif', category: 'image' },
      { format: 'bmp', name: 'BMP', mime: 'image/bmp', category: 'image' },
      { format: 'tiff', name: 'TIFF', mime: 'image/tiff', category: 'image' },
      { format: 'ico', name: 'ICO', mime: 'image/x-icon', category: 'image' },
    ],
  },
  {
    id: 'video',
    name: 'Video',
    emoji: '🎬',
    input_extensions: ['.mp4', '.avi', '.mkv', '.mov', '.wmv', '.flv', '.webm', '.m4v', '.mpg', '.mpeg', '.3gp'],
    output_formats: [
      { format: 'mp4', name: 'MP4', mime: 'video/mp4', category: 'video' },
      { format: 'avi', name: 'AVI', mime: 'video/x-msvideo', category: 'video' },
      { format: 'mkv', name: 'MKV', mime: 'video/x-matroska', category: 'video' },
      { format: 'webm', name: 'WebM', mime: 'video/webm', category: 'video' },
      { format: 'mov', name: 'MOV', mime: 'video/quicktime', category: 'video' },
      { format: 'gif', name: 'GIF', mime: 'image/gif', category: 'image' },
    ],
  },
  {
    id: 'audio',
    name: 'Audio',
    emoji: '🎵',
    input_extensions: ['.mp3', '.wav', '.flac', '.aac', '.ogg', '.m4a', '.wma', '.opus', '.aiff', '.alac'],
    output_formats: [
      { format: 'mp3', name: 'MP3', mime: 'audio/mpeg', category: 'audio' },
      { format: 'wav', name: 'WAV', mime: 'audio/wav', category: 'audio' },
      { format: 'flac', name: 'FLAC', mime: 'audio/flac', category: 'audio' },
      { format: 'aac', name: 'AAC', mime: 'audio/aac', category: 'audio' },
      { format: 'ogg', name: 'OGG', mime: 'audio/ogg', category: 'audio' },
      { format: 'm4a', name: 'M4A', mime: 'audio/mp4', category: 'audio' },
      { format: 'wma', name: 'WMA', mime: 'audio/x-ms-wma', category: 'audio' },
      { format: 'opus', name: 'OPUS', mime: 'audio/opus', category: 'audio' },
    ],
  },
  {
    id: 'document',
    name: 'Document',
    emoji: '📄',
    input_extensions: ['.pdf', '.docx', '.doc', '.txt', '.rtf', '.odt', '.md', '.html', '.htm', '.epub'],
    output_formats: [
      { format: 'pdf', name: 'PDF', mime: 'application/pdf', category: 'document' },
      { format: 'docx', name: 'DOCX', mime: 'application/vnd.openxmlformats-officedocument.wordprocessingml.document', category: 'document' },
      { format: 'txt', name: 'TXT', mime: 'text/plain', category: 'document' },
      { format: 'md', name: 'Markdown', mime: 'text/markdown', category: 'document' },
      { format: 'html', name: 'HTML', mime: 'text/html', category: 'document' },
      { format: 'rtf', name: 'RTF', mime: 'application/rtf', category: 'document' },
    ],
  },
]

export const FORMAT_EMOJIS: Record<string, string> = {
  png: '🖼️', jpg: '🖼️', jpeg: '🖼️', webp: '🖼️', gif: '🎞️', bmp: '🖼️', tiff: '🖼️', ico: '🖼️',
  mp4: '🎬', avi: '🎬', mkv: '🎬', mov: '🎬', wmv: '🎬', flv: '🎬', webm: '🎬',
  mp3: '🎵', wav: '🎵', flac: '🎵', aac: '🎵', ogg: '🎵', m4a: '🎵', wma: '🎵', opus: '🎵',
  pdf: '📄', docx: '📄', txt: '📄', md: '📄', html: '🌐', rtf: '📄',
}

export function getCategoryForExtension(ext: string): FormatCategory | undefined {
  const e = ext.toLowerCase()
  return CATEGORIES.find(c => c.input_extensions.includes(e))
}

export function formatFileSize(bytes: number): string {
  if (bytes < 1024) return `${bytes} B`
  if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`
  return `${(bytes / (1024 * 1024)).toFixed(1)} MB`
}
