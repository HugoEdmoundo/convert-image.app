import { useState } from 'react'
import type { OutputFormat, FormatSuggestion } from '../types'
import { FORMAT_EMOJIS } from '../constants/formats'

interface Props {
  suggestion: FormatSuggestion
  selected: OutputFormat | null
  onSelect: (fmt: OutputFormat) => void
}

export default function FormatSelector({ suggestion, selected, onSelect }: Props) {
  const [showAll, setShowAll] = useState(false)
  const formats = showAll ? suggestion.all : suggestion.suggested

  return (
    <div>
      <div className="mb-2 flex items-center justify-between">
        <h3 className="text-sm font-semibold text-gray-700">
          {suggestion.category
            ? `Convert to (${suggestion.category.emoji} ${suggestion.category.name})`
            : 'Convert to'}
        </h3>
        {suggestion.all.length > suggestion.suggested.length && (
          <button
            onClick={() => setShowAll(!showAll)}
            className="text-xs font-medium text-brand-orange hover:text-amber-600"
          >
            {showAll ? 'Show suggested' : `Show all ${suggestion.all.length} formats`}
          </button>
        )}
      </div>
      <div className="flex flex-wrap gap-2">
        {formats.map((fmt) => {
          const isSelected = selected?.format === fmt.format
          return (
            <button
              key={fmt.format}
              onClick={() => onSelect(fmt)}
              className={`inline-flex items-center gap-1.5 rounded-xl border-2 px-4 py-2 text-sm font-medium transition-all duration-150 ${
                isSelected
                  ? 'border-brand-orange bg-orange-50 text-brand-orange shadow-sm'
                  : 'border-gray-200 bg-white text-gray-600 hover:border-gray-300 hover:bg-gray-50'
              }`}
            >
              <span>{FORMAT_EMOJIS[fmt.format] ?? '📁'}</span>
              <span>{fmt.name}</span>
              <span className="text-xs text-gray-400">.{fmt.format}</span>
            </button>
          )
        })}
      </div>
    </div>
  )
}
